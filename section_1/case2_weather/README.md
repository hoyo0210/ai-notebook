# CASE 2: 天气查询

## 案例描述
使用阿里云百炼大模型API结合OpenWeatherMap天气API，实现智能天气查询功能。

## 应用场景
- 智能语音助手
- 移动应用天气功能
- 出行规划助手
- 农业气象服务

## 功能特性
- 自然语言天气查询
- Function Calling实现
- 智能回复生成
- 详细天气数据展示
- 支持中文城市名称
- 当前天气和未来预报

## 技术要点
- Function Calling 实现
- 外部API集成（OpenWeatherMap）
- 自然语言理解
- 结果格式化输出
- 地理编码支持

## 环境配置
```bash
# 安装依赖
pip install -r ../requirements.txt

# 配置环境变量
export DASHSCOPE_API_KEY=your_dashscope_api_key_here
export OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## 运行方式
```bash
# 方法1：使用启动脚本（推荐）
cd .. && ./start_app.sh weather

# 方法2：手动启动
source ../venv/bin/activate
streamlit run app.py
```

## 使用说明
1. 在侧边栏输入阿里云百炼API Key和OpenWeatherMap API Key
2. 选择模型（qwen-turbo、qwen-plus、qwen-max）
3. 用自然语言描述天气查询需求（如："北京今天天气怎么样？"）
4. 点击"查询天气"按钮
5. 查看智能化的天气信息回复

## API配置说明
- **阿里云百炼API Key**：用于自然语言理解和智能回复生成
- **OpenWeatherMap API Key**：用于获取真实天气数据
  - 免费注册：https://openweathermap.org/
  - 支持中文城市名称查询
  - 提供当前天气和5天预报

## 文件结构
- `app.py`: 主程序文件（Streamlit应用）
- `README.md`: 说明文档

## 访问地址
启动后访问：http://localhost:8501 