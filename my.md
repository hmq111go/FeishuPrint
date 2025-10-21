/Users/hmq/PycharmProjects/FeishuPrint/.venv/bin/python /Users/hmq/PycharmProjects/FeishuPrint/feishu_approval_fetch.py 
=== 步骤1: 获取 tenant_access_token ===
Successfully got tenant_access_token (first 20 chars): t-g104ahgTVLSQEBIQR3...

=== 步骤2: 批量获取审批实例ID ===
查询时间范围: 1750003200000 - 1750089599000
GET: https://open.feishu.cn/open-apis/approval/v4/instances
Params: {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "start_time": "1750003200000", "end_time": "1750089599000", "page_size": 100}
Response: {"code": 0, "data": {"has_more": false, "instance_code_list": ["FE589DD7-011A-4A30-AFCB-A3427B568D7E", "479E6D52-0915-429E-AA51-08483432D2C3", "14269F44-B5E7-4914-B950-EEF09A14052E", "6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7", "D6FD3777-8BEA-4736-B5C5-6A5432FE69C1", "A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3", "E1424BC7-5691-41C9-AF6F-FD5E60FB5403", "BD39FE1B-4AAA-4913-A19F-FDCD58652672", "72E5F359-5E92-4001-9CE3-C5FAB8B474CA", "74DF29E3-B419-443A-9CB0-BDCB09B406DA"], "page_token": ""}, "msg": ""}
Retrieved 10 instance ids, total=10, has_more=False
成功获取 10 个审批实例

