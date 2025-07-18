import streamlit as st
import dashscope
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="情感分析工具",
    page_icon="😊",
    layout="wide"
)

# 标题
st.title("😊 情感分析工具")
st.markdown("使用阿里云百炼大模型分析文本的情感倾向")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 选择要使用的模型")
    st.markdown("3. 在文本框中输入要分析的文本")
    st.markdown("4. 点击分析按钮获取结果")

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("输入文本")
    text_input = st.text_area(
        "请输入要分析的文本",
        height=200,
        placeholder="例如：这个产品真的很棒，我非常喜欢！"
    )
    
    if st.button("🔍 开始分析", type="primary"):
        if not api_key:
            st.error("请输入阿里云API Key")
        elif not text_input.strip():
            st.error("请输入要分析的文本")
        else:
            with st.spinner("正在分析中..."):
                try:
                    # 设置API key
                    dashscope.api_key = api_key
                    
                    # 构建prompt
                    prompt = f"""
                    请分析以下文本的情感倾向，并给出详细的分析结果。
                    
                    文本：{text_input}
                    
                    请按以下格式输出：
                    1. 情感倾向：[正面/负面/中性]
                    2. 置信度：[0-100%]
                    3. 关键词：[提取的关键情感词]
                    4. 详细分析：[详细的情感分析说明]
                    """
                    
                    # 调用API
                    response = dashscope.Generation.call(
                        model=model,
                        prompt=prompt,
                        result_format='message'
                    )
                    
                    if response.status_code == 200:
                        result = response.output.choices[0].message.content
                        
                        # 保存结果
                        st.session_state.last_result = result
                        
                        # 添加到历史记录
                        import datetime
                        st.session_state.analysis_history.append({
                            'text': text_input,
                            'result': result,
                            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        st.success("分析完成！")
                    else:
                        st.error(f"API调用失败：{response.message}")
                        
                except Exception as e:
                    st.error(f"分析失败：{str(e)}")

with col2:
    st.subheader("分析结果")
    if 'last_result' in st.session_state:
        st.markdown(st.session_state.last_result)
    else:
        st.info("请在左侧输入文本并点击分析按钮")

# 历史记录
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if st.button("📊 查看历史记录"):
    if st.session_state.analysis_history:
        st.subheader("历史分析记录")
        for i, record in enumerate(st.session_state.analysis_history[-5:], 1):
            with st.expander(f"记录 {i} - {record['timestamp']}"):
                st.write(f"**文本：** {record['text'][:100]}...")
                st.write(f"**结果：** {record['result']}")
    else:
        st.info("暂无历史记录")

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼")
st.markdown("**功能：** 文本情感分析、关键词提取、置信度评估") 