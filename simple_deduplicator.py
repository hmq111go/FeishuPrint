#!/usr/bin/env python3
"""
简化的去重机制
只存储 id+状态 组合，避免重复生成PDF
"""
import json
import os
import time
import logging
from datetime import datetime, timezone, timedelta
from typing import Set, Dict, Any
from pathlib import Path


class SimpleDeduplicator:
    """简化的去重管理器"""
    
    def __init__(self, data_dir: str = "data", retention_days: int = 7):
        """
        初始化简化去重管理器
        
        Args:
            data_dir: 数据存储目录
            retention_days: 数据保留天数，默认7天
        """
        self.data_dir = Path(data_dir)
        self.retention_days = retention_days
        self.logger = logging.getLogger(__name__)
        
        # 确保数据目录存在
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件路径
        self.processed_file = self.data_dir / "processed_combinations.json"
        
        # 内存缓存：存储已处理的 id+状态 组合
        self.processed_combinations: Set[str] = set()
        
        # 加载现有数据
        self._load_data()
        
        self.logger.info(f"简化去重管理器初始化完成，保留天数: {retention_days}")
        self.logger.info(f"当前已处理组合数: {len(self.processed_combinations)}")
    
    def _load_data(self):
        """从JSON文件加载数据"""
        try:
            if self.processed_file.exists():
                with open(self.processed_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.processed_combinations = set(data.get('combinations', []))
                    self.logger.info(f"已加载 {len(self.processed_combinations)} 个已处理组合")
            
        except Exception as e:
            self.logger.error(f"加载数据失败: {e}")
            self.processed_combinations = set()
    
    def _save_data(self):
        """保存数据到JSON文件"""
        try:
            data = {
                'combinations': list(self.processed_combinations),
                'last_updated': time.time()
            }
            
            with open(self.processed_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"保存数据失败: {e}")
    
    def is_processed(self, instance_id: str, status: str) -> bool:
        """
        检查 id+状态 组合是否已处理过
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
            
        Returns:
            True 如果已处理过，False 如果未处理过
        """
        combination = f"{instance_id}:{status}"
        return combination in self.processed_combinations
    
    def is_processing(self, instance_id: str, status: str) -> bool:
        """
        检查 id+状态 组合是否正在处理中
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
            
        Returns:
            True 如果正在处理中，False 如果未在处理中
        """
        processing_key = f"{instance_id}:{status}:processing"
        return processing_key in self.processed_combinations
    
    def mark_processing(self, instance_id: str, status: str):
        """
        标记 id+状态 组合为正在处理中
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
        """
        processing_key = f"{instance_id}:{status}:processing"
        self.processed_combinations.add(processing_key)
        self._save_data()
        self.logger.info(f"[重试机制] 已标记为正在处理: {instance_id}:{status}")
    
    def mark_processing_complete(self, instance_id: str, status: str):
        """
        标记处理完成，移除处理中标记，添加完成标记
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
        """
        processing_key = f"{instance_id}:{status}:processing"
        combination = f"{instance_id}:{status}"
        
        # 移除处理中标记
        self.processed_combinations.discard(processing_key)
        # 添加完成标记
        self.processed_combinations.add(combination)
        
        self._save_data()
        self.logger.info(f"[重试机制] 处理完成: {instance_id}:{status}")
    
    def mark_processing_failed(self, instance_id: str, status: str):
        """
        标记处理失败，移除处理中标记
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
        """
        processing_key = f"{instance_id}:{status}:processing"
        self.processed_combinations.discard(processing_key)
        self._save_data()
        self.logger.info(f"[重试机制] 处理失败，移除处理中标记: {instance_id}:{status}")
    
    def mark_processed(self, instance_id: str, status: str):
        """
        标记 id+状态 组合为已处理
        
        Args:
            instance_id: 实例ID
            status: 状态（如 "APPROVED"）
        """
        combination = f"{instance_id}:{status}"
        self.processed_combinations.add(combination)
        
        # 立即保存到文件
        self._save_data()
        
        self.logger.info(f"[简化去重] 已标记组合为已处理: {instance_id}:{status}")
    
    def cleanup_old_data(self):
        """清理过期数据"""
        try:
            current_time = time.time()
            
            # 如果文件超过保留天数未更新，清理所有数据
            if self.processed_file.exists():
                file_age = current_time - self.processed_file.stat().st_mtime
                if file_age > (self.retention_days * 24 * 3600):
                    self.logger.info(f"[简化去重] 数据文件超过 {self.retention_days} 天，清理所有数据")
                    self.processed_combinations.clear()
                    self._save_data()
                    return True
            
            # 如果组合数过多，清理一半（保留最新的）
            if len(self.processed_combinations) > 50000:  # 5万个组合
                self.logger.info(f"[简化去重] 组合数过多 ({len(self.processed_combinations)})，清理一半")
                combinations_list = list(self.processed_combinations)
                keep_count = len(combinations_list) // 2
                self.processed_combinations = set(combinations_list[-keep_count:])
                self._save_data()
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"清理过期数据失败: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "processed_combinations": len(self.processed_combinations),
            "retention_days": self.retention_days,
            "data_file_size": self.processed_file.stat().st_size if self.processed_file.exists() else 0,
            "data_dir": str(self.data_dir)
        }
    
    def force_cleanup(self):
        """强制清理所有数据"""
        try:
            self.processed_combinations.clear()
            
            if self.processed_file.exists():
                self.processed_file.unlink()
            
            self.logger.info("[简化去重] 已强制清理所有数据")
            
        except Exception as e:
            self.logger.error(f"强制清理失败: {e}")


def test_simple_deduplicator():
    """测试简化去重管理器"""
    import tempfile
    import shutil
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("=== 测试简化去重管理器 ===")
        
        # 创建去重管理器
        deduplicator = SimpleDeduplicator(data_dir=temp_dir, retention_days=7)
        
        # 测试基本功能
        print("\n1. 测试基本功能")
        instance_id = "test_instance_001"
        status = "APPROVED"
        
        # 第一次检查
        is_processed = deduplicator.is_processed(instance_id, status)
        print(f"组合 {instance_id}:{status} 是否已处理: {is_processed}")
        
        # 标记为已处理
        deduplicator.mark_processed(instance_id, status)
        print(f"已标记组合 {instance_id}:{status} 为已处理")
        
        # 再次检查
        is_processed = deduplicator.is_processed(instance_id, status)
        print(f"组合 {instance_id}:{status} 是否已处理: {is_processed}")
        
        # 测试不同状态
        print("\n2. 测试不同状态")
        status2 = "REJECTED"
        is_processed2 = deduplicator.is_processed(instance_id, status2)
        print(f"组合 {instance_id}:{status2} 是否已处理: {is_processed2}")
        
        # 测试大量数据
        print("\n3. 测试大量数据")
        for i in range(1000):
            test_id = f"test_instance_{i:06d}"
            test_status = "APPROVED"
            deduplicator.mark_processed(test_id, test_status)
        
        # 统计信息
        print("\n4. 统计信息")
        stats = deduplicator.get_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        print("\n✅ 测试完成")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"已清理临时目录: {temp_dir}")


if __name__ == "__main__":
    test_simple_deduplicator()
