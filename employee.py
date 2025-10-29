import os
import json
import time

import requests
import sys
import urllib.parse
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse, parse_qs


def get_verify_setting():
    """
    获取SSL验证设置
    在腾讯云等环境中可能需要禁用SSL验证
    """
    # 检查环境变量
    ssl_verify = os.environ.get('SSL_VERIFY', 'False').lower()
    return ssl_verify not in ('false', '0', 'no')

# === input params start
# Hardcoded credentials and query params
app_id = "cli_a88a2172ee6c101c"
app_secret = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
base_url = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn" # base_url, 多维表格应用 url, required


# === input params end

def get_tenant_access_token(app_id: str, app_secret: str) -> Tuple[str, Exception]:
    """获取 tenant_access_token

    Args:
        app_id: 应用ID
        app_secret: 应用密钥

    Returns:
        Tuple[str, Exception]: (access_token, error)
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        print(f"POST: {url}")
        print(f"Request body: {json.dumps(payload)}")
        response = requests.post(url, json=payload, headers=headers, verify=get_verify_setting())
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result)}")

        if result.get("code", 0) != 0:
            print(f"ERROR: failed to get tenant_access_token: {result.get('msg', 'unknown error')}", file=sys.stderr)
            return "", Exception(f"failed to get tenant_access_token: {response.text}")

        return result["tenant_access_token"], None

    except Exception as e:
        print(f"ERROR: getting tenant_access_token: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"ERROR: response body: {e.response.text}", file=sys.stderr)
        return "", e


def get_wiki_node_info(tenant_access_token: str, node_token: str) -> Dict[str, Any]:
    """获取知识空间节点信息

    Args:
        tenant_access_token: 租户访问令牌
        node_token: 节点令牌

    Returns:
        Dict[str, Any]: 节点信息对象
    """
    url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={urllib.parse.quote(node_token)}"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        print(f"GET: {url}")
        response = requests.get(url, headers=headers, verify=get_verify_setting())
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result)}")

        if result.get("code", 0) != 0:
            print(f"ERROR: 获取知识空间节点信息失败 {result}", file=sys.stderr)
            raise Exception(f"failed to get wiki node info: {result.get('msg', 'unknown error')}")

        if not result.get("data") or not result["data"].get("node"):
            raise Exception("未获取到节点信息")

        node_info = result["data"]["node"]
        print("节点信息获取成功:", {
            "node_token": node_info.get("node_token"),
            "obj_type": node_info.get("obj_type"),
            "obj_token": node_info.get("obj_token"),
            "title": node_info.get("title")
        })
        return node_info

    except Exception as e:
        print(f"ERROR: getting wiki node info: {e}", file=sys.stderr)
        raise


def parse_base_url(tenant_access_token: str, base_url_string: str) -> Dict[str, Optional[str]]:
    """解析多维表格参数

    Args:
        tenant_access_token: 租户访问令牌
        base_url_string: 基础URL字符串

    Returns:
        Dict[str, Optional[str]]: 包含appToken、tableID、viewID的字典
    """
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(base_url_string)
    pathname = parsed_url.path
    app_token = pathname.split("/")[-1]

    if "/wiki/" in pathname:
        node_info = get_wiki_node_info(tenant_access_token, app_token)
        app_token = node_info.get("obj_token", app_token)

    query_params = parse_qs(parsed_url.query)
    view_id = query_params.get("view", [None])[0]
    table_id = query_params.get("table", [None])[0]

    return {
        "app_token": app_token,
        "table_id": table_id,
        "view_id": view_id
    }


def list_tables(tenant_access_token: str, app_token: str) -> List[Dict[str, Any]]:
    """列出数据表

    Args:
        tenant_access_token: 租户访问令牌
        app_token: 多维表格应用token

    Returns:
        List[Dict[str, Any]]: 数据表列表
    """
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    tables = []
    page_token = None

    while True:
        params = {}
        if page_token:
            params["page_token"] = page_token

        print(f"GET: {url} with params: {params}")
        response = requests.get(url, headers=headers, params=params, verify=get_verify_setting())
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result)}")

        if result.get("code", 0) != 0:
            print(f"ERROR: 列出数据表失败: {result}", file=sys.stderr)
            raise Exception(f"failed to list tables: {result.get('msg', 'unknown error')}")

        data = result.get("data", {})
        items = data.get("items", [])
        tables.extend(items)

        if not data.get("has_more", False):
            break
        page_token = data.get("page_token")

    return tables


def search_records(tenant_access_token: str, app_token: str, table_id: str, view_id: Optional[str] = None) -> List[
    Dict[str, Any]]:
    """查询记录

    Args:
        tenant_access_token: 租户访问令牌
        app_token: 多维表格应用token
        table_id: 数据表ID
        view_id: 视图ID，可选

    Returns:
        List[Dict[str, Any]]: 记录列表
    """
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    records = []
    page_token = None

    while True:
        payload = {
            "user_id_type": "open_id"
        }
        if view_id:
            payload["view_id"] = view_id

        if page_token:
            payload["page_token"] = page_token

        print(f"POST: {url}")
        print(f"Request body: {json.dumps(payload)}")
        response = requests.post(url, json=payload, headers=headers, verify=get_verify_setting())
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result)}")

        if result.get("code", 0) != 0:
            print(f"ERROR: 查询记录失败: {result}", file=sys.stderr)
            raise Exception(f"failed to search records: {result.get('msg', 'unknown error')}")

        data = result.get("data", {})
        items = data.get("items", [])
        records.extend(items)

        if not data.get("has_more", False):
            break
        page_token = data.get("page_token")

    return records


def download_file(tenant_access_token: str, file_url: str, filename: str) -> bool:
    """下载文件

    Args:
        tenant_access_token: 租户访问令牌
        file_url: 文件下载URL
        filename: 保存的文件名

    Returns:
        bool: 是否下载成功
    """
    headers = {
        "Authorization": f"Bearer {tenant_access_token}"
    }

    try:
        print(f"Downloading file from: {file_url} to: {filename}")
        response = requests.get(file_url, headers=headers, verify=get_verify_setting())
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"File downloaded successfully: {filename}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to download file {filename}: {e}", file=sys.stderr)
        return False


def main():
    # 验证必要参数
    if not app_id:
        print("ERROR: APP_ID is required", file=sys.stderr)
        exit(1)
    if not app_secret:
        print("ERROR: APP_SECRET is required", file=sys.stderr)
        exit(1)
    if not base_url:
        print("ERROR: BASE_URL is required", file=sys.stderr)
        exit(1)

    # 获取 tenant_access_token
    tenant_access_token, err = get_tenant_access_token(app_id, app_secret)
    if err:
        print(f"ERROR: getting tenant_access_token: {err}", file=sys.stderr)
        exit(1)

    # 解析多维表格参数
    try:
        parsed_params = parse_base_url(tenant_access_token, base_url)
        app_token = parsed_params["app_token"]
        table_id = parsed_params["table_id"]
        view_id = parsed_params["view_id"]

        print(f"解析参数成功: app_token={app_token}, table_id={table_id}, view_id={view_id}")
    except Exception as e:
        print(f"ERROR: 解析多维表格参数失败: {e}", file=sys.stderr)
        exit(1)

    # 如果没有提供table_id，则列出所有数据表并使用第一个
    if not table_id:
        try:
            tables = list_tables(tenant_access_token, app_token)
            if len(tables) == 0:
                print("ERROR: 没有找到数据表", file=sys.stderr)
                exit(1)
            table_id = tables[0]["table_id"]
            print(f"使用第一个数据表: {table_id} - {tables[0].get('name', '无名称')}")
        except Exception as e:
            print(f"ERROR: 获取数据表列表失败: {e}", file=sys.stderr)
            exit(1)

    # 查询所有记录
    try:
        records = search_records(tenant_access_token, app_token, table_id, view_id)
        print(f"成功获取 {len(records)} 条记录")
    except Exception as e:
        print(f"ERROR: 查询记录失败: {e}", file=sys.stderr)
        exit(1)

    # 生成员工姓名-ID映射
    employee_mapping = {}
    processed_count = 0
    skipped_count = 0

    for record in records:
        fields = record.get("fields", {})

        # 获取员工字段（假设字段名为"员工"）
        employee_field = fields.get("员工", [])
        if not isinstance(employee_field, list) or len(employee_field) == 0:
            skipped_count += 1
            continue

        # 获取第一个员工的信息
        first_employee = employee_field[0]
        employee_name = first_employee.get("name")
        employee_id = first_employee.get("id")

        if not employee_name or not employee_id:
            skipped_count += 1
            continue

        # 构建映射（去重，同一姓名只保留首次出现的ID）
        if employee_name not in employee_mapping:
            employee_mapping[employee_name] = employee_id

        # 获取附件字段（假设字段名为"附件"）
        attachment_field = fields.get("附件", [])
        if not isinstance(attachment_field, list) or len(attachment_field) == 0:
            skipped_count += 1
            continue

        # 获取第一个附件
        first_attachment = attachment_field[0]
        file_url = first_attachment.get("url")
        original_name = first_attachment.get("name", "")

        if not file_url:
            skipped_count += 1
            continue

        # 解析原文件后缀
        file_extension = ""
        if "." in original_name:
            file_extension = original_name[original_name.rfind("."):]

        # 以员工姓名+原文件后缀命名
        new_filename = f"{employee_name}{file_extension}"
        signature_path = os.path.join("signatures", new_filename)

        # 下载文件
        if download_file(tenant_access_token, file_url, signature_path):
            processed_count += 1
        else:
            skipped_count += 1

    # 保存员工姓名-ID映射为JSON文件
    try:
        with open("data/employee_mapping.json", "w", encoding="utf-8") as f:
            json.dump(employee_mapping, f, ensure_ascii=False, indent=2)
        print(f"员工姓名-ID映射已保存到 data/employee_mapping.json")
    except Exception as e:
        print(f"ERROR: 保存员工映射文件失败: {e}", file=sys.stderr)

    print(f"处理完成: 成功处理 {processed_count} 个文件, 跳过 {skipped_count} 个记录")
    print(f"员工映射: {json.dumps(employee_mapping, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()