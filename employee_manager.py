#!/usr/bin/env python3
"""
员工管理模块
负责员工姓名映射和签名图片的实时获取和管理
"""
import json
import os
import time
from typing import Dict, Any, List, Optional
from feishu_api import FeishuAPI


class EmployeeManager:
    """员工管理器"""
    
    def __init__(self, feishu_api: FeishuAPI, base_url: str):
        self.feishu_api = feishu_api
        self.base_url = base_url
        self.employee_mapping = {}
        self.signature_cache = {}  # 签名图片缓存
        self.realtime_cache = {}  # 实时获取缓存，避免短时间内重复请求
        self.cache_ttl = 300  # 缓存有效期（秒）
        self._load_cached_mapping()
    
    def _load_cached_mapping(self):
        """加载缓存的员工映射"""
        try:
            mapping_file_path = os.path.join(os.path.dirname(__file__), "data", "employee_mapping.json")
            if os.path.exists(mapping_file_path):
                with open(mapping_file_path, 'r', encoding='utf-8') as f:
                    self.employee_mapping = json.load(f)
                print(f"已加载缓存的员工映射: {len(self.employee_mapping)} 个员工")
        except Exception as e:
            print(f"加载员工映射缓存失败: {e}")
            self.employee_mapping = {}
    
    def _save_mapping(self):
        """保存员工映射到文件"""
        try:
            mapping_file_path = os.path.join(os.path.dirname(__file__), "data", "employee_mapping.json")
            with open(mapping_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.employee_mapping, f, ensure_ascii=False, indent=2)
            print(f"员工映射已保存到 {mapping_file_path}")
        except Exception as e:
            print(f"保存员工映射失败: {e}")
    
    def refresh_employee_mapping(self) -> bool:
        """刷新员工映射数据"""
        try:
            print("开始刷新员工映射数据...")
            
            # 解析多维表格参数
            parsed_params = self.feishu_api.parse_base_url(self.base_url)
            app_token = parsed_params["app_token"]
            table_id = parsed_params["table_id"]
            view_id = parsed_params["view_id"]
            
            print(f"解析参数成功: app_token={app_token}, table_id={table_id}, view_id={view_id}")
            
            # 如果没有提供table_id，则列出所有数据表并使用第一个
            if not table_id:
                tables = self.feishu_api.list_tables(app_token)
                if len(tables) == 0:
                    print("ERROR: 没有找到数据表")
                    return False
                table_id = tables[0]["table_id"]
                print(f"使用第一个数据表: {table_id} - {tables[0].get('name', '无名称')}")
            
            # 查询所有记录
            records = self.feishu_api.search_records(app_token, table_id, view_id)
            print(f"成功获取 {len(records)} 条记录")
            
            # 生成员工姓名-ID映射
            new_mapping = {}
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
                if employee_name not in new_mapping:
                    new_mapping[employee_name] = employee_id
                
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
                signature_path = os.path.join(os.path.dirname(__file__), "signatures", new_filename)
                
                # 下载文件
                if self.feishu_api.download_file(file_url, signature_path):
                    processed_count += 1
                    # 缓存签名图片路径
                    self.signature_cache[employee_name] = signature_path
                else:
                    skipped_count += 1
            
            # 更新映射
            self.employee_mapping = new_mapping
            self._save_mapping()
            
            print(f"员工映射刷新完成: 成功处理 {processed_count} 个文件, 跳过 {skipped_count} 个记录")
            print(f"员工映射: {json.dumps(self.employee_mapping, ensure_ascii=False, indent=2)}")
            return True
            
        except Exception as e:
            print(f"刷新员工映射失败: {e}")
            return False
    
    def resolve_user_name_from_user_id(self, user_id: str) -> str:
        """根据用户ID解析用户姓名 - 实时获取"""
        if not user_id:
            return "未知用户"
        
        # 首先尝试从缓存中查找
        for name, open_id in self.employee_mapping.items():
            if open_id == user_id:
                return name
        
        # 如果缓存中没有，尝试实时获取
        try:
            print(f"缓存中未找到用户 {user_id}，尝试实时获取员工信息...")
            if self._refresh_single_employee(user_id):
                # 重新查找
                for name, open_id in self.employee_mapping.items():
                    if open_id == user_id:
                        return name
        except Exception as e:
            print(f"实时获取员工信息失败: {e}")
        
        return "未知用户"
    
    def get_signature_image_path(self, employee_name: str, force_refresh: bool = False) -> Optional[str]:
        """获取员工签名图片路径（支持强制刷新）"""
        if not employee_name or employee_name == "未知用户":
            return None
        
        # 如果强制刷新，清除缓存
        if force_refresh and employee_name in self.signature_cache:
            del self.signature_cache[employee_name]
        
        # 首先检查缓存
        if employee_name in self.signature_cache:
            cached_path = self.signature_cache[employee_name]
            if os.path.exists(cached_path):
                return cached_path
            else:
                # 缓存中的路径不存在，清除缓存
                del self.signature_cache[employee_name]
        
        # 构建图片文件路径
        image_filename = f"{employee_name}.png"
        image_path = os.path.join(os.path.dirname(__file__), "signatures", image_filename)
        
        # 检查文件是否存在
        if os.path.exists(image_path):
            # 更新缓存
            self.signature_cache[employee_name] = image_path
            return image_path
        else:
            # 尝试从多维表格获取最新的签名图片
            print(f"本地未找到员工 {employee_name} 的签名图片，尝试从多维表格获取...")
            if self._download_signature_from_table(employee_name):
                # 重新检查文件
                if os.path.exists(image_path):
                    self.signature_cache[employee_name] = image_path
                    return image_path
            
            print(f"警告: 未找到员工 {employee_name} 的签名图片: {image_path}")
            return None
    
    def _download_signature_from_table(self, employee_name: str) -> bool:
        """从多维表格下载指定员工的签名图片"""
        try:
            # 解析多维表格参数
            table_params = self.feishu_api.parse_base_url(self.base_url)
            app_token = table_params["app_token"]
            table_id = table_params["table_id"]
            view_id = table_params["view_id"]
            
            if not app_token or not table_id:
                print(f"无法解析多维表格参数")
                return False
            
            # 获取所有记录
            records = self.feishu_api.search_records(app_token, table_id, view_id)
            
            # 查找指定员工的记录
            for record in records:
                fields = record.get("fields", {})
                employee_field = fields.get("员工", [])
                
                if isinstance(employee_field, list) and len(employee_field) > 0:
                    first_employee = employee_field[0]
                    record_employee_name = first_employee.get("name")
                    
                    if record_employee_name == employee_name:
                        # 找到匹配的员工记录，获取签名图片
                        attachment_field = fields.get("附件", [])
                        if isinstance(attachment_field, list) and len(attachment_field) > 0:
                            first_attachment = attachment_field[0]
                            file_url = first_attachment.get("url")
                            original_name = first_attachment.get("name", "")
                            
                            if file_url:
                                file_extension = ""
                                if "." in original_name:
                                    file_extension = original_name[original_name.rfind("."):]
                                
                                new_filename = f"{employee_name}{file_extension}"
                                signature_path = os.path.join(os.path.dirname(__file__), "signatures", new_filename)
                                
                                if self.feishu_api.download_file(file_url, signature_path):
                                    self.signature_cache[employee_name] = signature_path
                                    print(f"成功从多维表格获取员工 {employee_name} 的最新签名图片")
                                    return True
                        break
            
            print(f"在多维表格中未找到员工 {employee_name} 的签名图片")
            return False
            
        except Exception as e:
            print(f"从多维表格获取签名图片失败: {e}")
            return False
    
    def refresh_all_signatures(self) -> Dict[str, bool]:
        """强制刷新所有员工的签名图片"""
        results = {}
        print("开始刷新所有员工的签名图片...")
        
        for employee_name in self.employee_mapping.keys():
            print(f"刷新员工 {employee_name} 的签名图片...")
            success = self._download_signature_from_table(employee_name)
            results[employee_name] = success
            if success:
                print(f"✅ 员工 {employee_name} 的签名图片刷新成功")
            else:
                print(f"❌ 员工 {employee_name} 的签名图片刷新失败")
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        print(f"签名图片刷新完成: {success_count}/{total_count} 成功")
        
        return results
    
    def get_employee_count(self) -> int:
        """获取员工数量"""
        return len(self.employee_mapping)
    
    def get_signature_count(self) -> int:
        """获取签名图片数量"""
        return len(self.signature_cache)
    
    def is_employee_known(self, user_id: str) -> bool:
        """检查用户ID是否在员工映射中"""
        return user_id in self.employee_mapping.values()
    
    def _refresh_single_employee(self, user_id: str) -> bool:
        """刷新单个员工的信息"""
        try:
            # 解析多维表格参数
            parsed_params = self.feishu_api.parse_base_url(self.base_url)
            app_token = parsed_params["app_token"]
            table_id = parsed_params["table_id"]
            view_id = parsed_params["view_id"]
            
            if not table_id:
                tables = self.feishu_api.list_tables(app_token)
                if len(tables) == 0:
                    return False
                table_id = tables[0]["table_id"]
            
            # 查询所有记录
            records = self.feishu_api.search_records(app_token, table_id, view_id)
            
            # 查找包含指定用户ID的记录
            for record in records:
                fields = record.get("fields", {})
                employee_field = fields.get("员工", [])
                
                if isinstance(employee_field, list) and len(employee_field) > 0:
                    first_employee = employee_field[0]
                    employee_name = first_employee.get("name")
                    employee_id = first_employee.get("id")
                    
                    if employee_id == user_id and employee_name:
                        # 更新映射
                        self.employee_mapping[employee_name] = employee_id
                        
                        # 获取并下载签名图片
                        attachment_field = fields.get("附件", [])
                        if isinstance(attachment_field, list) and len(attachment_field) > 0:
                            first_attachment = attachment_field[0]
                            file_url = first_attachment.get("url")
                            original_name = first_attachment.get("name", "")
                            
                            if file_url:
                                file_extension = ""
                                if "." in original_name:
                                    file_extension = original_name[original_name.rfind("."):]
                                
                                new_filename = f"{employee_name}{file_extension}"
                                signature_path = os.path.join(os.path.dirname(__file__), "signatures", new_filename)
                                
                                if self.feishu_api.download_file(file_url, signature_path):
                                    self.signature_cache[employee_name] = signature_path
                                    print(f"成功获取员工 {employee_name} 的签名图片")
                        
                        # 保存更新后的映射
                        self._save_mapping()
                        return True
            
            return False
            
        except Exception as e:
            print(f"刷新单个员工信息失败: {e}")
            return False
    
    def _is_cache_valid(self, user_id: str) -> bool:
        """检查缓存是否有效"""
        if user_id not in self.realtime_cache:
            return False
        
        cache_time = self.realtime_cache[user_id].get("timestamp", 0)
        current_time = time.time()
        return (current_time - cache_time) < self.cache_ttl
    
    def get_employee_info_realtime(self, user_id: str) -> Dict[str, Any]:
        """实时获取员工信息（姓名和签名图片路径）"""
        result = {
            "name": "未知用户",
            "signature_path": None
        }
        
        if not user_id:
            return result
        
        # 检查实时缓存是否有效
        if self._is_cache_valid(user_id):
            cached_info = self.realtime_cache[user_id]
            result["name"] = cached_info["name"]
            result["signature_path"] = cached_info["signature_path"]
            print(f"使用缓存的员工信息: {user_id} -> {result['name']}")
            return result
        
        # 首先尝试从员工映射缓存中查找
        for name, open_id in self.employee_mapping.items():
            if open_id == user_id:
                result["name"] = name
                # 尝试获取签名图片（如果本地没有则从多维表格获取）
                result["signature_path"] = self.get_signature_image_path(name)
                # 更新实时缓存
                self.realtime_cache[user_id] = {
                    "name": result["name"],
                    "signature_path": result["signature_path"],
                    "timestamp": time.time()
                }
                return result
        
        # 如果缓存中没有，尝试实时获取
        try:
            print(f"实时获取用户 {user_id} 的员工信息...")
            if self._refresh_single_employee(user_id):
                # 重新查找
                for name, open_id in self.employee_mapping.items():
                    if open_id == user_id:
                        result["name"] = name
                        result["signature_path"] = self.get_signature_image_path(name)
                        # 更新实时缓存
                        self.realtime_cache[user_id] = {
                            "name": result["name"],
                            "signature_path": result["signature_path"],
                            "timestamp": time.time()
                        }
                        break
        except Exception as e:
            print(f"实时获取员工信息失败: {e}")
        
        return result
    
    def clear_expired_cache(self):
        """清理过期的实时缓存"""
        current_time = time.time()
        expired_keys = []
        
        for user_id, cache_data in self.realtime_cache.items():
            cache_time = cache_data.get("timestamp", 0)
            if (current_time - cache_time) >= self.cache_ttl:
                expired_keys.append(user_id)
        
        for key in expired_keys:
            del self.realtime_cache[key]
        
        if expired_keys:
            print(f"清理了 {len(expired_keys)} 个过期的缓存项")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "employee_mapping_count": len(self.employee_mapping),
            "signature_cache_count": len(self.signature_cache),
            "realtime_cache_count": len(self.realtime_cache),
            "cache_ttl": self.cache_ttl
        }
