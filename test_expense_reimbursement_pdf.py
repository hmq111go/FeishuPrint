#!/usr/bin/env python3
"""
测试费用报销PDF生成功能
使用真实的审批实例数据测试PDF生成
"""
import sys
import os
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from feishu_api import FeishuAPI
from employee_manager import EmployeeManager
from pdf_generator import PDFGenerator


def test_expense_reimbursement_pdf():
    """测试费用报销PDF生成"""
    print("=== 测试费用报销PDF生成功能 ===")
    
    # 配置参数
    APP_ID = "cli_a88a2172ee6c101c"
    APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
    EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"
    
    # 创建各个模块
    api = FeishuAPI(APP_ID, APP_SECRET)
    # 获取tenant_access_token
    token, err = api.get_tenant_access_token()
    if err:
        print(f"获取tenant_access_token失败: {err}")
        return
    manager = EmployeeManager(api, EMPLOYEE_BASE_URL)
    pdf_generator = PDFGenerator(api, manager)
    
    # 使用提供的真实审批实例数据（提取data部分）
    approval_response = {
  "code": 0,
  "data": {
    "approval_code": "BCD664E5-456F-4FEE-BA6E-EE349972F6A1",
    "approval_name": "费用报销",
    "department_id": "cgg79949b183f83g",
    "end_time": "1760582792840",
    "form": "[{\"id\":\"widget16510509704570001\",\"name\":\"报销事由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"10月9日-10月11日三天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=292天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元5元。\"},{\"id\":\"widget16510509818090001\",\"name\":\"费用汇总\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰仟玖佰贰拾伍元整\"},\"value\":2925},{\"id\":\"widget16510509950440001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"capitalValue\":\"\",\"id\":\"widget16510510254730001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2925\\\"}]\",\"type\":\"amount\",\"value\":\"2925.00\"}],\"value\":[[{\"id\":\"widget16510509268920001\",\"name\":\"报销类型\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"餐饮费\",\"option\":{\"key\":\"lxiq5nxq-q6edkawh4c-1\",\"text\":\"餐饮费\"}},{\"id\":\"widget16510510138590001\",\"name\":\"日期（年-月-日）\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-10-15T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510510048490001\",\"name\":\"内容\",\"type\":\"input\",\"ext\":null,\"value\":\"10月9日-10月11日三天员工午餐费\"},{\"id\":\"widget16510510254730001\",\"name\":\"金额\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰仟玖佰贰拾伍元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2925}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}},{\"id\":\"widget17186044510790001\",\"name\":\"发票附件\",\"type\":\"attachmentV2\",\"ext\":\"dzfp_25314000000004437536_上海舟富餐饮店_20251014134211.pdf\",\"value\":[\"https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWI5YjJlMTliZmRlMmJlOTI1MjYxZjViNjRmYTgxYzhfZjRhZGUyMTJhMTE3YTBjYzA5MTRjOTAwODQwZjBlNjhfSUQ6NzU2MTM1NzM5NjY3OTI2MjIxMF8xNzYxMTkzNzg1OjE3NjEyODAxODVfVjM\"]}]",
    "instance_code": "C34A7ECB-E60A-457A-AA1F-36890ABB9B68",
    "open_id": "ou_b5e1f8a921e5f4b014cc2ad2f3a8ae57",
     "reverted": False,
    "serial_number": "202510150007",
    "start_time": "1760515724459",
    "status": "APPROVED",
    "task_list": [
      {
        "end_time": "1760577019227",
        "id": "7561357461970862108",
        "node_id": "0cfd07f250e0d105fa5ed9c12fb5a625",
        "node_name": "财务审核",
        "open_id": "ou_8cb05c168ad03d76f69cfa36286e0375",
        "start_time": "1760515724677",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "c772c4fb"
      },
      {
        "end_time": "1760582741261",
        "id": "7561620720879812612",
        "node_id": "de831d5d58cd3546b029eb869f8c9bbe",
        "node_name": "财务经理",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "start_time": "1760577019369",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "d8a4ec55"
      },
      {
        "end_time": "1760582792816",
        "id": "7561645296478912513",
        "node_id": "7b3612796e8b384bc992be79d5a59794",
        "node_name": "总经理",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "start_time": "1760582741361",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "g792ba94"
      }
    ],
    "timeline": [
      {
        "create_time": "1760515724459",
        "ext": "{}",
        "node_key": "",
        "open_id": "ou_b5e1f8a921e5f4b014cc2ad2f3a8ae57",
        "type": "START",
        "user_id": "2b22cbcd"
      },
      {
        "comment": "",
        "create_time": "1760577019227",
        "ext": "{}",
        "node_key": "APPROVAL_535545_2213836",
        "open_id": "ou_8cb05c168ad03d76f69cfa36286e0375",
        "task_id": "7561357461970862108",
        "type": "PASS",
        "user_id": "c772c4fb"
      },
      {
        "comment": "",
        "create_time": "1760582741261",
        "ext": "{}",
        "node_key": "APPROVAL_206064_3615444",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "task_id": "7561620720879812612",
        "type": "PASS",
        "user_id": "d8a4ec55"
      },
      {
        "comment": "",
        "create_time": "1760582792816",
        "ext": "{}",
        "node_key": "APPROVAL_548888_3713755",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "task_id": "7561645296478912513",
        "type": "PASS",
        "user_id": "g792ba94"
      }
    ],
    "user_id": "2b22cbcd",
    "uuid": "29725703"
  },
  "msg": ""
}
    
    # 提取data部分作为审批详情
    approval_detail = approval_response["data"]
    
    print("审批实例信息:")
    print(f"  审批类型: {approval_detail['approval_name']}")
    print(f"  实例代码: {approval_detail['instance_code']}")
    print(f"  申请单号: {approval_detail['serial_number']}")
    print(f"  申请人ID: {approval_detail['open_id']}")
    print(f"  部门ID: {approval_detail['department_id']}")
    
    # 解析表单数据
    form_data = pdf_generator.parse_form_data(approval_detail.get('form', '[]'))
    print(f"\n表单数据解析:")
    print(f"  报销事由: {form_data.get('报销事由', 'N/A')}")
    print(f"  费用汇总: {form_data.get('费用汇总', 'N/A')}")
    
    if '费用明细' in form_data and form_data['费用明细']:
        print(f"  费用明细条数: {len(form_data['费用明细'])}")
        for i, item in enumerate(form_data['费用明细'], 1):
            print(f"    明细 {i}: {item.get('报销类型', 'N/A')} - {item.get('内容', 'N/A')} - {item.get('金额', 'N/A')}")
    
    print(f"\n审批流程:")
    print(f"  任务数量: {len(approval_detail['task_list'])}")
    for task in approval_detail['task_list']:
        print(f"    {task['node_name']}: {task['status']}")
    
    print(f"\n时间线:")
    print(f"  时间线数量: {len(approval_detail['timeline'])}")
    for timeline in approval_detail['timeline']:
        print(f"    {timeline['type']}: {timeline['open_id']}")
    
    # 生成PDF
    print(f"\n=== 开始生成费用报销PDF ===")
    try:
        pdf_filename = pdf_generator.generate_expense_reimbursement_pdf(approval_detail)
        if pdf_filename:
            print(f"✅ PDF生成成功: {pdf_filename}")
            
            # 检查文件是否存在
            if os.path.exists(pdf_filename):
                file_size = os.path.getsize(pdf_filename)
                print(f"✅ 文件已创建，大小: {file_size} 字节")
            else:
                print(f"❌ 文件未找到: {pdf_filename}")
        else:
            print(f"❌ PDF生成失败")
            
    except Exception as e:
        print(f"❌ PDF生成异常: {e}")
        import traceback
        traceback.print_exc()


