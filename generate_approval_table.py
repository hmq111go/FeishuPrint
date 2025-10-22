#!/usr/bin/env python3
"""
生成审批进程表格
获取某一天通过的审批，生成包含采购订单明细和审批进程的表格
使用审批定义中的真实节点名称
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union

import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image

from feishu_approval_fetch import (
    request_tenant_access_token,
    list_approval_instance_ids,
    fetch_approval_instance_detail,
    resolve_user_name_from_user_id,
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


def load_employee_mapping() -> Dict[str, str]:
    """加载员工映射文件"""
    try:
        mapping_file_path = os.path.join(os.path.dirname(__file__), "employee_mapping.json")
        with open(mapping_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载员工映射文件失败: {e}")
        return {}


def get_approval_definition(tenant_token: str, approval_code: str) -> Dict[str, Any]:
    """获取审批定义信息"""
    url = f"https://open.feishu.cn/open-apis/approval/v4/approvals/{approval_code}"
    headers = {
        "Authorization": f"Bearer {tenant_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    print(f"GET: {url}")
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    result = response.json()
    print(f"Response: {json.dumps(result, ensure_ascii=False)}")
    if result.get("code", 0) != 0:
        raise RuntimeError(
            f"Feishu error fetching approval definition: code={result.get('code')} msg={result.get('msg')}"
        )
    return result.get("data", {})


def create_wrapped_text(text: str, font_name: str = "ChineseFont", font_size: int = 9) -> Paragraph:
    """创建支持自动换行的文本段落"""
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # 检查中文字体是否已注册
    registered_fonts = pdfmetrics.getRegisteredFontNames()
    if "ChineseFont" in registered_fonts and font_name == "ChineseFont":
        style.fontName = "ChineseFont"  # 使用中文字体
    else:
        style.fontName = "Helvetica"  # 使用安全的默认字体

    style.fontSize = font_size
    style.alignment = 1  # 居中对齐
    style.textColor = colors.black

    # 处理换行符和长文本
    wrapped_text = text.replace("\n", "<br/>")
    return Paragraph(wrapped_text, style)
    """获取审批定义信息"""


from reportlab.platypus import Image as RLImage  # 避免名字冲突


def process_table_data_for_pdf(table_data: List[List[Any]]) -> List[List[Any]]:
    """把字符串换成 Paragraph，其它（Image/Paragraph）保持原样"""
    processed = []
    for i, row in enumerate(table_data):
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                new_row.append(create_wrapped_text(cell))
            elif isinstance(cell, RLImage):
                new_row.append(cell)  # 原样保留
            else:
                new_row.append(cell)  # 已经是 Paragraph 或其它
        processed.append(new_row)
    return processed


def get_node_name_mapping(tenant_token: str, approval_code: str) -> Dict[str, str]:
    """获取节点ID到节点名称的映射"""
    approval_def = get_approval_definition(tenant_token, approval_code)
    node_list = approval_def.get("node_list", [])

    mapping = {}
    for node in node_list:
        node_id = node.get("node_id", "")
        node_name = node.get("name", "")
        if node_id and node_name:
            mapping[node_id] = node_name

    return mapping


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
        # Treat values with >=13 digits as milliseconds
        if ms < 10 ** 12:
            return ""  # likely seconds or smaller numbers we don't format here
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
                    # 处理费用明细的ext字段
                    result[widget_name] = widget
            else:
                # 对于其他类型的控件，直接存储value
                result[widget_name] = widget_value

        return result
    except Exception as e:
        print(f"解析表单数据失败: {e}")
        return {}


def get_node_name_from_task_list(task_list: List[Dict[str, Any]], node_id: str) -> str:
    """从任务列表中获取节点名称"""
    for task in task_list:
        if task.get('node_id') == node_id:
            return task.get('node_name', '未知节点')
    return '未知节点'

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle

# def build_header_block():
#     """黑字+大框表头（加高版）"""
#     sty_big = ParagraphStyle(
#         'HB1',
#         fontName='ChineseFont',
#         fontSize=20,
#         alignment=1,
#         textColor=colors.black,
#         spaceBefore=12,   # 段前
#         spaceAfter=12,    # 段后
#     )
#     sty_sml = ParagraphStyle(
#         'HB2',
#         fontName='ChineseFont',
#         fontSize=11,
#         alignment=1,
#         textColor=colors.black,
#         spaceBefore=8,
#         spaceAfter=8,
#     )
#
#     data = [
#         [Paragraph("上海硼矩新材料科技有限公司", sty_big)],
#         [Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml)],
#         [Paragraph("采购申请单", sty_big)],
#     ]
#
#     # 单行行高固定死，三行总和 ≈ 3.5 cm，想再高调大即可
#     tbl = Table(data, colWidths=[19 * cm], rowHeights=[1.2 * cm, 0.9 * cm, 1.2 * cm])
#     tbl.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 上下也居中
#         ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
#     ]))
#     return tbl
def build_header_block():
    """优化后的表头：统一宽度，增加内边距，避免文字压在框线上"""
    # 1. 左侧 BoronMatrix 文字
    sty_b = ParagraphStyle('LM', fontName='ChineseFont', fontSize=22, textColor=colors.black)
    left_par = Paragraph('<b>Boron</b>Matrix', sty_b)

    # 2. 右侧公司信息
    sty_big = ParagraphStyle('HB1', fontName='ChineseFont', fontSize=18, alignment=1, textColor=colors.black,
                             spaceBefore=6, spaceAfter=6)
    sty_sml = ParagraphStyle('HB2', fontName='ChineseFont', fontSize=10, alignment=1, textColor=colors.black,
                             spaceBefore=4, spaceAfter=4)
    right_data = [
        [Paragraph("上海硼矩新材料科技有限公司", sty_big)],
        [Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml)],
        [Paragraph("采购申请单", sty_big)]
    ]
    right_tbl = Table(right_data, colWidths=[13*cm])
    right_tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # 增加内边距
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
    ]))

    # 3. 左右合并 + 整体加框，使用标准宽度
    main_data = [[left_par, right_tbl]]
    main_tbl = Table(main_data, colWidths=[6*cm, 13*cm], rowHeights=[2.5*cm])  # 增加高度
    main_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX',    (0, 0), (-1, -1), 1.5, colors.black),  # 外框
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # 增加内边距，避免文字压在框线上
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
    ]))
    return main_tbl
def build_approval_info_block(serial: str, start_time: str):
    """优化后的审批信息块：统一宽度，增加内边距"""
    sty = ParagraphStyle('AI', fontName='ChineseFont', fontSize=11, textColor=colors.black)
    data = [[Paragraph(f"审批编号：{serial}", sty),
             Paragraph(f"申请时间：{start_time}", sty)]]
    tbl = Table(data, colWidths=[9.5*cm, 9.5*cm])  # 保持与表头一致的宽度
    tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # 增加内边距
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),  # 添加外框
    ]))
    return tbl
def format_timeline_table(timeline: List[Dict[str, Any]], task_list: List[Dict[str, Any]],
                          employee_mapping: Dict[str, str], node_name_mapping: Dict[str, str]) -> List[List[str]]:
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
            # 从任务列表中查找对应的节点名称
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
            # 从任务列表中查找对应的节点名称
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
                pass  # 如果解析失败，保持原来的processor_name

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


def generate_pdf_report(approval_data: List[Dict[str, Any]], query_date: str, output_filename: str = None):
    # 注册中文字体
    try:
        # 导入必要的模块
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        # 尝试注册系统中文字体
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

        # 检查字体是否已注册
        registered_fonts = pdfmetrics.getRegisteredFontNames()
        if "ChineseFont" in registered_fonts:
            print("中文字体已注册")
            chinese_font_registered = True
        else:
            chinese_font_registered = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        # 对于ttc文件，尝试注册第一个字体
                        if font_path.endswith('.ttc'):
                            pdfmetrics.registerFont(TTFont("ChineseFont", font_path, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                        chinese_font_registered = True
                        print(f"成功注册中文字体: {font_path}")
                        break
                    except Exception as e:
                        print(f"注册字体失败 {font_path}: {e}")
                        continue

        if not chinese_font_registered:
            # 如果无法注册系统字体，尝试下载并使用开源中文字体
            try:
                import urllib.request
                import tempfile

                print("尝试下载开源中文字体...")
                font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf"
                temp_dir = tempfile.gettempdir()
                font_path = os.path.join(temp_dir, "NotoSansSC-Regular.otf")

                if not os.path.exists(font_path):
                    urllib.request.urlretrieve(font_url, font_path)
                    print(f"字体已下载到: {font_path}")

                pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                chinese_font_registered = True
                print(f"成功注册下载的中文字体")
            except Exception as e:
                print(f"下载并注册字体失败: {e}")

        # 注册字体映射，确保中文字体能够正确应用
        if chinese_font_registered:
            # 创建字体映射，确保中文字体能够正确应用
            pdfmetrics.registerFontFamily('ChineseFont', normal='ChineseFont')
        else:
            print("警告: 未能注册中文字体，中文可能显示为方块")
    except Exception as e:
        print(f"字体注册过程出错: {e}")
    """生成PDF格式的审批报告"""
    if output_filename is None:
        output_filename = f"审批报告_{query_date}.pdf"

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

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
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
    sty_label = ParagraphStyle('Lab', fontName='ChineseFont', fontSize=10, textColor=colors.black)
    sty_val   = ParagraphStyle('Val', fontName='ChineseFont', fontSize=10, textColor=colors.black)
    # 遍历每个审批实例
    for i, detail in enumerate(approval_data, 1):
        # 0. 矢量表头
        story.append(build_header_block())
        story.append(Spacer(1, 20))   # 与正文空 20 pt

        # 1. 审批信息（审批编号和申请时间）
        story.append(build_approval_info_block(
            detail.get('serial_number', 'N/A'),
            detail.get('start_time_formatted', 'N/A')
        ))
        story.append(Spacer(1, 15))

        # 2. 费用明细标题
        # story.append(Paragraph("费用明细", heading_style))
        story.append(Spacer(1, 10))

        # ===== 费用明细标题 =====
        if detail.get('expense_details'):
            story.append(Spacer(1, 15))
            story.append(Paragraph("费用明细", heading_style))
            story.append(Spacer(1, 8))

            # ---- 申请人/部门/采购类别/期望交货时间 一行 ----
            form_data = parse_form_data(detail.get('form', '[]'))
            cat = form_data.get('采购类别', '未知')
            delivery = form_data.get('期望交货时间', '').split('T')[0] if 'T' in form_data.get('期望交货时间', '') else '未知'
            info_tbl = Table([[Paragraph("申请人", sty_label), Paragraph(detail.get('applicant_name', '')+'-'+detail.get('department_name', ''), sty_val),
                               # Paragraph("申请部门", sty_label), Paragraph(detail.get('department_name', ''), sty_val),
                               Paragraph("采购类别", sty_label), Paragraph(cat, sty_val),
                               Paragraph("期望交货时间", sty_label), Paragraph(delivery, sty_val)]],
                             colWidths=[2.2*cm, 2.8*cm]*4)
            info_tbl.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
                ('BACKGROUND', (2, 0), (2, -1), colors.whitesmoke),
                ('BACKGROUND', (4, 0), (4, -1), colors.whitesmoke),
                ('BACKGROUND', (6, 0), (6, -1), colors.whitesmoke),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # 增加内边距
                ('TOPPADDING',    (0, 0), (-1, -1), 8),
                ('LEFTPADDING',   (0, 0), (-1, -1), 8),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
                ('BOX', (0, 0), (-1, -1), 1.5, colors.black),  # 添加外框
            ]))
            story.append(info_tbl)
            story.append(Spacer(1, 10))

            # ---- 费用表格（原有逻辑，仅把表头/列宽粘过来） ----
            detail_headers = ['序号', '商品名称(可选)', '商品明细', '规格型号', '单位', '数量', '单价', '总价', '请购理由', '需求人', '备注']
            detail_data = [detail_headers]
            total_amount = 0
            for idx, item in enumerate(detail['expense_details'], 1):
                q = float(item.get('数量', 0))
                p = float(item.get('单价', 0))
                t = q * p
                total_amount += t
                detail_data.append([
                    str(idx), item.get('商品及其辅助属性', ''), item.get('名称', ''), item.get('规格型号', ''),
                    item.get('单位', ''), str(q), f"{p:.2f}", f"{t:.2f}",
                    item.get('请购理由', ''), item.get('需求人', ''), item.get('备注', '')
                ])
            detail_data.append(['总金额', '', '', '', '', '', '', f"{total_amount:.2f}", '', '', ''])

            detail_tbl = Table(process_table_data_for_pdf(detail_data),
                               colWidths=[0.8*cm, 2*cm, 2*cm, 1.8*cm, 0.8*cm, 0.8*cm, 1.2*cm, 1.2*cm, 1.8*cm, 1.2*cm, 1.2*cm])
            detail_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -2), 8),
                ('GRID', (0, 0), (-1, -2), 1, colors.black),
                ('BACKGROUND', (0, -1), (6, -1), colors.lightgrey),
                ('SPAN', (0, -1), (6, -1)),   # 总金额合并
                ('LINEABOVE', (0, -1), (-1, -1), 0, colors.white),  # 去上框
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # 增加内边距
                ('TOPPADDING',    (0, 0), (-1, -1), 6),
                ('LEFTPADDING',   (0, 0), (-1, -1), 6),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
                ('BOX', (0, 0), (-1, -2), 1.5, colors.black),  # 添加外框
            ]))
            story.append(detail_tbl)
            story.append(Spacer(1, 20))

        # ===== 审批进程（费用表格之后） =====
        if detail.get('timeline_table'):
            story.append(Paragraph("审批进程", heading_style))
            story.append(Spacer(1, 8))
            # 下面保持你原有 timeline_table 逻辑即可
            modified_timeline_data = []
            timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理时间']
            modified_timeline_data.append(timeline_headers)
            for row in detail['timeline_table']:
                processor_name = row[2]
                signature_path = get_signature_image_path(processor_name)
                if signature_path:
                    try:
                        signature_img = Image(signature_path, width=2.5*cm, height=1*cm)
                        modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                    except Exception as e:
                        print(f"签名图加载失败: {e}")
                        modified_timeline_data.append(row)
                else:
                    modified_timeline_data.append(row)

            timeline_tbl = Table(process_table_data_for_pdf(modified_timeline_data),
                                 colWidths=[1*cm, 2.5*cm, 3*cm, 2.5*cm, 3*cm])
            timeline_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), "ChineseFont"),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # 增加内边距
                ('TOPPADDING',    (0, 0), (-1, -1), 8),
                ('LEFTPADDING',   (0, 0), (-1, -1), 8),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
                ('BOX', (0, 0), (-1, -1), 1.5, colors.black),  # 添加外框
            ]))
            story.append(timeline_tbl)

        # 分页符保持原逻辑
        if i < len(approval_data):
            story.append(PageBreak())

    # 生成PDF
    doc.build(story)
    print(f"PDF报告已生成: {output_filename}")
    return output_filename


def generate_approval_report(query_date: str = "2025-10-17"):
    """生成审批报告"""
    # print(f"=== 获取 {query_date} 审批通过的采购申请 ===")

    # 计算查询时间范围
    d = datetime.strptime(query_date, "%Y-%m-%d").date()
    start_dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=LOCAL_TZ)
    end_dt = start_dt + timedelta(days=1) - timedelta(milliseconds=1)
    start_time = str(int(start_dt.timestamp() * 1000))
    end_time = str(int(end_dt.timestamp() * 1000))

    # 获取token和实例列表
    tenant_token = request_tenant_access_token(APP_ID, APP_SECRET)
    instance_ids = list_approval_instance_ids(tenant_token, APPROVAL_CODE, start_time, end_time)

    # 加载员工映射和节点名称映射
    employee_mapping = load_employee_mapping()
    node_name_mapping = get_node_name_mapping(tenant_token, APPROVAL_CODE)

    approved_count = 0
    approval_data = []  # 用于存储PDF数据

    for instance_id in instance_ids:
        try:
            detail = fetch_approval_instance_detail(tenant_token, instance_id)

            # 只处理审批通过的实例
            if detail.get("status") != "APPROVED":
                continue

            approved_count += 1

            # 显示部门信息
            department_id = detail.get('department_id', '')
            department_name = "未知部门"
            if department_id:
                department_name = get_department_name(tenant_token, department_id)
                print(f"申请部门: {department_name}")

            start_time_formatted = format_time_without_timezone(detail.get('start_time', ''), LOCAL_TZ)
            end_time_formatted = format_time_without_timezone(detail.get('end_time', ''), LOCAL_TZ)
            print(f"申请时间: {start_time_formatted}")
            print(f"完成时间: {end_time_formatted}")

            # 解析表单数据
            form_data = parse_form_data(detail.get('form', '[]'))

            # 显示采购明细
            expense_details = []
            if '费用明细' in form_data:
                print(f"\n--- 采购明细 ---")
                items = form_data['费用明细']
                if isinstance(items, list):
                    for i, item in enumerate(items, 1):
                        print(f" 商品及其辅助属性:{i}. {item.get('商品及其辅助属性', '')}")
                        print(f" 名称:{i}.{item.get('名称', '')}")
                        print(f" 规格型号:{i}.{item.get('规格型号', '')}")
                        print(f"   数量: {item.get('数量', '')} {item.get('单位', '')}")
                        print(f"   单价: {item.get('单价', '')} 元")
                        print(f"   金额: {item.get('金额', '')} 元")
                        print(f"   需求人: {item.get('需求人', '')}")
                        print(f"   备注: {item.get('备注', '')}")
                        expense_details.append(item)

            # 显示审批进程表格
            timeline = detail.get("timeline", [])
            task_list = detail.get("task_list", [])
            timeline_table = []
            if timeline:
                print("\n--- 审批进程 ---")
                timeline_table = format_timeline_table(timeline, task_list, employee_mapping, node_name_mapping)

                # 打印表格
                print("序号 | 节点名称 | 处理人 | 处理结果 | 处理时间")
                print("-" * 80)
                for row in timeline_table:
                    print(f"{row[0]:<4} | {row[1]:<8} | {row[2]:<8} | {row[3]:<12} | {row[4]}")

            # 收集PDF数据
            approval_data.append({
                'approval_name': detail.get('approval_name', 'N/A'),
                'serial_number': detail.get('serial_number', 'N/A'),
                'applicant_name': resolve_user_name_from_user_id(detail.get('open_id', '')),
                'department_name': department_name,
                'start_time_formatted': start_time_formatted,
                'end_time_formatted': end_time_formatted,
                'expense_details': expense_details,
                'timeline_table': timeline_table,
                'form': detail.get('form', '[]')  # 保存原始表单数据
            })

        except Exception as e:
            print(f"处理实例 {instance_id} 失败: {e}")
            continue

    print(f"\n=== 统计 ===")
    print(f"总共找到 {len(instance_ids)} 个审批实例")
    print(f"其中审批通过的有 {approved_count} 个")

    # 生成PDF
    if approval_data:
        pdf_filename = generate_pdf_report(approval_data, query_date)
        print(f"PDF报告已生成: {pdf_filename}")

    return approval_data


def main():
    """主函数"""
    if len(sys.argv) > 1:
        query_date = sys.argv[1]
    else:
        query_date = "2025-10-15"  # 默认查询日期

    generate_approval_report(query_date)


if __name__ == "__main__":
    main()
