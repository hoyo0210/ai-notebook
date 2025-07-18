# CASE 4: 文章摘要

## 案例描述
使用阿里云百炼大模型API对长篇文章进行智能总结，提取关键信息和核心观点。

## 应用场景
- 新闻摘要生成
- 学术论文总结
- 会议纪要整理
- 文档快速浏览

## 功能特性
- 智能文章总结
- 多风格输出（学术、通俗、新闻、技术）
- 关键点提取
- 文章分析
- URL文章抓取
- 文件上传支持
- 自定义摘要长度

## 技术要点
- 文本长度处理
- 关键信息提取
- 多层级总结
- 摘要质量控制
- 网页内容抓取
- 多格式文档处理

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
cd .. && ./start_app.sh summary

# 方法2：手动启动
source ../venv/bin/activate
streamlit run app.py
```

## 使用说明
1. 在侧边栏输入阿里云百炼API Key
2. 选择模型（qwen-turbo、qwen-plus、qwen-max）
3. 选择输入方式：
   - URL输入：输入文章网址
   - 文件上传：上传文本文件
4. 选择摘要风格（学术、通俗、新闻、技术）
5. 设置摘要长度
6. 点击"生成摘要"按钮
7. 查看摘要结果和关键点

## 支持的文件格式
- 文本文件：TXT、MD、DOC、DOCX
- 网页URL：支持大部分新闻和文章网站

## 文件结构
- `app.py`: 主程序文件（Streamlit应用）
- `README.md`: 说明文档

## 访问地址
启动后访问：http://localhost:8501 