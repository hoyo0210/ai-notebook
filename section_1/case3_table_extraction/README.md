# CASE 3: 表格提取

## 案例描述
使用阿里云百炼大模型API从文本或图像中提取表格数据，并进行结构化处理。

## 应用场景
- 文档数字化处理
- 财务报表分析
- 学术论文数据提取
- 报告自动化处理

## 功能特性
- 文本表格提取
- 图片表格识别
- 多格式输出（CSV、JSON、Excel、Markdown）
- 结果下载
- 表格结构分析
- 数据清洗和格式化

## 技术要点
- 表格识别与定位
- 数据提取与清洗
- 结构化输出
- 多格式支持（CSV、JSON、Excel、Markdown）
- OCR图像识别
- 表格结构分析

## 环境配置
```bash
# 安装依赖
pip install -r ../requirements.txt

# 配置环境变量
export DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

## 运行方式
```bash
# 方法1：使用启动脚本（推荐）
cd .. && ./start_app.sh table

# 方法2：手动启动
source ../venv/bin/activate
streamlit run app.py
```

## 使用说明
1. 在侧边栏输入阿里云百炼API Key
2. 选择模型（qwen-turbo、qwen-plus、qwen-max）
3. 选择输入方式：
   - 文本输入：直接粘贴包含表格的文本
   - 文件上传：上传包含表格的图片文件
4. 选择输出格式（CSV、JSON、Excel、Markdown）
5. 点击"提取表格"按钮
6. 查看提取结果并下载

## 支持的文件格式
- 图片格式：JPG、PNG、GIF、BMP
- 输出格式：CSV、JSON、Excel、Markdown

## 文件结构
- `app.py`: 主程序文件（Streamlit应用）
- `README.md`: 说明文档

## 访问地址
启动后访问：http://localhost:8501 