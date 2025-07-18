import streamlit as st
import dashscope
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="智能天气查询",
    page_icon="🌤️",
    layout="wide"
)

# 标题
st.title("🌤️ 智能天气查询")
st.markdown("使用阿里云百炼大模型结合OpenWeatherMap天气API，提供智能天气查询服务")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    dashscope_api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    openweather_api_key = st.text_input("OpenWeatherMap API Key", type="password", value=os.getenv("OPENWEATHER_API_KEY", ""))
    model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入API密钥")
    st.markdown("2. 用自然语言描述天气查询需求")
    st.markdown("3. AI会自动解析并调用OpenWeatherMap天气API")
    st.markdown("4. 获得智能化的天气信息")

# OpenWeatherMap API函数
def get_weather_data(city, api_key):
    """获取OpenWeatherMap天气数据"""
    try:
        # 首先通过Geocoding API获取城市坐标（支持中文城市名称）
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocode_params = {
            "q": city,
            "limit": 1,
            "appid": api_key
        }
        
        geocode_response = requests.get(geocode_url, params=geocode_params)
        if geocode_response.status_code == 200:
            geocode_data = geocode_response.json()
            
            if geocode_data:
                # 获取城市坐标和名称
                lat = geocode_data[0]["lat"]
                lon = geocode_data[0]["lon"]
                city_name = geocode_data[0]["name"]
                country = geocode_data[0]["country"]
                
                # 使用坐标获取当前天气数据
                current_url = "https://api.openweathermap.org/data/2.5/weather"
                current_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": api_key,
                    "units": "metric",  # 使用摄氏度
                    "lang": "zh_cn"     # 中文
                }
                
                current_response = requests.get(current_url, params=current_params)
                if current_response.status_code == 200:
                    current_data = current_response.json()
                    
                    # 使用坐标获取5天预报数据
                    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
                    forecast_params = {
                        "lat": lat,
                        "lon": lon,
                        "appid": api_key,
                        "units": "metric",
                        "lang": "zh_cn"
                    }
                    
                    forecast_response = requests.get(forecast_url, params=forecast_params)
                    if forecast_response.status_code == 200:
                        forecast_data = forecast_response.json()
                        
                        return {
                            "success": True,
                            "data": {
                                "current": current_data,
                                "forecast": forecast_data
                            },
                            "city_info": {
                                "name": city_name,
                                "country": country,
                                "lat": lat,
                                "lon": lon
                            }
                        }
                    else:
                        return {"success": False, "error": "预报API请求失败"}
                else:
                    return {"success": False, "error": f"天气API错误：{current_response.status_code}"}
            else:
                return {"success": False, "error": f"未找到城市：{city}"}
        else:
            return {"success": False, "error": "地理编码API请求失败"}
            
    except Exception as e:
        return {"success": False, "error": f"API调用异常：{str(e)}"}

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("天气查询")
    query_input = st.text_area(
        "请输入天气查询需求",
        height=150,
        placeholder="例如：北京今天天气怎么样？明天会下雨吗？",
        value=st.session_state.get('query_input', '')
    )
    
    if st.button("🌤️ 查询天气", type="primary"):
        if not dashscope_api_key:
            st.error("请输入阿里云API Key")
        # 使用模拟数据，不需要检查API密钥
        elif not query_input.strip():
            st.error("请输入查询需求")
        else:
            with st.spinner("正在查询中..."):
                try:
                    # 设置API key
                    dashscope.api_key = dashscope_api_key
                    
                    # 第一步：解析用户查询
                    parse_prompt = f"""
                    请解析以下天气查询需求，提取城市名称和查询内容。
                    
                    用户查询：{query_input}
                    
                    请按以下JSON格式输出：
                    {{
                        "city": "城市名称",
                        "query_type": "查询类型（当前天气/未来天气/温度/降水等）",
                        "time": "查询时间（今天/明天/后天等）"
                    }}
                    """
                    
                    parse_response = dashscope.Generation.call(
                        model=model,
                        prompt=parse_prompt,
                        result_format='message'
                    )
                    
                    if parse_response.status_code == 200:
                        parse_result = parse_response.output.choices[0].message.content
                        
                        # 尝试解析JSON
                        try:
                            parsed_data = json.loads(parse_result)
                            city = parsed_data.get("city", "深圳")
                            query_type = parsed_data.get("query_type", "当前天气")
                            time = parsed_data.get("time", "今天")
                        except:
                            # 如果JSON解析失败，使用简单的城市提取
                            city = "深圳"  # 默认城市
                        
                        # 第二步：获取天气数据
                        weather_result = get_weather_data(city, openweather_api_key)
                        
                        if weather_result["success"]:
                            weather_data = weather_result["data"]
                            city_info = weather_result["city_info"]
                            
                            # 提取当前天气信息
                            current_data = weather_data["current"]
                            weather_info = f"""
                            城市：{current_data['name']}, {current_data['sys']['country']}
                            温度：{current_data['main']['temp']}°C
                            体感温度：{current_data['main']['feels_like']}°C
                            天气：{current_data['weather'][0]['description']}
                            湿度：{current_data['main']['humidity']}%
                            气压：{current_data['main']['pressure']} hPa
                            风速：{current_data['wind']['speed']} m/s
                            风向：{current_data['wind'].get('deg', 'N/A')}°
                            能见度：{current_data.get('visibility', 'N/A')} m
                            云量：{current_data['clouds']['all']}%
                            更新时间：{datetime.fromtimestamp(current_data['dt']).strftime('%Y-%m-%d %H:%M:%S')}
                            """
                            
                            # 第三步：生成智能回复
                            response_prompt = f"""
                            你是一个专业的天气助手。以下是真实的天气数据，请基于这些数据回答用户的问题。
                            
                            用户查询：{query_input}
                            
                            当前天气数据（这是真实数据，请直接使用）：
                            {weather_info}
                            
                            请直接使用上述天气数据回答用户问题。数据中包含：
                            - 城市名称
                            - 当前温度
                            - 天气状况
                            - 湿度
                            - 风向和风力
                            - 发布时间
                            
                            请基于这些真实数据生成自然友好的回复，不要否认数据的存在。
                            """
                            
                            final_response = dashscope.Generation.call(
                                model=model,
                                prompt=response_prompt,
                                result_format='message'
                            )
                            
                            if final_response.status_code == 200:
                                result = final_response.output.choices[0].message.content
                                
                                # 保存结果
                                st.session_state.last_weather_result = result
                                st.session_state.last_weather_data = weather_data
                                
                                st.success("查询完成！")
                            else:
                                st.error(f"生成回复失败：{final_response.message}")
                                
                        else:
                            st.error(f"获取天气数据失败：{weather_result['error']}")
                    else:
                        st.error(f"解析查询失败：{parse_response.message}")
                        
                except Exception as e:
                    st.error(f"查询失败：{str(e)}")

