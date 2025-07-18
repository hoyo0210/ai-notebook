#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 创建虚拟环境失败"
        exit 1
    fi
    echo "✅ 虚拟环境创建成功"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查是否成功激活虚拟环境
if [ $? -ne 0 ]; then
    echo "❌ 虚拟环境激活失败"
    exit 1
fi

# 检查streamlit是否安装
if ! command -v streamlit &> /dev/null; then
    echo "📦 正在安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败"
        exit 1
    fi
    echo "✅ 依赖包安装成功"
fi

# 检查端口是否被占用，如果被占用则选择其他端口
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 1  # 端口被占用
    else
        return 0  # 端口可用
    fi
}

# 自动选择可用端口
PORT=8501
while ! check_port $PORT; do
    echo "⚠️  端口 $PORT 已被占用，尝试端口 $((PORT+1))"
    PORT=$((PORT+1))
    if [ $PORT -gt 8510 ]; then
        echo "❌ 无法找到可用端口"
        exit 1
    fi
done

# 定义应用列表
APPS_1="sentiment:情感分析"
APPS_2="weather:天气查询"
APPS_3="table:表格提取"
APPS_4="summary:文章摘要"
APPS_5="ops:运维事件"
APPS_6="customer:AI客服"
APPS_7="fraud:保险欺诈检测"

# 检查是否提供了应用参数
if [ $# -eq 0 ]; then
    echo ""
    echo "🚀 AI应用启动器"
    echo "=================="
    echo "请选择要启动的应用："
    echo ""
    
    for i in {1..7}; do
        app_var="APPS_$i"
        IFS=':' read -r app_name app_desc <<< "${!app_var}"
        echo "$i. $app_desc"
    done
    
    echo ""
    echo "输入数字选择应用，或直接输入应用名称："
    echo "示例: 1 或 sentiment"
    echo ""
    read -p "请选择: " choice
    
    # 如果输入的是数字，转换为应用名称
    if [[ "$choice" =~ ^[1-7]$ ]]; then
        app_var="APPS_$choice"
        IFS=':' read -r app_name app_desc <<< "${!app_var}"
        choice="$app_name"
    fi
else
    choice="$1"
fi

# 根据选择启动对应的应用
case $choice in
    "sentiment")
        echo "🎯 启动情感分析应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case1_sentiment_analysis/app.py --server.port $PORT
        ;;
    "weather")
        echo "🌤️  启动天气查询应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case2_weather/app.py --server.port $PORT
        ;;
    "table")
        echo "📊 启动表格提取应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case3_table_extraction/app.py --server.port $PORT
        ;;
    "summary")
        echo "📝 启动文章摘要应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case4_article_summary/app.py --server.port $PORT
        ;;
    "ops")
        echo "🔧 启动运维事件应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case5_ops_incident/app.py --server.port $PORT
        ;;
    "customer")
        echo "🤖 启动AI客服应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case6_ai_customer_service/app.py --server.port $PORT
        ;;
    "fraud")
        echo "🛡️  启动保险欺诈检测应用..."
        echo "📍 应用地址: http://localhost:$PORT"
        echo "⏹️  按 Ctrl+C 停止应用"
        echo ""
        streamlit run case7_insurance_fraud/app.py --server.port $PORT
        ;;
    *)
        echo "❌ 未知的应用类型: $choice"
        echo "可用的应用: sentiment, weather, table, summary, ops, customer, fraud"
        exit 1
        ;;
esac 