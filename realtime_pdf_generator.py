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
from typing import Dict, Any, Set

import lark_oapi as lark

from feishu_api import FeishuAPI
from employee_manager import EmployeeManager
from pdf_generator import PDFGenerator


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
            "采购申请": "A851D76E-6B63-4DD4-91F2-998693422C3C"
        }
        
        # 初始化各个模块
        self.feishu_api = FeishuAPI(app_id, app_secret)
        self.employee_manager = EmployeeManager(self.feishu_api, employee_base_url)
        self.pdf_generator = PDFGenerator(self.feishu_api, self.employee_manager)
        
        # 事件去重机制：记录已处理的审批实例
        self.processed_instances: Set[str] = set()
        self.instance_processing_time: Dict[str, float] = {}
        self.DEDUPLICATION_WINDOW = 300  # 5分钟内的重复事件将被忽略
    
    def get_approval_type_name(self, approval_code: str) -> str:
        """根据审批定义代码获取审批类型名称"""
        for type_name, code in self.approval_definitions.items():
            if code == approval_code:
                return type_name
        return "未知类型"
    
    def is_duplicate_event(self, instance_code: str, operate_time: str) -> bool:
        """检查是否为重复事件"""
        current_time = time.time()
        
        # 清理过期的处理记录
        expired_instances = []
        for instance, process_time in self.instance_processing_time.items():
            if current_time - process_time > self.DEDUPLICATION_WINDOW:
                expired_instances.append(instance)
        
        for instance in expired_instances:
            self.processed_instances.discard(instance)
            del self.instance_processing_time[instance]
        
        # 检查是否已处理过此实例
        if instance_code in self.processed_instances:
            self.logger.debug(f"[事件去重] 审批实例 {instance_code} 已在去重窗口内处理过，忽略重复事件")
            return True
        
        # 记录处理时间和实例
        self.processed_instances.add(instance_code)
        self.instance_processing_time[instance_code] = current_time
        
        return False
    
    def do_approval_instance_event(self, data: lark.CustomizedEvent) -> None:
        """处理审批实例状态变更事件"""
        event_data = lark.JSON.marshal(data, indent=4)
        event_dict = json.loads(event_data)

        self.logger.debug(f"[审批事件接收] 原始事件数据: {event_data}")

        # 提取事件信息
        if event_dict:
            status = event_dict.get("event", {}).get("status", "")
            instance_code = event_dict.get("event", {}).get("instance_code", "")
            approval_code = event_dict.get("event", {}).get("approval_code", "")
            operate_time = event_dict.get("event", {}).get("operate_time", "")

            self.logger.info(f"[审批事件处理] 审批状态: {status}, 实例Code: {instance_code}, 审批定义Code: {approval_code}")

            # 处理审批通过事件
            if status == "APPROVED":
                # 检查是否为重复事件
                if self.is_duplicate_event(instance_code, operate_time):
                    return
                # 清理过期缓存
                self.employee_manager.clear_expired_cache()
                
                # 获取审批类型
                approval_type = self.get_approval_type_name(approval_code)
                self.logger.info(f"[审批通过] 审批实例 {instance_code} 已通过审批，审批类型: {approval_type}，开始生成PDF...")
                
                try:
                    # 确保有有效的tenant_token
                    if not self.feishu_api.tenant_token:
                        tenant_token, err = self.feishu_api.get_tenant_access_token()
                        if err:
                            self.logger.error(f"获取tenant_access_token失败: {err}")
                            return
                    else:
                        tenant_token = self.feishu_api.tenant_token
                    
                    # 获取审批实例详情
                    instance_id = event_dict.get("event", {}).get("instance_code", "")
                    if not instance_id:
                        self.logger.error("未找到实例ID，无法获取详情")
                        return
                    
                    approval_detail = self.feishu_api.fetch_approval_instance_detail(instance_id)
                    
                    # 根据审批类型调用对应的PDF生成器
                    pdf_filename = None
                    if approval_type == "采购申请":
                        pdf_filename = self.pdf_generator.generate_procurement_approval_pdf(approval_detail)
                    elif approval_type == "三方比价":
                        pdf_filename = self.pdf_generator.generate_three_way_comparison_pdf(approval_detail)
                    elif approval_type == "固定资产":
                        pdf_filename = self.pdf_generator.generate_fixed_asset_pdf(approval_detail)
                    elif approval_type == "费用报销":
                        pdf_filename = self.pdf_generator.generate_expense_reimbursement_pdf(approval_detail)
                    else:
                        self.logger.error(f"[PDF生成失败] 未知的审批类型: {approval_type}")
                        return
                    
                    if pdf_filename:
                        self.logger.info(f"[PDF生成成功] 审批实例 {instance_code} ({approval_type}) 的PDF报告已生成: {pdf_filename}")
                    else:
                        self.logger.error(f"[PDF生成失败] 审批实例 {instance_code} ({approval_type}) 的PDF报告生成失败")
                        
                except Exception as e:
                    self.logger.error(f"[PDF生成异常] 处理审批实例 {instance_code} ({approval_type}) 时发生错误: {e}")
                    import traceback
                    traceback.print_exc()
    
    def refresh_employee_data(self) -> bool:
        """刷新员工数据"""
        self.logger.info("=== 刷新员工数据 ===")
        return self.employee_manager.refresh_employee_mapping()
    
    def start(self):
        """启动实时PDF生成器"""
        self.logger.info("=== 实时PDF生成器 V2 启动 ===")
        self.logger.info("当审批通过时自动生成包含签名图片的PDF报告")
        self.logger.info("支持的审批类型:")
        for approval_type, approval_code in self.approval_definitions.items():
            self.logger.info(f"  - {approval_type}: {approval_code}")
        
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

        self.logger.info("\n=== 步骤4: 注册事件处理函数 ===")
        # 注册审批实例状态变更事件（支持V1和V2版本）
        event_handler = lark.EventDispatcherHandler.builder(self.app_id, self.app_secret) \
            .register_p1_customized_event("approval_instance", self.do_approval_instance_event) \
            .register_p1_customized_event("approval_instance_v2", self.do_approval_instance_event) \
            .build()

        self.logger.info("\n=== 步骤5: 启动 WebSocket 客户端 ===")
        self.logger.info("正在连接飞书事件推送服务...")
        self.logger.info("等待审批通过事件，将自动生成包含签名图片的PDF报告...")
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
