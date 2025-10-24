#!/usr/bin/env python3
"""
测试采购订单PDF生成功能
"""
import json
from pdf_generator import PDFGenerator
from feishu_api import FeishuAPI
from employee_manager import EmployeeManager

def test_three_way_comparison_pdf():
    """测试采购订单PDF生成"""
    
    # 使用真实的三方比价审批数据
    approval_data={
  "code": 0,
  "data": {
    "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
    "approval_name": "采购申请",
    "comment_list": [
      {
        "comment": "声共振的配件",
        "create_time": "1761198591000",
        "id": "7564289661236133907",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "user_id": "c3eg1g9e"
      },
      {
        "comment": "@喻莹莹这是一个小泵，和我们的大流量加油真空泵不太一样，拟归入那套HAM声共振设备，作为其配件。",
        "create_time": "1761274220000",
        "id": "7564614751252611091",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "user_id": "c3eg1g9e"
      },
      {
        "comment": "归入声共振的话 那声共振的总价值也要包含这个泵 还是需要入固定资产库 要不没法算",
        "create_time": "1761274445000",
        "id": "7564615591615938563",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "user_id": "afg1f21c"
      },
      {
        "comment": "@喻莹莹OK",
        "create_time": "1761274467000",
        "id": "7564615747051864067",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "user_id": "c3eg1g9e"
      }
    ],
    "department_id": "f2da4c3b37ggg8fg",
    "end_time": "1761274563666",
    "form": "[{\"id\":\"widget17501412425820001\",\"name\":\"采购信息填写链接\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?from=from_copylink\"},{\"id\":\"widget17573351239240001\",\"name\":\"原料库存查询表\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://boronmatrix.feishu.cn/share/base/query/shrcnFoFYTYmO1obPyq0kvHBaUb\"},{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-10-28T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"1\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"1206\\\"}]\",\"type\":\"amount\",\"value\":\"1206.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"1206.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"力辰无油真空泵\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"【负压 60】LC-VP-90\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹仟贰佰零陆元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1206},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹仟贰佰零陆元整\"},\"value\":1206},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.jd.com/100045188686.html#switch-sku\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"NMP处理，需要无油真空泵（电池分散液项目）\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"付佳佳\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
    "instance_code": "3B141036-A420-4AF1-A965-9C1778BB0277",
    "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
    "reverted": False,
    "serial_number": "202510230003",
    "start_time": "1761198465464",
    "status": "APPROVED",
    "task_list": [
      {
        "end_time": "1761199661435",
        "id": "7564289813299920915",
        "node_id": "19269e901ef75391121e2658485d5897",
        "node_name": "直属上级",
        "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
        "start_time": "1761198465847",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "92bdg1f7"
      },
      {
        "end_time": "1761273992335",
        "id": "7564294948909465604",
        "node_id": "90337e18ff7947bbc9cc1ff04795077d",
        "node_name": "财务经理",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "start_time": "1761199661591",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "d8a4ec55"
      },
      {
        "end_time": "1761274010669",
        "id": "7564614197754740755",
        "node_id": "14fd352abcd55c10e565839f49af3cd0",
        "node_name": "总经理",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "start_time": "1761273992495",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "g792ba94"
      },
      {
        "end_time": "1761274088710",
        "id": "7564614276934516739",
        "node_id": "982f2752071cafaf5a3b3174a24703d2",
        "node_name": "采购",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "start_time": "1761274010935",
        "status": "DONE",
        "type": "AND",
        "user_id": "afg1f21c"
      },
      {
        "end_time": "1761274371708",
        "id": "7564614611191005188",
        "node_id": "b078ffd28db767c502ac367053f6e0ac",
        "node_name": "发起",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "start_time": "1761274088732",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "c3eg1g9e"
      },
      {
        "end_time": "1761274451624",
        "id": "7564615826603982851",
        "node_id": "982f2752071cafaf5a3b3174a24703d2",
        "node_name": "采购",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "start_time": "1761274371750",
        "status": "DONE",
        "type": "AND",
        "user_id": "afg1f21c"
      },
      {
        "end_time": "1761274483865",
        "id": "7564616169825976324",
        "node_id": "b078ffd28db767c502ac367053f6e0ac",
        "node_name": "发起",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "start_time": "1761274451651",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "c3eg1g9e"
      },
      {
        "end_time": "1761274500522",
        "id": "7564616308420509715",
        "node_id": "982f2752071cafaf5a3b3174a24703d2",
        "node_name": "采购",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "start_time": "1761274483909",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "afg1f21c"
      },
      {
        "end_time": "1761274563563",
        "id": "7564616380626354180",
        "node_id": "98b97e3670619f8d0b939ffc6d16f736",
        "node_name": "本人确认",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "start_time": "1761274500650",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "c3eg1g9e"
      }
    ],
    "timeline": [
      {
        "create_time": "1761198465464",
        "ext": "{}",
        "node_key": "",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "type": "START",
        "user_id": "c3eg1g9e"
      },
      {
        "comment": "",
        "create_time": "1761199661435",
        "ext": "{}",
        "node_key": "APPROVAL_356820_2517926",
        "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
        "task_id": "7564289813299920915",
        "type": "PASS",
        "user_id": "92bdg1f7"
      },
      {
        "comment": "",
        "create_time": "1761273992335",
        "ext": "{}",
        "node_key": "APPROVAL_463016_525501",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "task_id": "7564294948909465604",
        "type": "PASS",
        "user_id": "d8a4ec55"
      },
      {
        "comment": "",
        "create_time": "1761274010669",
        "ext": "{}",
        "node_key": "APPROVAL_776186_4250112",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "task_id": "7564614197754740755",
        "type": "PASS",
        "user_id": "g792ba94"
      },
      {
        "comment": "采购类别选错了\n",
        "create_time": "1761274088710",
        "ext": "{}",
        "node_key": "APPROVAL_563750_4347501",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "task_id": "7564614276934516739",
        "type": "ROLLBACK_SELECTED",
        "user_id": "afg1f21c"
      },
      {
        "create_time": "1761274371708",
        "ext": "{}",
        "node_key": "START",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "task_id": "7564614611191005188",
        "type": "PASS",
        "user_id": "c3eg1g9e"
      },
      {
        "create_time": "1761274451624",
        "ext": "{}",
        "node_key": "APPROVAL_563750_4347501",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "task_id": "7564615826603982851",
        "type": "ROLLBACK_SELECTED",
        "user_id": "afg1f21c"
      },
      {
        "create_time": "1761274483865",
        "ext": "{}",
        "node_key": "START",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "task_id": "7564616169825976324",
        "type": "PASS",
        "user_id": "c3eg1g9e"
      },
      {
        "comment": "",
        "create_time": "1761274500522",
        "ext": "{}",
        "node_key": "APPROVAL_563750_4347501",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "task_id": "7564616308420509715",
        "type": "PASS",
        "user_id": "afg1f21c"
      },
      {
        "comment": "",
        "create_time": "1761274563563",
        "ext": "{}",
        "node_key": "APPROVAL_426508_4434576",
        "open_id": "ou_37f682b09c1b0796e45f4c7d2927d32a",
        "task_id": "7564616380626354180",
        "type": "PASS",
        "user_id": "c3eg1g9e"
      }
    ],
    "user_id": "c3eg1g9e",
    "uuid": "4daa2730"
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
        print("开始生成采购订单PDF...")
        pdf_filename = pdf_generator.generate_procurement_approval_pdf(approval_data["data"])
        
        if pdf_filename:
            print(f"✅ 采购订单PDF生成成功: {pdf_filename}")
            return True
        else:
            print("❌ 采购订单PDF生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== 采购订单PDF生成测试 ===")
    success = test_three_way_comparison_pdf()
    if success:
        print("🎉 测试通过！")
    else:
        print("💥 测试失败！")
