import streamlit as st
import dashscope
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="AI智能客服",
    page_icon="🤖",
    layout="wide"
)

# 标题
st.title("🤖 AI智能客服")
st.markdown("24/7智能客服助手，为您提供专业的服务支持")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 客服设置")
    service_type = st.selectbox(
        "服务类型",
        ["电商客服", "技术支持", "银行服务", "保险咨询", "教育咨询", "通用客服"],
        index=0
    )
    
    personality = st.selectbox(
        "客服性格",
        ["专业严谨", "友好亲切", "幽默风趣", "简洁高效"],
        index=1
    )
    
    language = st.selectbox(
        "服务语言",
        ["中文", "English", "中文+English"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 选择服务类型和风格")
    st.markdown("3. 开始对话")
    st.markdown("4. 查看对话历史")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quick_reply" not in st.session_state:
    st.session_state.quick_reply = None

# 主界面
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 对话界面")
    
    # 处理快速回复
    if st.session_state.quick_reply:
        prompt = st.session_state.quick_reply
        st.session_state.quick_reply = None  # 清除快速回复状态
        
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成AI回复
        if api_key:
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    try:
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 构建系统提示
                        system_prompts = {
                            "电商客服": "你是一个专业的电商客服，熟悉产品知识、订单处理、退换货政策等。请用友好、专业的态度回答客户问题。",
                            "技术支持": "你是一个技术专家，能够解决各种技术问题，包括软件使用、系统故障、网络问题等。请提供准确、详细的技术支持。",
                            "银行服务": "你是一个银行客服代表，熟悉各种银行业务，包括开户、转账、理财、贷款等。请提供专业、安全的金融服务咨询。",
                            "保险咨询": "你是一个保险顾问，了解各种保险产品，包括人寿保险、健康保险、车险等。请为客户提供专业的保险建议。",
                            "教育咨询": "你是一个教育顾问，熟悉各种教育课程、学习方法、考试信息等。请为学生和家长提供教育咨询服务。",
                            "通用客服": "你是一个专业的客服代表，能够处理各种客户咨询和问题。请用友好、专业的态度为客户提供帮助。"
                        }
                        
                        personality_prompts = {
                            "专业严谨": "请保持专业、严谨的态度，提供准确、详细的信息。",
                            "友好亲切": "请用友好、亲切的语气，让客户感受到温暖和关怀。",
                            "幽默风趣": "请在回答中适当加入幽默元素，让对话更加轻松愉快。",
                            "简洁高效": "请提供简洁、高效的回复，直接回答客户问题。"
                        }
                        
                        system_content = f"{system_prompts[service_type]} {personality_prompts[personality]}"
                        
                        # 构建对话历史
                        conversation_history = f"系统角色：{system_content}\n\n"
                        for msg in st.session_state.messages[-10:]:  # 保留最近10条消息
                            conversation_history += f"{msg['role']}: {msg['content']}\n"
                        
                        # 调用API
                        response = dashscope.Generation.call(
                            model=model,
                            prompt=conversation_history,
                            result_format='message'
                        )
                        
                        if response.status_code == 200:
                            assistant_response = response.output.choices[0].message.content
                            
                            # 添加助手回复
                            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                            st.markdown(assistant_response)
                            
                            # 保存对话历史
                            st.session_state.chat_history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "user": prompt,
                                "assistant": assistant_response,
                                "service_type": service_type
                            })
                        else:
                            error_msg = f"抱歉，我遇到了一些问题：{response.message}"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)
                        
                    except Exception as e:
                        error_msg = f"抱歉，我遇到了一些问题：{str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)
        else:
            st.error("请输入阿里云API Key")
    
    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成AI回复
        if api_key:
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    try:
                        # 设置API key
                        dashscope.api_key = api_key
                        
                        # 构建系统提示
                        system_prompts = {
                            "电商客服": "你是一个专业的电商客服，熟悉产品知识、订单处理、退换货政策等。请用友好、专业的态度回答客户问题。",
                            "技术支持": "你是一个技术专家，能够解决各种技术问题，包括软件使用、系统故障、网络问题等。请提供准确、详细的技术支持。",
                            "银行服务": "你是一个银行客服代表，熟悉各种银行业务，包括开户、转账、理财、贷款等。请提供专业、安全的金融服务咨询。",
                            "保险咨询": "你是一个保险顾问，了解各种保险产品，包括人寿保险、健康保险、车险等。请为客户提供专业的保险建议。",
                            "教育咨询": "你是一个教育顾问，熟悉各种教育课程、学习方法、考试信息等。请为学生和家长提供教育咨询服务。",
                            "通用客服": "你是一个专业的客服代表，能够处理各种客户咨询和问题。请用友好、专业的态度为客户提供帮助。"
                        }
                        
                        personality_prompts = {
                            "专业严谨": "请保持专业、严谨的态度，提供准确、详细的信息。",
                            "友好亲切": "请用友好、亲切的语气，让客户感受到温暖和关怀。",
                            "幽默风趣": "请在回答中适当加入幽默元素，让对话更加轻松愉快。",
                            "简洁高效": "请提供简洁、高效的回复，直接回答客户问题。"
                        }
                        
                        system_content = f"{system_prompts[service_type]} {personality_prompts[personality]}"
                        
                        # 构建对话历史
                        conversation_history = f"系统角色：{system_content}\n\n"
                        for msg in st.session_state.messages[-10:]:  # 保留最近10条消息
                            conversation_history += f"{msg['role']}: {msg['content']}\n"
                        
                        # 调用API
                        response = dashscope.Generation.call(
                            model=model,
                            prompt=conversation_history,
                            result_format='message'
                        )
                        
                        if response.status_code == 200:
                            assistant_response = response.output.choices[0].message.content
                            
                            # 添加助手回复
                            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                            st.markdown(assistant_response)
                            
                            # 保存对话历史
                            st.session_state.chat_history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "user": prompt,
                                "assistant": assistant_response,
                                "service_type": service_type
                            })
                        else:
                            error_msg = f"抱歉，我遇到了一些问题：{response.message}"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)
                        
                    except Exception as e:
                        error_msg = f"抱歉，我遇到了一些问题：{str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)
        else:
            st.error("请输入阿里云API Key")

