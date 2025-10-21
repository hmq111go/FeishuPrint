#!/usr/bin/env python3
"""
生成审批进程表格
获取某一天通过的审批，生成包含采购订单明细和审批进程的表格
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple, Union

from feishu_approval_fetch import (
    request_tenant_access_token,
    list_approval_instance_ids,
    fetch_approval_instance_detail,
    resolve_user_name_from_user_id,
    safe_format_ms,
    LOCAL_TZ,
    APP_ID,
    APP_SECRET,
    APPROVAL_CODE
)


def load_employee_mapping() -> Dict[str, str]:
    """加载员工映射文件"""
    try:
        mapping_file_path = os.path.join(os.path.dirname(__file__), "employee_mapping.json")
        with open(mapping_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载员工映射文件失败: {e}")
        return {}


def parse_form_data(form_json: str) -> Dict[str, Any]:
    """解析表单数据"""
    try:
        form_data = json.loads(form_json)
        result = {}

        for widget in form_data:
            widget_id = widget.get('id', '')
            widget_name = widget.get('name', '')
            widget_type = widget.get('type', '')
            widget_value = widget.get('value', '')

            # 处理明细表格控件
            if widget_type == 'fieldList':
                if isinstance(widget_value, list) and len(widget_value) > 0:
                    items = []
                    for row in widget_value:
                        item = {}
                        for cell in row:
                            cell_name = cell.get('name', '')
                            cell_value = cell.get('value', '')
                            item[cell_name] = cell_value
                        items.append(item)
                    result[widget_name] = items
            else:
                result[widget_name] = widget_value

        return result
    except Exception as e:
        print(f"解析表单数据失败: {e}")
        return {}


def format_timeline_table(timeline: List[Dict[str, Any]], employee_mapping: Dict[str, str]) -> List[List[str]]:
    """格式化审批时间线为表格格式"""
    table_data = []

    for i, item in enumerate(timeline, 1):
        node_type = item.get('type', '')
        node_key = item.get('node_key', '')
        create_time = item.get('create_time', '')
        open_id = item.get('open_id', '')
        user_id = item.get('user_id', '')
        comment = item.get('comment', '')
        cc_user_list = item.get('cc_user_list', [])

        # 获取处理人姓名
        processor_name = "未知用户"
        if open_id:
            processor_name = resolve_user_name_from_user_id(open_id)
        elif user_id:
            processor_name = resolve_user_name_from_user_id(user_id)

        # 格式化时间
        formatted_time = safe_format_ms(create_time, LOCAL_TZ)

        # 根据节点类型确定节点名称和处理结果
        if node_type == "START":
            node_name = "发起"
            result = "发起审批"
        elif node_type == "PASS":
            node_name = "审批"
            result = "已通过"
        elif node_type == "REJECT":
            node_name = "审批"
            result = "已拒绝"
        elif node_type == "AUTO_PASS":
            node_name = "自动审批"
            result = "已通过"
        elif node_type == "AUTO_REJECT":
            node_name = "自动审批"
            result = "已拒绝"
        elif node_type == "CC":
            node_name = "抄送"
            cc_count = len(cc_user_list)
            cc_names = []
            for cc_user in cc_user_list:
                cc_open_id = cc_user.get('open_id', '')
                cc_name = resolve_user_name_from_user_id(cc_open_id)
                cc_names.append(cc_name)
            result = f"抄送 {cc_count} 人 {', '.join(cc_names)}"
        else:
            node_name = node_type
            result = "处理"

        # 使用node_key作为节点名称，如果为空则使用默认的node_name
        display_node_name = node_key if node_key else node_name

        table_data.append([
            str(i),
            display_node_name,
            processor_name,
            result,
            formatted_time
        ])

    return table_data


def generate_approval_report(query_date: str = "2025-10-15"):
    """生成审批报告"""
    print(f"=== 获取 {query_date} 审批通过的采购申请 ===")

    # 计算查询时间范围
    d = datetime.strptime(query_date, "%Y-%m-%d").date()
    start_dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=LOCAL_TZ)
    end_dt = start_dt + timedelta(days=1) - timedelta(milliseconds=1)
    start_time = str(int(start_dt.timestamp() * 1000))
    end_time = str(int(end_dt.timestamp() * 1000))

    # 获取token和实例列表
    tenant_token = request_tenant_access_token(APP_ID, APP_SECRET)
    instance_ids = list_approval_instance_ids(tenant_token, APPROVAL_CODE, start_time, end_time)

    # 加载员工映射
    employee_mapping = load_employee_mapping()

    approved_count = 0

    for instance_id in instance_ids:
        try:
            detail = fetch_approval_instance_detail(tenant_token, instance_id)

            # 只处理审批通过的实例
            if detail.get("status") != "APPROVED":
                continue

            approved_count += 1

            print(f"\n{'=' * 80}")
            print(f"【{approved_count}】{detail.get('approval_name', 'N/A')}")
            print(f"申请单号: {detail.get('serial_number', 'N/A')}")
            print(f"申请人: {resolve_user_name_from_user_id(detail.get('open_id', ''))}")
            print(f"申请时间: {safe_format_ms(detail.get('start_time', ''), LOCAL_TZ)}")
            print(f"完成时间: {safe_format_ms(detail.get('end_time', ''), LOCAL_TZ)}")

            # 解析表单数据
            form_data = parse_form_data(detail.get('form', '[]'))

            # 显示采购明细
            if '费用明细' in form_data:
                print(f"\n--- 采购明细 ---")
                items = form_data['费用明细']
                if isinstance(items, list):
                    for i, item in enumerate(items, 1):
                        print(f"{i}. {item.get('名称', 'N/A')} - {item.get('规格型号', 'N/A')}")
                        print(f"   数量: {item.get('数量', 'N/A')} {item.get('单位', 'N/A')}")
                        print(f"   单价: {item.get('单价', 'N/A')} 元")
                        print(f"   金额: {item.get('金额', 'N/A')} 元")
                        print(f"   供应商: {item.get('购买链接/供应商', 'N/A')}")
                        print(f"   请购理由: {item.get('请购理由', 'N/A')}")
                        print(f"   领用人: {item.get('领用人', 'N/A')}")
                        print()

            # 显示审批进程表格
            timeline = detail.get("timeline", [])
            if timeline:
                print("--- 审批进程 ---")
                table_data = format_timeline_table(timeline, employee_mapping)

                # 打印表格
                print("序号 | 节点名称 | 处理人 | 处理结果 | 处理时间")
                print("-" * 80)
                for row in table_data:
                    print(f"{row[0]:<4} | {row[1]:<8} | {row[2]:<8} | {row[3]:<12} | {row[4]}")

        except Exception as e:
            print(f"处理实例 {instance_id} 失败: {e}")
            continue

    print(f"\n=== 统计 ===")
    print(f"总共找到 {len(instance_ids)} 个审批实例")
    print(f"其中审批通过的有 {approved_count} 个")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        query_date = sys.argv[1]
    else:
        query_date = "2025-10-15"  # 默认查询日期

    generate_approval_report(query_date)


if __name__ == "__main__":
    main()
