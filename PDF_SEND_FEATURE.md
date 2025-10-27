# PDF发送功能使用说明

## 功能概述

系统已从自动打印PDF改为通过飞书机器人自动发送PDF给发起人。当审批通过时，系统会：

1. 生成PDF报告
2. 通过飞书机器人发送PDF给发起人
3. 重命名PDF文件添加"_已发送"标识

## 主要变更

### 1. 新增PDF发送模块 (`pdf_sender.py`)

- `PDFSender` 类：负责PDF文件的上传和发送
- 支持获取tenant_access_token
- 支持文件上传到飞书服务器
- 支持向指定用户发送文件消息

### 2. 修改PDF生成器 (`pdf_generator.py`)

- 将 `auto_print` 参数改为 `auto_send`
- 移除 `AutoPrinter` 依赖，新增 `PDFSender` 依赖
- 将 `_print_and_rename_pdf()` 方法改为 `_send_and_rename_pdf()`
- 将 `_add_printed_suffix()` 方法改为 `_add_sent_suffix()`
- 所有PDF生成方法现在都会自动发送给发起人

### 3. 更新实时PDF生成器

- `realtime_pdf_generator.py` 和 `realtime_pdf_generator_v2.py` 都已更新
- 初始化时启用 `auto_send=True`

## 使用方法

### 环境变量配置

```bash
export APP_ID="your_app_id"
export APP_SECRET="your_app_secret"
export OPEN_ID="target_user_open_id"  # 可选，用于测试
```

### 直接使用PDF发送器

```python
from pdf_sender import PDFSender

# 创建发送器
sender = PDFSender(app_id, app_secret)

# 发送PDF给用户
success, message = sender.send_pdf_to_user("path/to/file.pdf", "user_open_id")
if success:
    print(f"发送成功: {message}")
else:
    print(f"发送失败: {message}")
```

### 使用PDF生成器（自动发送）

```python
from pdf_generator import PDFGenerator
from feishu_api import FeishuAPI
from employee_manager import EmployeeManager

# 初始化
feishu_api = FeishuAPI(app_id, app_secret)
employee_manager = EmployeeManager(feishu_api, employee_base_url)
pdf_generator = PDFGenerator(feishu_api, employee_manager, auto_send=True)

# 生成PDF（会自动发送给发起人）
pdf_path = pdf_generator.generate_procurement_approval_pdf(approval_detail)
```

## 测试

### 运行测试脚本

```bash
# 设置环境变量
export APP_ID="your_app_id"
export APP_SECRET="your_app_secret"
export OPEN_ID="your_open_id"

# 运行测试
python test_pdf_sender.py
```

### 测试功能

测试脚本会：
1. 自动查找一个未发送的PDF文件
2. 尝试发送给指定的用户
3. 显示发送结果

## 文件命名规则

- 原始PDF: `张三_20250101_120000.pdf`
- 发送后: `张三_20250101_120000_已发送.pdf`

## 错误处理

- 如果发送失败，PDF文件不会被重命名
- 所有错误都会记录到日志中
- 发送失败不会影响PDF生成过程

## 注意事项

1. 确保飞书应用有发送消息的权限
2. 确保目标用户已添加机器人好友
3. 文件大小限制：飞书单文件最大100MB
4. 发送频率限制：避免过于频繁的发送请求

## 兼容性

- 保持与现有审批流程的完全兼容
- 所有现有的PDF生成功能保持不变
- 只是将打印改为发送，其他逻辑不变
