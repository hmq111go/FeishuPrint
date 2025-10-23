#!/usr/bin/env python3
"""
实时PDF生成器
当审批通过时自动生成包含签名图片的PDF报告
"""
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple, Union

import lark_oapi as lark
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 配置参数
APP_ID = "cli_a88a2172ee6c101c"
APP_SECRET = "cpsZfhOpTSKka72mQeCfWbCJHJfrNdvy"

# 四种审批定义类型
APPROVAL_DEFINITIONS = {
    "三方比价": "44A66AA6-201B-452C-AA90-531AC68C9023",
    "固定资产": "8466E949-4EFD-47CE-A6D7-FCC26EA07A54", 
    "费用报销": "BCD664E5-456F-4FEE-BA6E-EE349972F6A1",
    "采购申请": "A851D76E-6B63-4DD4-91F2-998693422C3C"
}

LOCAL_TZ = timezone.utc  # 可以根据需要调整时区

def get_tenant_access_token(app_id: str, app_secret: str) -> Tuple[str, Exception]:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        print(f"Request body: {json.dumps(payload)}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if result.get("code", 0) != 0:
            print(f"Error: failed to get tenant_access_token: {result.get('msg', 'unknown error')}", file=sys.stderr)
            return "", Exception(f"failed to get tenant_access_token: {response.text}")

        access_token = result["tenant_access_token"]
        print(f"获取 tenant_access_token 成功: {access_token[:10]}...")
        return access_token, None

    except Exception as e:
        print(f"Error: getting tenant_access_token: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}", file=sys.stderr)
        return "", e

def subscribe_approval_event(tenant_access_token: str, approval_code: str) -> bool:
    """订阅审批事件"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/approvals/{approval_code}/subscribe"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        print(f"POST: {url}")
        response = requests.post(url, headers=headers)
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if result.get("code") == 0:
            print("订阅审批事件成功")
            return True
        elif result.get("code") == 1390007:  # subscription existed
            print("审批事件已订阅，无需重复操作")
            return True
        else:
            print(f"ERROR: subscribing approval event: {result.get('msg', 'unknown error')}", file=sys.stderr)
            print(f"ERROR: Response body: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"ERROR: subscribing approval event: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"ERROR: Response body: {e.response.text}", file=sys.stderr)
        return False

def fetch_approval_instance_detail(tenant_access_token: str, instance_id: str) -> Dict[str, Any]:
    """获取审批实例详情"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/instances/{instance_id}"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    print(f"GET: {url}")
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    result = response.json()
    print(f"Response for instance {instance_id}: {json.dumps(result, ensure_ascii=False)}")
    if result.get("code", 0) != 0:
        raise RuntimeError(
            f"Feishu error fetching instance detail: code={result.get('code')} msg={result.get('msg')}"
        )
    return result.get("data", {})

def resolve_user_name_from_user_id(user_id: str) -> str:
    """根据用户ID解析用户姓名"""
    if not user_id:
        return "未知用户"
    
    try:
        # 加载员工映射文件
        mapping_file_path = os.path.join(os.path.dirname(__file__), "employee_mapping.json")
        with open(mapping_file_path, 'r', encoding='utf-8') as f:
            employee_mapping = json.load(f)
        
        # 反向查找：通过open_id找到姓名
        for name, open_id in employee_mapping.items():
            if open_id == user_id:
                return name
        
        return "未知用户"
    except Exception:
        return "未知用户"

def get_approval_type_name(approval_code: str) -> str:
    """根据审批定义代码获取审批类型名称"""
    for type_name, code in APPROVAL_DEFINITIONS.items():
        if code == approval_code:
            return type_name
    return "未知类型"

def get_signature_image_path(employee_name: str) -> str:
    """获取员工签名图片路径"""
    if not employee_name or employee_name == "未知用户":
        return None
    
    # 构建图片文件路径
    image_filename = f"{employee_name}.png"
    image_path = os.path.join(os.path.dirname(__file__), image_filename)
    
    # 检查文件是否存在
    if os.path.exists(image_path):
        return image_path
    else:
        print(f"警告: 未找到员工 {employee_name} 的签名图片: {image_path}")
        return None

def format_time_without_timezone(value: Union[str, int, float, None], tz: timezone) -> str:
    """格式化时间，不显示时区信息"""
    try:
        if value is None:
            return ""
        if isinstance(value, str):
            if not value.isdigit():
                return ""
            ms = int(value)
        else:
            ms = int(value)
        if ms < 10**12:
            return ""
        dt = datetime.fromtimestamp(ms / 1000.0, tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""

def get_department_name(tenant_token: str, department_id: str) -> str:
    """根据部门ID获取部门名称"""
    if not department_id:
        return "未知部门"
    url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}"
    headers = {"Authorization": f"Bearer {tenant_token}"}
    params = {"department_id_type": "department_id"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 0:
            department = data.get("data", {}).get("department", {})
            return department.get("name", "未知部门")
        else:
            print(f"获取部门信息失败 ({department_id}): {data.get('msg', '未知错误')}")
    except Exception as e:
        print(f"获取部门信息失败 ({department_id}): {e}")

    return "未知部门"

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

def format_timeline_table(timeline: List[Dict[str, Any]], task_list: List[Dict[str, Any]]) -> List[List[str]]:
    """格式化审批时间线为表格格式"""
    table_data = []

    for i, item in enumerate(timeline, 1):
        node_type = item.get('type', '')
        create_time = item.get('create_time', '')
        open_id = item.get('open_id', '')
        user_id = item.get('user_id', '')
        comment = item.get('comment', '')
        cc_user_list = item.get('cc_user_list', [])
        task_id = item.get('task_id', '')

        # 获取处理人姓名
        processor_name = "未知用户"
        if open_id:
            processor_name = resolve_user_name_from_user_id(open_id)
        elif user_id:
            processor_name = resolve_user_name_from_user_id(user_id)

        # 格式化时间
        formatted_time = format_time_without_timezone(create_time, LOCAL_TZ)

        # 根据节点类型和任务列表确定节点名称和处理结果
        if node_type == "START":
            node_name = "发起"
            result = "发起审批"
        elif node_type == "PASS":
            node_name = "审批"
            for task in task_list:
                if task.get('id') == task_id:
                    node_name = task.get('node_name', '审批')
                    break
            result = "已通过"
        elif node_type == "REJECT":
            node_name = "审批"
            for task in task_list:
                if task.get('id') == task_id:
                    node_name = task.get('node_name', '审批')
                    break
            result = "已拒绝"
        elif node_type == "AUTO_PASS":
            node_name = "自动审批"
            for task in task_list:
                if task.get('id') == task_id:
                    node_name = task.get('node_name', '自动审批')
                    break
            result = "已通过"
        elif node_type == "AUTO_REJECT":
            node_name = "自动审批"
            for task in task_list:
                if task.get('id') == task_id:
                    node_name = task.get('node_name', '自动审批')
                    break
            result = "已拒绝"
        elif node_type == "CC":
            node_name = "抄送"
            cc_count = len(cc_user_list)
            cc_names = []
            for cc_user in cc_user_list:
                cc_open_id = cc_user.get('open_id', '')
                cc_name = resolve_user_name_from_user_id(cc_open_id)
                cc_names.append(cc_name)

            # 从ext字段获取发起抄送的用户信息
            ext_str = item.get('ext', '{}')
            try:
                ext_data = json.loads(ext_str)
                cc_initiator_open_id = ext_data.get('open_id', '')
                if cc_initiator_open_id:
                    processor_name = resolve_user_name_from_user_id(cc_initiator_open_id)
            except:
                pass

            result = f"抄送 {cc_count} 人 {', '.join(cc_names)}"
        else:
            node_name = node_type
            result = "处理"

        table_data.append([
            str(i),
            node_name,
            processor_name,
            result,
            formatted_time
        ])

    return table_data

def register_chinese_fonts():
    """注册中文字体"""
    try:
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
            "/System/Library/Fonts/STHeiti Medium.ttc",  # macOS
            "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS
            "/Library/Fonts/Arial Unicode.ttf",  # macOS
            "/usr/share/fonts/truetype/arphic/uming.ttc",  # Linux
            "/usr/share/fonts/truetype/arphic/ukai.ttc",  # Linux
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
            "C:/Windows/Fonts/simsun.ttc",  # Windows
            "C:/Windows/Fonts/simhei.ttf",  # Windows
            "C:/Windows/Fonts/msyh.ttc",  # Windows
            "C:/Windows/Fonts/simfang.ttf",  # Windows
        ]
        
        # 添加当前目录下的字体文件
        current_dir = os.path.dirname(__file__)
        for font_file in os.listdir(current_dir):
            if font_file.endswith('.ttf') or font_file.endswith('.ttc'):
                font_paths.append(os.path.join(current_dir, font_file))
        
        registered_fonts = pdfmetrics.getRegisteredFontNames()
        if "ChineseFont" in registered_fonts:
            print("中文字体已注册")
            return True
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    if font_path.endswith('.ttc'):
                        pdfmetrics.registerFont(TTFont("ChineseFont", font_path, subfontIndex=0))
                    else:
                        pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                    print(f"成功注册中文字体: {font_path}")
                    return True
                except Exception as e:
                    print(f"注册字体失败 {font_path}: {e}")
                    continue
        
        print("警告: 未能注册中文字体，中文可能显示为方块")
        return False
    except Exception as e:
        print(f"字体注册过程出错: {e}")
        return False

def create_wrapped_text(text: str, font_name: str = "ChineseFont", font_size: int = 9) -> Paragraph:
    """创建支持自动换行的文本段落"""
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    
    registered_fonts = pdfmetrics.getRegisteredFontNames()
    if "ChineseFont" in registered_fonts and font_name == "ChineseFont":
        style.fontName = "ChineseFont"
    else:
        style.fontName = "Helvetica"
    
    style.fontSize = font_size
    style.alignment = 1  # 居中对齐
    style.textColor = colors.black
    style.wordWrap = 'CJK'
    style.firstLineIndent = 0
    
    if text is None:
        text = ""
    
    if not isinstance(text, str):
        text = str(text)
    
    wrapped_text = text.replace("\n", "<br/>")
    wrapped_text = wrapped_text.replace("&", "&amp;")
    wrapped_text = wrapped_text.replace("<", "&lt;")
    wrapped_text = wrapped_text.replace(">", "&gt;")
    return Paragraph(wrapped_text, style)

def process_table_data_for_pdf(table_data: List[List[Any]]) -> List[List[Any]]:
    """处理表格数据，将文本转换为支持换行的Paragraph"""
    processed = []
    for i, row in enumerate(table_data):
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                new_row.append(create_wrapped_text(cell))
            elif isinstance(cell, Image):
                new_row.append(cell)  # 原样保留图片
            else:
                new_row.append(cell)  # 已经是 Paragraph 或其它
        processed.append(new_row)
    return processed

def build_header_block():
    """公司信息表头"""
    # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
    sty_big = ParagraphStyle('HB1', fontName='ChineseFont', fontSize=14, alignment=1, textColor=colors.black,
                             spaceBefore=0, spaceAfter=0)
    sty_sml = ParagraphStyle('HB2', fontName='ChineseFont', fontSize=8, alignment=1, textColor=colors.black,
                             spaceBefore=0, spaceAfter=0)

    # 准备 Logo 图（放在第一行最左侧单元格）
    logo_cell = ""
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            # 控制在表格中的显示尺寸（高度约 14pt，与之前一致）
            logo_cell = Image(logo_path, width=100, height=14)
            logo_cell.hAlign = 'LEFT'
        else:
            logo_cell = ""
    except Exception:
        logo_cell = ""

    # 创建公司信息表格，第一行两列：[Logo, 公司中文名]；后续两行将中文左侧单元格留空
    company_data = [
        [logo_cell, Paragraph("上海硼矩新材料科技有限公司", sty_big)],
        ["", Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml)],
        ["", Paragraph("采购申请单", sty_big)]
    ]
    company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.8 * cm])
    company_tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (1, 1), (1, 2), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return company_tbl