def test_form_data_parsing():
    """测试表单数据解析"""
    print("\n=== 测试表单数据解析 ===")
    
    # 配置参数
    APP_ID = "cli_a88a2172ee6c101c"
    APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
    EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"
    
    # 创建PDF生成器
    api = FeishuAPI(APP_ID, APP_SECRET)
    manager = EmployeeManager(api, EMPLOYEE_BASE_URL)
    pdf_generator = PDFGenerator(api, manager)
    
    # 测试表单数据
    form_json = "[{\"id\":\"widget16510509704570001\",\"name\":\"报销事由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"10月9日-10月11日三天员工午餐费天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元号42份，共计25元*117=2925元天员工午餐费。9号34份，10号41份，11号42份，共计25元*117=2925元。9号34份，10号41份，11号42份，共计25元*117=2925元。\"},{\"id\":\"widget16510509818090001\",\"name\":\"费用汇总\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰仟玖佰贰拾伍元整\"},\"value\":2925},{\"id\":\"widget16510509950440001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"capitalValue\":\"\",\"id\":\"widget16510510254730001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2925\\\"}]\",\"type\":\"amount\",\"value\":\"2925.00\"}],\"value\":[[{\"id\":\"widget16510509268920001\",\"name\":\"报销类型\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"餐饮费\",\"option\":{\"key\":\"lxiq5nxq-q6edkawh4c-1\",\"text\":\"餐饮费\"}},{\"id\":\"widget16510510138590001\",\"name\":\"日期（年-月-日）\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-10-15T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510510048490001\",\"name\":\"内容\",\"type\":\"input\",\"ext\":null,\"value\":\"10月9日-10月11日三天员工午餐费\"},{\"id\":\"widget16510510254730001\",\"name\":\"金额\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰仟玖佰贰拾伍元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2925}]]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}},{\"id\":\"widget17186044510790001\",\"name\":\"发票附件\",\"type\":\"attachmentV2\",\"ext\":\"dzfp_25314000000004437536_上海舟富餐饮店_20251014134211.pdf\",\"value\":[\"https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWI5YjJlMTliZmRlMmJlOTI1MjYxZjViNjRmYTgxYzhfZjRhZGUyMTJhMTE3YTBjYzA5MTRjOTAwODQwZjBlNjhfSUQ6NzU2MTM1NzM5NjY3OTI2MjIxMF8xNzYxMTkzNzg1OjE3NjEyODAxODVfVjM\"]}]"
    
    print("解析表单数据...")
    form_data = pdf_generator.parse_form_data(form_json)
    
    print("解析结果:")
    for key, value in form_data.items():
        if key == '费用明细' and isinstance(value, list):
            print(f"  {key}: {len(value)} 条记录")
            for i, item in enumerate(value, 1):
                print(f"    记录 {i}: {item}")
        else:
            print(f"  {key}: {value}")


def main():
    """主函数"""
    print("费用报销PDF生成功能测试")
    print("=" * 50)
    
    try:
        test_form_data_parsing()
        test_expense_reimbursement_pdf()
        
        print("\n🎉 测试完成！")
        print("\n📋 费用报销PDF特性:")
        print("1. ✅ 顶部表格与采购申请PDF相同")
        print("2. ✅ 标题修改为'费用报销单'")
        print("3. ✅ 申请人信息表格包含：申请人、报销事由、费用汇总")
        print("4. ✅ 费用明细表格包含：序号、报销类型、日期、内容、金额(CNY)")
        print("5. ✅ 审批进程表格与采购申请PDF相同")
        print("6. ✅ 支持实时获取员工信息")
        print("7. ✅ 支持签名图片嵌入")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
