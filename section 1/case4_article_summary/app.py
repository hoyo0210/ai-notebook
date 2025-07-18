import streamlit as st
import dashscope
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="文章总结工具",
    page_icon="📝",
    layout="wide"
)

# 标题
st.title("📝 文章总结工具")
st.markdown("使用阿里云百炼大模型对长篇文章进行智能总结")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 总结选项")
    summary_length = st.selectbox(
        "总结长度",
        ["简短", "中等", "详细"],
        index=1
    )
    
    summary_style = st.selectbox(
        "总结风格",
        ["学术", "通俗", "新闻", "技术"],
        index=1
    )
    
    include_key_points = st.checkbox("包含关键点", value=True)
    include_quotes = st.checkbox("包含重要引用", value=False)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 选择输入方式（URL/文件/文本）")
    st.markdown("3. 选择总结选项")
    st.markdown("4. 点击总结按钮")

# 主界面
tab1, tab2 = st.tabs(["🌐 URL输入", "📁 文件上传"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("输入URL")
        url_input = st.text_input(
            "请输入文章URL",
            placeholder="https://example.com/article"
        )
        
        if st.button("📝 开始总结", type="primary", key="url_summary"):
            if not api_key:
                st.error("请输入阿里云API Key")
            elif not url_input.strip():
                st.error("请输入文章URL")
            else:
                with st.spinner("正在获取文章内容..."):
                    try:
                        # 获取网页内容
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        response = requests.get(url_input, headers=headers, timeout=10)
                        response.raise_for_status()
                        
                        # 简单的文本提取（可以后续优化）
                        import re
                        from bs4 import BeautifulSoup
                        
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # 移除script和style元素
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # 获取文本
                        text = soup.get_text()
                        
                        # 清理文本
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        if len(text) < 100:
                            st.error("无法从URL中提取到足够的文章内容")
                            st.stop()
                        
                        st.success(f"成功获取文章内容，长度：{len(text)}字符")
                        
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 构建prompt
                        length_map = {"简短": "100字以内", "中等": "200-300字", "详细": "500字左右"}
                        style_map = {
                            "学术": "学术论文风格，注重逻辑性和专业性",
                            "通俗": "通俗易懂，适合大众阅读",
                            "新闻": "新闻稿风格，突出重要信息",
                            "技术": "技术文档风格，注重准确性和实用性"
                        }
                        
                        prompt = f"""
                        请对以下文章进行智能总结。
                        
                        文章内容：
                        {text[:3000]}  # 限制长度避免token超限
                        
                        总结要求：
                        1. 长度：{length_map[summary_length]}
                        2. 风格：{style_map[summary_style]}
                        3. 包含关键点：{'是' if include_key_points else '否'}
                        4. 包含重要引用：{'是' if include_quotes else '否'}
                        
                        请按以下格式输出：
                        
                        ## 文章总结
                        [总结内容]
                        
                        ## 主要观点
                        [关键观点列表]
                        
                        ## 核心信息
                        [核心信息提取]
                        """
                        
                        # 调用API
                        response = dashscope.Generation.call(
                            model=model,
                            prompt=prompt,
                            result_format='message'
                        )
                        
                        if response.status_code == 200:
                            result = response.output.choices[0].message.content
                            
                            # 显示结果
                            with col2:
                                st.subheader("总结结果")
                                st.markdown(result)
                                
                                # 保存结果
                                st.session_state.last_summary = result
                                
                                # 下载按钮
                                st.download_button(
                                    label="📥 下载总结",
                                    data=result,
                                    file_name="article_summary.md",
                                    mime="text/markdown"
                                )
                        else:
                            st.error(f"API调用失败：{response.message}")
                            
                    except Exception as e:
                        st.error(f"总结失败：{str(e)}")

with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("上传文件")
        uploaded_file = st.file_uploader(
            "选择文章文件",
            type=['txt', 'md', 'pdf', 'docx'],
            help="支持文本文件、Markdown、PDF、Word文档"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.pdf'):
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    file_content = ""
                    for page in pdf_reader.pages:
                        file_content += page.extract_text()
                elif uploaded_file.name.endswith('.docx'):
                    from docx import Document
                    doc = Document(uploaded_file)
                    file_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                else:
                    file_content = uploaded_file.read().decode('utf-8')
                
                st.success(f"已加载文件：{uploaded_file.name}")
                st.text_area("文件内容预览", file_content[:500] + "..." if len(file_content) > 500 else file_content, height=200)
                
            except Exception as e:
                st.error(f"文件读取失败：{str(e)}")
        
        if st.button("📝 开始总结", type="primary", key="file_summary"):
            if not api_key:
                st.error("请输入阿里云API Key")
            elif uploaded_file is None:
                st.error("请先上传文件")
            else:
                with st.spinner("正在总结中..."):
                    try:
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 构建prompt
                        length_map = {"简短": "100字以内", "中等": "200-300字", "详细": "500字左右"}
                        style_map = {
                            "学术": "学术论文风格，注重逻辑性和专业性",
                            "通俗": "通俗易懂，适合大众阅读",
                            "新闻": "新闻稿风格，突出重要信息",
                            "技术": "技术文档风格，注重准确性和实用性"
                        }
                        
                        prompt = f"""
                        请对以下文章进行智能总结。
                        
                        文章内容：
                        {file_content[:3000]}  # 限制长度避免token超限
                        
                        总结要求：
                        1. 长度：{length_map[summary_length]}
                        2. 风格：{style_map[summary_style]}
                        3. 包含关键点：{'是' if include_key_points else '否'}
                        4. 包含重要引用：{'是' if include_quotes else '否'}
                        
                        请按以下格式输出：
                        
                        ## 文章总结
                        [总结内容]
                        
                        ## 主要观点
                        [关键观点列表]
                        
                        ## 核心信息
                        [核心信息提取]
                        """
                        
                        # 调用API
                        response = dashscope.Generation.call(
                            model=model,
                            prompt=prompt,
                            result_format='message'
                        )
                        
                        if response.status_code == 200:
                            result = response.output.choices[0].message.content
                            
                            # 显示结果
                            with col2:
                                st.subheader("总结结果")
                                st.markdown(result)
                                
                                # 保存结果
                                st.session_state.last_summary = result
                                
                                # 下载按钮
                                st.download_button(
                                    label="📥 下载总结",
                                    data=result,
                                    file_name="article_summary.md",
                                    mime="text/markdown"
                                )
                        else:
                            st.error(f"API调用失败：{response.message}")
                            
                    except Exception as e:
                        st.error(f"总结失败：{str(e)}")

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼 + BeautifulSoup")
st.markdown("**功能：** URL文章总结、文件总结、多风格输出") 