def build_approval_info_block(serial: str, start_time: str):
    """审批编号和申请时间信息块 - 无框线"""
    sty = ParagraphStyle('AI', fontName='ChineseFont', fontSize=9, textColor=colors.black)
    data = [[Paragraph(f"审批编号：{serial}", sty),
             Paragraph(f"申请时间：{start_time}", sty)]]
    tbl = Table(data, colWidths=[9.5 * cm, 9.5 * cm], rowHeights=[0.5 * cm])  # 进一步减少行高
    tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # 减少内边距
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        # 移除BOX边框
    ]))
    return tbl

def build_applicant_info_block(applicant_name: str, department_name: str, category: str, delivery_time: str):
    """申请人、采购类别、期望交货时间信息表格"""
    sty_label = ParagraphStyle('Lab', fontName='ChineseFont', fontSize=8, textColor=colors.black)
    sty_val = ParagraphStyle('Val', fontName='ChineseFont', fontSize=8, textColor=colors.black)

    data = [[Paragraph("申请人", sty_label), Paragraph(f"{applicant_name}-{department_name}", sty_val),
             Paragraph("采购类别", sty_label), Paragraph(category, sty_val),
             Paragraph("期望交货时间", sty_label), Paragraph(delivery_time, sty_val)]]

    tbl = Table(data, colWidths=[2.17 * cm, 4.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm],
                rowHeights=[0.6 * cm])  # 减少行高
    tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
        ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 调整字体大小
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('BACKGROUND', (4, 0), (4, -1), colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # 减少内边距
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return tbl

def generate_procurement_approval_pdf(approval_detail: Dict[str, Any], tenant_token: str) -> str:
    """为单个审批实例生成PDF报告 - 采用generate_pdf_report的模板风格"""
    try:
        # 注册中文字体
        register_chinese_fonts()
        
        # 生成PDF文件名
        instance_code = approval_detail.get('instance_code', 'unknown')
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"采购申请审批报告_{instance_code}_{current_time}.pdf"
        
        # 创建PDF文档 - 采用generate_pdf_report的页面设置
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            topMargin=0.2 * cm,  # 几乎顶格
            rightMargin=1 * cm,
            bottomMargin=1 * cm,
            leftMargin=1 * cm
        )
        story = []
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 1. 公司信息表头
        story.append(build_header_block())
        story.append(Spacer(1, 5))  # 减少间距
        
        # 2. 审批信息（审批编号和申请时间）
        applicant_name = resolve_user_name_from_user_id(approval_detail.get('open_id', ''))
        department_name = get_department_name(tenant_token, approval_detail.get('department_id', ''))
        start_time_formatted = format_time_without_timezone(approval_detail.get('start_time', ''), LOCAL_TZ)
        
        story.append(build_approval_info_block(
            approval_detail.get('serial_number', 'N/A'),
            start_time_formatted
        ))
        story.append(Spacer(1, 8))  # 减少间距
        
        # 3. 申请人信息表格
        form_data = parse_form_data(approval_detail.get('form', '[]'))
        category = form_data.get('采购类别', '未知')
        delivery_time = form_data.get('期望交货时间', '').split('T')[0] if 'T' in form_data.get('期望交货时间', '') else '未知'
        
        story.append(build_applicant_info_block(
            applicant_name,
            department_name,
            category,
            delivery_time
        ))
        story.append(Spacer(1, 8))  # 减少间距
        
        # 4. 费用明细表格
        expense_details = []
        if '费用明细' in form_data and form_data['费用明细']:
            # 从原始表单中获取汇总信息与币种
            summary_info = form_data.get('费用明细_summary', {})
            currency_code = summary_info.get('currency') or ''
            
            # 费用表格（若有币种，在列名中展示）
            unit_price_header = '单价' + (f"({currency_code})" if currency_code else '')
            amount_header = '总价' + (f"({currency_code})" if currency_code else '')
            detail_headers = ['序号', '商品名称', '商品明细', '规格型号', '单位', '数量', unit_price_header, amount_header, '请购理由',
                              '需求人', '备注']
            detail_data = [detail_headers]
            
            # 行数据直接使用接口返回的"单价"、"金额"，不再自行计算
            calc_total_fallback = 0.0
            for idx, item in enumerate(form_data['费用明细'], 1):
                q_val = item.get('数量', '')
                p_val = item.get('单价', '')
                t_val = item.get('金额', '')
                
                # 尝试用于兜底统计
                try:
                    calc_total_fallback += float(t_val)
                except Exception:
                    pass
                
                detail_data.append([
                    str(idx), item.get('商品及其辅助属性', ''), item.get('名称', ''), item.get('规格型号', ''),
                    item.get('单位', ''), str(q_val), str(p_val), str(t_val),
                    item.get('请购理由', ''), item.get('需求人', ''), item.get('备注', '')
                ])
                expense_details.append(item)
            
            # 总金额优先使用表单汇总，其次用行金额求和兜底
            total_amount_display = None
            total_from_summary = summary_info.get('total_amount')
            if isinstance(total_from_summary, (int, float)):
                total_amount_display = f"{total_from_summary:.2f}"
            elif isinstance(total_from_summary, str) and total_from_summary.strip():
                total_amount_display = total_from_summary
            else:
                total_amount_display = f"{calc_total_fallback:.2f}"
            
            detail_data.append(['总金额', '', '', '', '', '', '', total_amount_display, '', '', ''])
            
            detail_tbl = Table(process_table_data_for_pdf(detail_data),
                               colWidths=[1.0 * cm,  # 序号
                                          2.3 * cm,  # 商品名称
                                          2.3 * cm,  # 商品明细
                                          2.2 * cm,  # 规格型号
                                          1.0 * cm,  # 单位
                                          1.0 * cm,  # 数量
                                          1.2 * cm,  # 单价
                                          1.4 * cm,  # 总价
                                          2.8 * cm,  # 请购理由
                                          1.6 * cm,  # 需求人
                                          2.2 * cm]  # 备注
                               )  # 调整列宽，总宽度19cm
            
            detail_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
                ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
                ('FONTSIZE', (0, 0), (-1, 0), 7),  # 进一步减少字体大小
                ('FONTSIZE', (0, 1), (-1, -2), 6),  # 进一步减少字体大小
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BACKGROUND', (0, -1), (6, -1), colors.lightgrey),
                ('SPAN', (0, -1), (6, -1)),
                ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # 减少内边距
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            story.append(detail_tbl)
            story.append(Spacer(1, 10))  # 减少间距
        
        # 5. 审批进程（费用表格之后）
        timeline = approval_detail.get("timeline", [])
        task_list = approval_detail.get("task_list", [])
        if timeline:
            # 格式化审批进程表格
            timeline_table = format_timeline_table(timeline, task_list)
            
            # 处理签名图片
            modified_timeline_data = []
            timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理时间']
            modified_timeline_data.append(timeline_headers)
            
            for row in timeline_table:
                processor_name = row[2]
                signature_path = get_signature_image_path(processor_name)
                if signature_path:
                    try:
                        signature_img = Image(signature_path, width=24, height=10)
                        modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                    except Exception as e:
                        print(f"签名图加载失败: {e}")
                        modified_timeline_data.append(row)
                else:
                    modified_timeline_data.append(row)
            
            timeline_tbl = Table(process_table_data_for_pdf(modified_timeline_data),
                                 colWidths=[2.5 * cm, 3.8 * cm, 4.5 * cm, 3.8 * cm, 4.4 * cm])  # 总宽度19cm，与表头完全一致
            timeline_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
                ('FONTSIZE', (0, 0), (-1, 0), 7),  # 进一步减少字体大小
                ('FONTSIZE', (0, 1), (-1, -1), 6),  # 进一步减少字体大小
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # 进一步减少内边距，更紧凑
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            story.append(timeline_tbl)
        
        # 生成PDF
        doc.build(story)
        print(f"采购申请PDF报告已生成: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"生成采购申请PDF失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_three_way_comparison_pdf(approval_detail: Dict[str, Any], tenant_token: str) -> str:
    """生成三方比价审批PDF报告（占位实现）"""
    try:
        # 注册中文字体
        register_chinese_fonts()
        
        # 生成PDF文件名
        instance_code = approval_detail.get('instance_code', 'unknown')
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"三方比价审批报告_{instance_code}_{current_time}.pdf"
        
        # 创建PDF文档
        doc = SimpleDocTemplate(output_filename, pagesize=A4)
        story = []
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # 居中
            textColor=colors.darkblue,
            fontName="ChineseFont"
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName="ChineseFont"
        )
        
        # 添加标题
        story.append(Paragraph(f"三方比价审批报告（实时生成）", title_style))
        story.append(Paragraph(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        story.append(Spacer(1, 20))
        
        # 基本信息
        applicant_name = resolve_user_name_from_user_id(approval_detail.get('open_id', ''))
        department_name = get_department_name(tenant_token, approval_detail.get('department_id', ''))
        start_time_formatted = format_time_without_timezone(approval_detail.get('start_time', ''), LOCAL_TZ)
        
        basic_info = [
            ['申请单号', approval_detail.get('serial_number', 'N/A')],
            ['申请人', applicant_name],
            ['申请部门', department_name],
            ['申请时间', start_time_formatted],
            ['审批类型', '三方比价']
        ]
        
        basic_table = Table(process_table_data_for_pdf(basic_info), colWidths=[3*cm, 8*cm])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ("FONTNAME", (0, 0), (-1, 0), "ChineseFont"),
            ("FONTNAME", (0, 1), (-1, -1), "ChineseFont"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(basic_table)
        story.append(Spacer(1, 15))
        
        # 占位内容
        story.append(Paragraph("【三方比价详情】", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.darkblue, fontName="ChineseFont")))
        story.append(Paragraph("此部分为三方比价审批的详细内容，具体实现待完善。", normal_style))
        
        # 生成PDF
        doc.build(story)
        print(f"三方比价PDF报告已生成: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"生成三方比价PDF失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_fixed_asset_pdf(approval_detail: Dict[str, Any], tenant_token: str) -> str:
    """生成固定资产审批PDF报告（占位实现）"""
    try:
        # 注册中文字体
        register_chinese_fonts()
        
        # 生成PDF文件名
        instance_code = approval_detail.get('instance_code', 'unknown')
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"固定资产审批报告_{instance_code}_{current_time}.pdf"
        
        # 创建PDF文档
        doc = SimpleDocTemplate(output_filename, pagesize=A4)
        story = []
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # 居中
            textColor=colors.darkblue,
            fontName="ChineseFont"
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName="ChineseFont"
        )
        
        # 添加标题
        story.append(Paragraph(f"固定资产审批报告（实时生成）", title_style))
        story.append(Paragraph(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        story.append(Spacer(1, 20))
        
        # 基本信息
        applicant_name = resolve_user_name_from_user_id(approval_detail.get('open_id', ''))
        department_name = get_department_name(tenant_token, approval_detail.get('department_id', ''))
        start_time_formatted = format_time_without_timezone(approval_detail.get('start_time', ''), LOCAL_TZ)
        
        basic_info = [
            ['申请单号', approval_detail.get('serial_number', 'N/A')],
            ['申请人', applicant_name],
            ['申请部门', department_name],
            ['申请时间', start_time_formatted],
            ['审批类型', '固定资产']
        ]
        
        basic_table = Table(process_table_data_for_pdf(basic_info), colWidths=[3*cm, 8*cm])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ("FONTNAME", (0, 0), (-1, 0), "ChineseFont"),
            ("FONTNAME", (0, 1), (-1, -1), "ChineseFont"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(basic_table)
        story.append(Spacer(1, 15))
        
        # 占位内容
        story.append(Paragraph("【固定资产详情】", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.darkblue, fontName="ChineseFont")))
        story.append(Paragraph("此部分为固定资产审批的详细内容，具体实现待完善。", normal_style))
        
        # 生成PDF
        doc.build(story)
        print(f"固定资产PDF报告已生成: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"生成固定资产PDF失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_expense_reimbursement_pdf(approval_detail: Dict[str, Any], tenant_token: str) -> str:
    """生成费用报销审批PDF报告（占位实现）"""
    try:
        # 注册中文字体
        register_chinese_fonts()
        
        # 生成PDF文件名
        instance_code = approval_detail.get('instance_code', 'unknown')
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"费用报销审批报告_{instance_code}_{current_time}.pdf"
        
        # 创建PDF文档
        doc = SimpleDocTemplate(output_filename, pagesize=A4)
        story = []
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # 居中
            textColor=colors.darkblue,
            fontName="ChineseFont"
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName="ChineseFont"
        )
        
        # 添加标题
        story.append(Paragraph(f"费用报销审批报告（实时生成）", title_style))
        story.append(Paragraph(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        story.append(Spacer(1, 20))
        
        # 基本信息
        applicant_name = resolve_user_name_from_user_id(approval_detail.get('open_id', ''))
        department_name = get_department_name(tenant_token, approval_detail.get('department_id', ''))
        start_time_formatted = format_time_without_timezone(approval_detail.get('start_time', ''), LOCAL_TZ)
        
        basic_info = [
            ['申请单号', approval_detail.get('serial_number', 'N/A')],
            ['申请人', applicant_name],
            ['申请部门', department_name],
            ['申请时间', start_time_formatted],
            ['审批类型', '费用报销']
        ]
        
        basic_table = Table(process_table_data_for_pdf(basic_info), colWidths=[3*cm, 8*cm])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ("FONTNAME", (0, 0), (-1, 0), "ChineseFont"),
            ("FONTNAME", (0, 1), (-1, -1), "ChineseFont"),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(basic_table)
        story.append(Spacer(1, 15))
        
        # 占位内容
        story.append(Paragraph("【费用报销详情】", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.darkblue, fontName="ChineseFont")))
        story.append(Paragraph("此部分为费用报销审批的详细内容，具体实现待完善。", normal_style))
        
        # 生成PDF
        doc.build(story)
        print(f"费用报销PDF报告已生成: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"生成费用报销PDF失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def do_approval_instance_event(data: lark.CustomizedEvent) -> None:
    """处理审批实例状态变更事件"""
    event_data = lark.JSON.marshal(data, indent=4)
    event_dict = json.loads(event_data)

    print(f"[审批事件接收] 原始事件数据: {event_data}")

    # 提取事件信息
    if event_dict:
        status = event_dict.get("event", {}).get("status", "")
        instance_code = event_dict.get("event", {}).get("instance_code", "")
        approval_code = event_dict.get("event", {}).get("approval_code", "")

        print(f"[审批事件处理] 审批状态: {status}, 实例Code: {instance_code}, 审批定义Code: {approval_code}")

        # 处理审批通过事件
        if status == "APPROVED":
            # 获取审批类型
            approval_type = get_approval_type_name(approval_code)
            print(f"[审批通过] 审批实例 {instance_code} 已通过审批，审批类型: {approval_type}，开始生成PDF...")
            
            try:
                # 获取tenant_access_token
                tenant_token, err = get_tenant_access_token(APP_ID, APP_SECRET)
                if err:
                    print(f"获取tenant_access_token失败: {err}")
                    return
                
                # 获取审批实例详情
                instance_id = event_dict.get("event", {}).get("instance_code", "")
                if not instance_id:
                    print("未找到实例ID，无法获取详情")
                    return
                
                approval_detail = fetch_approval_instance_detail(tenant_token, instance_id)
                
                # 根据审批类型调用对应的PDF生成器
                pdf_filename = None
                if approval_type == "采购申请":
                    pdf_filename = generate_procurement_approval_pdf(approval_detail, tenant_token)
                elif approval_type == "三方比价":
                    pdf_filename = generate_three_way_comparison_pdf(approval_detail, tenant_token)
                elif approval_type == "固定资产":
                    pdf_filename = generate_fixed_asset_pdf(approval_detail, tenant_token)
                elif approval_type == "费用报销":
                    pdf_filename = generate_expense_reimbursement_pdf(approval_detail, tenant_token)
                else:
                    print(f"[PDF生成失败] 未知的审批类型: {approval_type}")
                    return
                
                if pdf_filename:
                    print(f"[PDF生成成功] 审批实例 {instance_code} ({approval_type}) 的PDF报告已生成: {pdf_filename}")
                else:
                    print(f"[PDF生成失败] 审批实例 {instance_code} ({approval_type}) 的PDF报告生成失败")
                    
            except Exception as e:
                print(f"[PDF生成异常] 处理审批实例 {instance_code} ({approval_type}) 时发生错误: {e}")
                import traceback
                traceback.print_exc()

def main():
    print("=== 实时PDF生成器启动 ===")
    print("当审批通过时自动生成包含签名图片的PDF报告")
    print("支持的审批类型:")
    for approval_type, approval_code in APPROVAL_DEFINITIONS.items():
        print(f"  - {approval_type}: {approval_code}")
    
    print("\n=== 步骤1: 获取 tenant_access_token ===")
    tenant_access_token, err = get_tenant_access_token(APP_ID, APP_SECRET)
    if err:
        print(f"Error: 获取 tenant_access_token 失败: {err}", file=sys.stderr)
        exit(1)

    print("\n=== 步骤2: 订阅审批事件 ===")
    subscription_success = True
    for approval_type, approval_code in APPROVAL_DEFINITIONS.items():
        print(f"正在订阅 {approval_type} 审批事件...")
        if not subscribe_approval_event(tenant_access_token, approval_code):
            print(f"订阅 {approval_type} 审批事件失败", file=sys.stderr)
            subscription_success = False
        else:
            print(f"订阅 {approval_type} 审批事件成功")
    
    if not subscription_success:
        print("部分审批事件订阅失败，但将继续启动WebSocket客户端...", file=sys.stderr)

    print("\n=== 步骤3: 注册事件处理函数 ===")
    # 注册审批实例状态变更事件（支持V1和V2版本）
    event_handler = lark.EventDispatcherHandler.builder(APP_ID, APP_SECRET) \
        .register_p1_customized_event("approval_instance", do_approval_instance_event) \
        .register_p1_customized_event("approval_instance_v2", do_approval_instance_event) \
        .build()

    print("\n=== 步骤4: 启动 WebSocket 客户端 ===")
    print("正在连接飞书事件推送服务...")
    print("等待审批通过事件，将自动生成包含签名图片的PDF报告...")
    cli = lark.ws.Client(APP_ID, APP_SECRET,
                         event_handler=event_handler, log_level=lark.LogLevel.DEBUG)
    print("WebSocket客户端已启动，等待接收审批事件...")
    cli.start()

if __name__ == "__main__":
    main()

