import streamlit as st
import dashscope
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from dotenv import load_dotenv
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="保险欺诈检测系统",
    page_icon="🛡️",
    layout="wide"
)

# 标题
st.title("🛡️ 保险欺诈检测系统")
st.markdown("基于机器学习的智能保险欺诈检测")

# 侧边栏配置
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("阿里云API Key", type="password", value=os.getenv("DASHSCOPE_API_KEY", ""))
    model_type = st.selectbox("选择模型", ["RandomForest", "XGBoost", "LogisticRegression"], index=0)
    
    st.markdown("---")
    st.markdown("### 模型设置")
    test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, 0.1)
    random_state = st.number_input("随机种子", value=42, min_value=1, max_value=1000)
    
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("1. 输入您的阿里云API Key")
    st.markdown("2. 训练机器学习模型")
    st.markdown("3. 输入保险理赔数据")
    st.markdown("4. 获取欺诈检测结果")

# 初始化会话状态
if "model" not in st.session_state:
    st.session_state.model = None
if "encoders" not in st.session_state:
    st.session_state.encoders = {}
if "scaler" not in st.session_state:
    st.session_state.scaler = None
if "feature_names" not in st.session_state:
    st.session_state.feature_names = None

def load_and_preprocess_data():
    """加载和预处理数据"""
    try:
        # 加载训练数据
        train_data = pd.read_csv('case7_insurance_fraud/train.csv')
        test_data = pd.read_csv('case7_insurance_fraud/test.csv')
        
        # 合并数据用于预处理
        combined_data = pd.concat([train_data, test_data], ignore_index=True)
        
        # 删除不需要的列
        columns_to_drop = ['policy_number', 'policy_bind_date', 'incident_date', '_c39']
        combined_data = combined_data.drop(columns=columns_to_drop, errors='ignore')
        
        # 分离特征和目标变量
        if 'fraud_reported' in combined_data.columns:
            X = combined_data.drop('fraud_reported', axis=1)
            y = combined_data['fraud_reported'].fillna(0).astype(int)  # 处理缺失值并确保标签是整数类型
        else:
            X = combined_data
            y = None
        
        # 处理特征中的缺失值
        X = X.fillna('Unknown')
        
        # 编码分类变量
        encoders = {}
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column].astype(str))
            encoders[column] = le
        
        # 标准化数值变量
        scaler = StandardScaler()
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X[numeric_columns] = scaler.fit_transform(X[numeric_columns])
        
        # 分离回训练和测试数据
        train_size = len(train_data)
        X_train = X[:train_size]
        y_train = y[:train_size] if y is not None else None
        X_test = X[train_size:]
        
        return X_train, y_train, X_test, encoders, scaler, X.columns.tolist()
        
    except Exception as e:
        st.error(f"数据加载失败：{str(e)}")
        return None, None, None, None, None, None

def train_model(X_train, y_train, model_type="RandomForest"):
    """训练模型"""
    try:
        if model_type == "RandomForest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == "XGBoost":
            from xgboost import XGBClassifier
            model = XGBClassifier(random_state=42)
        elif model_type == "LogisticRegression":
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(random_state=42)
        
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        st.error(f"模型训练失败：{str(e)}")
        return None

def predict_fraud(input_data, model, encoders, scaler, feature_names):
    """预测欺诈风险"""
    try:
        # 创建输入数据的DataFrame
        df = pd.DataFrame([input_data])
        
        # 编码分类变量
        for column in df.select_dtypes(include=['object']).columns:
            if column in encoders:
                try:
                    df[column] = encoders[column].transform(df[column].astype(str))
                except ValueError:
                    # 如果遇到未见过的标签，使用最常见的标签
                    most_common = encoders[column].classes_[0]
                    df[column] = encoders[column].transform([most_common])[0]
        
        # 标准化数值变量
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = scaler.transform(df[numeric_columns])
        
        # 确保列顺序一致
        df = df.reindex(columns=feature_names, fill_value=0)
        
        # 预测
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0]
        
        return prediction, probability
    except Exception as e:
        st.error(f"预测失败：{str(e)}")
        return None, None

# 主界面
tab1, tab2, tab3 = st.tabs(["📊 模型训练", "🔍 欺诈检测", "📈 数据分析"])

