#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple, Union

import requests
from zoneinfo import ZoneInfo


FEISHU_TENANT_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

# Approval v4 endpoints
FEISHU_APPROVAL_INSTANCES_LIST_URL = "https://open.feishu.cn/open-apis/approval/v4/instances"
FEISHU_APPROVAL_INSTANCE_DETAIL_URL_TMPL = "https://open.feishu.cn/open-apis/approval/v4/instances/{instance_id}"

# Contact v3 endpoint
FEISHU_USER_INFO_URL_TMPL = "https://open.feishu.cn/open-apis/contact/v3/users/{user_id}?user_id_type={user_id_type}"
FEISHU_DEPARTMENT_INFO_URL_TMPL = "https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}?department_id_type={department_id_type}"

# Hardcoded credentials and query params
APP_ID = "cli_a88a2172ee6c101c"
APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"

# Optional user access token to fetch richer user fields (like name)
USER_ACCESS_TOKEN = ""

# 这里填你的审批定义 Code（例如采购订单审批的 Code）
APPROVAL_CODE = "A851D76E-6B63-4DD4-91F2-998693422C3C"

# 查询日期与时区（自动计算毫秒时间戳区间）
QUERY_DATE = "2025-10-15"  # YYYY-MM-DD
LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def day_bounds_ms(date_str: str, tz: timezone) -> Tuple[str, str]:
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    start_dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
    end_dt = start_dt + timedelta(days=1) - timedelta(milliseconds=1)
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    return str(start_ms), str(end_ms)


START_TIME, END_TIME = day_bounds_ms(QUERY_DATE, LOCAL_TZ)


def request_tenant_access_token(app_id: str, app_secret: str) -> str:
    payload: Dict[str, Any] = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(FEISHU_TENANT_TOKEN_URL, json=payload, timeout=15)
    try:
        response.raise_for_status()
    except requests.HTTPError as http_err:
        raise RuntimeError(f"Failed to obtain tenant access token: {http_err}\n{response.text}") from http_err

    data = response.json()
    if data.get("code", 0) != 0:
        raise RuntimeError(f"Feishu returned error for token: code={data.get('code')} msg={data.get('msg')} data={data}")

    token = data.get("tenant_access_token")
    if not token:
        raise RuntimeError("tenant_access_token not found in response")
    return token


def list_approval_instance_ids(
    tenant_access_token: str,
    approval_code: str,
    start_time: str,
    end_time: str,
    page_size: int = 100,
) -> List[str]:
    instance_ids: List[str] = []
    page_token = ""
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    while True:
        params: Dict[str, Any] = {
            "approval_code": approval_code,
            "start_time": start_time,
            "end_time": end_time,
            "page_size": page_size,
        }
        if page_token:
            params["page_token"] = page_token
        print(f"GET: {FEISHU_APPROVAL_INSTANCES_LIST_URL}")
        print(f"Params: {json.dumps(params, ensure_ascii=False)}")
        response = requests.get(
            FEISHU_APPROVAL_INSTANCES_LIST_URL, headers=headers, params=params, timeout=20
        )
        response.raise_for_status()
        result = response.json()
        print(f"Response: {json.dumps(result, ensure_ascii=False)}")
        if result.get("code", 0) != 0:
            raise RuntimeError(
                f"Feishu error listing instances: code={result.get('code')} msg={result.get('msg')}"
            )
        data = result.get("data", {})
        batch = data.get("instance_code_list", [])
        instance_ids.extend(batch)
        page_token = data.get("page_token", "")
        has_more = data.get("has_more", False)
        print(
            f"Retrieved {len(batch)} instance ids, total={len(instance_ids)}, has_more={has_more}"
        )
        if not has_more:
            break
    return instance_ids


def fetch_approval_instance_detail(tenant_access_token: str, instance_id: str) -> Dict[str, Any]:
    url = FEISHU_APPROVAL_INSTANCE_DETAIL_URL_TMPL.format(instance_id=instance_id)
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    print(f"GET: {url}")
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    result = response.json()
    print(f"Response for instance {instance_id}: {json.dumps(result, ensure_ascii=False)}")
    if result.get("code", 0) != 0:
        raise RuntimeError(
            f"Feishu error fetching instance detail: code={result.get('code')} msg={result.get('msg')}"
        )
    return result.get("data", {})