with col2:
    st.subheader("查询结果")
    if 'last_weather_result' in st.session_state:
        st.markdown(st.session_state.last_weather_result)
        
        # 显示原始天气数据
        if 'last_weather_data' in st.session_state:
            with st.expander("📊 详细天气数据"):
                st.json(st.session_state.last_weather_data)
                
            # 显示预报信息
            weather_data = st.session_state.last_weather_data
            if "forecast" in weather_data and weather_data["forecast"]["list"]:
                with st.expander("📅 5天天气预报"):
                    forecast_data = weather_data["forecast"]
                    st.write(f"**城市：** {forecast_data['city']['name']}, {forecast_data['city']['country']}")
                    
                    # 按天分组显示预报
                    daily_forecasts = {}
                    for item in forecast_data["list"]:
                        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                        if date not in daily_forecasts:
                            daily_forecasts[date] = []
                        daily_forecasts[date].append(item)
                    
                    for date, items in list(daily_forecasts.items())[:5]:  # 显示5天
                        day_name = datetime.fromtimestamp(items[0]['dt']).strftime('%A')
                        min_temp = min(item['main']['temp'] for item in items)
                        max_temp = max(item['main']['temp'] for item in items)
                        weather_desc = items[0]['weather'][0]['description']
                        humidity = items[0]['main']['humidity']
                        wind_speed = items[0]['wind']['speed']
                        
                        st.write(f"**{date} ({day_name})：** {weather_desc}")
                        st.write(f"温度：{min_temp:.1f}°C / {max_temp:.1f}°C, 湿度：{humidity}%, 风速：{wind_speed} m/s")
                        
                        # 显示降水概率
                        if 'pop' in items[0]:
                            pop_percent = items[0]['pop'] * 100
                            st.write(f"降水概率：{pop_percent:.0f}%")
                        
                        st.write("---")
    else:
        st.info("请在左侧输入查询需求并点击查询按钮")

# 示例查询
st.markdown("---")
st.subheader("💡 查询示例")
examples = [
    "北京今天天气怎么样？",
    "上海明天会下雨吗？",
    "广州现在的温度是多少？",
    "深圳未来几天的天气如何？"
]

for example in examples:
    if st.button(example, key=example):
        st.session_state.query_input = example
        st.rerun()

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼 + OpenWeatherMap API")
st.markdown("**功能：** 自然语言天气查询、智能回复生成") 