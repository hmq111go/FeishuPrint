#!/usr/bin/env python3
"""
飞书API相关功能模块
包含认证、审批、多维表格等API调用
"""
import json
import os
import sys
from typing import Any, Dict, List, Tuple, Optional
import requests
import urllib.parse


class FeishuAPI:
    """飞书API客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_token = None
    
    def get_tenant_access_token(self) -> Tuple[str, Exception]:
        """获取 tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
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
            self.tenant_token = access_token
            print(f"获取 tenant_access_token 成功: {access_token[:10]}...")
            return access_token, None

        except Exception as e:
            print(f"Error: getting tenant_access_token: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response body: {e.response.text}", file=sys.stderr)
            return "", e

    def subscribe_approval_event(self, approval_code: str) -> bool:
        """订阅审批事件"""
        if not self.tenant_token:
            print("Error: tenant_token not available")
            return False
            
        url = f"https://open.feishu.cn/open-apis/approval/v4/approvals/{approval_code}/subscribe"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        try:
            print(f"POST: {url}")
            response = requests.post(url, headers=headers)
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

    def fetch_approval_instance_detail(self, instance_id: str) -> Dict[str, Any]:
        """获取审批实例详情"""
        if not self.tenant_token:
            raise RuntimeError("tenant_token not available")
            
        url = f"https://open.feishu.cn/open-apis/approval/v4/instances/{instance_id}"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
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

    def get_department_name(self, department_id: str) -> str:
        """根据部门ID获取部门名称"""
        if not self.tenant_token:
            return "未知部门"
            
        if not department_id:
            return "未知部门"
        
        # 根据部门ID前缀判断使用哪种department_id_type
        if department_id.startswith("od-"):
            # open_department_id类型
            department_id_type = "open_department_id"
        else:
            # department_id类型（自定义部门ID）
            department_id_type = "department_id"
            
        url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}"
        headers = {"Authorization": f"Bearer {self.tenant_token}"}
        params = {"department_id_type": department_id_type}

        try:
            print(f"获取部门信息: {department_id} (类型: {department_id_type})")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                department = data.get("data", {}).get("department", {})
                department_name = department.get("name", "未知部门")
                print(f"部门信息获取成功: {department_id} -> {department_name}")
                return department_name
            else:
                print(f"获取部门信息失败 ({department_id}): {data.get('msg', '未知错误')}")
        except Exception as e:
            print(f"获取部门信息失败 ({department_id}): {e}")

        return "未知部门"

    def get_wiki_node_info(self, node_token: str) -> Dict[str, Any]:
        """获取知识空间节点信息"""
        if not self.tenant_token:
            raise RuntimeError("tenant_token not available")
            
        url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={urllib.parse.quote(node_token)}"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        try:
            print(f"GET: {url}")
            response = requests.get(url, headers=headers)
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

    def parse_base_url(self, base_url_string: str) -> Dict[str, Optional[str]]:
        """解析多维表格参数"""
        from urllib.parse import urlparse, parse_qs

        parsed_url = urlparse(base_url_string)
        pathname = parsed_url.path
        app_token = pathname.split("/")[-1]

        if "/wiki/" in pathname:
            node_info = self.get_wiki_node_info(app_token)
            app_token = node_info.get("obj_token", app_token)

        query_params = parse_qs(parsed_url.query)
        view_id = query_params.get("view", [None])[0]
        table_id = query_params.get("table", [None])[0]

        return {
            "app_token": app_token,
            "table_id": table_id,
            "view_id": view_id
        }

    def list_tables(self, app_token: str) -> List[Dict[str, Any]]:
        """列出数据表"""
        if not self.tenant_token:
            raise RuntimeError("tenant_token not available")
            
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        tables = []
        page_token = None

        while True:
            params = {}
            if page_token:
                params["page_token"] = page_token

            print(f"GET: {url} with params: {params}")
            response = requests.get(url, headers=headers, params=params)
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

    def search_records(self, app_token: str, table_id: str, view_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """查询记录"""
        if not self.tenant_token:
            raise RuntimeError("tenant_token not available")
            
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
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
            response = requests.post(url, json=payload, headers=headers)
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

    def download_file(self, file_url: str, filename: str) -> bool:
        """下载文件"""
        if not self.tenant_token:
            return False
            
        headers = {
            "Authorization": f"Bearer {self.tenant_token}"
        }

        try:
            print(f"Downloading file from: {file_url} to: {filename}")
            response = requests.get(file_url, headers=headers)
            response.raise_for_status()

            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"File downloaded successfully: {filename}")
            return True

        except Exception as e:
            print(f"ERROR: Failed to download file {filename}: {e}", file=sys.stderr)
            return False