def safe_format_ms(value: Union[str, int, float, None], tz: timezone) -> str:
    try:
        if value is None:
            return ""
        if isinstance(value, str):
            if not value.isdigit():
                return ""
            ms = int(value)
        else:
            ms = int(value)
        # Treat values with >=13 digits as milliseconds
        if ms < 10**12:
            return ""  # likely seconds or smaller numbers we don't format here
        dt = datetime.fromtimestamp(ms / 1000.0, tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S%z")
    except Exception:
        return ""


def add_formatted_timestamps(data: Any, tz: timezone) -> Any:
    # Recursively add *_fmt next to keys containing 'time'
    if isinstance(data, dict):
        new_obj: Dict[str, Any] = {}
        for k, v in data.items():
            new_obj[k] = add_formatted_timestamps(v, tz)
            key_lower = k.lower()
            if "time" in key_lower:
                formatted = safe_format_ms(v, tz)
                if formatted:
                    new_obj[f"{k}_fmt"] = formatted
        return new_obj
    if isinstance(data, list):
        return [add_formatted_timestamps(item, tz) for item in data]
    return data


_department_name_cache: Dict[str, str] = {}


def get_user_profile(
    tenant_access_token: str, user_id: str, user_id_type: str = "open_id"
) -> Tuple[str, List[str]]:
    # First try via SDK if available; fall back to raw HTTP
    name, dept_ids = _get_user_profile_via_sdk(tenant_access_token, user_id, user_id_type)
    if name or dept_ids:
        return name or "未知用户", dept_ids
    if not user_id:
        return "未知用户", []
    url = FEISHU_USER_INFO_URL_TMPL.format(user_id=user_id, user_id_type=user_id_type)
    bearer_token = USER_ACCESS_TOKEN or tenant_access_token
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    print(f"GET: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()
    except Exception as exc:  # noqa: BLE001
        print(f"获取用户信息失败: {exc}", file=sys.stderr)
        return "未知用户", []

    print(f"User info response for {user_id}: {json.dumps(result, ensure_ascii=False)}")
    if result.get("code", 0) != 0:
        # 99992351: user id not found
        if result.get("code") == 99992351 and user_id_type == "open_id":
            # fallback to user_id if looks like user_id
            return get_user_profile(tenant_access_token, user_id, "user_id")
        return "未知用户", []

    user_data = result.get("data", {}).get("user", {})
    name = user_data.get("name", "未知用户")
    # department_ids often are open_department_id list when using open_id/user_id types
    department_ids: List[str] = user_data.get("department_ids", []) or []
    return name, department_ids


def _get_user_profile_via_sdk(
    tenant_access_token: str, user_id: str, user_id_type: str
) -> Tuple[str, List[str]]:
    """Try resolving user via Feishu SDK. Returns (name, department_ids) or ("", [])."""
    try:
        import lark_oapi as lark
        from lark_oapi.api.contact.v3 import GetUserRequest
    except Exception:
        return "", []

    try:
        client = (
            lark.Client.builder()
            .enable_set_token(True)
            .log_level(lark.LogLevel.ERROR)
            .build()
        )
        request = (
            GetUserRequest.builder()
            .user_id(user_id)
            .user_id_type(user_id_type)
            .department_id_type("open_department_id")
            .build()
        )
        # Prefer user_access_token if provided; else tenant token
        option_builder = lark.RequestOption.builder()
        if USER_ACCESS_TOKEN:
            option_builder = option_builder.user_access_token(USER_ACCESS_TOKEN)
        else:
            option_builder = option_builder.tenant_access_token(tenant_access_token)
        option = option_builder.build()
        response = client.contact.v3.user.get(request, option)
        if not response.success() or not response.data or not response.data.user:
            return "", []
        user = response.data.user
        name = getattr(user, "name", None) or ""
        dept_ids = getattr(user, "department_ids", None) or []
        return name, list(dept_ids)
    except Exception:
        return "", []


def get_department_name(
    tenant_access_token: str, department_id: str, department_id_type: str = "open_department_id"
) -> str:
    if not department_id:
        return ""
    if department_id in _department_name_cache:
        return _department_name_cache[department_id]
    url = FEISHU_DEPARTMENT_INFO_URL_TMPL.format(
        department_id=department_id, department_id_type=department_id_type
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    print(f"GET: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()
    except Exception as exc:  # noqa: BLE001
        print(f"获取部门信息失败: {exc}", file=sys.stderr)
        return ""

    if result.get("code", 0) != 0:
        return ""
    dept = result.get("data", {}).get("department", {})
    name = dept.get("name", "")
    if name:
        _department_name_cache[department_id] = name
    return name


def resolve_user_name_from_user_id(user_id: str) -> str:
    """Convenience helper: get user name directly from a user_id.

    Uses the employee_mapping.json file to resolve the name for the provided user_id.
    Returns "未知用户" on failure.
    """
    if not user_id:
        return "未知用户"
    
    try:
        # Load the employee mapping JSON file
        mapping_file_path = os.path.join(os.path.dirname(__file__), "employee_mapping.json")
        with open(mapping_file_path, 'r', encoding='utf-8') as f:
            employee_mapping = json.load(f)
        
        # Reverse lookup: find name by open_id
        for name, open_id in employee_mapping.items():
            if open_id == user_id:
                return name
        
        # If not found in mapping, return unknown user
        return "未知用户"
    except Exception:
        return "未知用户"


def get_signature_image_path(user_name: str) -> str:
    """Get the signature image path for a user name.
    
    Returns the image path if found, otherwise returns the user name.
    """
    if not user_name or user_name == "未知用户":
        return user_name
    
    try:
        # Load the signature mapping JSON file
        mapping_file_path = os.path.join(os.path.dirname(__file__), "signature_mapping.json")
        with open(mapping_file_path, 'r', encoding='utf-8') as f:
            signature_mapping = json.load(f)
        
        # Check if user has signature image
        if user_name in signature_mapping:
            image_filename = signature_mapping[user_name]
            image_path = os.path.join(os.path.dirname(__file__), image_filename)
            if os.path.exists(image_path):
                return f"[签名图片: {image_filename}]"
        
        return user_name
    except Exception:
        return user_name


def display_signature_ascii(image_path: str, width: int = 40) -> str:
    """Convert image to ASCII art for terminal display.
    
    This is a simplified version that returns a placeholder.
    For full functionality, you would need PIL/Pillow library.
    """
    try:
        # Check if PIL is available
        from PIL import Image
        import numpy as np
        
        # Load and resize image
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
        img = img.resize((width, width // 2))  # Resize for terminal
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # ASCII characters from dark to light
        ascii_chars = "@%#*+=-:. "
        
        # Convert to ASCII
        ascii_art = ""
        for row in img_array:
            for pixel in row:
                ascii_art += ascii_chars[pixel // 32]
            ascii_art += "\n"
        
        return ascii_art
    except ImportError:
        return f"[需要安装PIL库来显示ASCII签名: {os.path.basename(image_path)}]"
    except Exception:
        return f"[无法显示签名图片: {os.path.basename(image_path)}]"


def resolve_timeline_user_names(tenant_access_token: str, timeline: List[Dict[str, Any]]) -> None:
    print("\n=== 审批进程处理人信息 ===")
    for i, item in enumerate(timeline):
        print(f"\n--- 第{i+1}个审批节点 ---")
        print(f"节点类型: {item.get('type', 'N/A')}")
        print(f"节点名称: {item.get('node_key', 'N/A')}")
        raw_create_time = item.get('create_time', '')
        print(f"发生时间: {raw_create_time} ({safe_format_ms(raw_create_time, LOCAL_TZ)})")

        user_name = "未知用户"
        open_id = item.get("open_id")
        user_id = item.get("user_id")

        # Use JSON mapping for open_id lookup
        if open_id:
            print(open_id+", "+open_id)
            user_name = resolve_user_name_from_user_id(open_id)
        elif user_id:
            user_name = resolve_user_name_from_user_id(user_id)

        # Display signature instead of name if available
        signature_display = get_signature_image_path(user_name)
        print(f"处理人: {signature_display}")
        print(f"意见: {item.get('comment', 'N/A')}")


def main() -> None:
    if not APP_ID or not APP_SECRET:
        print("APP_ID/APP_SECRET 未设置", file=sys.stderr)
        sys.exit(2)
    if not APPROVAL_CODE:
        print("APPROVAL_CODE 未设置（请在代码中填写审批定义 Code）", file=sys.stderr)
        sys.exit(2)

    print("=== 步骤1: 获取 tenant_access_token ===")
    try:
        tenant_token = request_tenant_access_token(APP_ID, APP_SECRET)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(f"Successfully got tenant_access_token (first 20 chars): {tenant_token[:20]}...")

    print("\n=== 步骤2: 批量获取审批实例ID ===")
    print(
        f"查询时间范围: {START_TIME} - {END_TIME} "
        f"({safe_format_ms(START_TIME, LOCAL_TZ)} ~ {safe_format_ms(END_TIME, LOCAL_TZ)})"
    )
    try:
        instance_ids = list_approval_instance_ids(
            tenant_token, APPROVAL_CODE, START_TIME, END_TIME
        )
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(f"成功获取 {len(instance_ids)} 个审批实例")

    if not instance_ids:
        print("没有找到符合条件的审批实例")
        sys.exit(0)

    approved_count = 0
    for i, instance_id in enumerate(instance_ids, start=1):
        print(f"\n=== 步骤3: 处理第{i}个审批实例 ({instance_id}) ===")
        try:
            detail = fetch_approval_instance_detail(tenant_token, instance_id)
        except Exception as exc:  # noqa: BLE001
            print(f"获取实例详情失败: {exc}", file=sys.stderr)
            continue

        # 只处理审批通过的实例
        status = detail.get("status", "")
        if status != "APPROVED":
            print(f"跳过非审批通过实例，状态: {status}")
            continue
            
        approved_count += 1
        print(f"\n=== 审批通过的实例 #{approved_count} ===")
        print(f"实例ID: {instance_id}")
        print(f"审批名称: {detail.get('approval_name', 'N/A')}")
        print(f"申请单号: {detail.get('serial_number', 'N/A')}")
        print(f"申请人: {resolve_user_name_from_user_id(detail.get('open_id', ''))}")
        print(f"申请时间: {safe_format_ms(detail.get('start_time', ''), LOCAL_TZ)}")
        print(f"完成时间: {safe_format_ms(detail.get('end_time', ''), LOCAL_TZ)}")

        timeline = detail.get("timeline", [])
        if timeline:
            resolve_timeline_user_names(tenant_token, timeline)
        else:
            print("\n审批进程中没有找到处理人信息")
    
    print(f"\n=== 总结 ===")
    print(f"总共找到 {len(instance_ids)} 个审批实例")
    print(f"其中审批通过的有 {approved_count} 个")


if __name__ == "__main__":
    main()

