#!/usr/bin/env python3
"""
日志配置工具
用于控制应用程序的日志输出级别
"""

import logging
import sys
import os

# 禁用SSL证书验证警告（用于腾讯云等环境）
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置环境变量，允许不验证SSL证书（可选）
# 如果系统环境变量已设置，则使用它
if 'SSL_VERIFY' not in os.environ:
    os.environ['SSL_VERIFY'] = 'False'


def setup_logging(level=logging.INFO, show_debug=False):
    """
    设置日志配置
    
    Args:
        level: 日志级别 (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)
        show_debug: 是否显示DEBUG级别的日志
    """
    if show_debug:
        level = logging.DEBUG
    
    # 配置根日志器
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 设置第三方库的日志级别
    logging.getLogger('lark_oapi').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    print(f"日志级别设置为: {logging.getLevelName(level)}")


def set_quiet_mode():
    """设置为静默模式，只显示错误和警告"""
    setup_logging(level=logging.WARNING)


def set_verbose_mode():
    """设置为详细模式，显示所有日志"""
    setup_logging(level=logging.DEBUG, show_debug=True)


def set_normal_mode():
    """设置为正常模式，显示INFO及以上级别"""
    setup_logging(level=logging.INFO)


if __name__ == "__main__":
    print("日志配置工具")
    print("1. 静默模式 (只显示错误和警告)")
    print("2. 正常模式 (显示INFO及以上级别)")
    print("3. 详细模式 (显示所有日志)")
    
    choice = input("请选择模式 (1-3): ").strip()
    
    if choice == "1":
        set_quiet_mode()
    elif choice == "2":
        set_normal_mode()
    elif choice == "3":
        set_verbose_mode()
    else:
        print("无效选择，使用默认正常模式")
        set_normal_mode()






