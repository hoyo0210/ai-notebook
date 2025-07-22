"""
Section 3: Cursor AI应用开发示例
基于前面学到的AI理论和技术开发的完整应用
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="AI应用开发示例",
    page_icon="🚀",
    layout="wide"
)

def main():
    """主函数"""
    
    # 页面标题
    st.title("🚀 Cursor AI应用开发示例")
    st.markdown("基于前面学到的AI理论和技术开发的完整应用")
    
    # 侧边栏
    with st.sidebar:
        st.header("🎛️ 控制面板")
        
        # 功能选择
        app_mode = st.selectbox(
            "选择功能模块",
            ["📊 数据可视化", "🤖 AI模型演示", "📈 性能分析"]
        )
        
        # 模型选择
        model_type = st.selectbox(
            "选择AI模型",
            ["GPT-3.5", "DeepSeek-R1", "阿里云百炼"]
        )
    
    # 主要内容区域
    if app_mode == "📊 数据可视化":
        show_data_visualization()
    elif app_mode == "🤖 AI模型演示":
        show_ai_demo(model_type)
    elif app_mode == "📈 性能分析":
        show_performance_analysis()

def show_data_visualization():
    """数据可视化模块"""
    st.header("📊 数据可视化示例")
    
    # 创建示例数据
    import numpy as np
    
    # 销售数据
    dates = pd.date_range('2023-01-01', periods=30, freq='D')
    sales_data = pd.DataFrame({
        '日期': dates,
        '销售额': [100 + i * 10 + np.random.randint(-20, 20) for i in range(30)]
    })
    
    # 创建图表
    fig = px.line(sales_data, x='日期', y='销售额', title='月度销售趋势')
    st.plotly_chart(fig, use_container_width=True)
    
    # 产品分布
    products = ['产品A', '产品B', '产品C', '产品D']
    sales = [120, 85, 95, 110]
    
    fig2 = px.pie(values=sales, names=products, title='产品销售分布')
    st.plotly_chart(fig2, use_container_width=True)

def show_ai_demo(model_type):
    """AI模型演示模块"""
    st.header("🤖 AI模型演示")
    
    st.info(f"当前使用模型: {model_type}")
    
    # 输入区域
    user_input = st.text_area(
        "请输入您的需求",
        placeholder="例如：请帮我写一篇关于人工智能的文章...",
        height=150
    )
    
    # 生成按钮
    if st.button("🚀 生成结果", type="primary"):
        if user_input.strip():
            with st.spinner("AI正在思考中..."):
                # 模拟AI响应
                response = f"""
基于您的需求，我为您生成以下内容：

## 人工智能的发展与应用

人工智能（AI）作为当今科技领域最热门的话题之一，正在深刻改变着我们的生活方式和工作模式。

### 主要应用领域
1. **自然语言处理**：机器翻译、智能客服、内容生成
2. **计算机视觉**：图像识别、视频分析、自动驾驶
3. **机器学习**：预测分析、推荐系统、风险评估

*生成模型：{model_type}*
                """
                
                st.markdown(response)
        else:
            st.warning("请输入内容后再生成")

def show_performance_analysis():
    """性能分析模块"""
    st.header("📈 性能分析")
    
    # 性能指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("响应时间", "2.3s", "-0.2s")
    with col2:
        st.metric("成功率", "98.5%", "+0.5%")
    with col3:
        st.metric("并发数", "150", "+10")
    with col4:
        st.metric("错误率", "1.5%", "-0.3%")
    
    # 系统信息
    st.subheader("ℹ️ 系统信息")
    st.info(f"Python版本: {os.sys.version}")
    st.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 