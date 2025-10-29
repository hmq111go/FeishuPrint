#!/usr/bin/env python3
"""
PDF生成模块
负责不同类型审批的PDF报告生成
"""
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Union

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from employee_manager import EmployeeManager
from feishu_api import FeishuAPI
from pdf_sender import PDFSender


class PDFGenerator:
    """PDF生成器"""
    
    def __init__(self, feishu_api: FeishuAPI, employee_manager: EmployeeManager, auto_send: bool = True):
        self.feishu_api = feishu_api
        self.employee_manager = employee_manager
        self.auto_send = auto_send
        self.logger = logging.getLogger(__name__)
        
        # 使用中国时区 UTC+8
        self.local_tz = timezone(timedelta(hours=8))
        
        # 创建PDF存储目录
        self.pdf_base_dir = "pdf_reports"
        self.pdf_directories = {
            "采购申请": "procurement",
            "三方比价": "three_way_comparison", 
            "固定资产": "fixed_asset",
            "费用报销": "expense_reimbursement",
            "浙江采购申请": "zhejiang_procurement",
            "浙江费用报销": "zhejiang_expense_reimbursement",
            "知本采购申请": "zhiben_procurement",
            "知本费用报销": "zhiben_expense_reimbursement",
            "知本固定资产验收": "zhiben_fixed_asset"
        }
        self._ensure_directories_exist()
        
        # 初始化PDF发送器
        if self.auto_send:
            self.pdf_sender = PDFSender(feishu_api.app_id, feishu_api.app_secret)
            self.logger.info("自动发送功能已启用")
        else:
            self.pdf_sender = None
            self.logger.info("自动发送功能已禁用")
    
    def _ensure_directories_exist(self):
        """确保PDF存储目录存在"""
        # 创建基础目录
        os.makedirs(self.pdf_base_dir, exist_ok=True)
        
        # 创建各类PDF的子目录
        for approval_type, dir_name in self.pdf_directories.items():
            dir_path = os.path.join(self.pdf_base_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
    
    def _generate_pdf_filename(self, approval_type: str, approval_detail: Dict[str, Any]) -> str:
        """生成PDF文件名（简化版，不包含instance_code）"""
        # 获取申请人信息
        applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
        applicant_name = applicant_info.get("name", "未知申请人")
        
        # 获取申请时间
        start_time = approval_detail.get('start_time', '')
        if start_time:
            try:
                # 解析时间戳
                timestamp = int(start_time) / 1000  # 转换为秒
                dt = datetime.fromtimestamp(timestamp, tz=self.local_tz)
                date_str = dt.strftime("%Y%m%d")
            except:
                date_str = datetime.now().strftime("%Y%m%d")
        else:
            date_str = datetime.now().strftime("%Y%m%d")
        
        # 生成时间戳（避免重名）
        current_time = datetime.now().strftime("%H%M%S")
        
        # 生成文件名
        filename = f"{applicant_name}_{date_str}_{current_time}.pdf"
        
        # 获取对应的目录
        dir_name = self.pdf_directories.get(approval_type, "other")
        dir_path = os.path.join(self.pdf_base_dir, dir_name)
        
        # 返回完整路径
        return os.path.join(dir_path, filename)
    
    def _send_and_rename_pdf(self, pdf_path: str, open_id: str) -> str:
        """
        发送PDF并重命名文件添加已发送标识
        
        Args:
            pdf_path: PDF文件路径
            open_id: 接收用户的open_id
            
        Returns:
            重命名后的文件路径
        """
        if not self.auto_send or not self.pdf_sender:
            return pdf_path
        
        try:
            # 发送PDF
            self.logger.info(f"开始发送PDF: {pdf_path}")
            success, message = self.pdf_sender.send_pdf_to_user(pdf_path, open_id)
            
            if success:
                self.logger.info(f"PDF发送成功: {message}")
                
                # 重命名文件，添加已发送标识
                renamed_path = self._add_sent_suffix(pdf_path)
                self.logger.info(f"PDF已重命名为: {renamed_path}")
                return renamed_path
            else:
                self.logger.error(f"PDF发送失败: {message}")
                return pdf_path
                
        except Exception as e:
            self.logger.error(f"发送PDF时发生异常: {e}")
            return pdf_path
    
    def _add_sent_suffix(self, pdf_path: str) -> str:
        """
        为PDF文件名添加已发送标识
        
        Args:
            pdf_path: 原始PDF文件路径
            
        Returns:
            重命名后的文件路径
        """
        try:
            # 分离文件名和扩展名
            dir_path = os.path.dirname(pdf_path)
            filename = os.path.basename(pdf_path)
            name, ext = os.path.splitext(filename)
            
            # 添加已发送标识
            new_filename = f"{name}_已发送{ext}"
            new_path = os.path.join(dir_path, new_filename)
            
            # 重命名文件
            os.rename(pdf_path, new_path)
            return new_path
            
        except Exception as e:
            self.logger.error(f"重命名PDF文件失败: {e}")
            return pdf_path
    
    def register_chinese_fonts(self):
        """注册中文字体"""
        try:
            font_paths = [
                # macOS
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/Library/Fonts/Arial Unicode.ttf",
                # Linux - 多种常见路径
                "/usr/share/fonts/truetype/arphic/uming.ttc",
                "/usr/share/fonts/truetype/arphic/ukai.ttc",
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/google-noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/chinese/simsun.ttc",
                "/usr/share/fonts/chinese/uming.ttc",
                "/usr/share/fonts/chinese/ukai.ttc",
                "/usr/local/share/fonts/wqy-zenhei/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/arphic/wqy-zenhei.ttc",
                # Windows
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/simfang.ttf",
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
            
            print("警告: 未能注册中文字体，将使用默认字体")
            # 使用 Helvetica 作为后备字体
            return False
        except Exception as e:
            print(f"字体注册过程出错: {e}")
            return False
    
    def get_available_font_name(self) -> str:
        """获取可用的字体名称"""
        registered_fonts = pdfmetrics.getRegisteredFontNames()
        if "ChineseFont" in registered_fonts:
            return "ChineseFont"
        return "Helvetica"

    def create_wrapped_text(self, text: str, font_name: str = "ChineseFont", font_size: int = 9) -> Paragraph:
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

    def process_table_data_for_pdf(self, table_data: List[List[Any]]) -> List[List[Any]]:
        """处理表格数据，将文本转换为支持换行的Paragraph"""
        processed = []
        for i, row in enumerate(table_data):
            new_row = []
            for cell in row:
                if isinstance(cell, str):
                    new_row.append(self.create_wrapped_text(cell))
                elif isinstance(cell, Image):
                    new_row.append(cell)  # 原样保留图片
                else:
                    new_row.append(cell)  # 已经是 Paragraph 或其它
            processed.append(new_row)
        return processed

    def build_header_block(self):
        """公司信息表头"""
        font_name = self.get_available_font_name()
        # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
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

        # 创建公司信息表格：第一行两列仅放 Logo；文本各行合并两列，确保绝对居中
        company_data = [
            [logo_cell, ""],
            [Paragraph("上海硼矩新材料科技有限公司", sty_big), ""],
            [Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml), ""],
            [Paragraph("采购申请单", sty_big), ""]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # Logo 行保持左侧位置不变
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            # 公司名与副标题、单据名行合并两列并绝对居中
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 1), (1, 3), 'CENTER'),
            ('VALIGN', (0, 1), (1, 3), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl

    def build_header_block_zhejiang(self):
        """公司信息表头 - 浙江采购申请版本"""
        font_name = self.get_available_font_name()
        # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
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

        # 创建公司信息表格：第一行两列仅放 Logo；文本各行合并两列，确保绝对居中
        company_data = [
            [logo_cell, ""],
            [Paragraph("浙江硼矩新材料科技有限公司", sty_big), ""],
            [Paragraph("Zhejiang BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml), ""],
            [Paragraph("采购申请单", sty_big), ""]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # Logo 行保持左侧位置不变
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            # 公司名与副标题、单据名行合并两列并绝对居中
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 1), (1, 3), 'CENTER'),
            ('VALIGN', (0, 1), (1, 3), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl

    def build_approval_info_block(self, serial: str, start_time: str):
        """审批编号和申请时间信息块 - 无框线"""
        font_name = self.get_available_font_name()
        sty = ParagraphStyle('AI', fontName=font_name, fontSize=9, textColor=colors.black)
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

    def build_applicant_info_block(self, applicant_name: str, department_name: str, category: str, delivery_time: str):
        """申请人、采购类别、期望交货时间信息表格"""
        font_name = self.get_available_font_name()
        sty_label = ParagraphStyle('Lab', fontName=font_name, fontSize=8, textColor=colors.black)
        sty_val = ParagraphStyle('Val', fontName=font_name, fontSize=8, textColor=colors.black)

        data = [[Paragraph("申请人", sty_label), Paragraph(f"{applicant_name}-{department_name}", sty_val),
                 Paragraph("采购类别", sty_label), Paragraph(category, sty_val),
                 Paragraph("期望交货时间", sty_label), Paragraph(delivery_time, sty_val)]]

        tbl = Table(data, colWidths=[2.17 * cm, 4.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm],
                    rowHeights=[0.6 * cm])  # 减少行高
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
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
    
    def build_header_block_expense(self):
        """公司信息表头 - 费用报销版本"""
        font_name = self.get_available_font_name()
        # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
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

        # 创建公司信息表格：第一行两列仅放 Logo；文本各行合并两列，确保绝对居中
        company_data = [
            [logo_cell, ""],
            [Paragraph("上海硼矩新材料科技有限公司", sty_big), ""],
            [Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml), ""],
            [Paragraph("费用报销单", sty_big)]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # Logo 行保持左侧位置不变
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            # 公司名与副标题、单据名行合并两列并绝对居中
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 1), (1, 3), 'CENTER'),
            ('VALIGN', (0, 1), (1, 3), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl

    def build_header_block_zhejiang_expense(self):
        """公司信息表头 - 浙江费用报销版本"""
        font_name = self.get_available_font_name()
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)

        logo_cell = ""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                logo_cell = Image(logo_path, width=100, height=14)
                logo_cell.hAlign = 'LEFT'
            else:
                logo_cell = ""
        except Exception:
            logo_cell = ""

        # 创建公司信息表格：第一行两列仅放 Logo；文本各行合并两列，确保绝对居中
        company_data = [
            [logo_cell, ""],
            [Paragraph("浙江硼矩新材料科技有限公司", sty_big), ""],
            [Paragraph("Zhejiang BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml), ""],
            [Paragraph("费用报销单", sty_big)]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # Logo 行保持左侧位置不变
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            # 公司名与副标题、单据名行合并两列并绝对居中
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 1), (1, 3), 'CENTER'),
            ('VALIGN', (0, 1), (1, 3), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl
    
    def build_header_block_zhiben(self):
        """公司信息表头 - 知本采购申请版本"""
        font_name = self.get_available_font_name()
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)

        logo_cell = ""
        # try:
        #     logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        #     if os.path.exists(logo_path):
        #         logo_cell = Image(logo_path, width=100, height=14)
        #         logo_cell.hAlign = 'LEFT'
        #     else:
        #         logo_cell = ""
        # except Exception:
        #     logo_cell = ""

        # 知本没有logo，所有行合并两列并绝对居中
        company_data = [
            [Paragraph("知本昕科（上海）人工智能科技有限公司", sty_big), ""],
            [Paragraph("EpiScience Artificial Intelligence Technology Co., Ltd", sty_sml), ""],
            [Paragraph("采购申请单", sty_big), ""]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # 所有行合并两列并绝对居中
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('ALIGN', (0, 0), (1, 2), 'CENTER'),
            ('VALIGN', (0, 0), (1, 2), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl
    
    def build_header_block_zhiben_expense(self):
        """公司信息表头 - 知本费用报销版本"""
        font_name = self.get_available_font_name()
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)

        logo_cell = ""

        # 知本没有logo，所有行合并两列并绝对居中
        company_data = [
            [Paragraph("知本昕科（上海）人工智能科技有限公司", sty_big), ""],
            [Paragraph("EpiScience Artificial Intelligence Technology Co., Ltd", sty_sml), ""],
            [Paragraph("费用报销单", sty_big), ""]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # 所有行合并两列并绝对居中
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('ALIGN', (0, 0), (1, 2), 'CENTER'),
            ('VALIGN', (0, 0), (1, 2), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl
    
    def build_header_block_zhiben_fixed_asset(self):
        """公司信息表头 - 知本固定资产验收版本"""
        font_name = self.get_available_font_name()
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)

        logo_cell = ""

        # 知本没有logo，所有行合并两列并绝对居中
        company_data = [
            [Paragraph("知本昕科（上海）人工智能科技有限公司", sty_big), ""],
            [Paragraph("EpiScience Artificial Intelligence Technology Co., Ltd", sty_sml), ""],
            [Paragraph("固定资产验收单", sty_big), ""]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # 所有行合并两列并绝对居中
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('ALIGN', (0, 0), (1, 2), 'CENTER'),
            ('VALIGN', (0, 0), (1, 2), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl
    
    def build_applicant_info_block_expense(self, applicant_name: str, department_name: str, reimbursement_reason: str, total_amount: str):
        """申请人、报销事由、费用汇总信息表格"""
        font_name = self.get_available_font_name()
        sty_label = ParagraphStyle('Lab', fontName=font_name, fontSize=8, textColor=colors.black)
        sty_val = ParagraphStyle('Val', fontName=font_name, fontSize=8, textColor=colors.black)

        data = [[Paragraph("申请人", sty_label), Paragraph(f"{applicant_name}-{department_name}", sty_val),
                 Paragraph("费用汇总", sty_label), Paragraph(str(total_amount), sty_val),
                 Paragraph("报销事由", sty_label), Paragraph(reimbursement_reason, sty_val)]]

        tbl = Table(data, colWidths=[2.17 * cm, 4.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm, 3.17 * cm])
        # 移除固定行高设置，让表格自适应内容高度
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
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

    def format_time_without_timezone(self, value: Union[str, int, float, None]) -> str:
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
            dt = datetime.fromtimestamp(ms / 1000.0, self.local_tz)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return ""

    def format_date_string(self, date_str: str) -> str:
        """格式化日期字符串，处理时区问题"""
        try:
            if not date_str:
                return ""
            
            # 如果包含T，说明是ISO格式，需要解析时区
            if 'T' in date_str:
                # 解析ISO格式日期
                from datetime import datetime
                # 移除时区信息并解析
                if '+' in date_str:
                    date_str = date_str.split('+')[0]
                elif 'Z' in date_str:
                    date_str = date_str.replace('Z', '')
                
                # 解析为datetime对象
                dt = datetime.fromisoformat(date_str)
                # 转换为中国时区
                dt = dt.replace(tzinfo=timezone.utc).astimezone(self.local_tz)
                return dt.strftime("%Y-%m-%d")
            else:
                # 如果已经是简单日期格式，直接返回
                return date_str
        except Exception:
            return date_str

    def parse_form_data(self, form_json: str) -> Dict[str, Any]:
        """解析表单数据"""
        import json
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
                        
                        # 处理费用明细的汇总信息
                        if widget_name == '费用明细' and 'ext' in widget:
                            ext_data = widget.get('ext', [])
                            if isinstance(ext_data, list) and len(ext_data) > 0:
                                summary_info = {}
                                for ext_item in ext_data:
                                    if 'sumItems' in ext_item:
                                        try:
                                            sum_items = json.loads(ext_item['sumItems'])
                                            if isinstance(sum_items, list) and len(sum_items) > 0:
                                                currency_info = sum_items[0]
                                                summary_info['currency'] = currency_info.get('currency', 'CNY')
                                                summary_info['total_amount'] = currency_info.get('value', '0')
                                        except:
                                            pass
                                    # 处理浙江采购申请中的formula类型ext item
                                    elif ext_item.get('type') == 'formula':
                                        summary_info['total_amount'] = ext_item.get('value')
                                if summary_info:
                                    result[f"{widget_name}_summary"] = summary_info
                    else:
                        # 处理费用明细的ext字段
                        result[widget_name] = widget
                else:
                    # 对于其他类型的控件，直接存储value                                               
                    result[widget_name] = widget_value

            return result
        except Exception as e:
            print(f"解析表单数据失败: {e}")
            # 尝试修复常见的JSON格式问题
            try:
                # 替换可能的问题字符
                fixed_json = form_json.replace('\\"', '"').replace('\\n', '\n')
                form_data = json.loads(fixed_json)
                result = {}
                
                for widget in form_data:
                    widget_name = widget.get('name', '')
                    widget_type = widget.get('type', '')
                    widget_value = widget.get('value', '')
                    
                    if widget_type == 'fieldList' and isinstance(widget_value, list):
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
                
                print("使用修复后的JSON解析成功")
                return result
            except Exception as e2:
                print(f"修复JSON后仍然解析失败: {e2}")
                return {}

    def format_timeline_table(self, timeline: List[Dict[str, Any]], task_list: List[Dict[str, Any]]) -> List[List[str]]:
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

            # 实时获取处理人姓名
            processor_name = "未知用户"
            if open_id:
                processor_info = self.employee_manager.get_employee_info_realtime(open_id)
                processor_name = processor_info["name"]
            elif user_id:
                processor_info = self.employee_manager.get_employee_info_realtime(user_id)
                processor_name = processor_info["name"]

            # 格式化时间
            formatted_time = self.format_time_without_timezone(create_time)

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
                # 从任务列表中查找对应的节点名称
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
                # 从任务列表中查找对应的节点名称
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
                    cc_info = self.employee_manager.get_employee_info_realtime(cc_open_id)
                    cc_names.append(cc_info["name"])

                # 从ext字段获取发起抄送的用户信息
                ext_str = item.get('ext', '{}')
                try:
                    import json
                    ext_data = json.loads(ext_str)
                    cc_initiator_open_id = ext_data.get('open_id', '')
                    if cc_initiator_open_id:
                        cc_initiator_info = self.employee_manager.get_employee_info_realtime(cc_initiator_open_id)
                        processor_name = cc_initiator_info["name"]
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
                comment if comment and comment.strip() else "",
                formatted_time
            ])

        return table_data

    def generate_procurement_approval_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """为单个审批实例生成PDF报告 - 采用generate_pdf_report的模板风格"""
        try:
            # 注册中文字体
            self.register_chinese_fonts()
            
            # 生成PDF文件名（使用新的命名规则和目录结构）
            output_filename = self._generate_pdf_filename("采购申请", approval_detail)
            
            # 创建PDF文档 - 采用generate_pdf_report的页面设置
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,  # 几乎顶格
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []
            
            # 获取样式
            styles = getSampleStyleSheet()
            
            # 1. 公司信息表头
            story.append(self.build_header_block())
            story.append(Spacer(1, 5))  # 减少间距
            
            # 2. 审批信息（审批编号和申请时间）
            # 实时获取申请人信息
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 3. 申请人信息表格
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            category = form_data.get('采购类别', '未知')
            delivery_time = form_data.get('期望交货时间', '').split('T')[0] if 'T' in form_data.get('期望交货时间', '') else '未知'
            
            story.append(self.build_applicant_info_block(
                applicant_name,
                department_name,
                category,
                delivery_time
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 4. 费用明细表格
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
                
                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
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
                timeline_table = self.format_timeline_table(timeline, task_list)
                
                # 处理签名图片
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理时间']
                modified_timeline_data.append(timeline_headers)
                
                for row in timeline_table:
                    processor_name = row[2]
                    # 通过姓名获取签名图片路径
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            # 移除处理意见列（第4列），保留：序号、节点名称、处理人、处理结果、处理时间
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:4] + row[5:])
                        except Exception as e:
                            print(f"签名图加载失败: {e}")
                            # 移除处理意见列（第4列）
                            modified_timeline_data.append(row[:4] + row[5:])
                    else:
                        # 移除处理意见列（第4列）
                        modified_timeline_data.append(row[:4] + row[5:])
                
                # 创建单个审批进程表格
                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 7.5 * cm])  # 总宽度19cm，移除处理意见列后调整列宽
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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
            
            # 自动发送并重命名
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename
            
        except Exception as e:
            print(f"生成采购申请PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def build_header_block_procurement(self):
        """公司信息表头 - 三方比价单版本"""
        font_name = self.get_available_font_name()
        # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
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

        # 创建公司信息表格：第一行两列仅放 Logo；文本各行合并两列，确保绝对居中
        company_data = [
            [logo_cell, ""],
            [Paragraph("上海硼矩新材料科技有限公司", sty_big), ""],
            [Paragraph("Shanghai BoronMatrix Advanced Materials Technology Co., Ltd", sty_sml), ""],
            [Paragraph("三方比价单", sty_big)]
        ]
        company_tbl = Table(company_data, colWidths=[1.6 * cm, 17.4 * cm], rowHeights=[0.8 * cm, 0.6 * cm, 0.6 * cm, 0.8 * cm])
        company_tbl.setStyle(TableStyle([
            # Logo 行保持左侧位置不变
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            # 公司名与副标题、单据名行合并两列并绝对居中
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('ALIGN', (0, 1), (1, 3), 'CENTER'),
            ('VALIGN', (0, 1), (1, 3), 'MIDDLE'),
            # 内边距与边框
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return company_tbl

    def build_procurement_requirement_table(self, form_data: Dict[str, Any], applicant_name: str, department_name: str) -> Table:
        """构建采购需求表格"""
        # 获取表单数据
        category = form_data.get('采购类别', '')
        material_description = form_data.get('物料描述/服务', '')  # 修正字段名
        procurement_requirement = form_data.get('请购理由', '')  # 修正字段名
        
        # 构建表格数据
        table_data = [
            [self.create_wrapped_text('采购需求表')],
            ['需求部门', department_name, '需求人员', applicant_name],
            ['采购类别', category, '物料描述/服务', material_description],
            ['请购理由', procurement_requirement, '', '']
        ]
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[3.0 * cm, 5.0 * cm, 3.0 * cm, 8.0 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (0, 1), colors.lightgrey),
            ('BACKGROUND', (2, 1), (2, 1), colors.lightgrey),
            ('BACKGROUND', (0, 2), (0, 2), colors.lightgrey),
            ('BACKGROUND', (2, 2), (2, 2), colors.lightgrey),
            ('BACKGROUND', (0, 3), (0, 3), colors.lightgrey),
            ('SPAN', (1, 3), (-1, 3)),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def build_three_way_comparison_table(self, form_data: Dict[str, Any]) -> Table:
        """构建三方比价表格"""
        headers = ['序号', '供应商名称', '规格型号', '价格', '备注']
        table_data = [[self.create_wrapped_text('三方比价表')], headers]
        
        # 从表单数据中获取三方比价信息
        three_way_comparison = form_data.get('三方比价', [])
        if three_way_comparison and isinstance(three_way_comparison, list):
            for idx, supplier_data in enumerate(three_way_comparison, 1):
                if isinstance(supplier_data, list):
                    # 处理fieldList格式的数据
                    supplier_name = ''
                    spec_model = ''
                    price = ''
                    
                    for item in supplier_data:
                        if isinstance(item, dict):
                            if item.get('name') == '供应商名称':
                                supplier_name = item.get('value', '')
                            elif item.get('name') == '规格型号':
                                spec_model = item.get('value', '')
                            elif item.get('name') == '价格':
                                price_value = item.get('value', '')
                                price_ext = item.get('ext', {})
                                currency = price_ext.get('currency', 'CNY')
                                if price_value:
                                    try:
                                        if currency == 'CNY':
                                            price = f"¥{int(price_value):,}"
                                        elif currency == 'USD':
                                            price = f"${int(price_value):,}"
                                        elif currency == 'EUR':
                                            price = f"€{int(price_value):,}"
                                        else:
                                            price = f"{currency} {int(price_value):,}"
                                    except:
                                        price = str(price_value)
                    
                    table_data.append([str(idx), supplier_name, spec_model, price, ''])
                elif isinstance(supplier_data, dict):
                    # 处理字典格式的数据
                    supplier_name = supplier_data.get('供应商名称', '')
                    spec_model = supplier_data.get('规格型号', '')
                    price_value = supplier_data.get('价格', '')
                    price_ext = supplier_data.get('价格_ext', {})
                    currency = price_ext.get('currency', 'CNY')
                    if price_value:
                        try:
                            if currency == 'CNY':
                                price = f"¥{int(price_value):,}"
                            elif currency == 'USD':
                                price = f"${int(price_value):,}"
                            elif currency == 'EUR':
                                price = f"€{int(price_value):,}"
                            else:
                                price = f"{currency} {int(price_value):,}"
                        except:
                            price = str(price_value)
                    else:
                        price = ''
                    
                    table_data.append([str(idx), supplier_name, spec_model, price, ''])
        else:
            # 如果没有数据，添加空行供填写
            for i in range(3):
                table_data.append([str(i+1), '', '', '', ''])
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[2.0 * cm, 4.0 * cm, 4.0 * cm, 3.0 * cm, 6.0 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, 1), 7),
            ('FONTSIZE', (0, 2), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def build_procurement_opinion_table(self, form_data: Dict[str, Any]) -> Table:
        """构建采购意见表格"""
        # 从表单数据中获取采购意见
        procurement_opinion = form_data.get('采购意见', '')
        
        # 构建表格数据
        table_data = [
            ['采购意见', procurement_opinion]
        ]
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[3.0 * cm, 16.0 * cm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def generate_three_way_comparison_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成三方比价审批PDF报告"""
        try:
            # 注册中文字体
            self.register_chinese_fonts()
            
            # 生成PDF文件名（使用新的命名规则和目录结构）
            output_filename = self._generate_pdf_filename("三方比价", approval_detail)
            
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []
            
            # 1. 公司信息表头
            story.append(self.build_header_block_procurement())
            story.append(Spacer(1, 5))
            
            # 2. 审批信息（审批编号和申请时间）
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))
            
            # 3. 采购需求表格
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            procurement_requirement_table = self.build_procurement_requirement_table(form_data, applicant_name, department_name)
            story.append(procurement_requirement_table)
            story.append(Spacer(1, 10))
            
            # 4. 三方比价表格
            three_way_comparison_table = self.build_three_way_comparison_table(form_data)
            story.append(three_way_comparison_table)
            story.append(Spacer(1, 10))
            
            # 5. 采购意见表格
            procurement_opinion_table = self.build_procurement_opinion_table(form_data)
            story.append(procurement_opinion_table)
            story.append(Spacer(1, 10))
            
            # 6. 审批进程表格
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                
                # 处理签名图片
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理意见', '处理时间']
                modified_timeline_data.append(timeline_headers)
                
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception as e:
                            print(f"签名图加载失败: {e}")
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)
                
                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)
            
            # 生成PDF
            doc.build(story)
            print(f"三方比价PDF报告已生成: {output_filename}")
            
            # 自动发送并重命名
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename
            
        except Exception as e:
            print(f"生成三方比价PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None


    def build_header_block_fixed_asset(self):
        """公司信息表头 - 固定资产验收版本"""
        font_name = self.get_available_font_name()
        # 公司信息样式 - 减少spaceBefore和spaceAfter，避免文字压在框线上
        sty_big = ParagraphStyle('HB1', fontName=font_name, fontSize=14, alignment=1, textColor=colors.black,
                                 spaceBefore=0, spaceAfter=0)
        sty_sml = ParagraphStyle('HB2', fontName=font_name, fontSize=8, alignment=1, textColor=colors.black,
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
            ["", Paragraph("固定资产验收单", sty_big)]  # 修改为固定资产验收单
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

    def build_approval_info_block_fixed_asset(self, serial: str, start_time: str, supplier: str):
        """审批编号、申请时间和供应商信息块 - 无框线"""
        font_name = self.get_available_font_name()
        sty = ParagraphStyle('AI', fontName=font_name, fontSize=9, textColor=colors.black)
        data = [[Paragraph(f"审批编号：{serial}", sty),
                 Paragraph(f"申请时间：{start_time}", sty),
                 Paragraph(f"供应商：{supplier}", sty)]]
        tbl = Table(data, colWidths=[6.0 * cm, 6.0 * cm, 7.0 * cm], rowHeights=[0.5 * cm])  # 三列布局
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # 减少内边距
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            # 移除BOX边框
        ]))
        return tbl

    def build_asset_info_table(self, asset_data: List[Dict[str, Any]]) -> Table:
        """构建资产信息表格（首行表名，列宽总计19cm）"""
        headers = ['序号', '资产编码', '名称', '规格型号', '数量/单位', '到货日期', '购置日期']
        table_data = [[self.create_wrapped_text('资产信息')], headers]
        
        for idx, asset in enumerate(asset_data, 1):
            # 格式化日期
            arrival_date = self.format_date_string(asset.get('到货日期', ''))
            purchase_date = self.format_date_string(asset.get('购置日期', ''))
            
            # 直接使用数量/单位字段
            quantity_unit = asset.get('数量/单位', '')
            
            table_data.append([
                str(idx),
                '',  # 资产编码 - 从数据中提取或留空
                asset.get('资产名称', ''),
                asset.get('规格型号', ''),
                quantity_unit,
                arrival_date,
                purchase_date
            ])
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[1.5 * cm, 2.0 * cm, 3.5 * cm, 3.5 * cm, 2.5 * cm, 3.0 * cm, 3.0 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, 1), 7),
            ('FONTSIZE', (0, 2), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def build_accessory_list_table(self) -> Table:
        """构建配件清单表格（首行表名，列宽总计19cm）"""
        headers = ['序号', '名称', '规格型号', '数量/单位', '备注']
        table_data = [[self.create_wrapped_text('配件清单')], headers]
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[1.5 * cm, 4.0 * cm, 3.0 * cm, 3.0 * cm, 7.5 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, 1), 7),
            ('FONTSIZE', (0, 2), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def build_acceptance_check_table(self, form_data: Dict[str, Any]) -> Table:
        """构建验收情况表格（首行表名，列宽总计19cm）"""
        # 左列：1.数量是否符合, 3.配件是否齐全, 5.功能测试结果
        # 右列：2.规格型号是否符合, 4.外观包装是否完好
        left_headers = ['1.数量是否符合', '3.配件是否齐全', '5.功能测试结果']
        right_headers = ['2.规格型号是否符合', '4.外观包装是否完好']
        
        # 获取表单数据
        quantity_match = form_data.get('1.数量是否符合', '')
        spec_match = form_data.get('2.规格型号是否符合', '')
        accessories_complete = form_data.get('3.配件是否齐全', '')
        appearance_ok = form_data.get('4.外观包装是否完好', '')
        function_test = form_data.get('5.功能测试结果', '')
        
        # 构建表格数据
        table_data = [[self.create_wrapped_text('验收情况（验收人填写）')]]
        max_rows = max(len(left_headers), len(right_headers))
        
        for i in range(max_rows):
            left_item = left_headers[i] if i < len(left_headers) else ''
            right_item = right_headers[i] if i < len(right_headers) else ''
            
            left_value = ''
            right_value = ''
            
            if i == 0:  # 1.数量是否符合
                left_value = quantity_match
            elif i == 1:  # 3.配件是否齐全
                left_value = accessories_complete
            elif i == 2:  # 5.功能测试结果
                left_value = function_test
                
            if i == 0:  # 2.规格型号是否符合
                right_value = spec_match
            elif i == 1:  # 4.外观包装是否完好
                right_value = appearance_ok
            
            table_data.append([left_item, left_value, right_item, right_value])
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[6.0 * cm, 3.5 * cm, 6.0 * cm, 3.5 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def build_acceptance_record_table(self, form_data: Dict[str, Any]) -> Table:
        """构建验收记录表格（首行表名，总宽19cm；前两行值独占一行，第三行人员与日期同一行）"""
        # 获取表单数据
        acceptance_result = form_data.get('验收结果', '')
        other_notes = form_data.get('其他情况说明', '')
        participants = form_data.get('参与验收人员', '')
        acceptance_date = form_data.get('验收日期', '')
        
        # 构建表格数据
        table_data = [[self.create_wrapped_text('验收记录（验收人填写）')],
            ['验收结果', acceptance_result, '', ''],
            ['其他情况说明', other_notes, '', ''],
            ['参与验收人员', participants, '验收日期', acceptance_date]
        ]
        
        tbl = Table(self.process_table_data_for_pdf(table_data),
                   colWidths=[3.0 * cm, 8.0 * cm, 3.0 * cm, 5.0 * cm])
        tbl.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (0, 2), colors.lightgrey),
            ('SPAN', (1, 1), (-1, 1)),
            ('SPAN', (1, 2), (-1, 2)),
            ('BACKGROUND', (0, 3), (0, 3), colors.lightgrey),
            ('BACKGROUND', (2, 3), (2, 3), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        return tbl

    def generate_fixed_asset_acceptance_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成固定资产验收审批PDF报告"""
        try:
            # 注册中文字体
            self.register_chinese_fonts()
            
            # 生成PDF文件名（使用新的命名规则和目录结构）
            output_filename = self._generate_pdf_filename("固定资产", approval_detail)
            
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []
            
            # 1. 公司信息表头
            story.append(self.build_header_block_fixed_asset())
            story.append(Spacer(1, 5))
            
            # 2. 审批信息（审批编号、申请时间、供应商）
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            supplier = form_data.get('供应商', '未知')
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            
            story.append(self.build_approval_info_block_fixed_asset(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted,
                supplier
            ))
            story.append(Spacer(1, 8))
            
            # 3. 资产信息表格
            if '资产信息' in form_data and form_data['资产信息']:
                asset_table = self.build_asset_info_table(form_data['资产信息'])
                story.append(asset_table)
                story.append(Spacer(1, 10))
            
            # 4. 配件清单表格
            accessory_table = self.build_accessory_list_table()
            story.append(accessory_table)
            story.append(Spacer(1, 10))
            
            # 5. 验收情况表格
            acceptance_check_table = self.build_acceptance_check_table(form_data)
            story.append(acceptance_check_table)
            story.append(Spacer(1, 10))
            
            # 6. 验收记录表格
            acceptance_record_table = self.build_acceptance_record_table(form_data)
            story.append(acceptance_record_table)
            story.append(Spacer(1, 10))
            
            # 7. 审批进程表格
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                
                # 处理签名图片
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理意见', '处理时间']
                modified_timeline_data.append(timeline_headers)
                
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception as e:
                            print(f"签名图加载失败: {e}")
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)
                
                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)
            
            # 生成PDF
            doc.build(story)
            print(f"固定资产验收PDF报告已生成: {output_filename}")
            
            # 自动发送并重命名
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename
            
        except Exception as e:
            print(f"生成固定资产验收PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_expense_reimbursement_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成费用报销审批PDF报告 - 采用与采购申请相同的模板风格"""
        try:
            # 注册中文字体
            self.register_chinese_fonts()
            
            # 生成PDF文件名（使用新的命名规则和目录结构）
            output_filename = self._generate_pdf_filename("费用报销", approval_detail)
            
            # 创建PDF文档 - 采用与采购申请相同的页面设置
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,  # 几乎顶格
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []
            
            # 获取样式
            styles = getSampleStyleSheet()
            
            # 1. 公司信息表头（修改为费用报销）
            story.append(self.build_header_block_expense())
            story.append(Spacer(1, 5))  # 减少间距
            
            # 2. 审批信息（审批编号和申请时间）
            # 实时获取申请人信息
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 3. 申请人信息表格
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            reimbursement_reason = form_data.get('报销事由', '未知')
            total_amount = form_data.get('费用汇总', '未知')
            
            story.append(self.build_applicant_info_block_expense(
                applicant_name,
                department_name,
                reimbursement_reason,
                total_amount
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 4. 费用明细表格
            expense_details = []
            if '费用明细' in form_data and form_data['费用明细']:
                # 从原始表单中获取汇总信息与币种
                summary_info = form_data.get('费用明细_summary', {})
                currency_code = summary_info.get('currency') or 'CNY'
                
                # 费用表格（若有币种，在列名中展示）
                amount_header = '金额' + (f"({currency_code})" if currency_code else '')
                detail_headers = ['序号', '报销类型', '日期', '内容', amount_header]
                detail_data = [detail_headers]
                
                # 行数据直接使用接口返回的金额
                calc_total_fallback = 0.0
                for idx, item in enumerate(form_data['费用明细'], 1):
                    amount_val = item.get('金额', '')
                    
                    # 尝试用于兜底统计
                    try:
                        calc_total_fallback += float(amount_val)
                    except Exception:
                        pass
                    
                    # 格式化日期
                    date_val = item.get('日期（年-月-日）', '')
                    date_val = self.format_date_string(date_val)
                    
                    detail_data.append([
                        str(idx), 
                        item.get('报销类型', ''), 
                        date_val,
                        item.get('内容', ''),
                        str(amount_val)
                    ])
                    expense_details.append(item)
                
                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
                                   colWidths=[1.5 * cm,  # 序号
                                              2.5 * cm,  # 报销类型
                                              2.5 * cm,  # 日期
                                              8.0 * cm,  # 内容
                                              4.5 * cm]  # 金额
                                   )  # 总宽度19cm
                
                detail_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
                    ('FONTSIZE', (0, 0), (-1, 0), 7),  # 进一步减少字体大小
                    ('FONTSIZE', (0, 1), (-1, -2), 6),  # 进一步减少字体大小
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
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
                timeline_table = self.format_timeline_table(timeline, task_list)
                
                # 处理签名图片
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果',  '处理意见','处理时间']
                modified_timeline_data.append(timeline_headers)
                
                for row in timeline_table:
                    processor_name = row[2]
                    # 通过姓名获取签名图片路径
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception as e:
                            print(f"签名图加载失败: {e}")
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)
                
                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])  # 总宽度19cm，与表头完全一致
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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
            print(f"费用报销PDF报告已生成: {output_filename}")
            
            # 自动发送并重命名
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename
            
        except Exception as e:
            print(f"生成费用报销PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_zhejiang_expense_reimbursement_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成浙江费用报销审批PDF报告（参考普通费用报销模板）"""
        try:
            self.register_chinese_fonts()

            output_filename = self._generate_pdf_filename("浙江费用报销", approval_detail)

            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []

            # 1. 浙江公司表头
            story.append(self.build_header_block_zhejiang_expense())
            story.append(Spacer(1, 5))

            # 2. 审批信息
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))

            # 3. 申请人信息
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            reimbursement_reason = form_data.get('报销事由', '未知')
            total_amount = form_data.get('费用汇总', '') or form_data.get('费用明细_summary', {}).get('total_amount', '')
            story.append(self.build_applicant_info_block_expense(
                applicant_name,
                department_name,
                reimbursement_reason,
                total_amount
            ))
            story.append(Spacer(1, 8))

            # 4. 费用明细
            if '费用明细' in form_data and form_data['费用明细']:
                summary_info = form_data.get('费用明细_summary', {})
                currency_code = summary_info.get('currency') or 'CNY'
                amount_header = '金额' + (f"({currency_code})" if currency_code else '')
                detail_headers = ['序号', '报销类型', '日期', '内容', amount_header]
                detail_data = [detail_headers]

                for idx, item in enumerate(form_data['费用明细'], 1):
                    date_val = self.format_date_string(item.get('日期（年-月-日）', ''))
                    detail_data.append([
                        str(idx),
                        item.get('报销类型', ''),
                        date_val,
                        item.get('内容', ''),
                        str(item.get('金额', ''))
                    ])

                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
                                   colWidths=[1.5 * cm, 2.5 * cm, 2.5 * cm, 8.0 * cm, 4.5 * cm])
                detail_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(detail_tbl)
                story.append(Spacer(1, 10))

            # 5. 审批进程
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果',  '处理意见','处理时间']
                modified_timeline_data.append(timeline_headers)
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception:
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)

                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)

            doc.build(story)
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename

        except Exception as e:
            print(f"生成浙江费用报销PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_zhiben_expense_reimbursement_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成知本费用报销审批PDF报告（参考浙江费用报销模板）"""
        try:
            self.register_chinese_fonts()

            output_filename = self._generate_pdf_filename("知本费用报销", approval_detail)

            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []

            # 1. 知本公司表头
            story.append(self.build_header_block_zhiben_expense())
            story.append(Spacer(1, 5))

            # 2. 审批信息
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))

            # 3. 申请人信息
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            reimbursement_reason = form_data.get('报销事由', '未知')
            total_amount = form_data.get('费用汇总', '') or form_data.get('费用明细_summary', {}).get('total_amount', '')
            story.append(self.build_applicant_info_block_expense(
                applicant_name,
                department_name,
                reimbursement_reason,
                total_amount
            ))
            story.append(Spacer(1, 8))

            # 4. 费用明细
            if '费用明细' in form_data and form_data['费用明细']:
                summary_info = form_data.get('费用明细_summary', {})
                currency_code = summary_info.get('currency') or 'CNY'
                amount_header = '金额' + (f"({currency_code})" if currency_code else '')
                detail_headers = ['序号', '报销类型', '日期', '内容', amount_header]
                detail_data = [detail_headers]

                for idx, item in enumerate(form_data['费用明细'], 1):
                    date_val = self.format_date_string(item.get('日期（年-月-日）', ''))
                    detail_data.append([
                        str(idx),
                        item.get('报销类型', ''),
                        date_val,
                        item.get('内容', ''),
                        str(item.get('金额', ''))
                    ])

                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
                                   colWidths=[1.5 * cm, 2.5 * cm, 2.5 * cm, 8.0 * cm, 4.5 * cm])
                detail_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(detail_tbl)
                story.append(Spacer(1, 10))

            # 5. 审批进程
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果',  '处理意见','处理时间']
                modified_timeline_data.append(timeline_headers)
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception:
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)

                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)

            doc.build(story)
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename

        except Exception as e:
            print(f"生成知本费用报销PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_zhiben_fixed_asset_acceptance_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """生成知本固定资产验收审批PDF报告（参考固定资产验收模板）"""
        try:
            self.register_chinese_fonts()

            output_filename = self._generate_pdf_filename("知本固定资产验收", approval_detail)

            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []

            # 1. 知本公司表头
            story.append(self.build_header_block_zhiben_fixed_asset())
            story.append(Spacer(1, 5))

            # 2. 审批信息（审批编号、申请时间、供应商）
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            supplier = form_data.get('供应商', '未知')
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            story.append(self.build_approval_info_block_fixed_asset(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted,
                supplier
            ))
            story.append(Spacer(1, 8))

            # 3. 资产信息表格
            if '资产信息' in form_data and form_data['资产信息']:
                asset_table = self.build_asset_info_table(form_data['资产信息'])
                story.append(asset_table)
                story.append(Spacer(1, 10))

            # 4. 配件清单表格
            accessory_table = self.build_accessory_list_table()
            story.append(accessory_table)
            story.append(Spacer(1, 10))

            # 5. 验收情况表格
            acceptance_check_table = self.build_acceptance_check_table(form_data)
            story.append(acceptance_check_table)
            story.append(Spacer(1, 10))

            # 6. 验收记录表格
            acceptance_record_table = self.build_acceptance_record_table(form_data)
            story.append(acceptance_record_table)
            story.append(Spacer(1, 10))

            # 7. 审批进程表格
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理意见', '处理时间']
                modified_timeline_data.append(timeline_headers)
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:])
                        except Exception:
                            modified_timeline_data.append(row)
                    else:
                        modified_timeline_data.append(row)

                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 3.5 * cm, 4.0 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)

            doc.build(story)
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename

        except Exception as e:
            print(f"生成知本固定资产验收PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_zhiben_procurement_approval_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """为知本采购申请审批实例生成PDF报告（参考浙江采购申请模板）"""
        try:
            self.register_chinese_fonts()

            output_filename = self._generate_pdf_filename("知本采购申请", approval_detail)

            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []

            # 1. 知本公司表头
            story.append(self.build_header_block_zhiben())
            story.append(Spacer(1, 5))

            # 2. 审批信息
            applicant_info = self.employee_manager.get_employee_info_realtime(approval_detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(approval_detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(approval_detail.get('start_time', ''))
            story.append(self.build_approval_info_block(
                approval_detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))

            # 3. 申请人信息
            form_data = self.parse_form_data(approval_detail.get('form', '[]'))
            category = form_data.get('采购类别', '未知')
            delivery_time = form_data.get('期望交货时间', '').split('T')[0] if 'T' in form_data.get('期望交货时间', '') else '未知'
            story.append(self.build_applicant_info_block(
                applicant_name,
                department_name,
                category,
                delivery_time
            ))
            story.append(Spacer(1, 8))

            # 4. 费用明细
            if '费用明细' in form_data and form_data['费用明细']:
                summary_info = form_data.get('费用明细_summary', {})

                price_key = '单价(元)'
                unit_name = '元'
                try:
                    first_row = form_data['费用明细'][0]
                    for k in first_row.keys():
                        if isinstance(k, str) and k.startswith('单价(') and k.endswith(')'):
                            price_key = k
                            unit_name = k[k.find('(')+1:k.rfind(')')].strip() or '元'
                            break
                except Exception:
                    pass

                detail_headers = ['序号', '名称', '规格型号', f'单价({unit_name})', '数量', '单位', '金额', '请购理由', '备注']
                detail_data = [detail_headers]

                calc_total_fallback = 0.0
                for idx, item in enumerate(form_data['费用明细'], 1):
                    q_val = item.get('数量', '')
                    p_val = item.get(price_key, '')
                    t_val = item.get('金额', '')

                    try:
                        calc_total_fallback += float(t_val)
                    except Exception:
                        pass

                    detail_data.append([
                        str(idx),
                        item.get('名称', ''),
                        item.get('规格型号', ''),
                        str(p_val),
                        str(q_val),
                        item.get('单位', ''),
                        str(t_val),
                        item.get('请购理由', ''),
                        item.get('备注', '')
                    ])

                total_amount_display = None
                if summary_info.get('total_amount'):
                    try:
                        total_amount_display = f"{float(summary_info.get('total_amount')):.2f}"
                    except:
                        total_amount_display = f"{calc_total_fallback:.2f}"
                elif isinstance(calc_total_fallback, (int, float)) and calc_total_fallback > 0:
                    total_amount_display = f"{calc_total_fallback:.2f}"
                else:
                    total_amount_display = "0.00"

                detail_data.append(['总金额', '', '', '', '', '', total_amount_display, '', ''])

                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
                                   colWidths=[1.0 * cm, 2.5 * cm, 2.5 * cm, 1.5 * cm, 1.0 * cm, 1.0 * cm, 1.5 * cm, 3.5 * cm, 4.5 * cm])

                detail_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -2), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BACKGROUND', (0, -1), (5, -1), colors.lightgrey),
                    ('SPAN', (0, -1), (5, -1)),
                    ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.black),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(detail_tbl)
                story.append(Spacer(1, 10))

            # 5. 审批进程
            timeline = approval_detail.get("timeline", [])
            task_list = approval_detail.get("task_list", [])
            if timeline:
                timeline_table = self.format_timeline_table(timeline, task_list)
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理时间']
                modified_timeline_data.append(timeline_headers)
                for row in timeline_table:
                    processor_name = row[2]
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:4] + row[5:])
                        except Exception:
                            modified_timeline_data.append(row[:4] + row[5:])
                    else:
                        modified_timeline_data.append(row[:4] + row[5:])

                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 7.5 * cm])
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 2),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(timeline_tbl)

            doc.build(story)
            final_filename = self._send_and_rename_pdf(output_filename, approval_detail.get('open_id', ''))
            return final_filename

        except Exception as e:
            print(f"生成知本采购申请PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_zhejiang_procurement_approval_pdf(self, approval_detail: Dict[str, Any]) -> str:
        """为浙江采购申请审批实例生成PDF报告"""
        try:
            # 兼容顶层或 data 嵌套结构
            detail = approval_detail.get('data', approval_detail)
            
            # 注册中文字体
            self.register_chinese_fonts()
            
            # 生成PDF文件名（使用新的命名规则和目录结构）
            output_filename = self._generate_pdf_filename("浙江采购申请", detail)
            
            # 创建PDF文档 - 采用generate_pdf_report的页面设置
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                topMargin=0.5 * cm,  # 几乎顶格
                rightMargin=1 * cm,
                bottomMargin=1 * cm,
                leftMargin=1 * cm
            )
            story = []
            
            # 获取样式
            styles = getSampleStyleSheet()
            
            # 1. 公司信息表头（浙江版本）
            story.append(self.build_header_block_zhejiang())
            story.append(Spacer(1, 5))  # 减少间距
            
            # 2. 审批信息（审批编号和申请时间）
            # 实时获取申请人信息
            applicant_info = self.employee_manager.get_employee_info_realtime(detail.get('open_id', ''))
            applicant_name = applicant_info["name"]
            department_name = self.feishu_api.get_department_name(detail.get('department_id', ''))
            start_time_formatted = self.format_time_without_timezone(detail.get('start_time', ''))
            
            story.append(self.build_approval_info_block(
                detail.get('serial_number', 'N/A'),
                start_time_formatted
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 3. 申请人信息表格
            form_data = self.parse_form_data(detail.get('form', '[]'))
            category = form_data.get('采购类别', '未知')
            delivery_time = form_data.get('期望交货时间', '').split('T')[0] if 'T' in form_data.get('期望交货时间', '') else '未知'
            
            story.append(self.build_applicant_info_block(
                applicant_name,
                department_name,
                category,
                delivery_time
            ))
            story.append(Spacer(1, 8))  # 减少间距
            
            # 4. 费用明细表格（浙江版本 - 简化列）
            if '费用明细' in form_data and form_data['费用明细']:
                # 从原始表单中获取汇总信息
                summary_info = form_data.get('费用明细_summary', {})
                
                # 动态解析单价字段名与单位（如 单价(元)、单价(USD) 等）
                price_key = '单价(元)'
                unit_name = '元'
                try:
                    first_row = form_data['费用明细'][0]
                    # 查找以 "单价(" 开头并以 ")" 结尾的字段名
                    for k in first_row.keys():
                        if isinstance(k, str) and k.startswith('单价(') and k.endswith(')'):
                            price_key = k
                            unit_name = k[k.find('(')+1:k.rfind(')')].strip() or '元'
                            break
                except Exception:
                    pass
                
                # 浙江采购申请表格列：序号、名称、规格型号、单价(元)、数量、单位、金额、请购理由、备注
                detail_headers = ['序号', '名称', '规格型号', f'单价({unit_name})', '数量', '单位', '金额', '请购理由', '备注']
                detail_data = [detail_headers]
                
                # 行数据直接使用接口返回的"单价"、"金额"，不再自行计算
                calc_total_fallback = 0.0
                for idx, item in enumerate(form_data['费用明细'], 1):
                    q_val = item.get('数量', '')
                    p_val = item.get(price_key, '')
                    t_val = item.get('金额', '')
                    
                    # 尝试用于兜底统计
                    try:
                        calc_total_fallback += float(t_val)
                    except Exception:
                        pass
                    
                    detail_data.append([
                        str(idx), 
                        item.get('名称', ''), 
                        item.get('规格型号', ''),
                        str(p_val), 
                        str(q_val), 
                        item.get('单位', ''), 
                        str(t_val),
                        item.get('请购理由', ''), 
                        item.get('备注', '')
                    ])
                
                # 总金额优先从summary_info获取，其次用行金额求和兜底
                total_amount_display = None
                if summary_info.get('total_amount'):
                    try:
                        total_amount_display = f"{float(summary_info.get('total_amount')):.2f}"
                    except:
                        total_amount_display = f"{calc_total_fallback:.2f}"
                elif isinstance(calc_total_fallback, (int, float)) and calc_total_fallback > 0:
                    total_amount_display = f"{calc_total_fallback:.2f}"
                else:
                    total_amount_display = "0.00"
                
                detail_data.append(['总金额', '', '', '', '', '', total_amount_display, '', ''])
                
                detail_tbl = Table(self.process_table_data_for_pdf(detail_data),
                                   colWidths=[1.0 * cm,  # 序号
                                              2.5 * cm,  # 名称
                                              2.5 * cm,  # 规格型号
                                              1.5 * cm,  # 单价
                                              1.0 * cm,  # 数量
                                              1.0 * cm,  # 单位
                                              1.5 * cm,  # 金额
                                              3.5 * cm,  # 请购理由
                                              4.5 * cm]  # 备注
                                   )  # 调整列宽，总宽度19cm
                
                detail_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
                    ('FONTSIZE', (0, 0), (-1, 0), 7),  # 进一步减少字体大小
                    ('FONTSIZE', (0, 1), (-1, -2), 6),  # 进一步减少字体大小
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BACKGROUND', (0, -1), (5, -1), colors.lightgrey),
                    ('SPAN', (0, -1), (5, -1)),
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
            timeline = detail.get("timeline", [])
            task_list = detail.get("task_list", [])
            if timeline:
                # 格式化审批进程表格
                timeline_table = self.format_timeline_table(timeline, task_list)
                
                # 处理签名图片
                modified_timeline_data = []
                timeline_headers = ['序号', '节点名称', '处理人', '处理结果', '处理时间']
                modified_timeline_data.append(timeline_headers)
                
                for row in timeline_table:
                    processor_name = row[2]
                    # 通过姓名获取签名图片路径
                    signature_path = self.employee_manager.get_signature_image_path(processor_name)
                    
                    if signature_path:
                        try:
                            signature_img = Image(signature_path, width=36, height=15)
                            # 移除处理意见列（第4列），保留：序号、节点名称、处理人、处理结果、处理时间
                            modified_timeline_data.append(row[:2] + [signature_img] + row[3:4] + row[5:])
                        except Exception as e:
                            print(f"签名图加载失败: {e}")
                            # 移除处理意见列（第4列）
                            modified_timeline_data.append(row[:4] + row[5:])
                    else:
                        # 移除处理意见列（第4列）
                        modified_timeline_data.append(row[:4] + row[5:])
                
                # 创建单个审批进程表格
                timeline_tbl = Table(self.process_table_data_for_pdf(modified_timeline_data),
                                     colWidths=[2.0 * cm, 3.0 * cm, 3.5 * cm, 3.0 * cm, 7.5 * cm])  # 总宽度19cm，移除处理意见列后调整列宽
                timeline_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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
            print(f"浙江采购申请PDF报告已生成: {output_filename}")
            
            # 自动发送并重命名
            final_filename = self._send_and_rename_pdf(output_filename, detail.get('open_id', ''))
            return final_filename
            
        except Exception as e:
            print(f"生成浙江采购申请PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None
