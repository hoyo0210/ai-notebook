#!/bin/bash

# Section 2: DeepSeek使用与Prompt工程 启动脚本

echo "=== Section 2: DeepSeek使用与Prompt工程 ==="
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

echo ""
echo "=== 可用的案例应用 ==="
echo "1. DeepSeek 基础使用"
echo "2. Prompt 工程实践"
echo "3. 高级 Prompt 技巧"
echo "4. Prompt 优化与调试"
echo "5. 实际应用案例"
echo ""

# 检查是否有环境变量文件
if [ ! -f ".env" ]; then
    echo "提示: 请创建 .env 文件并配置 DeepSeek API 密钥"
    echo "示例:"
    echo "DEEPSEEK_API_KEY=your_api_key_here"
    echo ""
fi

echo "启动方式:"
echo "- 运行特定案例: python case1_deepseek_basics/app.py"
echo "- 使用 Streamlit: streamlit run case1_deepseek_basics/app.py"
echo ""

echo "环境准备完成！"
echo "请选择要运行的案例应用。" 