with tab1:
    st.subheader("模型训练")
    
    if st.button("🚀 开始训练模型", type="primary"):
        with st.spinner("正在加载数据和训练模型..."):
            # 加载数据
            X_train, y_train, X_test, encoders, scaler, feature_names = load_and_preprocess_data()
            
            if X_train is not None and y_train is not None:
                # 分割数据
                X_train_split, X_val, y_train_split, y_val = train_test_split(
                    X_train, y_train, test_size=test_size, random_state=random_state
                )
                
                # 训练模型
                model = train_model(X_train_split, y_train_split, model_type)
                
                if model is not None:
                    # 保存模型和预处理器
                    st.session_state.model = model
                    st.session_state.encoders = encoders
                    st.session_state.scaler = scaler
                    st.session_state.feature_names = feature_names
                    
                    # 评估模型
                    y_pred = model.predict(X_val)
                    accuracy = accuracy_score(y_val, y_pred)
                    
                    st.success(f"模型训练完成！验证集准确率：{accuracy:.4f}")
                    
                    # 显示分类报告
                    st.subheader("模型性能报告")
                    report = classification_report(y_val, y_pred, output_dict=True)
                    st.json(report)
                    
                    # 混淆矩阵
                    cm = confusion_matrix(y_val, y_pred)
                    fig = px.imshow(cm, 
                                  labels=dict(x="预测", y="实际", color="数量"),
                                  x=["非欺诈", "欺诈"],
                                  y=["非欺诈", "欺诈"],
                                  title="混淆矩阵")
                    st.plotly_chart(fig)
                else:
                    st.error("模型训练失败")
            else:
                st.error("数据加载失败")

