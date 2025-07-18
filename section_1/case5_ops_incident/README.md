# CASE 5: 运维事件处理

## 案例描述
使用阿里云百炼大模型API获取本机系统信息并进行智能分析，提供系统状态诊断和优化建议。

## 应用场景
- IT运维自动化
- 系统监控告警处理
- 故障诊断助手
- 运维知识库管理

## 功能特性
- 系统信息收集
- 性能指标分析
- 智能诊断建议
- 系统优化推荐
- 实时监控数据
- 历史趋势分析

## 技术要点
- 系统信息采集
- 性能指标监控
- 智能分析诊断
- 优化建议生成
- 实时数据处理

## 环境配置
```bash
# 安装依赖
pip install -r ../requirements.txt

# 配置环境变量
export DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

## 运行方式
```bash
# 方法1：使用启动脚本（推荐）
cd .. && ./start_app.sh ops

# 方法2：手动启动
source ../venv/bin/activate
streamlit run app.py
```

## 使用说明
1. 在侧边栏输入阿里云百炼API Key
2. 选择模型（qwen-turbo、qwen-plus、qwen-max）
3. 点击"获取系统信息"按钮
4. 查看系统状态和性能指标
5. 获取AI分析建议和优化方案

## 监控指标
- CPU使用率和负载
- 内存使用情况
- 磁盘空间和IO
- 网络连接状态
- 进程信息
- 系统运行时间

## 文件结构
- `app.py`: 主程序文件（Streamlit应用）
- `README.md`: 说明文档

## 访问地址
启动后访问：http://localhost:8501 