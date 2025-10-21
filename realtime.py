import json
import os
import sys
from typing import Tuple

import lark_oapi as lark
import requests

# === input params start
app_id = os.getenv("APP_ID")  # app_id, 应用 ID
app_secret = os.getenv("APP_SECRET")  # app_secret, 应用 secret
app_id = "cli_a88a2172ee6c101c"
app_secret = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"

approval_code = "A851D76E-6B63-4DD4-91F2-998693422C3C"  # string, 审批定义 Code


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
        print(f"Request body: {json.dumps(payload)}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if result.get("code", 0) != 0:
            print(f"Error: failed to get tenant_access_token: {result.get('msg', 'unknown error')}", file=sys.stderr)
            return "", Exception(f"failed to get tenant_access_token: {response.text}")

        access_token = result["tenant_access_token"]
        print(f"获取 tenant_access_token 成功: {access_token[:10]}...")
        return access_token, None

    except Exception as e:
        print(f"Error: getting tenant_access_token: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}", file=sys.stderr)
        return "", e


def subscribe_approval_event(tenant_access_token: str, approval_code: str) -> bool:
    """订阅审批事件

    Args:
        tenant_access_token: 租户访问令牌
        approval_code: 审批定义Code

    Returns:
        bool: 订阅是否成功（包括已存在的情况）
    """
    url = f"https://open.feishu.cn/open-apis/approval/v4/approvals/{approval_code}/subscribe"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        print(f"POST: {url}")
        response = requests.post(url, headers=headers)
        # 不直接raise_for_status，因为1390007是预期的"已存在"错误
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if result.get("code") == 0:
            print("订阅审批事件成功")
            return True
        elif result.get("code") == 1390007:  # subscription existed
            print("审批事件已订阅，无需重复操作")
            return True
        else:
            print(f"ERROR: subscribing approval event: {result.get('msg', 'unknown error')}", file=sys.stderr)
            print(f"ERROR: Response body: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"ERROR: subscribing approval event: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"ERROR: Response body: {e.response.text}", file=sys.stderr)
        return False


def do_approval_instance_event(data: lark.CustomizedEvent) -> None:
    """处理审批实例状态变更事件

    Args:
        data: 审批事件数据
    """
    event_data = lark.JSON.marshal(data, indent=4)
    event_dict = json.loads(event_data)

    print(f"[审批事件接收] 原始事件数据: {event_data}")

    # 提取事件信息
    event = event_data
    if event:
        status = event_dict.get("event", {}).get("status", "")
        instance_code = event_dict.get("event", {}).get("instance_code", "")
        approval_code = event_dict.get("event", {}).get("approval_code", "")

        print(f"[审批事件处理] 审批状态: {status}, 实例Code: {instance_code}, 审批定义Code: {approval_code}")

        # 处理审批通过事件
        if status == "APPROVED":
            print(f"[审批通过] 审批实例 {instance_code} 已通过审批")
            # 在这里添加审批通过后的业务逻辑


def main():
    print("=== 步骤1: 获取 tenant_access_token ===")
    tenant_access_token, err = get_tenant_access_token(app_id, app_secret)
    if err:
        print(f"Error: 获取 tenant_access_token 失败: {err}", file=sys.stderr)
        exit(1)

    print("\n=== 步骤2: 订阅审批事件 ===")
    if not subscribe_approval_event(tenant_access_token, approval_code):
        print("订阅审批事件失败，但将继续启动WebSocket客户端...", file=sys.stderr)

    print("\n=== 步骤3: 注册事件处理函数 ===")
    # 注册审批实例状态变更事件（支持V1和V2版本）
    event_handler = lark.EventDispatcherHandler.builder(app_id, app_secret) \
        .register_p1_customized_event("approval_instance", do_approval_instance_event) \
        .register_p1_customized_event("approval_instance_v2", do_approval_instance_event) \
        .build()

    print("\n=== 步骤4: 启动 WebSocket 客户端 ===")
    print("正在连接飞书事件推送服务...")
    cli = lark.ws.Client(app_id, app_secret,
                         event_handler=event_handler, log_level=lark.LogLevel.DEBUG)
    print("WebSocket客户端已启动，等待接收审批事件...")
    cli.start()


if __name__ == "__main__":
    main()
