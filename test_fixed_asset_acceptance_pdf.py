#!/usr/bin/env python3
"""
测试固定资产验收PDF生成
"""
import json
from pdf_generator import PDFGenerator
from feishu_api import FeishuAPI
from employee_manager import EmployeeManager

def test_fixed_asset_acceptance_pdf():
    """测试固定资产验收PDF生成"""
    
    # 模拟审批数据
    # approval_data = {
    #     "code": 0,
    #     "data": {
    #         "approval_code": "8466E949-4EFD-47CE-A6D7-FCC26EA07A54",
    #         "approval_name": "固定资产验收单",
    #         "comment_list": [
    #             {
    #                 "comment": "发票已到",
    #                 "create_time": "1749100288000",
    #                 "id": "7512327608856985603",
    #                 "open_id": "ou_275653b7df1ce4f279274540915e7b63",
    #                 "user_id": "afg1f21c"
    #             }
    #         ],
    #         "department_id": "7978g91d9744b3cg",
    #         "end_time": "1749103697484",
    #         "form": """[{"id":"widget17453863872090001","name":"说明 1","type":"text","ext":null,"value":"固定资产验收意见从以下四个方面进行:\\n1.资产核实:清点核对实物数量型号规格等是否一致,同时核实供应商提供的配件附件是否完备;\\n2.资产状况检查:保证其外观无损坏，正常运转,强调对设备运行指标、性能要求等检查;\\n3.资产功能测试:根据其用途进行相应测试,确保资产能够正常工作,如果有人员培训情况也一并说明;\\n4.验收记录:在验收过程中及时记录资产的验收情况,包括验收日期、人员、结果等信息。同时对于不合格资产需要详细记录并及时与供应商联系。（若有供应商提供的验收报告也一并上传）"},{"id":"widget17182776409580001","name":"供应商","type":"input","ext":null,"value":"巴斯德仪器(苏州)有限公司"},{"id":"widget17182796346940001","name":"使用部门","type":"checkboxV2","ext":null,"value":["复合材料事业部"],"option":[{"key":"lxd7bvgm-7lwvky81yqx-0","text":"复合材料事业部"}]},{"id":"widget17182776530460001","name":"资产信息","type":"fieldList","ext":[],"value":[[{"id":"widget17182776850450001","name":"资产名称","type":"input","ext":null,"value":"厚度计"},{"id":"widget17182793745190001","name":"规格型号","type":"input","ext":null,"value":"547-401A"},{"id":"widget17182776934400001","name":"数量/单位","type":"input","ext":null,"value":"1个"},{"id":"widget17183323389860001","name":"到货日期","type":"date","ext":null,"value":"2025-05-30T00:00:00+08:00","timezoneOffset":-480},{"id":"widget17182794373820001","name":"购置日期","type":"date","ext":null,"value":"2025-05-28T00:00:00+08:00","timezoneOffset":-480}],[{"id":"widget17182776850450001","name":"资产名称","type":"input","ext":null,"value":"厚度计"},{"id":"widget17182793745190001","name":"规格型号","type":"input","ext":null,"value":"547-321A"},{"id":"widget17182776934400001","name":"数量/单位","type":"input","ext":null,"value":"1个"},{"id":"widget17183323389860001","name":"到货日期","type":"date","ext":null,"value":"2025-05-30T00:00:00+08:00","timezoneOffset":-480},{"id":"widget17182794373820001","name":"购置日期","type":"date","ext":null,"value":"2025-05-28T00:00:00+08:00","timezoneOffset":-480}]],"option":{"input_type":"LIST","mobile_detail_type":"CARD","print_type":"FORM"}},{"id":"widget17182800812470001","name":"到货资料","type":"attachmentV2","ext":"img_v3_02mv_0eb2c966-5d10-4820-85ff-093b60734a3g.jpg","value":["https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjZkMDRiOWZiYzBjZmZkYjA3NWFiYmRiOGVlOWI2MTRfNmYwOWQ1ZDU1MjZmN2M3MDk2MTM3YWVmMmNiOWJjMzhfSUQ6NzUxMjMxMDI3NDUyMzg1Njg5OV8xNzYxMjA2ODkyOjE3NjEyOTMyOTJfVjM"]},{"id":"widget17477962183030001","name":"说明 2","type":"text","ext":null,"value":"验收情况（验收人填写）"},{"id":"widget17477931839460001","name":"1.数量是否符合","type":"radioV2","ext":null,"value":"是","option":{"key":"maxaxnt6-e024hywlko-0","text":"是"}},{"id":"widget17477931876010001","name":"2.规格型号是否符合","type":"radioV2","ext":null,"value":"是","option":{"key":"maxaxqmq-gorhnia0k4f-0","text":"是"}},{"id":"widget17477931907240001","name":"3.配件是否齐全","type":"radioV2","ext":null,"value":"是","option":{"key":"maxaxt1g-3ja8bouty7a-0","text":"是"}},{"id":"widget17477931893490001","name":"4.外观包装是否完好","type":"radioV2","ext":null,"value":"是","option":{"key":"maxaxrz9-fyiz4y7q0jk-0","text":"是"}},{"id":"widget17477968198490001","name":"5.功能测试结果","type":"input","ext":null,"value":"正常使用"},{"id":"widget17477962724260001","name":"说明 3","type":"text","ext":null,"value":"验收记录（验收人填写）"},{"id":"widget17477964834430001","name":"验收结果","type":"radioV2","ext":null,"value":"通过","option":{"key":"maxcwdpv-e6mebxe7e1g-0","text":"通过"}},{"id":"widget17477962999420001","name":"参与验收人员","type":"input","ext":null,"value":"马俊丽、代建"},{"id":"widget17477963190600001","name":"验收日期","type":"input","ext":null,"value":"20250603"}]""",
    #         "instance_code": "584BFD93-6F76-42BC-A27B-3FA1F8B73625",
    #         "open_id": "ou_5c2544b23439593d0f9195d2aaaecda3",
    #         "reverted": False,
    #         "serial_number": "202506050002",
    #         "start_time": "1749096064416",
    #         "status": "APPROVED",
    #         "task_list": [
    #             {
    #                 "end_time": "1749097335561",
    #                 "id": "7512310395815919635",
    #                 "node_id": "68ffedca539bb73e09a3d44aaa5ff060",
    #                 "node_name": "使用人",
    #                 "open_id": "ou_66eaa49640ee1660c021ab50623135f2",
    #                 "start_time": "1749096064631",
    #                 "status": "APPROVED",
    #                 "type": "AND",
    #                 "user_id": "4f24egfg"
    #             },
    #             {
    #                 "end_time": "1749098141198",
    #                 "id": "7512315854869413907",
    #                 "node_id": "7dddd64e00a4e238d99720e1fce90c86",
    #                 "node_name": "直属上级",
    #                 "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
    #                 "start_time": "1749097335671",
    #                 "status": "APPROVED",
    #                 "type": "AND",
    #                 "user_id": "92bdg1f7"
    #             },
    #             {
    #                 "end_time": "1749100291285",
    #                 "id": "7512319315581239299",
    #                 "node_id": "2e70ccedff335e77440dd5f13bff3f52",
    #                 "node_name": "采购审核",
    #                 "open_id": "ou_275653b7df1ce4f279274540915e7b63",
    #                 "start_time": "1749098141347",
    #                 "status": "APPROVED",
    #                 "type": "AND",
    #                 "user_id": "afg1f21c"
    #             },
    #             {
    #                 "end_time": "1749103114130",
    #                 "id": "7512328549928353811",
    #                 "node_id": "7c4751efad1f32b298bc7102f0597783",
    #                 "node_name": "财务经理",
    #                 "open_id": "ou_e8396bd2538203347cc5146425531d69",
    #                 "start_time": "1749100291465",
    #                 "status": "APPROVED",
    #                 "type": "AND",
    #                 "user_id": "d8a4ec55"
    #             },
    #             {
    #                 "end_time": "1749103697433",
    #                 "id": "7512340673390362625",
    #                 "node_id": "08a1f4532ea2e7c78f83fc4f7a852942",
    #                 "node_name": "总经理",
    #                 "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
    #                 "start_time": "1749103114237",
    #                 "status": "APPROVED",
    #                 "type": "AND",
    #                 "user_id": "g792ba94"
    #             }
    #         ],
    #         "timeline": [
    #             {
    #                 "create_time": "1749096064416",
    #                 "ext": "{}",
    #                 "node_key": "",
    #                 "open_id": "ou_5c2544b23439593d0f9195d2aaaecda3",
    #                 "type": "START",
    #                 "user_id": "5ba33374"
    #             },
    #             {
    #                 "comment": "使用无异常，验收通过。",
    #                 "create_time": "1749097335561",
    #                 "ext": "{}",
    #                 "node_key": "APPROVAL_869758_1955538",
    #                 "open_id": "ou_66eaa49640ee1660c021ab50623135f2",
    #                 "task_id": "7512310395815919635",
    #                 "type": "PASS",
    #                 "user_id": "4f24egfg"
    #             },
    #             {
    #                 "comment": "",
    #                 "create_time": "1749098141198",
    #                 "ext": "{}",
    #                 "node_key": "APPROVAL_379811_2455273",
    #                 "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
    #                 "task_id": "7512315854869413907",
    #                 "type": "PASS",
    #                 "user_id": "92bdg1f7"
    #             },
    #             {
    #                 "comment": "",
    #                 "create_time": "1749100291285",
    #                 "ext": "{}",
    #                 "node_key": "APPROVAL_764295_5237239",
    #                 "open_id": "ou_275653b7df1ce4f279274540915e7b63",
    #                 "task_id": "7512319315581239299",
    #                 "type": "PASS",
    #                 "user_id": "afg1f21c"
    #             },
    #             {
    #                 "comment": "",
    #                 "create_time": "1749103114130",
    #                 "ext": "{}",
    #                 "node_key": "APPROVAL_495332_261894",
    #                 "open_id": "ou_e8396bd2538203347cc5146425531d69",
    #                 "task_id": "7512328549928353811",
    #                 "type": "PASS",
    #                 "user_id": "d8a4ec55"
    #             },
    #             {
    #                 "comment": "",
    #                 "create_time": "1749103697433",
    #                 "ext": "{}",
    #                 "node_key": "APPROVAL_361877_261573",
    #                 "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
    #                 "task_id": "7512340673390362625",
    #                 "type": "PASS",
    #                 "user_id": "g792ba94"
    #             }
    #         ],
    #         "user_id": "5ba33374",
    #         "uuid": "af77e9c3"
    #     },
    #     "msg": ""
    # }
    approval_data={
  "code": 0,
  "data": {
    "approval_code": "8466E949-4EFD-47CE-A6D7-FCC26EA07A54",
    "approval_name": "固定资产验收单",
    "comment_list": [
      {
        "comment": "发票已到",
        "create_time": "1761202946000",
        "id": "7564308624572530692",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "user_id": "afg1f21c"
      }
    ],
    "department_id": "7978g91d9744b3cg",
    "end_time": "1761274968755",
    "form": "[{\"id\":\"widget17453863872090001\",\"name\":\"说明 1\",\"type\":\"text\",\"ext\":null,\"value\":\"固定资产验收意见从以下四个方面进行:\\n1.资产核实:清点核对实物数量型号规格等是否一致,同时核实供应商提供的配件附件是否完备;\\n2.资产状况检查:保证其外观无损坏，正常运转,强调对设备运行指标、性能要求等检查;\\n3.资产功能测试:根据其用途进行相应测试,确保资产能够正常工作,如果有人员培训情况也一并说明;\\n4.验收记录:在验收过程中及时记录资产的验收情况,包括验收日期、人员、结果等信息。同时对于不合格资产需要详细记录并及时与供应商联系。（若有供应商提供的验收报告也一并上传）\"},{\"id\":\"widget17182776409580001\",\"name\":\"供应商\",\"type\":\"input\",\"ext\":null,\"value\":\"深圳市忠信仪器仪表有限公司\"},{\"id\":\"widget17182796346940001\",\"name\":\"使用部门\",\"type\":\"checkboxV2\",\"ext\":null,\"value\":[\"复合材料事业部\"],\"option\":[{\"key\":\"lxd7bvgm-7lwvky81yqx-0\",\"text\":\"复合材料事业部\"}]},{\"id\":\"widget17182776530460001\",\"name\":\"资产信息\",\"type\":\"fieldList\",\"ext\":[],\"value\":[[{\"id\":\"widget17182776850450001\",\"name\":\"资产名称\",\"type\":\"input\",\"ext\":null,\"value\":\"交流耐压测试仪\"},{\"id\":\"widget17182793745190001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"LK2671B 10KV\"},{\"id\":\"widget17182776934400001\",\"name\":\"数量/单位\",\"type\":\"input\",\"ext\":null,\"value\":\"1台\"},{\"id\":\"widget17183323389860001\",\"name\":\"到货日期\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-09-12T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget17182794373820001\",\"name\":\"购置日期\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-09-09T00:00:00+08:00\",\"timezoneOffset\":-480}]],\"option\":{\"input_type\":\"LIST\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}},{\"id\":\"widget17477962183030001\",\"name\":\"说明 2\",\"type\":\"text\",\"ext\":null,\"value\":\"验收情况（验收人填写）\"},{\"id\":\"widget17477931839460001\",\"name\":\"1.数量是否符合\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"是\",\"option\":{\"key\":\"maxaxnt6-e024hywlko-0\",\"text\":\"是\"}},{\"id\":\"widget17477931876010001\",\"name\":\"2.规格型号是否符合\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"是\",\"option\":{\"key\":\"maxaxqmq-gorhnia0k4f-0\",\"text\":\"是\"}},{\"id\":\"widget17477931907240001\",\"name\":\"3.配件是否齐全\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"是\",\"option\":{\"key\":\"maxaxt1g-3ja8bouty7a-0\",\"text\":\"是\"}},{\"id\":\"widget17477931893490001\",\"name\":\"4.外观包装是否完好\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"是\",\"option\":{\"key\":\"maxaxrz9-fyiz4y7q0jk-0\",\"text\":\"是\"}},{\"id\":\"widget17477968198490001\",\"name\":\"5.功能测试结果\",\"type\":\"input\",\"ext\":null,\"value\":\"仪器功能正常，可正常进行测试\"},{\"id\":\"widget17477962724260001\",\"name\":\"说明 3\",\"type\":\"text\",\"ext\":null,\"value\":\"验收记录（验收人填写）\"},{\"id\":\"widget17477964834430001\",\"name\":\"验收结果\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"通过\",\"option\":{\"key\":\"maxcwdpv-e6mebxe7e1g-0\",\"text\":\"通过\"}},{\"id\":\"widget17477962999420001\",\"name\":\"参与验收人员\",\"type\":\"input\",\"ext\":null,\"value\":\"黄玉双\"},{\"id\":\"widget17477963190600001\",\"name\":\"验收日期\",\"type\":\"input\",\"ext\":null,\"value\":\"2025/09/24\"}]",
    "instance_code": "555FADC5-CE37-4053-8D08-4A0F8E865150",
    "open_id": "ou_5c2544b23439593d0f9195d2aaaecda3",
    "reverted": False,
    "serial_number": "202509220014",
    "start_time": "1758531981723",
    "status": "APPROVED",
    "task_list": [
      {
        "end_time": "1758680120597",
        "id": "7552837351257276418",
        "node_id": "68ffedca539bb73e09a3d44aaa5ff060",
        "node_name": "使用人",
        "open_id": "ou_267e5092b6a6a2b32047e82619691938",
        "start_time": "1758531981831",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "2a18gf22"
      },
      {
        "end_time": "1758680158696",
        "id": "7553473602617147393",
        "node_id": "7dddd64e00a4e238d99720e1fce90c86",
        "node_name": "直属上级",
        "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
        "start_time": "1758680120630",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "92bdg1f7"
      },
      {
        "end_time": "1761202948959",
        "id": "7553473766438961180",
        "node_id": "2e70ccedff335e77440dd5f13bff3f52",
        "node_name": "采购审核",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "start_time": "1758680158766",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "afg1f21c"
      },
      {
        "end_time": "1761274219933",
        "id": "7564309068865110020",
        "node_id": "7c4751efad1f32b298bc7102f0597783",
        "node_name": "财务经理",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "start_time": "1761202949128",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "d8a4ec55"
      },
      {
        "end_time": "1761274968660",
        "id": "7564615175842086915",
        "node_id": "08a1f4532ea2e7c78f83fc4f7a852942",
        "node_name": "总经理",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "start_time": "1761274220200",
        "status": "APPROVED",
        "type": "AND",
        "user_id": "g792ba94"
      }
    ],
    "timeline": [
      {
        "create_time": "1758531981723",
        "ext": "{}",
        "node_key": "",
        "open_id": "ou_5c2544b23439593d0f9195d2aaaecda3",
        "type": "START",
        "user_id": "5ba33374"
      },
      {
        "comment": "仪器完好，配件齐全，功能正常，可进行常规耐电压测试",
        "create_time": "1758680120597",
        "ext": "{}",
        "node_key": "APPROVAL_869758_1955538",
        "open_id": "ou_267e5092b6a6a2b32047e82619691938",
        "task_id": "7552837351257276418",
        "type": "PASS",
        "user_id": "2a18gf22"
      },
      {
        "comment": "",
        "create_time": "1758680158696",
        "ext": "{}",
        "node_key": "APPROVAL_379811_2455273",
        "open_id": "ou_46ce45a1fab3fc5d05d2cc84b0510466",
        "task_id": "7553473602617147393",
        "type": "PASS",
        "user_id": "92bdg1f7"
      },
      {
        "comment": "",
        "create_time": "1761202948959",
        "ext": "{}",
        "node_key": "APPROVAL_764295_5237239",
        "open_id": "ou_275653b7df1ce4f279274540915e7b63",
        "task_id": "7553473766438961180",
        "type": "PASS",
        "user_id": "afg1f21c"
      },
      {
        "comment": "",
        "create_time": "1761274219933",
        "ext": "{}",
        "node_key": "APPROVAL_495332_261894",
        "open_id": "ou_e8396bd2538203347cc5146425531d69",
        "task_id": "7564309068865110020",
        "type": "PASS",
        "user_id": "d8a4ec55"
      },
      {
        "comment": "",
        "create_time": "1761274968660",
        "ext": "{}",
        "node_key": "APPROVAL_361877_261573",
        "open_id": "ou_48ae40c37cdeb24f9c7669726b84c499",
        "task_id": "7564615175842086915",
        "type": "PASS",
        "user_id": "g792ba94"
      },
      {
        "cc_user_list": [
          {
            "cc_id": "7564618391290953756",
            "open_id": "ou_8cb05c168ad03d76f69cfa36286e0375",
            "user_id": "c772c4fb"
          }
        ],
        "create_time": "1761274968759",
        "ext": "{}",
        "node_key": "",
        "open_id": "",
        "open_id_list": [
          "ou_8cb05c168ad03d76f69cfa36286e0375"
        ],
        "type": "CC",
        "user_id_list": [
          "c772c4fb"
        ]
      }
    ],
    "user_id": "5ba33374",
    "uuid": "4bac5f06"
  },
  "msg": ""
}
    
    try:
        # 初始化组件
        # feishu_api = FeishuAPI()
        # employee_manager = EmployeeManager()
        # pdf_generator = PDFGenerator(feishu_api, employee_manager)
        # APP_ID = "cli_a88a2172ee6c101c"
        # APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
        # EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"
        #
        # # 创建PDF生成器
        # feishu_api = FeishuAPI(APP_ID, APP_SECRET)
        # employee_manager = EmployeeManager(api, EMPLOYEE_BASE_URL)
        # pdf_generator = PDFGenerator(api, manager)
        APP_ID = "cli_a88a2172ee6c101c"
        APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"
        EMPLOYEE_BASE_URL = "https://boronmatrix.feishu.cn/base/BRx3bEh91aUfWtsMCshcE4ksnKg?table=tbldKFyEpQcaxo98&view=vewuq32tpn"

        # 创建PDF生成器
        api = FeishuAPI(APP_ID, APP_SECRET)
        manager = EmployeeManager(api, EMPLOYEE_BASE_URL)
        pdf_generator = PDFGenerator(api, manager)

        # 生成PDF
        print("开始生成固定资产验收PDF...")
        pdf_filename = pdf_generator.generate_fixed_asset_acceptance_pdf(approval_data["data"])
        
        if pdf_filename:
            print(f"✅ 固定资产验收PDF生成成功: {pdf_filename}")
        else:
            print("❌ 固定资产验收PDF生成失败")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_asset_acceptance_pdf()
