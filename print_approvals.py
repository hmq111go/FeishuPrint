#!/usr/bin/env python3
"""
简化版审批打印脚本
只显示审批通过实例的关键信息
"""
import sys
from feishu_approval_fetch import main, resolve_user_name_from_user_id, safe_format_ms, LOCAL_TZ
from feishu_approval_fetch import request_tenant_access_token, list_approval_instance_ids, fetch_approval_instance_detail
from feishu_approval_fetch import APP_ID, APP_SECRET, APPROVAL_CODE, START_TIME, END_TIME

def print_simple_approvals():
    """打印简化的审批信息"""
    print("=== 审批通过实例汇总 ===")
    
    # 获取token和实例列表
    tenant_token = request_tenant_access_token(APP_ID, APP_SECRET)
    instance_ids = list_approval_instance_ids(tenant_token, APPROVAL_CODE, START_TIME, END_TIME)
    
    approved_count = 0
    for instance_id in instance_ids:
        try:
            detail = fetch_approval_instance_detail(tenant_token, instance_id)
            
            # 只处理审批通过的实例
            if detail.get("status") != "APPROVED":
                continue
                
            approved_count += 1
            print(f"\n【{approved_count}】{detail.get('approval_name', 'N/A')}")
            print(f"    申请单号: {detail.get('serial_number', 'N/A')}")
            print(f"    申请人: {resolve_user_name_from_user_id(detail.get('open_id', ''))}")
            print(f"    申请时间: {safe_format_ms(detail.get('start_time', ''), LOCAL_TZ)}")
            
            # 显示审批节点
            timeline = detail.get("timeline", [])
            if timeline:
                print("    审批流程:")
                for i, item in enumerate(timeline, 1):
                    node_type = item.get('type', 'N/A')
                    user_name = resolve_user_name_from_user_id(item.get('open_id', ''))
                    create_time = safe_format_ms(item.get('create_time', ''), LOCAL_TZ)
                    
                    if node_type == "START":
                        print(f"      {i}. 申请提交 - {user_name} ({create_time})")
                    elif node_type == "AUTO_PASS":
                        print(f"      {i}. 自动通过 - 系统 ({create_time})")
                    else:
                        print(f"      {i}. {node_type} - {user_name} ({create_time})")
            
        except Exception as e:
            print(f"处理实例 {instance_id} 失败: {e}")
            continue
    
    print(f"\n=== 统计 ===")
    print(f"总共找到 {len(instance_ids)} 个审批实例")
    print(f"其中审批通过的有 {approved_count} 个")

if __name__ == "__main__":
    print_simple_approvals()