with tab2:
    st.subheader("欺诈检测")
    
    if st.session_state.model is None:
        st.warning("请先训练模型")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("输入理赔数据")
            
            # 创建输入表单
            with st.form("fraud_detection_form"):
                # 客户信息
                st.markdown("### 客户信息")
                months_as_customer = st.number_input("客户时长（月）", min_value=0, value=100)
                age = st.number_input("年龄", min_value=18, max_value=100, value=35)
                insured_sex = st.selectbox("性别", ["MALE", "FEMALE"])
                insured_education_level = st.selectbox("教育水平", ["High School", "Bachelors", "Masters", "JD", "MD", "PhD"])
                insured_occupation = st.selectbox("职业", ["craft-repair", "machine-op-inspct", "sales", "armed-forces", "tech-support", "exec-managerial", "prof-specialty", "other-service", "handlers-cleaners", "farming-fishing", "transport-moving", "priv-house-serv", "protective-serv", "adm-clerical"])
                insured_hobbies = st.selectbox("爱好", ["reading", "video-games", "exercise", "music", "paintball", "camping", "hiking", "yachting", "cross-fit", "dancing", "bunjee-jumping", "base-jumping", "skydiving", "chess", "polo"])
                insured_relationship = st.selectbox("关系", ["wife", "own-child", "husband", "not-in-family", "other-relative", "unmarried"])
                
                # 保单信息
                st.markdown("### 保单信息")
                policy_state = st.selectbox("保单州", ["IN", "IL", "OH", "NC", "WV", "PA", "NY", "SC"])
                policy_csl = st.selectbox("责任限额", ["500/1000", "250/500", "100/300"])
                policy_deductable = st.number_input("免赔额", min_value=0, value=1000)
                policy_annual_premium = st.number_input("年保费", min_value=0.0, value=1000.0)
                umbrella_limit = st.number_input("伞险限额", min_value=0, value=0)
                insured_zip = st.number_input("邮编", min_value=10000, max_value=99999, value=45000)
                
                # 财务信息
                st.markdown("### 财务信息")
                capital_gains = st.number_input("资本收益", value=0)
                capital_loss = st.number_input("资本损失", value=0)
                
                # 事故信息
                st.markdown("### 事故信息")
                incident_type = st.selectbox("事故类型", ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"])
                collision_type = st.selectbox("碰撞类型", ["Side Collision", "Front Collision", "Rear Collision", "Unknown"])
                incident_severity = st.selectbox("事故严重程度", ["Minor Damage", "Major Damage", "Total Loss"])
                authorities_contacted = st.selectbox("联系机构", ["Police", "Fire", "Ambulance", "Other", "None"])
                incident_state = st.selectbox("事故州", ["NC", "WV", "PA", "NY", "SC", "IN", "IL", "OH"])
                incident_city = st.text_input("事故城市", value="Springfield")
                incident_location = st.text_input("事故地点", value="123 Main St")
                incident_hour_of_the_day = st.number_input("事故时间（小时）", min_value=0, max_value=23, value=12)
                number_of_vehicles_involved = st.number_input("涉事车辆数", min_value=1, value=2)
                property_damage = st.selectbox("财产损失", ["YES", "NO", "?"])
                bodily_injuries = st.number_input("人身伤害", min_value=0, value=0)
                witnesses = st.number_input("目击证人", min_value=0, value=0)
                police_report_available = st.selectbox("警方报告", ["YES", "NO", "?"])
                
                # 理赔信息
                st.markdown("### 理赔信息")
                total_claim_amount = st.number_input("总理赔金额", min_value=0, value=50000)
                injury_claim = st.number_input("人身伤害理赔", min_value=0, value=5000)
                property_claim = st.number_input("财产损失理赔", min_value=0, value=10000)
                vehicle_claim = st.number_input("车辆损失理赔", min_value=0, value=35000)
                
                # 车辆信息
                st.markdown("### 车辆信息")
                auto_make = st.selectbox("汽车品牌", ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "Dodge", "Jeep", "Suburu", "Mercedes", "Saab", "BMW", "Audi", "Volkswagen", "Lexus", "Acura", "Volvo", "Mazda", "Buick", "Hyundai", "Kia", "Infiniti", "Lincoln", "Pontiac", "Cadillac", "Saturn", "Oldsmobile", "Plymouth", "Mitsubishi", "Suzuki", "Isuzu", "Eagle", "Geo", "Scion", "Ferrari", "Lamborghini", "Porsche", "Bentley", "Rolls-Royce", "Aston Martin", "McLaren", "Bugatti", "Koenigsegg", "Pagani", "Rimac", "Lotus", "Caterham", "Ariel", "Morgan", "TVR", "Noble", "Gumpert", "Spyker", "Wiesmann", "Donkervoort", "KTM", "Hispano-Suiza", "De Tomaso", "Bizzarrini", "Intermeccanica", "Iso", "Bristol", "Jensen", "Gordon-Keeble", "Monteverdi", "DeLorean", "Vector", "Saleen", "Panoz", "Rossion", "Hennessey", "SSC", "Ruf", "Alpina", "Brabus", "Mansory", "Novitec", "Hamann", "Gemballa", "TechArt", "Rinspeed", "Zagato", "Pininfarina", "Bertone", "Italdesign", "Ghia", "Frua", "Vignale", "Touring", "Scaglietti", "Carrozzeria", "Stola", "Fioravanti", "I.DE.A", "Stile Bertone", "Carrozzeria", "Stola", "Fioravanti", "I.DE.A", "Stile Bertone"])
                auto_model = st.text_input("汽车型号", value="Civic")
                auto_year = st.number_input("汽车年份", min_value=1900, max_value=2024, value=2010)
                
                submitted = st.form_submit_button("🔍 检测欺诈风险")
        
        with col2:
            st.subheader("检测结果")
            
            if submitted:
                # 构建输入数据
                input_data = {
                    'months_as_customer': months_as_customer,
                    'age': age,
                    'policy_state': policy_state,
                    'policy_csl': policy_csl,
                    'policy_deductable': policy_deductable,
                    'policy_annual_premium': policy_annual_premium,
                    'umbrella_limit': umbrella_limit,
                    'insured_zip': insured_zip,
                    'insured_sex': insured_sex,
                    'insured_education_level': insured_education_level,
                    'insured_occupation': insured_occupation,
                    'insured_hobbies': insured_hobbies,
                    'insured_relationship': insured_relationship,
                    'capital-gains': capital_gains,
                    'capital-loss': capital_loss,
                    'incident_type': incident_type,
                    'collision_type': collision_type,
                    'incident_severity': incident_severity,
                    'authorities_contacted': authorities_contacted,
                    'incident_state': incident_state,
                    'incident_city': incident_city,
                    'incident_location': incident_location,
                    'incident_hour_of_the_day': incident_hour_of_the_day,
                    'number_of_vehicles_involved': number_of_vehicles_involved,
                    'property_damage': property_damage,
                    'bodily_injuries': bodily_injuries,
                    'witnesses': witnesses,
                    'police_report_available': police_report_available,
                    'total_claim_amount': total_claim_amount,
                    'injury_claim': injury_claim,
                    'property_claim': property_claim,
                    'vehicle_claim': vehicle_claim,
                    'auto_make': auto_make,
                    'auto_model': auto_model,
                    'auto_year': auto_year
                }
                
                # 预测
                prediction, probability = predict_fraud(
                    input_data, 
                    st.session_state.model, 
                    st.session_state.encoders, 
                    st.session_state.scaler, 
                    st.session_state.feature_names
                )
                
                if prediction is not None:
                    # 显示结果
                    if prediction == 1:
                        st.error("🚨 高风险：检测到潜在的保险欺诈行为")
                        risk_level = "高风险"
                        color = "red"
                    else:
                        st.success("✅ 低风险：未检测到明显的欺诈行为")
                        risk_level = "低风险"
                        color = "green"
                    
                            # 风险概率
                    fraud_probability = probability[1] if probability is not None and len(probability) > 1 else 0
                    st.metric("欺诈概率", f"{fraud_probability:.2%}")
                    
                    # 风险评分
                    risk_score = int(fraud_probability * 100)
                    st.progress(risk_score / 100)
                    st.write(f"风险评分：{risk_score}/100")
                    
                    # 详细分析
                    if api_key:
                        try:
                            dashscope.api_key = api_key
                            
                            analysis_prompt = f"""
                            请分析以下保险理赔数据的欺诈风险：
                            
                            理赔数据：
                            {json.dumps(input_data, ensure_ascii=False, indent=2)}
                            
                            检测结果：
                            - 风险等级：{risk_level}
                            - 欺诈概率：{fraud_probability:.2%}
                            
                            请提供：
                            1. 风险因素分析
                            2. 可疑指标识别
                            3. 建议措施
                            4. 进一步调查建议
                            """
                            
                            response = dashscope.Generation.call(
                                model="qwen-turbo",
                                prompt=analysis_prompt,
                                result_format='message'
                            )
                            
                            if response.status_code == 200:
                                analysis = response.output.choices[0].message.content
                                st.subheader("AI风险分析")
                                st.markdown(analysis)
                            else:
                                st.error("AI分析失败")
                        except Exception as e:
                            st.error(f"AI分析失败：{str(e)}")

