#!/usr/bin/env python3
"""
跨平台自动打印模块
支持 macOS、Ubuntu 和 Windows 系统的 PDF 自动打印
"""
import os
import sys
import subprocess
import logging
import time
from typing import Optional, Tuple
from pathlib import Path


class AutoPrinter:
    """跨平台自动打印器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platform = self._detect_platform()
        self.logger.info(f"检测到操作系统: {self.platform}")
    
    def _detect_platform(self) -> str:
        """检测操作系统平台"""
        if sys.platform == "darwin":
            return "macos"
        elif sys.platform.startswith("linux"):
            return "linux"
        elif sys.platform.startswith("win"):
            return "windows"
        else:
            return "unknown"
    
    def print_pdf(self, pdf_path: str, printer_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        打印PDF文件
        
        Args:
            pdf_path: PDF文件路径
            printer_name: 打印机名称（可选，默认使用系统默认打印机）
            
        Returns:
            (成功标志, 错误信息)
        """
        if not os.path.exists(pdf_path):
            return False, f"PDF文件不存在: {pdf_path}"
        
        try:
            if self.platform == "macos":
                return self._print_macos(pdf_path, printer_name)
            elif self.platform == "linux":
                return self._print_linux(pdf_path, printer_name)
            elif self.platform == "windows":
                return self._print_windows(pdf_path, printer_name)
            else:
                return False, f"不支持的操作系统: {sys.platform}"
                
        except Exception as e:
            self.logger.error(f"打印PDF时发生异常: {e}")
            return False, str(e)
    
    def _print_macos(self, pdf_path: str, printer_name: Optional[str] = None) -> Tuple[bool, str]:
        """macOS系统打印"""
        try:
            # 使用lpr命令打印
            cmd = ["lpr"]
            
            if printer_name:
                cmd.extend(["-P", printer_name])
            
            cmd.append(pdf_path)
            
            self.logger.info(f"执行打印命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.logger.info(f"PDF打印成功: {pdf_path}")
                return True, "打印成功"
            else:
                error_msg = f"打印失败: {result.stderr}"
                self.logger.error(error_msg)
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "打印超时"
        except Exception as e:
            return False, f"macOS打印异常: {e}"
    
    def _print_linux(self, pdf_path: str, printer_name: Optional[str] = None) -> Tuple[bool, str]:
        """Linux系统打印"""
        try:
            # 使用lp命令打印
            cmd = ["lp"]
            
            if printer_name:
                cmd.extend(["-d", printer_name])
            
            cmd.append(pdf_path)
            
            self.logger.info(f"执行打印命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.logger.info(f"PDF打印成功: {pdf_path}")
                return True, "打印成功"
            else:
                error_msg = f"打印失败: {result.stderr}"
                self.logger.error(error_msg)
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "打印超时"
        except Exception as e:
            return False, f"Linux打印异常: {e}"
    
    def _print_windows(self, pdf_path: str, printer_name: Optional[str] = None) -> Tuple[bool, str]:
        """Windows系统打印"""
        try:
            # 使用Windows的默认PDF查看器打印
            # 这里使用PowerShell命令来打印
            if printer_name:
                # 如果有指定打印机，使用PowerShell的Start-Process命令
                ps_cmd = f'Start-Process -FilePath "{pdf_path}" -Verb Print -ArgumentList "-printer", "{printer_name}"'
            else:
                # 使用默认打印机
                ps_cmd = f'Start-Process -FilePath "{pdf_path}" -Verb Print'
            
            cmd = ["powershell", "-Command", ps_cmd]
            
            self.logger.info(f"执行打印命令: {ps_cmd}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.logger.info(f"PDF打印成功: {pdf_path}")
                return True, "打印成功"
            else:
                error_msg = f"打印失败: {result.stderr}"
                self.logger.error(error_msg)
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "打印超时"
        except Exception as e:
            return False, f"Windows打印异常: {e}"
    
    def get_available_printers(self) -> list:
        """获取可用的打印机列表"""
        try:
            if self.platform == "macos":
                return self._get_macos_printers()
            elif self.platform == "linux":
                return self._get_linux_printers()
            elif self.platform == "windows":
                return self._get_windows_printers()
            else:
                return []
        except Exception as e:
            self.logger.error(f"获取打印机列表失败: {e}")
            return []
    
    def _get_macos_printers(self) -> list:
        """获取macOS打印机列表"""
        try:
            result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                printers = []
                for line in result.stdout.split('\n'):
                    # 支持中英文格式
                    if line.startswith('printer ') or line.startswith('打印机'):
                        # 提取打印机名称
                        if line.startswith('printer '):
                            printer_name = line.split()[1]
                        else:  # 中文格式 "打印机Canon_iR_C3222L闲置..."
                            # 提取 "打印机" 后面的部分，直到遇到空格或中文字符
                            import re
                            match = re.search(r'打印机([^\s\u4e00-\u9fff]+)', line)
                            if match:
                                printer_name = match.group(1)
                            else:
                                continue
                        printers.append(printer_name)
                return printers
            return []
        except Exception:
            return []
    
    def _get_linux_printers(self) -> list:
        """获取Linux打印机列表"""
        try:
            result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                printers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('printer '):
                        printer_name = line.split()[1]
                        printers.append(printer_name)
                return printers
            return []
        except Exception:
            return []
    
    def _get_windows_printers(self) -> list:
        """获取Windows打印机列表"""
        try:
            # 使用PowerShell获取打印机列表
            ps_cmd = "Get-Printer | Select-Object Name | ForEach-Object { $_.Name }"
            result = subprocess.run(["powershell", "-Command", ps_cmd], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                printers = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                return printers
            return []
        except Exception:
            return []
    
    def wait_for_print_completion(self, timeout: int = 60) -> bool:
        """
        等待打印完成
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            是否在超时前完成
        """
        # 这里可以实现更复杂的打印状态检查
        # 目前使用简单的等待机制
        time.sleep(2)  # 等待2秒让打印开始
        return True


def test_auto_printer():
    """测试自动打印功能"""
    printer = AutoPrinter()
    
    print(f"检测到操作系统: {printer.platform}")
    
    # 获取可用打印机
    printers = printer.get_available_printers()
    print(f"可用打印机: {printers}")
    
    # 测试打印（需要提供一个测试PDF文件）
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        success, message = printer.print_pdf(test_pdf)
        print(f"打印结果: {success}, {message}")
    else:
        print("未找到测试PDF文件")


if __name__ == "__main__":
    test_auto_printer()
