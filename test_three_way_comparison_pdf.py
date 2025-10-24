#!/usr/bin/env python3
"""
测试三方比价单PDF生成功能
"""
import json
from pdf_generator import PDFGenerator
from feishu_api import FeishuAPI
from employee_manager import EmployeeManager

def test_three_way_comparison_pdf():
    """测试三方比价单PDF生成"""
    
    # 使用真实的三方比价审批数据
    approval_data = {
        "code": 0,
        "data": {
            "approval_code": "44A66AA6-201B-452C-AA90-531AC68C9023",
            "approval_name": "三方比价审批",
            "department_id": "7978g91d9744b3cg",
            "end_time": "1760170322101",
            "form": "[{\"id\":\"widget17187899037180001\",\"name\":\"申请日期\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-10-11T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget17187872518740001\",\"name\":\"需求部门\",\"type\":\"department\",\"ext\":{},\"value\":[{\"name\":\"热管理材料事业部\",\"open_id\":\"od-a1d9b874ba55fca2e178a1f8ef81d9cf\"}]},{\"id\":\"widget17187874750690001\",\"name\":\"需求人员\",\"type\":\"contact\",\"ext\":null,\"value\":[\"4f24egfg\"],\"open_ids\":[\"ou_66eaa49640ee1660c021ab50623135f2\"]},{\"id\":\"widget17170578162420001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产类\",\"option\":{\"key\":\"lwszw2b9-z02ahj8srf-0\",\"text\":\"固定资产类\"}},{\"id\":\"widget17170578517900001\",\"name\":\"物料描述/服务\",\"type\":\"input\",\"ext\":null,\"value\":\"旋转型真空等离子处理仪\"},{\"id\":\"widget17187872788750001\",\"name\":\"请购理由\",\"type\":\"input\",\"ext\":null,\"value\":\"表面处理氮化硼粉体\"},{\"id\":\"widget17234368161040001\",\"name\":\"三方比价\",\"type\":\"fieldList\",\"ext\":[],\"value\":[[{\"id\":\"widget17234368559160001\",\"name\":\"供应商名称\",\"type\":\"input\",\"ext\":null,\"value\":\"广州善准科技有限公司\"},{\"id\":\"widget17234368705110001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VP-TS7\"},{\"id\":\"widget17234369336230001\",\"name\":\"价格\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖万肆仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":94000}],[{\"id\":\"widget17234368559160001\",\"name\":\"供应商名称\",\"type\":\"input\",\"ext\":null,\"value\":\"合肥巢蜀仪器设备有限公司\"},{\"id\":\"widget17234368705110001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CS-PT7\"},{\"id\":\"widget17234369336230001\",\"name\":\"价格\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖万玖仟玖佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":99900}],[{\"id\":\"widget17234368559160001\",\"name\":\"供应商名称\",\"type\":\"input\",\"ext\":null,\"value\":\"海南硕方仪器设备有限公司\"},{\"id\":\"widget17234368705110001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"SFPT-7\"},{\"id\":\"widget17234369336230001\",\"name\":\"价格\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖万捌仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":98000}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}},{\"id\":\"widget17187875775230001\",\"name\":\"采购意见\",\"type\":\"textarea\",\"ext\":null,\"value\":\"基于对三家公司技术方案与报价的综合比价，建议采购善准科技VP-TS7型真空等离子处理仪。该设备在核心参数（13.56MHz射频、500W功率、7L旋转腔体、两路进气等）与竞品相当的情况下，具备以下突出优势：一是价格最优（94,000元），较另外两家低4,000-5,900元；二是交货最快（15个工作日），能及时满足使用需求；三是质保最长（主机2年），提供更可靠的售后保障。综上，善准科技产品在成本、效率和服务三方面均表现最佳，建议作为首选方案。\"},{\"id\":\"widget17170591482380001\",\"name\":\"比较参数文件\",\"type\":\"attachmentV2\",\"ext\":\"20251011-旋转型真空等离子处理仪-三方比价文件.zip,20251011-旋转型真空等离子处理仪-三方比价单.xlsx\",\"value\":[\"https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzBiNTI4NDA2ZDVmMGFmMDEyNTIwMTA1YTk5MTk1MWRfMmQ4ODA1YWUwODZlNWU3NDFhNTUxZmM3MDRiZTE1MThfSUQ6NzU1OTg1ODE4OTIwOTE1NzYzNF8xNzYxMjczNTQyOjE3NjEzNTk5NDJfVjM\",\"https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGVkZDNlNmYxMTFmNjczZGM5MTRkMWZiZjdmMzY4MTFfYjQ0M2Q1YjMxYTZiYWFlYzU3NTY4YTQ5NmViZmU2YzhfSUQ6NzU1OTg1ODIzNDAxNTg0MjMwOF8xNzYxMjczNTQyOjE3NjEzNTk5NDJfVjM\"]},{\"id\":\"widget17234426022670001\",\"name\":\"关联审批\",\"type\":\"connect\",\"ext\":{\"serialIDs\":\"202510110004\"},\"value\":[\"445257C7-FDC4-4BAB-8288-9E64DBE95B3A\"]}]",
            "instance_code": "DAFA56B8-452B-49A2-AEB4-9BA09B2CEA77",
            "open_id": "ou_275653b7df1ce4f279274540915e7b63",
            "reverted": False,
            "serial_number": "202510110005",
            "start_time": "1760166714805",
            "status": "APPROVED",
            "task_list": [
                {
                    "end_time": "1760167947329",
                    "id": "7559858477032308737",
                    "node_id": "61986b81b45736e536e29088282c08b5",
                    "node_name": "使用人",
                    "open_id": "ou_66eaa49640ee1660c021ab50623135f2",
                    "start_time": "1760166714952",
                    "status": "APPROVED",
                    "type": "AND",
                    "user_id": "4f24egfg"
                },
                {
                    "end_time": "1760169324926",
                    "id": "7559863770098139164",
                    "node_id": "259121169a075046b801e54c60fea432",
                    "node_name": "直属上级",
                    "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
                    "start_time": "1760167947355",
                    "status": "APPROVED",
                    "type": "AND",
                    "user_id": "92bdg1f7"
                },
                {
                    "end_time": "1760170004116",
                    "id": "7559869687305404444",
                    "node_id": "a4009f51d0d365cb460cdbc23756d1fa",
                    "node_name": "财务经理",
                    "open_id": "ou_e8396bd2538203347cc5146425531d69",
                    "start_time": "1760169325045",
                    "status": "APPROVED",
                    "type": "AND",
                    "user_id": "d8a4ec55"
                },
                {
                    "end_time": "1760170322077",
                    "id": "7559872604862611459",
                    "node_id": "4ddef6d4139f1ec493da92a7556b7212",
                    "node_name": "总经理",
                    "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
                    "start_time": "1760170004294",
                    "status": "APPROVED",
                    "type": "AND",
                    "user_id": "g792ba94"
                }
            ],
            "timeline": [
                {
                    "create_time": "1760166714805",
                    "ext": "{}",
                    "node_key": "",
                    "open_id": "ou_275653b7df1ce4f279274540915e7b63",
                    "type": "START",
                    "user_id": "afg1f21c"
                },
                {
                    "comment": "",
                    "create_time": "1760167947329",
                    "ext": "{}",
                    "node_key": "APPROVAL_359424_2927708",
                    "open_id": "ou_66eaa49640ee1660c021ab50623135f2",
                    "task_id": "7559858477032308737",
                    "type": "PASS",
                    "user_id": "4f24egfg"
                },
                {
                    "comment": "",
                    "create_time": "1760169324926",
                    "ext": "{}",
                    "node_key": "APPROVAL_471036_5850881",
                    "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
                    "task_id": "7559863770098139164",
                    "type": "PASS",
                    "user_id": "92bdg1f7"
                },
                {
                    "comment": "",
                    "create_time": "1760170004116",
                    "ext": "{}",
                    "node_key": "APPROVAL_355094_5519653",
                    "open_id": "ou_e8396bd2538203347cc5146425531d69",
                    "task_id": "7559869687305404444",
                    "type": "PASS",
                    "user_id": "d8a4ec55"
                },
                {
                    "comment": "",
                    "create_time": "1760170322077",
                    "ext": "{}",
                    "node_key": "APPROVAL_418755_5535183",
                    "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
                    "task_id": "7559872604862611459",
                    "type": "PASS",
                    "user_id": "g792ba94"
                }
            ],
            "user_id": "afg1f21c",
            "uuid": "83470881"
        },
        "msg": ""
    }
    
    try:
        APP_ID = "cli_a88a2172ee6c101c"
        APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
        EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"

        # 创建PDF生成器
        feishu_api = FeishuAPI(APP_ID, APP_SECRET)
        
        # 获取tenant_access_token
        token, error = feishu_api.get_tenant_access_token()
        if error:
            print(f"获取token失败: {error}")
            return False
        
        employee_manager = EmployeeManager(feishu_api, EMPLOYEE_BASE_URL)
        pdf_generator = PDFGenerator(feishu_api, employee_manager)
        
        # 生成PDF
        print("开始生成三方比价单PDF...")
        pdf_filename = pdf_generator.generate_three_way_comparison_pdf(approval_data["data"])
        
        if pdf_filename:
            print(f"✅ 三方比价单PDF生成成功: {pdf_filename}")
            return True
        else:
            print("❌ 三方比价单PDF生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== 三方比价单PDF生成测试 ===")
    success = test_three_way_comparison_pdf()
    if success:
        print("🎉 测试通过！")
    else:
        print("💥 测试失败！")
