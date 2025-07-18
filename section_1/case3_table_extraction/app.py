import streamlit as st
import dashscope
import pandas as pd
import json
import os
from dotenv import load_dotenv
import io

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="表格提取工具",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 表格提取工具")
st.markdown("使用阿里云百炼大模型从文本或图像中提取表格数据")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 上传文件或输入文本")
    st.markdown("3. 选择输出格式")
    st.markdown("4. 点击提取按钮")

# 主界面
tab2, tab3 = st.tabs(["📁 文件上传", "🖼️ 图片识别"])

with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("上传文件")
        uploaded_file = st.file_uploader(
            "选择包含表格的文件",
            type=['txt', 'csv', 'xlsx', 'xls'],
            help="支持文本文件、CSV、Excel格式"
        )
        
        if uploaded_file is not None:
            st.success(f"已上传文件：{uploaded_file.name}")
            
            # 读取文件内容
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    file_content = df.to_string()
                elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                    file_content = df.to_string()
                else:
                    file_content = uploaded_file.read().decode('utf-8')
                
                st.text_area("文件内容预览", file_content, height=200)
                
            except Exception as e:
                st.error(f"文件读取失败：{str(e)}")
        
        st.info("文件提取功能将表格内容转换为清晰易读的文本格式")
        
        if st.button("📊 提取表格", type="primary", key="file_extract"):
            if not api_key:
                st.error("请输入阿里云API Key")
            elif uploaded_file is None:
                st.error("请先上传文件")
            else:
                with st.spinner("正在提取表格..."):
                    try:
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 构建prompt
                        prompt = f"""
                        请从以下文件内容中提取表格内容，将表格转换为清晰易读的文本格式。
                        
                        文件内容：
                        {file_content}
                        
                        要求：
                        1. 识别表格结构
                        2. 提取所有数据
                        3. 将表格内容转换为清晰、整洁的文本格式
                        4. 保持数据的完整性和准确性
                        5. 确保文本格式清晰易读，不要有乱码或格式错误
                        6. 输出格式应该是清晰的行列结构，便于阅读
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
                                st.subheader("提取结果")
                                
                                # 转换为Markdown格式并渲染
                                if not result.startswith('#'):
                                    # 如果没有Markdown标题，添加一个
                                    md_result = f"# 表格提取结果\n\n{result}"
                                else:
                                    md_result = result
                                
                                st.markdown(md_result)
                                
                                # 下载按钮
                                st.download_button(
                                    label="📥 下载Markdown结果",
                                    data=md_result,
                                    file_name="extracted_table.md",
                                    mime="text/markdown"
                                )
                        else:
                            st.error(f"API调用失败：{response.message}")
                        
                    except Exception as e:
                        st.error(f"提取失败：{str(e)}")

with tab3:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("上传图片")
        uploaded_image = st.file_uploader(
            "选择包含表格的图片",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="支持PNG、JPG、JPEG、GIF、BMP格式的图片",
            key="image_uploader"
        )
        
        if uploaded_image is not None:
            st.success(f"已上传图片：{uploaded_image.name}")
            
            # 显示图片预览
            st.image(uploaded_image, caption="图片预览", use_container_width=True)
        
        st.info("图片识别功能将表格内容转换为文本格式")
        
        if st.button("🖼️ 识别表格", type="primary", key="image_extract"):
            if not api_key:
                st.error("请输入阿里云API Key")
            elif uploaded_image is None:
                st.error("请先上传图片")
            else:
                with st.spinner("正在识别图片中的表格..."):
                    try:
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 保存图片到临时文件
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                            tmp_file.write(uploaded_image.read())
                            tmp_file_path = tmp_file.name
                        
                        # 构建prompt
                        prompt = f"""
                        请仔细识别这张图片中的表格内容，将表格转换为清晰易读的文本格式。
                        
                        要求：
                        1. 仔细识别图片中的表格结构和所有数据
                        2. 将表格内容转换为清晰、整洁的文本格式
                        3. 保持数据的完整性和准确性
                        4. 确保文本格式清晰易读，不要有乱码或格式错误
                        5. 如果图片中有多个表格，请分别提取
                        6. 输出格式应该是清晰的行列结构，便于阅读
                        7. 避免出现重复字符、乱码或格式混乱的情况
                        """
                        
                        # 调用多模态API
                        response = dashscope.MultiModalConversation.call(
                            model='qwen-vl-max',
                            messages=[
                                {
                                    'role': 'user',
                                    'content': [
                                        {'text': prompt},
                                        {'image': tmp_file_path}
                                    ]
                                }
                            ]
                        )
                        
                        # 清理临时文件
                        try:
                            os.unlink(tmp_file_path)
                        except:
                            pass
                        
                        if response.status_code == 200:
                            # 解析多模态API响应
                            if hasattr(response.output.choices[0].message, 'content'):
                                content = response.output.choices[0].message.content
                                if isinstance(content, list) and len(content) > 0:
                                    if hasattr(content[0], 'text'):
                                        result = content[0].text
                                    elif isinstance(content[0], dict) and 'text' in content[0]:
                                        result = content[0]['text']
                                    else:
                                        result = str(content[0])
                                else:
                                    result = str(content)
                            else:
                                result = str(response.output.choices[0].message)
                            
                            # 显示结果
                            with col2:
                                st.subheader("识别结果")
                                
                                # 转换为Markdown格式并渲染
                                if not result.startswith('#'):
                                    # 如果没有Markdown标题，添加一个
                                    md_result = f"# 表格识别结果\n\n{result}"
                                else:
                                    md_result = result
                                
                                st.markdown(md_result)
                                
                                # 下载按钮
                                st.download_button(
                                    label="📥 下载Markdown结果",
                                    data=md_result,
                                    file_name="extracted_table.md",
                                    mime="text/markdown"
                                )
                        else:
                            st.error(f"API调用失败：{response.message}")
                        
                    except Exception as e:
                        st.error(f"识别失败：{str(e)}")

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼 + 多模态AI")
st.markdown("**功能：** 表格识别、文本转换、图片识别") 