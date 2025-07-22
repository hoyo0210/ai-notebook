#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek Ollama API 调用示例
适用于已通过 Ollama 部署的 DeepSeek 模型
"""

import requests
import json
import time
from typing import List, Dict, Optional

class DeepSeekOllamaClient:
    """DeepSeek Ollama 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "deepseek-r1:1.5b"):
        """
        初始化客户端
        
        Args:
            base_url: Ollama 服务地址，默认本地11434端口
            model: 模型名称，默认使用 deepseek-r1:1.5b
        """
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
    
    def check_model_status(self) -> bool:
        """检查模型是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(model['name'] == self.model for model in models)
            return False
        except:
            return False
    
    def generate_text(self, prompt: str, **kwargs) -> Dict:
        """
        生成文本（单次调用）
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数（temperature, max_tokens等）
        
        Returns:
            包含生成结果的字典
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_url, json=data, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {str(e)}"}
    
    def chat(self, messages: List[Dict], **kwargs) -> Dict:
        """
        多轮对话
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}, ...]
            **kwargs: 其他参数
        
        Returns:
            包含回复的字典
        """
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(self.chat_url, json=data, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {str(e)}"}
    
    def stream_generate(self, prompt: str, **kwargs):
        """
        流式生成文本
        
        Args:
            prompt: 输入提示词
            **kwargs: 其他参数
        
        Yields:
            生成的内容片段
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_url, json=data, stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            yield chunk['response']
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
        except requests.exceptions.RequestException as e:
            yield f"错误: {str(e)}"

def test_basic_functionality():
    """测试基础功能"""
    print("🔍 检查模型状态...")
    client = DeepSeekOllamaClient()
    
    if not client.check_model_status():
        print("❌ 模型不可用，请确保：")
        print("   1. Ollama 服务已启动")
        print("   2. DeepSeek 模型已下载")
        print("   3. 服务地址正确")
        return False
    
    print("✅ 模型状态正常")
    return True

def example_usage():
    """使用示例"""
    print("\n" + "="*60)
    print("🚀 DeepSeek Ollama API 调用示例")
    print("="*60)
    
    # 初始化客户端
    client = DeepSeekOllamaClient()
    
    # 1. 基础文本生成
    print("\n📝 1. 基础文本生成")
    print("-" * 30)
    result = client.generate_text(
        prompt="请用一句话介绍一下人工智能",
        temperature=0.7,
        max_tokens=100
    )
    
    if 'error' in result:
        print(f"❌ 错误: {result['error']}")
    else:
        print(f"✅ 生成结果: {result.get('response', '')}")
    
    # 2. 多轮对话
    print("\n💬 2. 多轮对话")
    print("-" * 30)
    messages = [
        {"role": "user", "content": "你好，请简单介绍一下自己"},
        {"role": "assistant", "content": "你好！我是DeepSeek，一个强大的大语言模型。"},
        {"role": "user", "content": "你能做什么？"}
    ]
    
    chat_result = client.chat(messages, temperature=0.5)
    if 'error' in chat_result:
        print(f"❌ 错误: {chat_result['error']}")
    else:
        print(f"✅ 对话回复: {chat_result.get('message', {}).get('content', '')}")
    
    # 3. 流式生成
    print("\n🌊 3. 流式生成")
    print("-" * 30)
    print("正在生成...")
    try:
        for chunk in client.stream_generate(
            prompt="请写一首关于春天的短诗",
            temperature=0.8
        ):
            print(chunk, end='', flush=True)
        print("\n✅ 流式生成完成")
    except Exception as e:
        print(f"❌ 流式生成错误: {str(e)}")

def advanced_examples():
    """高级用法示例"""
    print("\n" + "="*60)
    print("🎯 高级用法示例")
    print("="*60)
    
    client = DeepSeekOllamaClient()
    
    # 1. 代码生成
    print("\n💻 1. 代码生成")
    print("-" * 30)
    code_prompt = """
    请用Python编写一个函数，实现以下功能：
    1. 接收一个字符串列表
    2. 统计每个字符串的长度
    3. 返回长度大于5的字符串列表
    4. 包含适当的错误处理和文档字符串
    """
    
    code_result = client.generate_text(
        prompt=code_prompt,
        temperature=0.3,  # 降低温度以获得更稳定的代码
        max_tokens=800
    )
    
    if 'error' in code_result:
        print(f"❌ 错误: {code_result['error']}")
    else:
        print("✅ 生成的代码:")
        print(code_result.get('response', ''))
    
    # 2. 数学推理
    print("\n🧮 2. 数学推理")
    print("-" * 30)
    math_prompt = """
    请解决以下数学问题，并详细说明解题步骤：
    
    问题：一个长方形的长是宽的2倍，周长是30厘米，求长方形的面积。
    
    请按照以下格式回答：
    1. 设未知数
    2. 列方程
    3. 解方程
    4. 求面积
    5. 验证答案
    """
    
    math_result = client.generate_text(
        prompt=math_prompt,
        temperature=0.1,  # 数学问题需要更精确的答案
        max_tokens=600
    )
    
    if 'error' in math_result:
        print(f"❌ 错误: {math_result['error']}")
    else:
        print("✅ 数学推理结果:")
        print(math_result.get('response', ''))
    
    # 3. 角色扮演
    print("\n🎭 3. 角色扮演")
    print("-" * 30)
    role_prompt = """
    你现在是一位经验丰富的Python开发工程师，具有以下特点：
    - 有10年以上的Python开发经验
    - 熟悉Django、Flask、FastAPI等Web框架
    - 擅长数据库设计和优化
    - 有丰富的项目架构经验
    
    请回答用户的问题，并提供专业的建议和最佳实践。
    
    用户问题：我想开发一个在线商城系统，应该选择什么技术栈？请详细说明理由。
    """
    
    role_result = client.generate_text(
        prompt=role_prompt,
        temperature=0.7,
        max_tokens=1000
    )
    
    if 'error' in role_result:
        print(f"❌ 错误: {role_result['error']}")
    else:
        print("✅ 角色扮演回复:")
        print(role_result.get('response', ''))

def robust_api_call():
    """健壮的API调用示例"""
    print("\n" + "="*60)
    print("🛡️ 健壮调用示例")
    print("="*60)
    
    client = DeepSeekOllamaClient()
    max_retries = 3
    
    for attempt in range(max_retries):
        print(f"\n🔄 尝试 {attempt + 1}/{max_retries}")
        try:
            result = client.generate_text(
                prompt="请简单介绍一下机器学习",
                temperature=0.5,
                max_tokens=300
            )
            
            if 'error' not in result:
                print("✅ 健壮调用成功")
                print(f"结果: {result.get('response', '')}")
                break
            else:
                print(f"❌ 尝试失败: {result['error']}")
                
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            print(f"⏳ 等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    else:
        print("❌ 所有重试都失败了")

def interactive_chat():
    """交互式聊天"""
    print("\n" + "="*60)
    print("💬 交互式聊天模式")
    print("="*60)
    print("输入 'quit' 或 'exit' 退出聊天")
    print("输入 'clear' 清空对话历史")
    print("-" * 60)
    
    client = DeepSeekOllamaClient()
    messages = []
    
    while True:
        try:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
            
            if user_input.lower() == 'clear':
                messages = []
                print("🧹 对话历史已清空")
                continue
            
            if not user_input:
                continue
            
            # 添加用户消息
            messages.append({"role": "user", "content": user_input})
            
            # 调用API
            print("🤖 正在思考...")
            response = client.chat(messages, temperature=0.7)
            
            if 'error' in response:
                print(f"❌ 错误: {response['error']}")
                continue
            
            assistant_message = response.get('message', {}).get('content', '')
            print(f"🤖 DeepSeek: {assistant_message}")
            
            # 添加助手回复到历史
            messages.append({"role": "assistant", "content": assistant_message})
            
        except KeyboardInterrupt:
            print("\n👋 聊天已中断")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")

def main():
    """主函数"""
    print("🎯 DeepSeek Ollama API 测试工具")
    print("=" * 50)
    
    # 检查模型状态
    if not test_basic_functionality():
        return
    
    while True:
        print("\n📋 请选择测试模式:")
        print("1. 基础功能测试")
        print("2. 高级用法示例")
        print("3. 健壮调用测试")
        print("4. 交互式聊天")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == '1':
            example_usage()
        elif choice == '2':
            advanced_examples()
        elif choice == '3':
            robust_api_call()
        elif choice == '4':
            interactive_chat()
        elif choice == '5':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 