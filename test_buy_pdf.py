#!/usr/bin/env python3
"""
测试采购订单PDF生成功能
"""
import json
from pdf_generator import PDFGenerator
from feishu_api import FeishuAPI
from employee_manager import EmployeeManager

def test_buy():
    """测试采购订单PDF生成"""
    
    # 使用真实的三方比价审批数据
    approval_data={
  "code": 0,
  "data": {
    "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
    "approval_name": "采购申请",
    "department_id": "cgg79949b183f83g",
    "end_time": "1761637856722",
    "form": "[{\"id\":\"widget17501412425820001\",\"name\":\"采购信息填写链接\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?from=from_copylink\"},{\"id\":\"widget17573351239240001\",\"name\":\"原料库存查询表\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://boronmatrix.feishu.cn/share/base/query/shrcnFoFYTYmO1obPyq0kvHBaUb\"},{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-11-14T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"费用类\",\"option\":{\"key\":\"lwhggrby-3izab5oq1d-3\",\"text\":\"费用类\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"23\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"375\\\"}]\",\"type\":\"amount\",\"value\":\"375.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"1295.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增 |\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"抽纸\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"20包/提\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"提\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":8},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":50},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"肆佰元整\"},\"value\":400},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"京东\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"办公室行政\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"江涛\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增 |\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"擦手纸\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"20包/箱\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"箱\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"捌拾伍元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":85},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰佰伍拾伍元整\"},\"value\":255},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"京东\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"办公室行政\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"江涛\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增 |\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"卷纸\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"20卷/箱\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"箱\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":5},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":50},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\"},\"value\":250},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"京东\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"办公室行政\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"江涛\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增 |\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"矿泉水\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"箱\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"箱\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":6},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":40},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰佰肆拾元整\"},\"value\":240},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"京东\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"办公室行政\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"江涛\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增 |\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"A4打印纸\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"10包/箱\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"箱\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":150},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰伍拾元整\"},\"value\":150},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"京东\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"办公室行政\"},{\"id\":\"widget17497940675090001\",\"name\":\"需求人\",\"type\":\"input\",\"ext\":null,\"value\":\"江涛\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}},{\"id\":\"widget16510609389860001\",\"name\":\"附件\",\"type\":\"attachmentV2\",\"ext\":\"办公用品购买记录.xlsx\",\"value\":[\"https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGJlNTVkMzc2MDNjYmMwNWRhNGRmZjBlYmJjNzM2ODlfNTg5ODdhNjkxNjViNGJkNDRiNzFhMDAyYTA5ZjI1NTNfSUQ6NzU2NjE1NDcxNzQxOTExMDQwM18xNzYxNjM4MzU3OjE3NjE3MjQ3NTdfVjM\"]}]",
    "instance_code": "E3CF92C0-B0C6-429C-A76D-8525403A55C9",
    "open_id": "ou_f429f462cc8f7a9c709baadcc7b1f70b",
    "reverted": False,
    "serial_number": "202510280005",
    "start_time": "1761632698469",
    "status": "APPROVED",
    "task_list": [
      {
        "end_time": "1761632726172",
        "id": "7566154830163525636",
        "node_id": "19269e901ef75391121e2658485d5897",
        "node_name": "直属上级",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "start_time": "1761632698911",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "g792ba94"
      },
      {
        "end_time": "1761637789496",
        "id": "7566154947751182339",
        "node_id": "90337e18ff7947bbc9cc1ff04795077d",
        "node_name": "财务经理",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "start_time": "1761632726318",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "d8a4ec55"
      },
      {
        "end_time": "1761637811461",
        "id": "7566176694607527939",
        "node_id": "14fd352abcd55c10e565839f49af3cd0",
        "node_name": "总经理",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "start_time": "1761637789651",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "g792ba94"
      },
      {
        "end_time": "1761637833959",
        "id": "7566176789362851844",
        "node_id": "982f2752071cafaf5a3b3174a24703d2",
        "node_name": "采购",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "start_time": "1761637811719",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "afg1f21c"
      },
      {
        "end_time": "1761637856606",
        "id": "7566176885551497220",
        "node_id": "98b97e3670619f8d0b939ffc6d16f736",
        "node_name": "本人确认",
        "open_id": "ou_f429f462cc8f7a9c709baadcc7b1f70b",
        "start_time": "1761637834088",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "2b22cbcd"
      }
    ],
    "timeline": [
      {
        "create_time": "1761632698469",
        "ext": "{}",
        "node_key": "",
        "open_id": "ou_f429f462cc8f7a9c709baadcc7b1f70b",
        "type": "START",
        "user_id": "2b22cbcd"
      },
      {
        "comment": "",
        "create_time": "1761632726172",
        "ext": "{}",
        "node_key": "APPROVAL_356820_2517926",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "task_id": "7566154830163525636",
        "type": "PASS",
        "user_id": "g792ba94"
      },
      {
        "comment": "",
        "create_time": "1761637789496",
        "ext": "{}",
        "node_key": "APPROVAL_463016_525501",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "task_id": "7566154947751182339",
        "type": "PASS",
        "user_id": "d8a4ec55"
      },
      {
        "comment": "",
        "create_time": "1761637811461",
        "ext": "{}",
        "node_key": "APPROVAL_776186_4250112",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "task_id": "7566176694607527939",
        "type": "PASS",
        "user_id": "g792ba94"
      },
      {
        "comment": "",
        "create_time": "1761637833959",
        "ext": "{}",
        "node_key": "APPROVAL_563750_4347501",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "task_id": "7566176789362851844",
        "type": "PASS",
        "user_id": "afg1f21c"
      },
      {
        "comment": "",
        "create_time": "1761637856606",
        "ext": "{}",
        "node_key": "APPROVAL_426508_4434576",
        "open_id": "ou_f429f462cc8f7a9c709baadcc7b1f70b",
        "task_id": "7566176885551497220",
        "type": "PASS",
        "user_id": "2b22cbcd"
      }
    ],
    "user_id": "2b22cbcd",
    "uuid": "0394264b"
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
    success = test_buy()
    if success:
        print("🎉 测试通过！")
    else:
        print("💥 测试失败！")
