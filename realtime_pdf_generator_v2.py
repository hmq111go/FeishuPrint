#!/usr/bin/env python3
"""
实时PDF生成器 V2 - 模块化版本
当审批通过时自动生成包含签名图片的PDF报告
支持员工映射和签名图片的实时获取
"""
import json
import os
import sys
import time
import logging
import threading
from typing import Dict, Any, Set, Optional
from concurrent.futures import ThreadPoolExecutor

import lark_oapi as lark

from feishu_api import FeishuAPI
from employee_manager import EmployeeManager
from pdf_generator import PDFGenerator
from simple_deduplicator import SimpleDeduplicator


class RealtimePDFGenerator:
    """实时PDF生成器主类"""
    
    def __init__(self, app_id: str, app_secret: str, employee_base_url: str):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.app_id = app_id
        self.app_secret = app_secret
        self.employee_base_url = employee_base_url
        
        # 四种审批定义类型
        self.approval_definitions = {
            "三方比价": "44A66AA6-201B-452C-AA90-531AC68C9023",
            "固定资产": "8466E949-4EFD-47CE-A6D7-FCC26EA07A54", 
            "费用报销": "BCD664E5-456F-4FEE-BA6E-EE349972F6A1",
            "采购申请": "A851D76E-6B63-4DD4-91F2-998693422C3C",
            "浙江采购申请": "8234771B-2FE6-4111-B648-0EC3480A61D2",
            "浙江费用报销": "0B800158-599F-4876-8C04-36E8B5B4290B",
            "知本采购申请": "A66AF5F6-650A-486E-AF48-A4E37385471F"
        }
        
        # 初始化各个模块
        self.feishu_api = FeishuAPI(app_id, app_secret)
        self.employee_manager = EmployeeManager(self.feishu_api, employee_base_url)
        self.pdf_generator = PDFGenerator(self.feishu_api, self.employee_manager, auto_send=True)
        
        # 初始化简化去重管理器（7天窗口）
        self.deduplicator = SimpleDeduplicator(data_dir="data", retention_days=7)
        
        # 异步处理相关
        self.executor = ThreadPoolExecutor(max_workers=3)  # 限制并发数避免资源竞争
        self.response_timeout = 2.5  # 2.5秒内必须返回响应，留0.5秒缓冲
    
    def get_approval_type_name(self, approval_code: str) -> str:
        """根据审批定义代码获取审批类型名称"""
        for type_name, code in self.approval_definitions.items():
            if code == approval_code:
                return type_name
        return "未知类型"
    
    def extract_event_id(self, event_dict: Dict[str, Any]) -> Optional[str]:
        """提取事件唯一标识符（支持v1.0和v2.0版本）"""
        event_data = event_dict.get("event", {})
        
        # v2.0版本事件：使用event_id字段
        if "event_id" in event_data:
            return event_data["event_id"]
        
        # v1.0版本事件：使用uuid字段
        if "uuid" in event_data:
            return event_data["uuid"]
        
        # 如果都没有，使用instance_code作为备选（向后兼容）
        instance_code = event_data.get("instance_code", "")
        if instance_code:
            self.logger.warning(f"[事件去重] 未找到uuid或event_id字段，使用instance_code作为备选: {instance_code}")
            return f"instance_{instance_code}"
        
        return None
    
    def is_duplicate_event(self, event_id: str, status: str, retry_count: int = 0) -> bool:
        """检查是否为重复事件"""
        return self.deduplicator.is_processed(event_id, status)
    
    def is_instance_pdf_generated(self, instance_code: str) -> bool:
        """检查实例是否已经生成过PDF"""
        return self.deduplicator.is_processed(instance_code, "APPROVED")
    
    def is_instance_processing(self, instance_code: str) -> bool:
        """检查实例是否正在处理中"""
        return self.deduplicator.is_processing(instance_code, "APPROVED")
    
    def mark_instance_processing(self, instance_code: str):
        """标记实例正在处理中"""
        self.deduplicator.mark_processing(instance_code, "APPROVED")
    
    def mark_instance_processing_complete(self, instance_code: str):
        """标记实例处理完成"""
        self.deduplicator.mark_processing_complete(instance_code, "APPROVED")
    
    def mark_instance_processing_failed(self, instance_code: str):
        """标记实例处理失败"""
        self.deduplicator.mark_processing_failed(instance_code, "APPROVED")
    
    def mark_instance_pdf_generated(self, instance_code: str, pdf_filename: str):
        """标记实例已生成PDF"""
        self.deduplicator.mark_processed(instance_code, "APPROVED")
    
    def cleanup_expired_events(self):
        """清理过期数据"""
        self.deduplicator.cleanup_old_data()
    
    def do_approval_instance_event(self, data: lark.CustomizedEvent) -> None:
        """处理审批实例状态变更事件（快速响应版本）"""
        start_time = time.time()
        
        try:
            event_data = lark.JSON.marshal(data, indent=4)
            event_dict = json.loads(event_data)

            self.logger.debug(f"[审批事件接收] 原始事件数据: {event_data}")

            # 提取事件信息
            if not event_dict:
                self.logger.warning("[事件处理] 事件数据为空，忽略")
                return

            # 提取事件唯一标识符
            event_id = self.extract_event_id(event_dict)
            if not event_id:
                self.logger.error("[事件处理] 无法提取事件唯一标识符，忽略事件")
                return

            # 提取事件信息
            event_data = event_dict.get("event", {})
            status = event_data.get("status", "")
            instance_code = event_data.get("instance_code", "")
            approval_code = event_data.get("approval_code", "")
            operate_time = event_data.get("operate_time", "")

            # 提取重试次数信息（如果存在）
            retry_count = 0
            if "retry_cnt" in event_dict:
                retry_count = event_dict["retry_cnt"]
                self.logger.info(f"[事件处理] 检测到重试事件，重试次数: {retry_count}")

            # 检查是否为重复事件（基于事件ID + 状态）
            if self.is_duplicate_event(event_id, status, retry_count):
                return

            self.logger.info(f"[审批事件处理] 事件ID: {event_id}, 审批状态: {status}, 实例Code: {instance_code}, 审批定义Code: {approval_code}")

            # 只处理审批通过事件
            if status != "APPROVED":
                self.logger.debug(f"[事件处理] 审批状态为 {status}，无需处理")
                return

            # 检查响应时间，确保在3秒内返回
            elapsed_time = time.time() - start_time
            if elapsed_time > self.response_timeout:
                self.logger.warning(f"[事件处理] 响应时间过长 ({elapsed_time:.2f}s)，可能导致飞书重发事件")

            # 异步处理PDF生成，立即返回响应
            self.executor.submit(self._process_approval_async, event_id, instance_code, approval_code, event_dict)
            
            # 记录处理统计
            processing_time = time.time() - start_time
            self.logger.info(f"[事件处理] 事件 {event_id} 已提交异步处理，响应时间: {processing_time:.3f}s")

        except Exception as e:
            self.logger.error(f"[事件处理异常] 处理事件时发生错误: {e}")
            import traceback
            traceback.print_exc()

    def _process_approval_async(self, event_id: str, instance_code: str, approval_code: str, event_dict: Dict[str, Any]):
        """异步处理审批通过事件（带重试机制）"""
        max_retries = 3
        retry_delay = 5  # 重试间隔（秒）
        
        try:
            # 检查是否已经生成过PDF
            if self.is_instance_pdf_generated(instance_code):
                self.logger.info(f"[去重] 实例 {instance_code} 已生成过PDF，跳过重复处理")
                return
            
            # 检查是否正在处理中
            if self.is_instance_processing(instance_code):
                self.logger.info(f"[重试] 实例 {instance_code} 正在处理中，跳过重复处理")
                return
            
            # 标记为正在处理中
            self.mark_instance_processing(instance_code)
            
            # 清理过期缓存
            self.employee_manager.clear_expired_cache()
            
            # 获取审批类型
            approval_type = self.get_approval_type_name(approval_code)
            self.logger.info(f"[异步处理] 开始处理审批实例 {instance_code} ({approval_type})，事件ID: {event_id}")
            
            # 重试循环
            for attempt in range(max_retries):
                try:
                    # 确保有有效的tenant_token
                    if not self.feishu_api.tenant_token:
                        tenant_token, err = self.feishu_api.get_tenant_access_token()
                        if err:
                            self.logger.error(f"[异步处理] 获取tenant_access_token失败: {err}")
                            raise Exception(f"获取tenant_access_token失败: {err}")
                    else:
                        tenant_token = self.feishu_api.tenant_token
                    
                    # 获取审批实例详情
                    if not instance_code:
                        self.logger.error("[异步处理] 未找到实例ID，无法获取详情")
                        raise Exception("未找到实例ID")
                    
                    try:
                        approval_detail = self.feishu_api.fetch_approval_instance_detail(instance_code)
                    except Exception as e:
                        self.logger.error(f"[异步处理] 获取审批实例详情失败: {e}")
                        self.logger.error(f"[异步处理] 实例ID: {instance_code}")
                        raise Exception(f"获取审批实例详情失败: {e}")
                    
                    # 根据审批类型调用对应的PDF生成器
                    pdf_filename = None
                    if approval_type == "采购申请":
                        pdf_filename = self.pdf_generator.generate_procurement_approval_pdf(approval_detail)
                    elif approval_type == "浙江采购申请":
                        pdf_filename = self.pdf_generator.generate_zhejiang_procurement_approval_pdf(approval_detail)
                    elif approval_type == "浙江费用报销":
                        pdf_filename = self.pdf_generator.generate_zhejiang_expense_reimbursement_pdf(approval_detail)
                    elif approval_type == "知本-采购申请":
                        pdf_filename = self.pdf_generator.generate_zhiben_procurement_approval_pdf(approval_detail)
                    elif approval_type == "三方比价":
                        pdf_filename = self.pdf_generator.generate_three_way_comparison_pdf(approval_detail)
                    elif approval_type == "固定资产":
                        pdf_filename = self.pdf_generator.generate_fixed_asset_acceptance_pdf(approval_detail)
                    elif approval_type == "费用报销":
                        pdf_filename = self.pdf_generator.generate_expense_reimbursement_pdf(approval_detail)
                    else:
                        self.logger.error(f"[异步处理] 未知的审批类型: {approval_type}")
                        raise Exception(f"未知的审批类型: {approval_type}")
                    
                    if pdf_filename:
                        # 标记处理完成
                        self.mark_instance_processing_complete(instance_code)
                        self.logger.info(f"[异步处理成功] 审批实例 {instance_code} ({approval_type}) 的PDF报告已生成: {pdf_filename}")
                        return  # 成功，退出重试循环
                    else:
                        raise Exception("PDF生成失败")
                        
                except Exception as e:
                    self.logger.error(f"[异步处理] 第 {attempt + 1} 次尝试失败: {e}")
                    
                    if attempt < max_retries - 1:
                        self.logger.info(f"[重试] 等待 {retry_delay} 秒后进行第 {attempt + 2} 次重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                    else:
                        # 最后一次尝试失败
                        self.mark_instance_processing_failed(instance_code)
                        self.logger.error(f"[异步处理失败] 审批实例 {instance_code} ({approval_type}) 经过 {max_retries} 次重试后仍然失败")
                        raise
                
        except Exception as e:
            self.logger.error(f"[异步处理异常] 处理审批实例 {instance_code} 时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    def refresh_employee_data(self) -> bool:
        """刷新员工数据"""
        self.logger.info("=== 刷新员工数据 ===")
        return self.employee_manager.refresh_employee_mapping()
    
    def get_event_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.deduplicator.get_stats()
        return {
            "processed_combinations": stats["processed_combinations"],
            "response_timeout": self.response_timeout,
            "executor_threads": self.executor._max_workers,
            "retention_days": stats["retention_days"],
            "data_dir": stats["data_dir"],
            "data_file_size": stats["data_file_size"]
        }
    
    def start_periodic_cleanup(self):
        """启动定期清理任务"""
        def cleanup_task():
            while True:
                try:
                    time.sleep(300)  # 每5分钟清理一次
                    self.cleanup_expired_events()
                except Exception as e:
                    self.logger.error(f"[定期清理] 清理任务异常: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
        self.logger.info("[定期清理] 已启动定期清理任务，每5分钟清理一次")
    
    def start_retry_mechanism(self):
        """启动重试机制"""
        def retry_task():
            while True:
                try:
                    time.sleep(60)  # 每分钟检查一次
                    self._retry_failed_tasks()
                except Exception as e:
                    self.logger.error(f"[重试机制] 重试任务异常: {e}")
        
        retry_thread = threading.Thread(target=retry_task, daemon=True)
        retry_thread.start()
        self.logger.info("[重试机制] 已启动重试任务，每分钟检查一次失败的任务")
    
    def _retry_failed_tasks(self):
        """重试失败的任务"""
        try:
            # 这里可以实现更复杂的重试逻辑
            # 目前简化处理，主要依赖主流程的重试机制
            self.logger.debug("[重试机制] 检查失败任务...")
        except Exception as e:
            self.logger.error(f"[重试机制] 重试失败任务时发生错误: {e}")
    
    def start(self):
        """启动实时PDF生成器"""
        self.logger.info("=== 实时PDF生成器 V2 启动（优化版） ===")
        self.logger.info("当审批通过时自动生成包含签名图片的PDF报告")
        self.logger.info("支持的审批类型:")
        for approval_type, approval_code in self.approval_definitions.items():
            self.logger.info(f"  - {approval_type}: {approval_code}")
        
        # 显示配置信息
        stats = self.get_event_stats()
        self.logger.info(f"\n系统配置:")
        self.logger.info(f"  - 响应超时: {stats['response_timeout']} 秒")
        self.logger.info(f"  - 异步线程数: {stats['executor_threads']}")
        self.logger.info(f"  - 数据保留: {stats['retention_days']} 天")
        
        self.logger.info(f"\n员工管理状态:")
        cache_stats = self.employee_manager.get_cache_stats()
        self.logger.info(f"  - 员工映射数量: {cache_stats['employee_mapping_count']}")
        self.logger.info(f"  - 签名图片数量: {cache_stats['signature_cache_count']}")
        self.logger.info(f"  - 实时缓存数量: {cache_stats['realtime_cache_count']}")
        self.logger.info(f"  - 缓存有效期: {cache_stats['cache_ttl']} 秒")
        
        self.logger.info("\n=== 步骤1: 获取 tenant_access_token ===")
        tenant_access_token, err = self.feishu_api.get_tenant_access_token()
        if err:
            self.logger.error(f"Error: 获取 tenant_access_token 失败: {err}")
            return False

        self.logger.info("\n=== 步骤2: 刷新员工数据 ===")
        if not self.refresh_employee_data():
            self.logger.warning("警告: 员工数据刷新失败，将使用缓存数据")

        self.logger.info("\n=== 步骤3: 订阅审批事件 ===")
        subscription_success = True
        for approval_type, approval_code in self.approval_definitions.items():
            self.logger.info(f"正在订阅 {approval_type} 审批事件...")
            if not self.feishu_api.subscribe_approval_event(approval_code):
                self.logger.error(f"订阅 {approval_type} 审批事件失败")
                subscription_success = False
            else:
                self.logger.info(f"订阅 {approval_type} 审批事件成功")
        
        if not subscription_success:
            self.logger.warning("部分审批事件订阅失败，但将继续启动WebSocket客户端...")

        self.logger.info("\n=== 步骤4: 启动定期清理任务 ===")
        self.start_periodic_cleanup()
        
        self.logger.info("\n=== 步骤5: 启动重试机制 ===")
        self.start_retry_mechanism()

        self.logger.info("\n=== 步骤6: 注册事件处理函数 ===")
        # 注册审批实例状态变更事件（支持V1和V2版本）
        event_handler = lark.EventDispatcherHandler.builder(self.app_id, self.app_secret) \
            .register_p1_customized_event("approval_instance", self.do_approval_instance_event) \
            .register_p1_customized_event("approval_instance_v2", self.do_approval_instance_event) \
            .build()

        self.logger.info("\n=== 步骤7: 启动 WebSocket 客户端 ===")
        self.logger.info("正在连接飞书事件推送服务...")
        self.logger.info("等待审批通过事件，将自动生成包含签名图片的PDF报告...")
        self.logger.info("注意: 系统已优化为快速响应模式，确保3秒内返回HTTP 200状态码")
        cli = lark.ws.Client(self.app_id, self.app_secret,
                             event_handler=event_handler, log_level=lark.LogLevel.WARNING)
        self.logger.info("WebSocket客户端已启动，等待接收审批事件...")
        cli.start()
        
        return True


def main():
    """主函数"""
    # 配置参数
    APP_ID = "cli_a88a2172ee6c101c"
    APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
    EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"
    
    # 创建并启动实时PDF生成器
    generator = RealtimePDFGenerator(APP_ID, APP_SECRET, EMPLOYEE_BASE_URL)
    
    try:
        generator.start()
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"程序运行异常: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
