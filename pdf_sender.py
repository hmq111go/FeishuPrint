#!/usr/bin/env python3
"""
PDF发送模块
负责将生成的PDF通过飞书机器人发送给发起人
"""
import os
import json
import requests
import sys
import logging
import mimetypes
from typing import Dict, Any, Tuple, Optional


def get_verify_setting():
    """
    获取SSL验证设置
    在腾讯云等环境中可能需要禁用SSL验证
    """
    # 检查环境变量
    ssl_verify = os.environ.get('SSL_VERIFY', 'False').lower()
    return ssl_verify not in ('false', '0', 'no')


class PDFSender:
    """PDF发送器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.logger = logging.getLogger(__name__)
        self.tenant_access_token = None
        self.token_expire_time = None
    
    def get_tenant_access_token(self, force_refresh: bool = False) -> Tuple[str, Optional[Exception]]:
        """获取 tenant_access_token

        Returns:
            Tuple[str, Optional[Exception]]: (access_token, error)
        """
        import time
        
        # 检查是否需要刷新token
        if not force_refresh and self.tenant_access_token and self.token_expire_time:
            if time.time() < self.token_expire_time - 300:  # 提前5分钟刷新
                self.logger.debug("使用缓存的token")
                return self.tenant_access_token, None
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        try:
            self.logger.debug(f"POST: {url}")
            self.logger.debug(f"Request body: {json.dumps(payload)}")
            response = requests.post(url, json=payload, headers=headers, verify=get_verify_setting())
            response.raise_for_status()

            result = response.json()
            self.logger.debug(f"Response: {json.dumps(result, indent=2)}")

            if result.get("code", 0) != 0:
                error_msg = f"failed to get tenant_access_token: {result.get('msg', 'unknown error')}"
                self.logger.error(f"ERROR: {error_msg}")
                return "", Exception(error_msg)

            self.tenant_access_token = result["tenant_access_token"]
            expire_time = result.get("expire", 7200)  # 默认2小时
            
            import time
            self.token_expire_time = time.time() + expire_time
            
            self.logger.info(f"获取 tenant_access_token 成功: {self.tenant_access_token[:10]}... (有效期: {expire_time}秒)")
            return self.tenant_access_token, None

        except Exception as e:
            self.logger.error(f"ERROR: getting tenant_access_token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"ERROR: Response: {e.response.text}")
            return "", e

    def upload_file(self, file_path: str) -> Tuple[str, Optional[Exception]]:
        """上传文件到飞书服务器

        Args:
            file_path: 本地文件路径

        Returns:
            Tuple[str, Optional[Exception]]: (file_key, error)
        """
        if not self.tenant_access_token:
            token, err = self.get_tenant_access_token()
            if err:
                return "", err
        
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }

        # 获取文件类型和文件名
        file_name = os.path.basename(file_path)
        file_type, _ = mimetypes.guess_type(file_path)
        
        # 根据文件扩展名设置 file_type
        if file_type:
            if file_type.startswith('audio/'):
                file_type = 'opus'  # 飞书要求音频文件为opus格式
            elif file_type.startswith('video/'):
                file_type = 'mp4'
            elif file_type == 'application/pdf':
                file_type = 'pdf'
            elif file_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                file_type = 'doc'
            elif file_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                file_type = 'xls'
            elif file_type in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
                file_type = 'ppt'
            else:
                file_type = 'stream'
        else:
            # 根据文件扩展名猜测类型
            ext = os.path.splitext(file_name)[1].lower()
            if ext in ['.mp3', '.wav', '.aac', '.m4a']:
                file_type = 'opus'
            elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                file_type = 'mp4'
            elif ext == '.pdf':
                file_type = 'pdf'
            elif ext in ['.doc', '.docx']:
                file_type = 'doc'
            elif ext in ['.xls', '.xlsx']:
                file_type = 'xls'
            elif ext in ['.ppt', '.pptx']:
                file_type = 'ppt'
            else:
                file_type = 'stream'

        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_name, f, 'application/octet-stream')
                }
                data = {
                    'file_type': file_type,
                    'file_name': file_name
                }
                
                self.logger.debug(f"POST: {url}")
                self.logger.debug(f"Headers: Authorization: Bearer [HIDDEN]")
                self.logger.debug(f"Form data: file_type={file_type}, file_name={file_name}")
                self.logger.debug(f"Uploading file: {file_path}")
                
                response = requests.post(url, headers=headers, data=data, files=files, verify=get_verify_setting())
                
                # 检查是否是token问题
                if response.status_code != 200:
                    self.logger.error(f"HTTP {response.status_code} error uploading file")
                    self.logger.error(f"Response: {response.text}")
                    
                    try:
                        error_data = response.json()
                        error_code = error_data.get('code', response.status_code)
                        error_msg = error_data.get('msg', 'Unknown error')
                        
                        # 如果是token问题，尝试刷新token
                        if error_code == 99991663:  # Invalid access token
                            self.logger.warning("检测到token失效，尝试刷新token")
                            new_token, err = self.get_tenant_access_token(force_refresh=True)
                            if err:
                                return "", Exception(f"刷新token失败: {err}")
                            
                            # 使用新token重试
                            headers["Authorization"] = f"Bearer {new_token}"
                            self.logger.info("使用新token重试上传")
                            
                            # 重新打开文件进行重试
                            with open(file_path, 'rb') as f:
                                files = {
                                    'file': (file_name, f, 'application/octet-stream')
                                }
                                response = requests.post(url, headers=headers, data=data, files=files, verify=get_verify_setting())
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    if result.get("code", 0) == 0:
                                        file_key = result["data"]["file_key"]
                                        self.logger.info(f"使用新token成功上传文件, file_key: {file_key}")
                                        return file_key, None
                        
                        return "", Exception(f"上传文件失败: code={error_code}, msg={error_msg}")
                    except:
                        return "", Exception(f"HTTP {response.status_code} error: {response.text}")
                
                response.raise_for_status()
                
                result = response.json()
                self.logger.debug(f"Response: {json.dumps(result, indent=2)}")
                
                if result.get("code", 0) != 0:
                    error_msg = f"failed to upload file: {result.get('msg', 'unknown error')}"
                    self.logger.error(f"ERROR: {error_msg}")
                    return "", Exception(error_msg)
                
                file_key = result["data"]["file_key"]
                self.logger.info(f"File uploaded successfully, file_key: {file_key}")
                return file_key, None
                
        except Exception as e:
            self.logger.error(f"ERROR: uploading file: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"ERROR: Response: {e.response.text}")
            return "", e

    def send_file_message(self, open_id: str, file_key: str) -> Tuple[Dict[str, Any], Optional[Exception]]:
        """向指定用户发送文件消息

        Args:
            open_id: 接收用户的open_id
            file_key: 文件key

        Returns:
            Tuple[Dict[str, Any], Optional[Exception]]: (response_data, error)
        """
        if not self.tenant_access_token:
            token, err = self.get_tenant_access_token()
            if err:
                return {}, err
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {
            "receive_id_type": "open_id"
        }
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        content = {
            "file_key": file_key
        }
        
        payload = {
            "receive_id": open_id,
            "msg_type": "file",
            "content": json.dumps(content)
        }
        
        try:
            self.logger.debug(f"POST: {url}")
            self.logger.debug(f"Params: {json.dumps(params)}")
            self.logger.debug(f"Headers: Authorization: Bearer [HIDDEN]")
            self.logger.debug(f"Request body: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, params=params, headers=headers, json=payload, verify=get_verify_setting())
            response.raise_for_status()
            
            result = response.json()
            self.logger.debug(f"Response: {json.dumps(result, indent=2)}")
            
            if result.get("code", 0) != 0:
                error_msg = f"failed to send file message: {result.get('msg', 'unknown error')}"
                self.logger.error(f"ERROR: {error_msg}")
                return {}, Exception(error_msg)
            
            self.logger.info(f"File message sent successfully to user {open_id}")
            return result["data"], None
            
        except Exception as e:
            self.logger.error(f"ERROR: sending file message: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"ERROR: Response: {e.response.text}")
            return {}, e

    def send_pdf_to_user(self, pdf_path: str, open_id: str) -> Tuple[bool, str]:
        """发送PDF文件给指定用户
        
        Args:
            pdf_path: PDF文件路径
            open_id: 接收用户的open_id
            
        Returns:
            Tuple[bool, str]: (成功标志, 消息)
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(pdf_path):
                error_msg = f"PDF文件不存在: {pdf_path}"
                self.logger.error(error_msg)
                return False, error_msg
            
            # 上传文件
            file_key, err = self.upload_file(pdf_path)
            if err:
                error_msg = f"上传PDF文件失败: {err}"
                self.logger.error(error_msg)
                return False, error_msg
            
            # 发送文件消息
            response_data, err = self.send_file_message(open_id, file_key)
            if err:
                error_msg = f"发送PDF消息失败: {err}"
                self.logger.error(error_msg)
                return False, error_msg
            
            message_id = response_data.get('message_id', 'N/A')
            success_msg = f"PDF文件已成功发送给用户 {open_id}，消息ID: {message_id}"
            self.logger.info(success_msg)
            return True, success_msg
            
        except Exception as e:
            error_msg = f"发送PDF文件时发生异常: {e}"
            self.logger.error(error_msg)
            return False, error_msg


if __name__ == "__main__":
    # 测试代码
    import argparse
    
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="发送PDF文件给飞书用户")
        parser.add_argument("--app_id", required=True, help="飞书应用ID")
        parser.add_argument("--app_secret", required=True, help="飞书应用密钥")
        parser.add_argument("--open_id", required=True, help="接收用户的open_id")
        parser.add_argument("--file_path", required=True, help="要发送的PDF文件路径")
        return parser.parse_args()
    
    args = parse_args()
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建PDF发送器
    sender = PDFSender(args.app_id, args.app_secret)
    
    # 发送PDF
    success, message = sender.send_pdf_to_user(args.file_path, args.open_id)
    
    if success:
        print(f"成功: {message}")
        sys.exit(0)
    else:
        print(f"失败: {message}")
        sys.exit(1)
