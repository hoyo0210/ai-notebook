#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 检查是否提供了应用参数
if [ $# -eq 0 ]; then
    echo "请指定要运行的应用："
    echo "1. 情感分析: ./start_app.sh sentiment"
    echo "2. 天气查询: ./start_app.sh weather"
    echo "3. 表格提取: ./start_app.sh table"
    echo "4. 文章摘要: ./start_app.sh summary"
    echo "5. 运维事件: ./start_app.sh ops"
    echo "6. AI客服: ./start_app.sh customer"
    echo "7. 保险欺诈: ./start_app.sh fraud"
    echo ""
    echo "示例: ./start_app.sh sentiment"
    exit 1
fi

# 根据参数启动对应的应用
case $1 in
    "sentiment")
        echo "启动情感分析应用..."
        streamlit run case1_sentiment_analysis/app.py
        ;;
    "weather")
        echo "启动天气查询应用..."
        streamlit run case2_weather/app.py
        ;;
    "table")
        echo "启动表格提取应用..."
        streamlit run case3_table_extraction/app.py
        ;;
    "summary")
        echo "启动文章摘要应用..."
        streamlit run case4_article_summary/app.py
        ;;
    "ops")
        echo "启动运维事件应用..."
        streamlit run case5_ops_incident/app.py
        ;;
    "customer")
        echo "启动AI客服应用..."
        streamlit run case6_ai_customer_service/app.py
        ;;
    "fraud")
        echo "启动保险欺诈检测应用..."
        streamlit run case7_insurance_fraud/app.py
        ;;
    *)
        echo "未知的应用类型: $1"
        echo "请使用: sentiment, weather, table, summary, ops, customer, fraud"
        exit 1
        ;;
esac 