=== 步骤3: 处理第1个审批实例 (FE589DD7-011A-4A30-AFCB-A3427B568D7E) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/FE589DD7-011A-4A30-AFCB-A3427B568D7E
Response for instance FE589DD7-011A-4A30-AFCB-A3427B568D7E: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750042827718", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"5\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"100\\\"}]\",\"type\":\"amount\",\"value\":\"100.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"500.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"十六异构烷烃\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CAS：68551-20-2\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"L\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":5},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"伍佰元整\"},\"value\":500},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"埃克森美孚化工\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验清洗\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"任丽\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "FE589DD7-011A-4A30-AFCB-A3427B568D7E", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160006", "start_time": "1750042827388", "status": "APPROVED", "task_list": [{"end_time": "1750042827638", "id": "7516376721671634947", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750042827638", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750042827689", "id": "7516376721752145939", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750042827689", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750042827388", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750042827638", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516376721671634947", "type": "AUTO_PASS"}, {"create_time": "1750042827689", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516376721752145939", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "0c15271c"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750042827718",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"5\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"100\\\"}]\",\"type\":\"amount\",\"value\":\"100.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"500.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"十六异构烷烃\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CAS：68551-20-2\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"L\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":5},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"伍佰元整\"},\"value\":500},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"埃克森美孚化工\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验清洗\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"任丽\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "FE589DD7-011A-4A30-AFCB-A3427B568D7E",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160006",
  "start_time": "1750042827388",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750042827638",
      "id": "7516376721671634947",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042827638",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750042827689",
      "id": "7516376721752145939",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042827689",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750042827388",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750042827638",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516376721671634947",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750042827689",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516376721752145939",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "0c15271c"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750042827388
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750042827638
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750042827689
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第2个审批实例 (479E6D52-0915-429E-AA51-08483432D2C3) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/479E6D52-0915-429E-AA51-08483432D2C3
Response for instance 479E6D52-0915-429E-AA51-08483432D2C3: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750042848232", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"1\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"450\\\"}]\",\"type\":\"amount\",\"value\":\"450.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"450.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"Ecoflex  00-30铂金固化硅胶\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"2 lbs (0.9kg)\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"组\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":450},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"肆佰伍拾元整\"},\"value\":450},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=12\\u0026detail_redpacket_pop=true\\u0026id=563842558717\\u0026ltk2=174781563751536jiws2vnxow1oohz44h4h\\u0026ns=1\\u0026priceTId=2147852417478150246383079e119a\\u0026query=Ecoflex%2000-30\\u0026skuId=3789054499576\\u0026spm=a21n57.1.hoverItem.2\\u0026utparam=%7B%22aplus_abtest%22%3A%22219fcb86bdf8006a64e7ba6175a20f00%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁取向实验\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"},{\"id\":\"widget17181796633580001\",\"name\":\"备注\",\"type\":\"input\",\"ext\":null,\"value\":\"联系客服，上海地区可免邮费\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "479E6D52-0915-429E-AA51-08483432D2C3", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160007", "start_time": "1750042847956", "status": "APPROVED", "task_list": [{"end_time": "1750042848160", "id": "7516376809379135490", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750042848160", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750042848202", "id": "7516376809408774146", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750042848202", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750042847956", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750042848160", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516376809379135490", "type": "AUTO_PASS"}, {"create_time": "1750042848202", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516376809408774146", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "de27c396"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750042848232",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"1\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"450\\\"}]\",\"type\":\"amount\",\"value\":\"450.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"450.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"Ecoflex  00-30铂金固化硅胶\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"2 lbs (0.9kg)\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"组\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":450},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"肆佰伍拾元整\"},\"value\":450},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=12\\u0026detail_redpacket_pop=true\\u0026id=563842558717\\u0026ltk2=174781563751536jiws2vnxow1oohz44h4h\\u0026ns=1\\u0026priceTId=2147852417478150246383079e119a\\u0026query=Ecoflex%2000-30\\u0026skuId=3789054499576\\u0026spm=a21n57.1.hoverItem.2\\u0026utparam=%7B%22aplus_abtest%22%3A%22219fcb86bdf8006a64e7ba6175a20f00%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁取向实验\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"},{\"id\":\"widget17181796633580001\",\"name\":\"备注\",\"type\":\"input\",\"ext\":null,\"value\":\"联系客服，上海地区可免邮费\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "479E6D52-0915-429E-AA51-08483432D2C3",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160007",
  "start_time": "1750042847956",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750042848160",
      "id": "7516376809379135490",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042848160",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750042848202",
      "id": "7516376809408774146",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042848202",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750042847956",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750042848160",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516376809379135490",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750042848202",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516376809408774146",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "de27c396"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750042847956
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750042848160
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750042848202
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第3个审批实例 (14269F44-B5E7-4914-B950-EEF09A14052E) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/14269F44-B5E7-4914-B950-EEF09A14052E
Response for instance 14269F44-B5E7-4914-B950-EEF09A14052E: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750042910128", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"21\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"18.2\\\"}]\",\"type\":\"amount\",\"value\":\"18.20\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"98.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"手动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"DIY塑料蛋糕烘焙转台\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"白色转盘\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹拾肆元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":14},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹拾肆元整\"},\"value\":14},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://mobile.yangkeduo.com/goods2.html?refer_share_id=KXH8LwXW2q7NJYefY4iSc0ObcdIGybkE\\u0026refer_share_channel=message\\u0026_oak_share_detail_id=9740181003\\u0026_oc_trace_mark=199\\u0026pxq_secret_key=WL6G6LKWG26ZIZBJGUHXR2TCPGTUULIML53FTPIZLXYRFR7POUDQ\\u0026_oak_share_time=1749195400\\u0026share_oak_rcto=YWI3GD9camziWiNjQc91qlIKVfUI4l0O-vXgc7xQ67vXcwM9N_XNkQOX\\u0026share_uin=6PYO5XSYY3HD6HY3DLZW5SAENA_GEXDA\\u0026_x_query=%E6%89%8B%E5%8A%A8%E8%BD%AC%E7%9B%98%E6%97%8B%E8%BD%AC%E5%8F%B0\\u0026page_from=23\\u0026refer_share_uin=6PYO5XSYY3HD6HY3DLZW5SAENA_GEXDA\\u0026goods_id=696728992769\\u0026_oak_share_snapshot_num=1509\\u0026_x_org=2\\u0026_x_share_id=KXH8LwXW2q7NJYefY4iSc0ObcdIGybkE\\u0026refer_page_name=login\\u0026refer_page_id=10169_1749447292939_q2c9qbc3mf\\u0026refer_page_sn=10169\\u0026uin=ILIR7WJ77R3HVEAHZZMD2GNQGA_GEXDA\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁取向实验\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"实验辅助用品｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"实验室磁力搅拌子\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"B型8*45mm 1个【高磁吸附】\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":20},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆元贰角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":4.2},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"捌拾肆元整\"},\"value\":84},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?from=cart\\u0026id=705230967023\\u0026pisk=g4BiX4TWV1R1zszp999_ZY9hcWVKCd9XuZHvkKL4Te8CBlOvk6xVkwZbfdI2oZbpROE6MECnmg_hoIZ6kE8cki5Tv8eRfG9X3K48e83hDIMVSxlw7o-ef3Zpb1QVMUpX3zUm9xR_EK_amvWm3X-eRnxq7I7qLH-y8ckVuFRE83xW3K72_JJeX3hq_A8NYkxy0f-27KyET3-20A723kjeRnJ2bZJqT0k2rtWCLyGLRneecFXHjCYPx7MqnikJ_UWk8xzAKh4WzG8n3x8O4hxhxGUiFMp1paxRWJkGrG5Pu_7UKAAC_MXDNtgaYKRV9_dGtPkDJOKDaKRn0xSHQeO53Lyr-H1FXsW1SmD2fOBJiUO30xOvLTdPaNmbVMJw0ZO5HzM67iS5F_punvJMgg-ITbkMQxtUD9ljGC-BxUF7dHECWsdg3kqnN5OwAhU8xkcjGC-BxUE3xbg6_HtTy\\u0026skuId=4957500164317\\u0026spm=a1z0d.6639537%2F202410.item.d705230967023.673b7484Ih4Ij1\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁力搅拌\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "14269F44-B5E7-4914-B950-EEF09A14052E", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160008", "start_time": "1750042909867", "status": "APPROVED", "task_list": [{"end_time": "1750042910059", "id": "7516377075375947804", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750042910059", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750042910097", "id": "7516377075403571201", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750042910097", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750042909867", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750042910059", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516377075375947804", "type": "AUTO_PASS"}, {"create_time": "1750042910097", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516377075403571201", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "d7b4b223"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750042910128",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"21\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"18.2\\\"}]\",\"type\":\"amount\",\"value\":\"18.20\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"98.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"手动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"DIY塑料蛋糕烘焙转台\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"白色转盘\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹拾肆元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":14},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹拾肆元整\"},\"value\":14},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://mobile.yangkeduo.com/goods2.html?refer_share_id=KXH8LwXW2q7NJYefY4iSc0ObcdIGybkE\\u0026refer_share_channel=message\\u0026_oak_share_detail_id=9740181003\\u0026_oc_trace_mark=199\\u0026pxq_secret_key=WL6G6LKWG26ZIZBJGUHXR2TCPGTUULIML53FTPIZLXYRFR7POUDQ\\u0026_oak_share_time=1749195400\\u0026share_oak_rcto=YWI3GD9camziWiNjQc91qlIKVfUI4l0O-vXgc7xQ67vXcwM9N_XNkQOX\\u0026share_uin=6PYO5XSYY3HD6HY3DLZW5SAENA_GEXDA\\u0026_x_query=%E6%89%8B%E5%8A%A8%E8%BD%AC%E7%9B%98%E6%97%8B%E8%BD%AC%E5%8F%B0\\u0026page_from=23\\u0026refer_share_uin=6PYO5XSYY3HD6HY3DLZW5SAENA_GEXDA\\u0026goods_id=696728992769\\u0026_oak_share_snapshot_num=1509\\u0026_x_org=2\\u0026_x_share_id=KXH8LwXW2q7NJYefY4iSc0ObcdIGybkE\\u0026refer_page_name=login\\u0026refer_page_id=10169_1749447292939_q2c9qbc3mf\\u0026refer_page_sn=10169\\u0026uin=ILIR7WJ77R3HVEAHZZMD2GNQGA_GEXDA\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁取向实验\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"实验辅助用品｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"实验室磁力搅拌子\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"B型8*45mm 1个【高磁吸附】\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":20},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆元贰角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":4.2},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"捌拾肆元整\"},\"value\":84},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?from=cart\\u0026id=705230967023\\u0026pisk=g4BiX4TWV1R1zszp999_ZY9hcWVKCd9XuZHvkKL4Te8CBlOvk6xVkwZbfdI2oZbpROE6MECnmg_hoIZ6kE8cki5Tv8eRfG9X3K48e83hDIMVSxlw7o-ef3Zpb1QVMUpX3zUm9xR_EK_amvWm3X-eRnxq7I7qLH-y8ckVuFRE83xW3K72_JJeX3hq_A8NYkxy0f-27KyET3-20A723kjeRnJ2bZJqT0k2rtWCLyGLRneecFXHjCYPx7MqnikJ_UWk8xzAKh4WzG8n3x8O4hxhxGUiFMp1paxRWJkGrG5Pu_7UKAAC_MXDNtgaYKRV9_dGtPkDJOKDaKRn0xSHQeO53Lyr-H1FXsW1SmD2fOBJiUO30xOvLTdPaNmbVMJw0ZO5HzM67iS5F_punvJMgg-ITbkMQxtUD9ljGC-BxUF7dHECWsdg3kqnN5OwAhU8xkcjGC-BxUE3xbg6_HtTy\\u0026skuId=4957500164317\\u0026spm=a1z0d.6639537%2F202410.item.d705230967023.673b7484Ih4Ij1\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"磁力搅拌\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"张宜荷\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "14269F44-B5E7-4914-B950-EEF09A14052E",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160008",
  "start_time": "1750042909867",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750042910059",
      "id": "7516377075375947804",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042910059",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750042910097",
      "id": "7516377075403571201",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042910097",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750042909867",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750042910059",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516377075375947804",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750042910097",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516377075403571201",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "d7b4b223"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750042909867
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750042910059
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750042910097
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第4个审批实例 (6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7
Response for instance 6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750042932261", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"7\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"276.26\\\"}]\",\"type\":\"amount\",\"value\":\"276.26\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"518.16\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"860*630*480，黄色带盖子\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰壹拾陆元肆角肆分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":116.44},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰佰叁拾贰元捌角捌分\"},\"value\":232.88},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=13\\u0026detail_redpacket_pop=true\\u0026id=633285558973\\u0026ltk2=1749782071818ths6n44986anz0zndcpwu\\u0026ns=1\\u0026priceTId=2147840317497813838761207e09b3\\u0026query=%E5%91%A8%E8%BD%AC%E7%AE%B1\\u0026skuId=5230953659393\\u0026spm=a21n57.1.hoverItem.3\\u0026utparam=%7B%22aplus_abtest%22%3A%2273a4096248ae4e573a2e1ea837843072%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"药品库装大袋粉末用的，先买几个试试\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"1000*600*400无把手孔，高分子PP灰色\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰壹拾捌元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":118},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰壹拾捌元整\"},\"value\":118},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?id=547261697345\\u0026ns=1\\u0026pisk=gfM-Ea0HdEYkRED8m0Rc-xfjSjKmyImyZ4o1Ky4lOq3x-V6uOyArJW3nuWMuE00YRV0xJW-z-yaK-DGkmdvi40yUdJLMIdqKeP2IJuZQdotQjlXWm7OSQ427dFYMpsjbaU2I-0ySqI1bbrZ7V_ZWDKZTvJZQVJtYlkENOagIRnFbYlCCPTaClsZal_6CFW1bhlERPTaQVnnbuk4QdJgQGnEEM_TLlgahpfVCSm8dWBBNQxE8wyB3k9Ho3OVz5RUfdeeu2NzsVrBCdPnQbOoxqUBZm8kmWl0khT3tVfgI1q9AeSlSDvFZLatbdWGms7hvP9UmEkF_dSICdme7l2H4Cd_Y0jioOYuRv9ZrEAVL7SKCLW2jI5GsyM-Zc8ZI85kH7TzSAckZsRpdh8FC4LkiBOs5Sc4dNnKAT6P70l9g4hdVkzMYDPxJp65UgnrYSnKcT6PASoUM235FTSkO.\\u0026priceTId=2147825f17496266111952830e1285\\u0026spm=tbpc.sem.p4pright.4.5115lyCglyCgz9\\u0026utparam=%7B%22aplus_abtest%22%3A%22c7734f8d98bfdc05fb21380304fd297a%22%7D\\u0026xxc=ad_ztc\\u0026skuId=5787914289284\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"装雨伞用的周转箱\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"600*400*300，灰色箱带平盖\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":4},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆拾壹元捌角贰分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":41.82},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾柒元贰角捌分\"},\"value\":167.28},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=13\\u0026detail_redpacket_pop=true\\u0026id=524599904828\\u0026ltk2=1749781985427ixtl2twozcmmq8zopqwm\\u0026ns=1\\u0026priceTId=2147840317497813838761207e09b3\\u0026query=%E5%91%A8%E8%BD%AC%E7%AE%B1\\u0026skuId=5486898988660\\u0026spm=a21n57.1.hoverItem.11\\u0026utparam=%7B%22aplus_abtest%22%3A%221ae97e8b0dc2fdde1dac927ec8c2bf81%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"药品库装小瓶粉末用的，买几个试试\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160009", "start_time": "1750042932009", "status": "APPROVED", "task_list": [{"end_time": "1750042932197", "id": "7516377170300600321", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750042932197", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750042932232", "id": "7516377170307612673", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750042932232", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750042932009", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750042932197", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516377170300600321", "type": "AUTO_PASS"}, {"create_time": "1750042932232", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516377170307612673", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "1e231a63"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750042932261",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"7\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"276.26\\\"}]\",\"type\":\"amount\",\"value\":\"276.26\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"518.16\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"860*630*480，黄色带盖子\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰壹拾陆元肆角肆分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":116.44},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰佰叁拾贰元捌角捌分\"},\"value\":232.88},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=13\\u0026detail_redpacket_pop=true\\u0026id=633285558973\\u0026ltk2=1749782071818ths6n44986anz0zndcpwu\\u0026ns=1\\u0026priceTId=2147840317497813838761207e09b3\\u0026query=%E5%91%A8%E8%BD%AC%E7%AE%B1\\u0026skuId=5230953659393\\u0026spm=a21n57.1.hoverItem.3\\u0026utparam=%7B%22aplus_abtest%22%3A%2273a4096248ae4e573a2e1ea837843072%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"药品库装大袋粉末用的，先买几个试试\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"1000*600*400无把手孔，高分子PP灰色\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰壹拾捌元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":118},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰壹拾捌元整\"},\"value\":118},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?id=547261697345\\u0026ns=1\\u0026pisk=gfM-Ea0HdEYkRED8m0Rc-xfjSjKmyImyZ4o1Ky4lOq3x-V6uOyArJW3nuWMuE00YRV0xJW-z-yaK-DGkmdvi40yUdJLMIdqKeP2IJuZQdotQjlXWm7OSQ427dFYMpsjbaU2I-0ySqI1bbrZ7V_ZWDKZTvJZQVJtYlkENOagIRnFbYlCCPTaClsZal_6CFW1bhlERPTaQVnnbuk4QdJgQGnEEM_TLlgahpfVCSm8dWBBNQxE8wyB3k9Ho3OVz5RUfdeeu2NzsVrBCdPnQbOoxqUBZm8kmWl0khT3tVfgI1q9AeSlSDvFZLatbdWGms7hvP9UmEkF_dSICdme7l2H4Cd_Y0jioOYuRv9ZrEAVL7SKCLW2jI5GsyM-Zc8ZI85kH7TzSAckZsRpdh8FC4LkiBOs5Sc4dNnKAT6P70l9g4hdVkzMYDPxJp65UgnrYSnKcT6PASoUM235FTSkO.\\u0026priceTId=2147825f17496266111952830e1285\\u0026spm=tbpc.sem.p4pright.4.5115lyCglyCgz9\\u0026utparam=%7B%22aplus_abtest%22%3A%22c7734f8d98bfdc05fb21380304fd297a%22%7D\\u0026xxc=ad_ztc\\u0026skuId=5787914289284\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"装雨伞用的周转箱\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"包装展示材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"周转箱\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"600*400*300，灰色箱带平盖\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"个\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":4},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆拾壹元捌角贰分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":41.82},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾柒元贰角捌分\"},\"value\":167.28},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=13\\u0026detail_redpacket_pop=true\\u0026id=524599904828\\u0026ltk2=1749781985427ixtl2twozcmmq8zopqwm\\u0026ns=1\\u0026priceTId=2147840317497813838761207e09b3\\u0026query=%E5%91%A8%E8%BD%AC%E7%AE%B1\\u0026skuId=5486898988660\\u0026spm=a21n57.1.hoverItem.11\\u0026utparam=%7B%22aplus_abtest%22%3A%221ae97e8b0dc2fdde1dac927ec8c2bf81%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"药品库装小瓶粉末用的，买几个试试\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"李嘉欣\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "6CEB51A8-91CF-4F38-BAAA-2911B8CAF4D7",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160009",
  "start_time": "1750042932009",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750042932197",
      "id": "7516377170300600321",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042932197",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750042932232",
      "id": "7516377170307612673",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750042932232",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750042932009",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750042932197",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516377170300600321",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750042932232",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516377170307612673",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "1e231a63"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750042932009
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750042932197
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750042932232
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第5个审批实例 (D6FD3777-8BEA-4736-B5C5-6A5432FE69C1) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/D6FD3777-8BEA-4736-B5C5-6A5432FE69C1
Response for instance D6FD3777-8BEA-4736-B5C5-6A5432FE69C1: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750043681105", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "D6FD3777-8BEA-4736-B5C5-6A5432FE69C1", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": true, "serial_number": "202506160010", "start_time": "1750043680823", "status": "APPROVED", "task_list": [{"end_time": "1750043681033", "id": "7516380386505719812", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750043681033", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750043681074", "id": "7516380386543845380", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750043681074", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750043680823", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750043681033", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516380386505719812", "type": "AUTO_PASS"}, {"create_time": "1750043681074", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516380386543845380", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "bf153afe"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750043681105",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "D6FD3777-8BEA-4736-B5C5-6A5432FE69C1",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": true,
  "serial_number": "202506160010",
  "start_time": "1750043680823",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750043681033",
      "id": "7516380386505719812",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750043681033",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750043681074",
      "id": "7516380386543845380",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750043681074",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750043680823",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750043681033",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516380386505719812",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750043681074",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516380386543845380",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "bf153afe"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750043680823
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750043681033
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750043681074
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第6个审批实例 (A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3
Response for instance A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750044312904", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "reverted_instance_code": "D6FD3777-8BEA-4736-B5C5-6A5432FE69C1", "serial_number": "202506160010", "start_time": "1750044312623", "status": "APPROVED", "task_list": [{"end_time": "1750044312874", "id": "7516383101515038724", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750044312874", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750044312835", "id": "7516383101772644371", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750044312835", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750044312623", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750044312835", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516383101772644371", "type": "AUTO_PASS"}, {"create_time": "1750044312874", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516383101515038724", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "d7e5564c-02b5-474a-96f2-454cedadf052"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750044312904",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "A1D6F662-9B67-4F92-B94B-6DAEC4FB23E3",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "reverted_instance_code": "D6FD3777-8BEA-4736-B5C5-6A5432FE69C1",
  "serial_number": "202506160010",
  "start_time": "1750044312623",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750044312874",
      "id": "7516383101515038724",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750044312874",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750044312835",
      "id": "7516383101772644371",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750044312835",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750044312623",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750044312835",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516383101772644371",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750044312874",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516383101515038724",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "d7e5564c-02b5-474a-96f2-454cedadf052"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750044312623
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750044312835
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750044312874
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第7个审批实例 (E1424BC7-5691-41C9-AF6F-FD5E60FB5403) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/E1424BC7-5691-41C9-AF6F-FD5E60FB5403
Response for instance E1424BC7-5691-41C9-AF6F-FD5E60FB5403: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750044349015", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "E1424BC7-5691-41C9-AF6F-FD5E60FB5403", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160012", "start_time": "1750044348743", "status": "APPROVED", "task_list": [{"end_time": "1750044348944", "id": "7516383255459151875", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750044348944", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750044348983", "id": "7516383255592222724", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750044348983", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750044348743", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750044348944", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516383255459151875", "type": "AUTO_PASS"}, {"create_time": "1750044348983", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516383255592222724", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "eccb7016"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750044349015",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-17T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"4\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2625000\\\"}]\",\"type\":\"amount\",\"value\":\"2625000.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"2670000.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":1600000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰陆拾万元整\"},\"value\":1600000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"样品生产需求\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-30000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"肆万伍仟元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":45000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖万元整\"},\"value\":90000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机水冷改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"非介入式材料均质机-维修改造设备\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"ZYMB-100000VS\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":980000},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖拾捌万元整\"},\"value\":980000},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"苏州中毅精密科技有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"搅拌机机械臂改造\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"邵刚刚\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "E1424BC7-5691-41C9-AF6F-FD5E60FB5403",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160012",
  "start_time": "1750044348743",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750044348944",
      "id": "7516383255459151875",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750044348944",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750044348983",
      "id": "7516383255592222724",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750044348983",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750044348743",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750044348944",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516383255459151875",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750044348983",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516383255592222724",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "eccb7016"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750044348743
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750044348944
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750044348983
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第8个审批实例 (BD39FE1B-4AAA-4913-A19F-FDCD58652672) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/BD39FE1B-4AAA-4913-A19F-FDCD58652672
Response for instance BD39FE1B-4AAA-4913-A19F-FDCD58652672: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750065318302", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"8\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"40.52\\\"}]\",\"type\":\"amount\",\"value\":\"40.52\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"51.18\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"电动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"丝锥\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"八件套【散装丝锥7件+扳手】限时活动00:00:29\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"套\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹拾元捌角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":10.8},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹拾元捌角整\"},\"value\":10.8},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=17\\u0026detail_redpacket_pop=true\\u0026id=858774743985\\u0026ltk2=1743582686306yu8ubmvokbf9otjlppszkd\\u0026ns=1\\u0026pisk=gdxqUcDmEmn4C15Ao3sazkiQeyIxZGMSOS-1IOv9BRfcmsTPICO-BxIXI1RwN_EXlqQ1_RSvVEZ1GjIwIBsZOXiIAKpA2GcIOcr08XIhnPXg1NqkEG6Z0bg7NKpAX14MyK0yH5P8L2eGI1DPqOWFsGbcI8blwOacsCfcr7XFpGjMssblE9WUmrjGI8DPH9PgiofgZTXG354DsGDyE_BGjOAGjAq5SwrPBZDZq_7zkWl39svcalqMmcI5TcXleOtP3Z5huHEGF3WVu6v2cqGd4TxW4w_7CbSkpUOcUMo49t8kLiXwXv4N_N-A4O8-grOeMOvlzIM_WT8wIHIAYRmDUi5V-3bxbxRHUdYCz3MnviSciFsvCJlXUnRXH3J_IzjVcU7e0MmLi1TWLhWwXfnyTdvpSa-agg5b6Tj7yhL4sP7ceT5IUYreU8ddfPlRDPUOl7BPOxD0WPQceT5IUYzTWZgRU6Mmn\\u0026priceTId=215042f317435825924842915e1aa2\\u0026query=M3%E8%9E%BA%E7%BA%B9%E6%94%BB\\u0026skuId=5839075638677\\u0026spm=a21n57.1.hoverItem.9\\u0026utparam=%7B%22aplus_abtest%22%3A%22e3047b43124f60a9ea2acdc8dcfefac3%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"打螺纹\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"电动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"麻花钻头\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"【高硬含钴】工业塑盒13件套送13支麻花钻\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"套\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰拾叁元玖角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":23.9},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰拾叁元玖角整\"},\"value\":23.9},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=17\\u0026detail_redpacket_pop=true\\u0026id=557061845116\\u0026ltk2=1743583234764uikk5h5tpbi5ah6zqiztno\\u0026ns=1\\u0026pisk=g1eKEwY6lNbnw3eKjk5MEB_UnYIGv1qF-yrXE40HNPUTVVvlYvfrez3Tz2cnd2v-euUzrzEPY0g7Pz3ut1X0YkkrFZDRntqEi_l9ny3BOAsSqDO5jXTLAv-IFZbce094BaD7-xvci1Os0ViIV495XAixDeMSNDZ1X0ikRQ9QPGItV0OBAYiBfci-2YOIApZ610mBFBGIOCst4VgSFYaS1GnrBWpKyHg2eSsCw5uCcZ9kERnK94poWLh4QKcElkg9FaeZvEubAVpWe24rlrZTxwp4jvy0km4hCpUYVoPS68L1k4yTfJN7beQSb7anC2DfOhH3LkNjN-_yNrHLyjwI639bYkg-BcwfqIugB247pfsDHbD_njMQs17nZvnYPJzp2Labjo2E_8Qv54Pn0Ai8UiO-ybsPH-2AhBYmk0ACXGdyaXiwQGNnE_OIK6otoGzwaQltbc3cXGdyaXiZXqjZ_QRr6c5..\\u0026priceTId=2150431c17435832012904050e18bc\\u0026query=%E7%A0%96%E5%A4%B4%E9%92%BB%E5%A4%B4\\u0026skuId=5629448780134\\u0026spm=a21n57.1.hoverItem.2\\u0026utparam=%7B%22aplus_abtest%22%3A%2200988a80c5c3d07228829904ca3f5ac8%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"打孔\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"紧固连接件｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"吊环\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"M12x16德标吊环(碳钢)\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"件\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":4},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰元肆角贰分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2.42},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖元陆角捌分\"},\"value\":9.68},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?detail_redpacket_pop=true\\u0026id=20813287526\\u0026ltk2=1743985486757w7tzl80ybv01adac66lag8\\u0026ns=1\\u0026pisk=gNooe7AwQ4zSW4AYkmZWSovDfo8vnuZQPXIL9kFeuSPf2yPpPX4n9jaE2uH-iWlttJn-vD0fxAMI2LZpFuM7AkR96hhnFYZQhceFP0qVgRk4LJzekoRR3kxv6hKtnZSTiKAt2Sd-l8eOYkzz8iW4GJfFaJlUuiyQggyF4J52nSNV4gzFzny4QRCPUXzE3tyLdJ5F48zVuSwUYWlUYK44GJkT0QPrY0n2GP-M_Hndumeur5kzaYH-0Ia5PYNcYMom6rVaXSjFYm2rHxniiGYL_VN8W5G2Dgqn3Jc0W4AGqXDEC2zmx_J-_vlSmuZMJLaiuq3TrqAPxSn8KPrUo9SEnoVjsDrwbs2juY3EVbXhY8i-XyV_opSQJooT7VllddM44JlQ5Dd1V7kECcgTj3f_EqkgmgRCuNP5XMw2pm7CRzybn5eIwRv01gPXvKvcSWazh8P9nKbCRzybnXpDnND0z-wkz\\u0026priceTId=214784b217439854294305885e1cbf\\u0026query=%E5%90%8A%E8%80%B3%E8%9E%BA%E6%A0%93\\u0026skuId=5274399896544\\u0026spm=a21n57.1.hoverItem.1\\u0026utparam=%7B%22aplus_abtest%22%3A%2225359f3a1441fb3edfc23c139ae2a3f8%22%7D\\u0026xxc=ad_ztc\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"吊装\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"紧固连接件｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"内六角沉头螺钉\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"M1.6*8（200个）\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"组\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁元肆角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":3.4},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"陆元捌角整\"},\"value\":6.8},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=1\\u0026id=643310565481\\u0026ns=1\\u0026pisk=g4gq3GADZEL4wHu2I74N8AIIRkaYRrvBuVw_sfcgG-20hfVg7YD6M-GMHAuaEfnXMl9A_s3rLN_XHnhG7PaMdpTBRjdYWPvQZSzUFtFb_sY_j-2uk5ZvFQ6WRjhYWsWMO0YCQAV4ItjgIA4uq5PQSSVgmuAz1SP0S-qGEgV3ER4iIRquq5FNmSV0jbAzTWbcoo4GrgVQtOVmIPArZ8FiatqgYaPTmCVGv-fXBfq4Kj2P8b3ziqjxg87Pr4ozVJbQUNbizScSN2kP8hwnv-ZQpYY5uPlu_YrI0p7qQfcKjuuNnIMnsx3zky-6MkooVDZq4KbaFqNaxPqPsNczz8HESyYhU7noGc0x317gMqgQbJEysNE_r2Znxx599b40sAEK5pQYnfcKJDaeu9FqqXzP4K6TZoDIWmWGboV8aJOya1A5FYz1bLUAXGEfe7yBiIjOXo4F5iu6SGITcKFzdIuO.\\u0026priceTId=2147865d17363911891378516e6081\\u0026skuId=4633837949914\\u0026spm=a21n57.1.hoverItem.8\\u0026utparam=%7B%22aplus_abtest%22%3A%2221d8d941bf5e028be15f11643c374a73%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"老化壳体固定\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "BD39FE1B-4AAA-4913-A19F-FDCD58652672", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160017", "start_time": "1750065318013", "status": "APPROVED", "task_list": [{"end_time": "1750065318236", "id": "7516473318087458820", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750065318236", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750065318273", "id": "7516473318147850259", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750065318273", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750065318013", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750065318236", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516473318087458820", "type": "AUTO_PASS"}, {"create_time": "1750065318273", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516473318147850259", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "cd657248"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750065318302",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"低值易耗品\",\"option\":{\"key\":\"$i18n-lwhgg4db-spducgc1nhs-1\",\"text\":\"低值易耗品\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"8\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"40.52\\\"}]\",\"type\":\"amount\",\"value\":\"40.52\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"51.18\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"电动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"丝锥\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"八件套【散装丝锥7件+扳手】限时活动00:00:29\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"套\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹拾元捌角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":10.8},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹拾元捌角整\"},\"value\":10.8},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?abbucket=17\\u0026detail_redpacket_pop=true\\u0026id=858774743985\\u0026ltk2=1743582686306yu8ubmvokbf9otjlppszkd\\u0026ns=1\\u0026pisk=gdxqUcDmEmn4C15Ao3sazkiQeyIxZGMSOS-1IOv9BRfcmsTPICO-BxIXI1RwN_EXlqQ1_RSvVEZ1GjIwIBsZOXiIAKpA2GcIOcr08XIhnPXg1NqkEG6Z0bg7NKpAX14MyK0yH5P8L2eGI1DPqOWFsGbcI8blwOacsCfcr7XFpGjMssblE9WUmrjGI8DPH9PgiofgZTXG354DsGDyE_BGjOAGjAq5SwrPBZDZq_7zkWl39svcalqMmcI5TcXleOtP3Z5huHEGF3WVu6v2cqGd4TxW4w_7CbSkpUOcUMo49t8kLiXwXv4N_N-A4O8-grOeMOvlzIM_WT8wIHIAYRmDUi5V-3bxbxRHUdYCz3MnviSciFsvCJlXUnRXH3J_IzjVcU7e0MmLi1TWLhWwXfnyTdvpSa-agg5b6Tj7yhL4sP7ceT5IUYreU8ddfPlRDPUOl7BPOxD0WPQceT5IUYzTWZgRU6Mmn\\u0026priceTId=215042f317435825924842915e1aa2\\u0026query=M3%E8%9E%BA%E7%BA%B9%E6%94%BB\\u0026skuId=5839075638677\\u0026spm=a21n57.1.hoverItem.9\\u0026utparam=%7B%22aplus_abtest%22%3A%22e3047b43124f60a9ea2acdc8dcfefac3%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"打螺纹\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"电动工具｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"麻花钻头\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"【高硬含钴】工业塑盒13件套送13支麻花钻\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"套\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰拾叁元玖角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":23.9},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰拾叁元玖角整\"},\"value\":23.9},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=17\\u0026detail_redpacket_pop=true\\u0026id=557061845116\\u0026ltk2=1743583234764uikk5h5tpbi5ah6zqiztno\\u0026ns=1\\u0026pisk=g1eKEwY6lNbnw3eKjk5MEB_UnYIGv1qF-yrXE40HNPUTVVvlYvfrez3Tz2cnd2v-euUzrzEPY0g7Pz3ut1X0YkkrFZDRntqEi_l9ny3BOAsSqDO5jXTLAv-IFZbce094BaD7-xvci1Os0ViIV495XAixDeMSNDZ1X0ikRQ9QPGItV0OBAYiBfci-2YOIApZ610mBFBGIOCst4VgSFYaS1GnrBWpKyHg2eSsCw5uCcZ9kERnK94poWLh4QKcElkg9FaeZvEubAVpWe24rlrZTxwp4jvy0km4hCpUYVoPS68L1k4yTfJN7beQSb7anC2DfOhH3LkNjN-_yNrHLyjwI639bYkg-BcwfqIugB247pfsDHbD_njMQs17nZvnYPJzp2Labjo2E_8Qv54Pn0Ai8UiO-ybsPH-2AhBYmk0ACXGdyaXiwQGNnE_OIK6otoGzwaQltbc3cXGdyaXiZXqjZ_QRr6c5..\\u0026priceTId=2150431c17435832012904050e18bc\\u0026query=%E7%A0%96%E5%A4%B4%E9%92%BB%E5%A4%B4\\u0026skuId=5629448780134\\u0026spm=a21n57.1.hoverItem.2\\u0026utparam=%7B%22aplus_abtest%22%3A%2200988a80c5c3d07228829904ca3f5ac8%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"打孔\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"紧固连接件｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"吊环\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"M12x16德标吊环(碳钢)\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"件\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":4},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰元肆角贰分\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2.42},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"玖元陆角捌分\"},\"value\":9.68},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://item.taobao.com/item.htm?detail_redpacket_pop=true\\u0026id=20813287526\\u0026ltk2=1743985486757w7tzl80ybv01adac66lag8\\u0026ns=1\\u0026pisk=gNooe7AwQ4zSW4AYkmZWSovDfo8vnuZQPXIL9kFeuSPf2yPpPX4n9jaE2uH-iWlttJn-vD0fxAMI2LZpFuM7AkR96hhnFYZQhceFP0qVgRk4LJzekoRR3kxv6hKtnZSTiKAt2Sd-l8eOYkzz8iW4GJfFaJlUuiyQggyF4J52nSNV4gzFzny4QRCPUXzE3tyLdJ5F48zVuSwUYWlUYK44GJkT0QPrY0n2GP-M_Hndumeur5kzaYH-0Ia5PYNcYMom6rVaXSjFYm2rHxniiGYL_VN8W5G2Dgqn3Jc0W4AGqXDEC2zmx_J-_vlSmuZMJLaiuq3TrqAPxSn8KPrUo9SEnoVjsDrwbs2juY3EVbXhY8i-XyV_opSQJooT7VllddM44JlQ5Dd1V7kECcgTj3f_EqkgmgRCuNP5XMw2pm7CRzybn5eIwRv01gPXvKvcSWazh8P9nKbCRzybnXpDnND0z-wkz\\u0026priceTId=214784b217439854294305885e1cbf\\u0026query=%E5%90%8A%E8%80%B3%E8%9E%BA%E6%A0%93\\u0026skuId=5274399896544\\u0026spm=a21n57.1.hoverItem.1\\u0026utparam=%7B%22aplus_abtest%22%3A%2225359f3a1441fb3edfc23c139ae2a3f8%22%7D\\u0026xxc=ad_ztc\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"吊装\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"紧固连接件｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"内六角沉头螺钉\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"M1.6*8（200个）\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"组\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":2},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁元肆角整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":3.4},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"陆元捌角整\"},\"value\":6.8},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=1\\u0026id=643310565481\\u0026ns=1\\u0026pisk=g4gq3GADZEL4wHu2I74N8AIIRkaYRrvBuVw_sfcgG-20hfVg7YD6M-GMHAuaEfnXMl9A_s3rLN_XHnhG7PaMdpTBRjdYWPvQZSzUFtFb_sY_j-2uk5ZvFQ6WRjhYWsWMO0YCQAV4ItjgIA4uq5PQSSVgmuAz1SP0S-qGEgV3ER4iIRquq5FNmSV0jbAzTWbcoo4GrgVQtOVmIPArZ8FiatqgYaPTmCVGv-fXBfq4Kj2P8b3ziqjxg87Pr4ozVJbQUNbizScSN2kP8hwnv-ZQpYY5uPlu_YrI0p7qQfcKjuuNnIMnsx3zky-6MkooVDZq4KbaFqNaxPqPsNczz8HESyYhU7noGc0x317gMqgQbJEysNE_r2Znxx599b40sAEK5pQYnfcKJDaeu9FqqXzP4K6TZoDIWmWGboV8aJOya1A5FYz1bLUAXGEfe7yBiIjOXo4F5iu6SGITcKFzdIuO.\\u0026priceTId=2147865d17363911891378516e6081\\u0026skuId=4633837949914\\u0026spm=a21n57.1.hoverItem.8\\u0026utparam=%7B%22aplus_abtest%22%3A%2221d8d941bf5e028be15f11643c374a73%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"老化壳体固定\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"王一鸣\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "BD39FE1B-4AAA-4913-A19F-FDCD58652672",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160017",
  "start_time": "1750065318013",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750065318236",
      "id": "7516473318087458820",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065318236",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750065318273",
      "id": "7516473318147850259",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065318273",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750065318013",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750065318236",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516473318087458820",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750065318273",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516473318147850259",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "cd657248"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750065318013
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750065318236
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750065318273
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第9个审批实例 (72E5F359-5E92-4001-9CE3-C5FAB8B474CA) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/72E5F359-5E92-4001-9CE3-C5FAB8B474CA
Response for instance 72E5F359-5E92-4001-9CE3-C5FAB8B474CA: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750065354830", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"2\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"5396\\\"}]\",\"type\":\"amount\",\"value\":\"5396.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"5396.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"钳形电流表\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"376FC（1000V，2500A）含i2500-18 iFlex\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁仟贰佰捌拾陆元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":3286},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁仟贰佰捌拾陆元整\"},\"value\":3286},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?id=586674596361\\u0026ns=1\\u0026pisk=g9qSeoi7uQAWWenpd4XqhnhOYtiIvtSwNpMLIJKyp0n-9rwgObWhr0zjOSFjw3Wlr2hQZ033zXlrODw31t5NbGyuEDmR_1SaGZhU2cYpJvdEHnHrAYI50ZW8EDmdOK-d7Gwu6EsQMUHKHtMELHLL94LxHAhxpUnL9j3xBAR-vWFpHiHnQQLKwb3AhAkJJeK-9nIxCvYKeWndh-hmpDH89Dh2FZMAPjy5eRx9WGfR07GXvHEjH6cTFKxEhoHSbfw80QRPKYgS68hAseK-1qenRkvHAVe8SWDTwQCItowY2PFOgUl85vwaR8IJD0rueP3LX6YL10NIWu3Xp3imcbnjHlBeSjrjaWESkO-s8mEZW0UVo_uEVANLq79Bv5e4Qu00A1OxtzkiDvZhBeGIJgSpbfsAhe9jSHMj_t6X-eAP1Uy2AfWqt4HmndWfhF8nyxDj_t6X-Q0-nxjdhtTMP\\u0026priceTId=undefined\\u0026skuId=5922324882700\\u0026spm=a21n57.1.hoverItem.8\\u0026utparam=%7B%22aplus_abtest%22%3A%226692cfff54d53a6abdd51a03acd53099%22%7D\\u0026xxc=ad_ztc\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"厂区设备电流检测\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"郑海民\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"号码管打印机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"TP76i 电脑蓝牙（含5套管5色带1贴纸+支架+配件）\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰仟壹佰壹拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2110},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰仟壹佰壹拾元整\"},\"value\":2110},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=5\\u0026detail_redpacket_pop=true\\u0026id=567233543922\\u0026ltk2=1743561410555ek7pmi0e4e62babz94flcr\\u0026ns=1\\u0026pisk=gJ5KEb1Bilqnz6CpSwyiZX6vBAagORbUxM7jZ3xnFGIOPhcu8B2ywgKO4HvHOHcJwaIPqgQz8Ut5VgKlKRVc8wRyNoc8iSbUj6wKvMhWVfaWlUcQSpidRBuBNoq0wUGV6uA5xI2YhRM6uhTBP3T7WCTXJYOWFe__WUToAYGCVPU9PEHId3O55FTvJQMBPX96fUTxNXMBFda9zhtWNQsWCPLrCEqJf2towtadbIw8Y2Hmn1Lpp3hkXbLGOjvBcwttNosBJm-fRhhSwH4LtRQO-khVSB5VDEj31XIAu1S95iN8XQSNFgTRfSokTtjFgdQahf_p9hJXfsiIdEdpvK1BQ2GCSL6O6BfQ4x7GWH9vsO2axLAdvt-2dRrN2NKhV6psvlxlnNfBBiZi6gJR3aYRvWhCcgWAispwTmxvrvaTWYkydFla59Au7SVnIFK0J7HrUdzwWn4TWYkydF89myU-UYJa7\\u0026priceTId=undefined\\u0026query=%E5%8F%B7%E7%A0%81%E7%AE%A1%E7%BA%BF%E5%8F%B7%E6%89%93%E5%8D%B0%E6%9C%BA\\u0026skuId=5666111270361\\u0026spm=a21n57.1.hoverItem.3\\u0026utparam=%7B%22aplus_abtest%22%3A%22db9cca1dc67ebf731fa6c6e53b94b59b%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"取向压粉等后期设备电控箱内线号标签\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"郑海民\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "72E5F359-5E92-4001-9CE3-C5FAB8B474CA", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160018", "start_time": "1750065354580", "status": "APPROVED", "task_list": [{"end_time": "1750065354765", "id": "7516473474264743938", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750065354765", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750065354801", "id": "7516473474276786178", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750065354801", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750065354580", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750065354765", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516473474264743938", "type": "AUTO_PASS"}, {"create_time": "1750065354801", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516473474276786178", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "7eaf8805"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750065354830",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"固定资产\",\"option\":{\"key\":\"lwhggrby-aj455ju84cr-5\",\"text\":\"固定资产\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"2\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"5396\\\"}]\",\"type\":\"amount\",\"value\":\"5396.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"5396.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"钳形电流表\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"376FC（1000V，2500A）含i2500-18 iFlex\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁仟贰佰捌拾陆元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":3286},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁仟贰佰捌拾陆元整\"},\"value\":3286},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?id=586674596361\\u0026ns=1\\u0026pisk=g9qSeoi7uQAWWenpd4XqhnhOYtiIvtSwNpMLIJKyp0n-9rwgObWhr0zjOSFjw3Wlr2hQZ033zXlrODw31t5NbGyuEDmR_1SaGZhU2cYpJvdEHnHrAYI50ZW8EDmdOK-d7Gwu6EsQMUHKHtMELHLL94LxHAhxpUnL9j3xBAR-vWFpHiHnQQLKwb3AhAkJJeK-9nIxCvYKeWndh-hmpDH89Dh2FZMAPjy5eRx9WGfR07GXvHEjH6cTFKxEhoHSbfw80QRPKYgS68hAseK-1qenRkvHAVe8SWDTwQCItowY2PFOgUl85vwaR8IJD0rueP3LX6YL10NIWu3Xp3imcbnjHlBeSjrjaWESkO-s8mEZW0UVo_uEVANLq79Bv5e4Qu00A1OxtzkiDvZhBeGIJgSpbfsAhe9jSHMj_t6X-eAP1Uy2AfWqt4HmndWfhF8nyxDj_t6X-Q0-nxjdhtTMP\\u0026priceTId=undefined\\u0026skuId=5922324882700\\u0026spm=a21n57.1.hoverItem.8\\u0026utparam=%7B%22aplus_abtest%22%3A%226692cfff54d53a6abdd51a03acd53099%22%7D\\u0026xxc=ad_ztc\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"厂区设备电流检测\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"郑海民\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"号码管打印机\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"TP76i 电脑蓝牙（含5套管5色带1贴纸+支架+配件）\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"台\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":1},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰仟壹佰壹拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":2110},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"贰仟壹佰壹拾元整\"},\"value\":2110},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"https://detail.tmall.com/item.htm?abbucket=5\\u0026detail_redpacket_pop=true\\u0026id=567233543922\\u0026ltk2=1743561410555ek7pmi0e4e62babz94flcr\\u0026ns=1\\u0026pisk=gJ5KEb1Bilqnz6CpSwyiZX6vBAagORbUxM7jZ3xnFGIOPhcu8B2ywgKO4HvHOHcJwaIPqgQz8Ut5VgKlKRVc8wRyNoc8iSbUj6wKvMhWVfaWlUcQSpidRBuBNoq0wUGV6uA5xI2YhRM6uhTBP3T7WCTXJYOWFe__WUToAYGCVPU9PEHId3O55FTvJQMBPX96fUTxNXMBFda9zhtWNQsWCPLrCEqJf2towtadbIw8Y2Hmn1Lpp3hkXbLGOjvBcwttNosBJm-fRhhSwH4LtRQO-khVSB5VDEj31XIAu1S95iN8XQSNFgTRfSokTtjFgdQahf_p9hJXfsiIdEdpvK1BQ2GCSL6O6BfQ4x7GWH9vsO2axLAdvt-2dRrN2NKhV6psvlxlnNfBBiZi6gJR3aYRvWhCcgWAispwTmxvrvaTWYkydFla59Au7SVnIFK0J7HrUdzwWn4TWYkydF89myU-UYJa7\\u0026priceTId=undefined\\u0026query=%E5%8F%B7%E7%A0%81%E7%AE%A1%E7%BA%BF%E5%8F%B7%E6%89%93%E5%8D%B0%E6%9C%BA\\u0026skuId=5666111270361\\u0026spm=a21n57.1.hoverItem.3\\u0026utparam=%7B%22aplus_abtest%22%3A%22db9cca1dc67ebf731fa6c6e53b94b59b%22%7D\\u0026xxc=taobaoSearch\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"取向压粉等后期设备电控箱内线号标签\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"郑海民\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "72E5F359-5E92-4001-9CE3-C5FAB8B474CA",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160018",
  "start_time": "1750065354580",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750065354765",
      "id": "7516473474264743938",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065354765",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750065354801",
      "id": "7516473474276786178",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065354801",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750065354580",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750065354765",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516473474264743938",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750065354801",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516473474276786178",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "7eaf8805"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750065354580
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750065354765
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750065354801
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

=== 步骤3: 处理第10个审批实例 (74DF29E3-B419-443A-9CB0-BDCB09B406DA) ===
GET: https://open.feishu.cn/open-apis/approval/v4/instances/74DF29E3-B419-443A-9CB0-BDCB09B406DA
Response for instance 74DF29E3-B419-443A-9CB0-BDCB09B406DA: {"code": 0, "data": {"approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C", "approval_name": "采购申请", "department_id": "7978g91d9744b3cg", "end_time": "1750065388209", "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"39\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2320\\\"}]\",\"type\":\"amount\",\"value\":\"2320.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"6960.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 1B\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 1B\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"陆拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":60},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰捌拾元整\"},\"value\":180},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 12\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 12\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"陆拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":60},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰捌拾元整\"},\"value\":180},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 18 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 18 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 19\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 19\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 23 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 23 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 30 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 30 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 100\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 100\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 500\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 500\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 6\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 6\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰贰拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":220},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"陆佰陆拾元整\"},\"value\":660},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 188-160\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 188-160\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰捌拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":280},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"捌佰肆拾元整\"},\"value\":840},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 1040\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 1040\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":350},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹仟零伍拾元整\"},\"value\":1050},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"RH-H502\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":50},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰伍拾元整\"},\"value\":150},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"浙江润禾有机硅新材料有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油｜MV 500\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"MV 500\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]", "instance_code": "74DF29E3-B419-443A-9CB0-BDCB09B406DA", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "reverted": false, "serial_number": "202506160019", "start_time": "1750065387937", "status": "APPROVED", "task_list": [{"end_time": "1750065388137", "id": "7516473618223038466", "node_id": "19269e901ef75391121e2658485d5897", "node_name": "自动通过", "open_id": "", "start_time": "1750065388137", "status": "APPROVED", "type": "AUTO_PASS"}, {"end_time": "1750065388172", "id": "7516473618304188417", "node_id": "90337e18ff7947bbc9cc1ff04795077d", "node_name": "自动通过", "open_id": "", "start_time": "1750065388172", "status": "APPROVED", "type": "AUTO_PASS"}], "timeline": [{"create_time": "1750065387937", "ext": "{}", "node_key": "", "open_id": "ou_275653b7df1ce4f279274540915e7b63", "type": "START", "user_id": "afg1f21c"}, {"create_time": "1750065388137", "ext": "{}", "node_key": "APPROVAL_356820_2517926", "open_id": "", "task_id": "7516473618223038466", "type": "AUTO_PASS"}, {"create_time": "1750065388172", "ext": "{}", "node_key": "APPROVAL_463016_525501", "open_id": "", "task_id": "7516473618304188417", "type": "AUTO_PASS"}], "user_id": "afg1f21c", "uuid": "5475be37"}, "msg": ""}

