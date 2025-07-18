# CASE 1: 情感分析

## 案例描述
使用阿里云百炼大模型API进行文本情感分析，判断文本的情感倾向（正面、负面、中性）。

## 应用场景
- 社交媒体评论分析
- 客户反馈情感分析
- 产品评价分析
- 舆情监控

## 功能特性
- 文本情感分析
- 关键词提取
- 置信度评估
- 历史记录查看
- 批量文本处理

## 技术要点
- 文本预处理
- 情感分类模型调用
- 结果解析与展示
- Streamlit Web界面

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
cd .. && ./start_app.sh sentiment

# 方法2：手动启动
source ../venv/bin/activate
streamlit run app.py
```

## 使用说明
1. 在侧边栏输入阿里云百炼API Key
2. 选择模型（qwen-turbo、qwen-plus、qwen-max）
3. 输入要分析的文本
4. 点击"分析情感"按钮
5. 查看分析结果和置信度

## 文件结构
- `app.py`: 主程序文件（Streamlit应用）
- `README.md`: 说明文档

## 访问地址
启动后访问：http://localhost:8501 