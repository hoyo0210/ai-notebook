import streamlit as st
import dashscope
import os
import platform
import psutil
import subprocess
from dotenv import load_dotenv
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="系统信息分析助手",
    page_icon="💻",
    layout="wide"
)

# 标题
st.title("💻 系统信息分析助手")
st.markdown("获取本机系统信息并使用AI分析当前问题")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 分析选项")
    include_processes = st.checkbox("包含进程信息", value=True)
    include_network = st.checkbox("包含网络信息", value=True)
    include_disk = st.checkbox("包含磁盘信息", value=True)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 选择要收集的系统信息")
    st.markdown("3. 点击获取系统信息")
    st.markdown("4. 输入您遇到的问题")
    st.markdown("5. 获取AI分析和建议")

def get_system_info():
    """获取系统基本信息"""
    info = {
        "系统信息": {
            "操作系统": platform.system(),
            "系统版本": platform.version(),
            "架构": platform.machine(),
            "处理器": platform.processor(),
            "主机名": platform.node(),
            "Python版本": platform.python_version()
        },
        "硬件信息": {
            "CPU核心数": psutil.cpu_count(),
            "CPU使用率": f"{psutil.cpu_percent(interval=1)}%",
            "内存总量": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "内存使用率": f"{psutil.virtual_memory().percent}%",
            "可用内存": f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
        }
    }
    
    # 磁盘信息
    if include_disk:
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "挂载点": partition.mountpoint,
                    "文件系统": partition.fstype,
                    "总容量": f"{usage.total / (1024**3):.2f} GB",
                    "已使用": f"{usage.used / (1024**3):.2f} GB",
                    "可用空间": f"{usage.free / (1024**3):.2f} GB",
                    "使用率": f"{usage.percent}%"
                }
            except:
                continue
        info["磁盘信息"] = disk_info
    
    # 网络信息
    if include_network:
        network_info = {}
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == 2:  # IPv4 (AF_INET = 2)
                    network_info[interface] = addr.address
        info["网络信息"] = network_info
    
    # 进程信息
    if include_processes:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "PID": proc.info['pid'],
                    "名称": proc.info['name'],
                    "CPU使用率": f"{proc.info['cpu_percent']:.1f}%",
                    "内存使用率": f"{proc.info['memory_percent']:.1f}%"
                })
            except:
                continue
        # 按CPU使用率排序，取前10个
        processes.sort(key=lambda x: float(x['CPU使用率'].rstrip('%')), reverse=True)
        info["进程信息"] = processes[:10]
    
    return info

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("系统信息收集")
    
    if st.button("🔍 获取系统信息", type="primary"):
        with st.spinner("正在收集系统信息..."):
            try:
                system_info = get_system_info()
                st.session_state.system_info = system_info
                st.success("系统信息收集完成！")
                
                # 显示系统信息
                st.json(system_info)
                
            except Exception as e:
                st.error(f"获取系统信息失败：{str(e)}")
    
    # 显示已收集的系统信息
    if 'system_info' in st.session_state:
        st.subheader("当前系统信息")
        st.json(st.session_state.system_info)
    
    st.markdown("---")
    st.subheader("问题描述")
    
    # 问题描述
    problem_description = st.text_area(
        "请描述您遇到的问题",
        height=150,
        placeholder="例如：系统运行缓慢、某个应用无法启动、网络连接问题等..."
    )
    
    # 错误日志
    error_log = st.text_area(
        "错误日志（可选）",
        height=100,
        placeholder="如果有错误日志，请粘贴在这里..."
    )

with col2:
    st.subheader("AI分析结果")
    
    if st.button("🤖 开始分析", type="primary"):
        if not api_key:
            st.error("请输入阿里云API Key")
        elif 'system_info' not in st.session_state:
            st.error("请先获取系统信息")
        elif not problem_description.strip():
            st.error("请描述您遇到的问题")
        else:
            with st.spinner("正在分析问题..."):
                try:
                    # 设置API key
                    dashscope.api_key = api_key
                    
                    # 构建prompt
                    system_info_text = json.dumps(st.session_state.system_info, ensure_ascii=False, indent=2)
                    
                    error_log_text = f"错误日志：{error_log}" if error_log.strip() else ""
                    
                    prompt = f"""
                    请根据以下系统信息和问题描述，提供详细的分析和解决方案。
                    
                    系统信息：
                    {system_info_text}
                    
                    问题描述：
                    {problem_description}
                    
                    {error_log_text}
                    
                    请按以下格式提供分析结果：
                    
                    ## 问题分析
                    [基于系统信息的问题分析]
                    
                    ## 可能原因
                    [列出可能的原因]
                    
                    ## 解决方案
                    [具体的解决步骤]
                    
                    ## 预防措施
                    [如何避免类似问题]
                    
                    ## 相关命令
                    [可能用到的诊断和修复命令]
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
                        st.markdown(result)
                        
                        # 保存结果
                        st.session_state.last_analysis = result
                        
                        # 生成分析报告
                        report = f"""
# 系统问题分析报告

**分析时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**系统：** {platform.system()} {platform.version()}

## 系统信息
{system_info_text}

## 问题描述
{problem_description}

{f"## 错误日志\n{error_log}" if error_log.strip() else ""}

## AI分析结果
{result}
                        """
                        
                        st.download_button(
                            label="📥 下载分析报告",
                            data=report,
                            file_name=f"system_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(f"API调用失败：{response.message}")
                        
                except Exception as e:
                    st.error(f"分析失败：{str(e)}")
    
    # 显示历史分析结果
    if 'last_analysis' in st.session_state:
        st.subheader("历史分析结果")
        st.markdown(st.session_state.last_analysis)

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼 + psutil")
st.markdown("**功能：** 系统信息收集、问题诊断、AI分析建议") 