with tab3:
    st.subheader("数据分析")
    
    if st.button("📊 加载数据"):
        with st.spinner("正在加载数据..."):
            X_train, y_train, X_test, encoders, scaler, feature_names = load_and_preprocess_data()
            
            if X_train is not None:
                # 加载原始数据用于可视化
                train_data = pd.read_csv('case7_insurance_fraud/train.csv')
                
                # 欺诈分布
                if 'fraud_reported' in train_data.columns:
                    fraud_counts = train_data['fraud_reported'].value_counts()
                    fig = px.pie(values=fraud_counts.values, names=['非欺诈', '欺诈'], title="欺诈分布")
                    st.plotly_chart(fig)
                
                # 年龄分布
                fig = px.histogram(train_data, x='age', title="年龄分布", nbins=20)
                st.plotly_chart(fig)
                
                # 理赔金额分布
                fig = px.histogram(train_data, x='total_claim_amount', title="理赔金额分布", nbins=20)
                st.plotly_chart(fig)
                
                # 事故类型分布
                if 'incident_type' in train_data.columns:
                    incident_counts = train_data['incident_type'].value_counts()
                    fig = px.bar(x=incident_counts.index, y=incident_counts.values, title="事故类型分布")
                    st.plotly_chart(fig)

# 页脚
st.markdown("---")
st.markdown("**技术栈：** Streamlit + 阿里云百炼 + Scikit-learn")
st.markdown("**功能：** 机器学习模型训练、欺诈检测、风险分析") 