with col2:
    st.subheader("📊 对话统计")
    
    # 统计信息
    if st.session_state.messages:
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.metric("总对话数", total_messages)
        st.metric("用户消息", user_messages)
        st.metric("AI回复", assistant_messages)
    
    st.markdown("---")
    
    # 快速回复
    st.subheader("⚡ 快速回复")
    quick_replies = {
        "电商客服": [
            "如何查询订单状态？",
            "退换货政策是什么？",
            "有优惠活动吗？",
            "如何修改收货地址？"
        ],
        "技术支持": [
            "系统无法登录怎么办？",
            "如何重置密码？",
            "软件安装失败",
            "网络连接问题"
        ],
        "银行服务": [
            "如何开通网银？",
            "转账限额是多少？",
            "理财产品推荐",
            "如何申请信用卡？"
        ]
    }
    
    if service_type in quick_replies:
        for reply in quick_replies[service_type]:
            if st.button(reply, key=reply):
                st.session_state.quick_reply = reply
                st.rerun()

# 对话管理
st.markdown("---")
col_manage1, col_manage2, col_manage3 = st.columns(3)

with col_manage1:
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

with col_manage2:
    if st.button("📥 导出对话"):
        if st.session_state.chat_history:
            chat_export = ""
            for chat in st.session_state.chat_history:
                chat_export += f"时间：{chat['timestamp']}\n"
                chat_export += f"用户：{chat['user']}\n"
                chat_export += f"客服：{chat['assistant']}\n"
                chat_export += "-" * 50 + "\n"
            
            st.download_button(
                label="下载对话记录",
                data=chat_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

with col_manage3:
    if st.button("📊 查看历史"):
        if st.session_state.chat_history:
            st.subheader("对话历史")
            for i, chat in enumerate(st.session_state.chat_history[-5:], 1):
                with st.expander(f"对话 {i} - {chat['timestamp']}"):
                    st.write(f"**用户：** {chat['user']}")
                    st.write(f"**客服：** {chat['assistant']}")
        else:
            st.info("暂无对话历史")

# 知识库
st.markdown("---")
st.subheader("📚 知识库")

knowledge_topics = {
    "电商客服": ["订单管理", "退换货政策", "支付方式", "物流配送"],
    "技术支持": ["系统故障", "软件使用", "网络问题", "数据备份"],
    "银行服务": ["账户管理", "转账汇款", "理财产品", "信用卡服务"],
    "保险咨询": ["保险产品", "理赔流程", "保费计算", "保险条款"]
}

if service_type in knowledge_topics:
    selected_knowledge = st.selectbox("选择知识主题", knowledge_topics[service_type])
    if st.button("获取知识"):
        if not api_key:
            st.error("请输入阿里云API Key")
        else:
            with st.spinner("正在获取相关知识..."):
                try:
                    # 设置API key
                    dashscope.api_key = api_key
                    
                    knowledge_prompt = f"""
                    请提供关于"{selected_knowledge}"的详细知识，包括：
                    1. 基本概念
                    2. 常见问题
                    3. 操作步骤
                    4. 注意事项
                    5. 相关链接
                    """
                    
                    knowledge_response = dashscope.Generation.call(
                        model=model,
                        prompt=knowledge_prompt,
                        result_format='message'
                    )
                    
                    if knowledge_response.status_code == 200:
                        knowledge_result = knowledge_response.output.choices[0].message.content
                        st.markdown(knowledge_result)
                    else:
                        st.error(f"获取知识失败：{knowledge_response.message}")
                    
                except Exception as e:
                    st.error(f"获取知识失败：{str(e)}")

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼")
st.markdown("**功能：** 智能对话、多场景支持、知识库查询") 