=== 审批实例所有字段数据 ===
{
  "approval_code": "A851D76E-6B63-4DD4-91F2-998693422C3C",
  "approval_name": "采购申请",
  "department_id": "7978g91d9744b3cg",
  "end_time": "1750065388209",
  "form": "[{\"id\":\"widget16510608918180001\",\"name\":\"期望交货时间\",\"type\":\"date\",\"ext\":null,\"value\":\"2025-06-30T00:00:00+08:00\",\"timezoneOffset\":-480},{\"id\":\"widget16510608666360001\",\"name\":\"采购类别\",\"type\":\"radioV2\",\"ext\":null,\"value\":\"原材料\",\"option\":{\"key\":\"lwhggrby-u7rsuzkxqlc-1\",\"text\":\"原材料\"}},{\"id\":\"widget16510609006710001\",\"name\":\"费用明细\",\"type\":\"fieldList\",\"ext\":[{\"id\":\"widget16510609215120001\",\"type\":\"number\",\"value\":\"39\"},{\"capitalValue\":\"\",\"id\":\"widget17361541018990001\",\"sumItems\":\"[{\\\"currency\\\":\\\"CNY\\\",\\\"value\\\":\\\"2320\\\"}]\",\"type\":\"amount\",\"value\":\"2320.00\"},{\"capitalValue\":\"\",\"id\":\"widget17167713798900001\",\"type\":\"formula\",\"value\":\"6960.00\"}],\"value\":[[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 1B\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 1B\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"陆拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":60},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰捌拾元整\"},\"value\":180},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 12\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 12\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"陆拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":60},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰捌拾元整\"},\"value\":180},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 18 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 18 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 19\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 19\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜XL 23 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"XL 23 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 30 LV\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 30 LV\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":250},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"柒佰伍拾元整\"},\"value\":750},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 100\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 100\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油｜CE 500\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"含氢硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"CE 500\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 6\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 6\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰贰拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":220},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"陆佰陆拾元整\"},\"value\":660},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 188-160\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 188-160\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"贰佰捌拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":280},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"捌佰肆拾元整\"},\"value\":840},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基MQ树脂｜VQM 1040\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"VQM 1040\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"叁佰伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":350},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹仟零伍拾元整\"},\"value\":1050},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"新增原材料｜\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"RH-H502\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"伍拾元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":50},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"壹佰伍拾元整\"},\"value\":150},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"浙江润禾有机硅新材料有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}],[{\"id\":\"widget17497939529430001\",\"name\":\"商品及其辅助属性\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油｜MV 500\"},{\"id\":\"widget16510609105290001\",\"name\":\"名称\",\"type\":\"input\",\"ext\":null,\"value\":\"乙烯基硅油\"},{\"id\":\"widget16510609161480001\",\"name\":\"规格型号\",\"type\":\"input\",\"ext\":null,\"value\":\"MV 500\"},{\"id\":\"widget17171356180990001\",\"name\":\"单位\",\"type\":\"input\",\"ext\":null,\"value\":\"kg\"},{\"id\":\"widget16510609215120001\",\"name\":\"数量\",\"type\":\"number\",\"ext\":null,\"value\":3},{\"id\":\"widget17361541018990001\",\"name\":\"单价\",\"type\":\"amount\",\"ext\":{\"capitalValue\":\"壹佰元整\",\"currency\":\"CNY\",\"currencyRange\":[\"CNY\",\"USD\",\"EUR\"],\"maxValue\":\"\",\"minValue\":\"\"},\"value\":100},{\"id\":\"widget17167713798900001\",\"name\":\"金额\",\"type\":\"formula\",\"ext\":{\"capitalValue\":\"叁佰元整\"},\"value\":300},{\"id\":\"widget17182722815070001\",\"name\":\"购买链接/供应商\",\"type\":\"textarea\",\"ext\":null,\"value\":\"安必亚特种有机硅有限公司\"},{\"id\":\"widget17163614121230001\",\"name\":\"请购理由\",\"type\":\"textarea\",\"ext\":null,\"value\":\"实验用\"},{\"id\":\"widget17497940675090001\",\"name\":\"领用人\",\"type\":\"input\",\"ext\":null,\"value\":\"姚一伟\"}]],\"option\":{\"input_type\":\"FORM\",\"mobile_detail_type\":\"CARD\",\"print_type\":\"FORM\"}}]",
  "instance_code": "74DF29E3-B419-443A-9CB0-BDCB09B406DA",
  "open_id": "ou_275653b7df1ce4f279274540915e7b63",
  "reverted": false,
  "serial_number": "202506160019",
  "start_time": "1750065387937",
  "status": "APPROVED",
  "task_list": [
    {
      "end_time": "1750065388137",
      "id": "7516473618223038466",
      "node_id": "19269e901ef75391121e2658485d5897",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065388137",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    },
    {
      "end_time": "1750065388172",
      "id": "7516473618304188417",
      "node_id": "90337e18ff7947bbc9cc1ff04795077d",
      "node_name": "自动通过",
      "open_id": "",
      "start_time": "1750065388172",
      "status": "APPROVED",
      "type": "AUTO_PASS"
    }
  ],
  "timeline": [
    {
      "create_time": "1750065387937",
      "ext": "{}",
      "node_key": "",
      "open_id": "ou_275653b7df1ce4f279274540915e7b63",
      "type": "START",
      "user_id": "afg1f21c"
    },
    {
      "create_time": "1750065388137",
      "ext": "{}",
      "node_key": "APPROVAL_356820_2517926",
      "open_id": "",
      "task_id": "7516473618223038466",
      "type": "AUTO_PASS"
    },
    {
      "create_time": "1750065388172",
      "ext": "{}",
      "node_key": "APPROVAL_463016_525501",
      "open_id": "",
      "task_id": "7516473618304188417",
      "type": "AUTO_PASS"
    }
  ],
  "user_id": "afg1f21c",
  "uuid": "5475be37"
}

=== 审批进程处理人信息 ===

--- 第1个审批节点 ---
节点类型: START
节点名称: 
发生时间: 1750065387937
GET: https://open.feishu.cn/open-apis/contact/v3/users/ou_275653b7df1ce4f279274540915e7b63?user_id_type=open_id
User info response for ou_275653b7df1ce4f279274540915e7b63: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
GET: https://open.feishu.cn/open-apis/contact/v3/users/afg1f21c?user_id_type=user_id
User info response for afg1f21c: {"code": 0, "data": {"user": {"mobile_visible": true, "open_id": "ou_275653b7df1ce4f279274540915e7b63", "union_id": "on_1182c94859b78143b8b12b636b2de2ef", "user_id": "afg1f21c"}}, "msg": "success"}
处理人姓名: 未知用户
处理人ID(user_id): afg1f21c
处理人ID(open_id): ou_275653b7df1ce4f279274540915e7b63
意见: N/A

--- 第2个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_356820_2517926
发生时间: 1750065388137
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

--- 第3个审批节点 ---
节点类型: AUTO_PASS
节点名称: APPROVAL_463016_525501
发生时间: 1750065388172
处理人姓名: 未知用户
处理人ID(user_id): None
处理人ID(open_id): 
意见: N/A

进程已结束，退出代码为 0
