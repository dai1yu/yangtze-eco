import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 页面配置
st.set_page_config(page_title="长江生态保护大屏", layout="wide", page_icon="🌊")

# ==================== 自定义CSS - 炫酷大屏风格 ====================
st.markdown("""
<style>
    /* 整体背景 - 深色科技感 */
    .stApp {
        background: linear-gradient(135deg, #0a0f1a 0%, #0a1a2a 100%);
    }
    
    /* 卡片样式 - 半透明玻璃 */
    .card {
        background: rgba(15, 25, 45, 0.65);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
    }
    
    /* 大数字样式 */
    .big-number {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(135deg, #00ffff, #00aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 标题样式 */
    .title {
        font-size: 24px;
        font-weight: bold;
        color: #00ffff;
        border-left: 4px solid #00ffff;
        padding-left: 15px;
        margin: 15px 0;
        text-shadow: 0 0 5px rgba(0,255,255,0.5);
    }
    
    /* 小标题 */
    .sub-title {
        font-size: 14px;
        color: #88aaff;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    /* 指标值 */
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #00ffff;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: rgba(10, 20, 30, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* 表格样式 */
    .stDataFrame {
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
    }
    
    /* 分隔线 */
    hr {
        border-color: rgba(0, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==================== 模拟数据 ====================
water_data = pd.DataFrame({
    "监测点": ["宜昌", "武汉", "南京", "上海", "岳阳", "九江", "芜湖"],
    "pH值": [7.2, 7.5, 7.1, 7.3, 7.4, 7.2, 7.3],
    "溶解氧(mg/L)": [6.8, 6.5, 6.9, 6.7, 6.6, 6.8, 6.7],
    "水质等级": ["Ⅱ类", "Ⅱ类", "Ⅰ类", "Ⅱ类", "Ⅱ类", "Ⅱ类", "Ⅱ类"]
})

fish_data = pd.DataFrame({
    "年份": [2020, 2021, 2022, 2023, 2024, 2025],
    "四大家鱼(万尾)": [120, 135, 150, 170, 195, 220],
    "珍稀鱼类(万尾)": [8, 10, 13, 17, 22, 28]
})

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("# 🌊 长江生态保护")
    st.markdown("### 智慧监测 · 生态修复")
    st.markdown("---")
    page = st.selectbox("选择驾驶舱", ["📊 总览大屏", "💧 水质监测", "🐟 鱼类修复"])
    st.markdown("---")
    st.caption("数据实时更新 | 来源：长江水利委员会")

# ==================== 总览大屏 ====================
if page == "📊 总览大屏":
    st.markdown('<div class="title">📊 长江生态保护 · 数据驾驶舱</div>', unsafe_allow_html=True)
    
    # 第一行：大数字卡片（4个）
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="sub-title">📡 监测点位</div>
            <div class="metric-value">52</div>
            <div style="color:#44ff44;">↑ 新增 8个</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="sub-title">🐟 鱼类恢复率</div>
            <div class="metric-value">+32%</div>
            <div style="color:#44ff44;">近3年累计</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div class="sub-title">💧 水质达标率</div>
            <div class="metric-value">94.2%</div>
            <div style="color:#44ff44;">↑ 提升 8.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card">
            <div class="sub-title">🌿 修复面积</div>
            <div class="metric-value">1,280</div>
            <div style="color:#44ff44;">km² ↑ 156</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 第二行：环形图 + 趋势图
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 水质等级分布")
        # 环形图
        fig = go.Figure(data=[go.Pie(
            labels=["Ⅰ类", "Ⅱ类", "Ⅲ类"],
            values=[1, 5, 1],
            hole=0.6,
            marker_colors=["#00ffaa", "#44aaff", "#ffaa44"],
            textinfo="label+percent"
        )])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff", height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📈 鱼类种群恢复趋势")
        fig = px.line(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                      color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#cccccc", height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 第三行：监测点排名
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🏆 监测点水质排名")
    ranking = water_data.sort_values("溶解氧(mg/L)", ascending=False)
    ranking["排名"] = range(1, len(ranking)+1)
    st.dataframe(ranking[["排名", "监测点", "pH值", "溶解氧(mg/L)", "水质等级"]], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 第四行：项目使命
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div class="sub-title">🌱 生态效益</div>
            <div>恢复鱼类种群，提升水质达标率</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div class="sub-title">👥 社会价值</div>
            <div>提升公众环保意识，带动绿色就业</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div class="sub-title">💰 经济价值</div>
            <div>环保数据服务，生态旅游衍生收益</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== 水质监测 ====================
elif page == "💧 水质监测":
    st.markdown('<div class="title">💧 水质监测中心</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><div class="sub-title">📊 平均pH</div><div class="metric-value">7.3</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="sub-title">💨 平均溶解氧</div><div class="metric-value">6.7 mg/L</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><div class="sub-title">🏆 Ⅰ类水质占比</div><div class="metric-value">20%</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📋 实时监测数据")
    st.dataframe(water_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 鱼类修复 ====================
elif page == "🐟 鱼类修复":
    st.markdown('<div class="title">🐟 鱼类生态修复系统</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📈 种群恢复趋势")
        fig = px.area(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                      color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cccccc")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎣 近期放流活动")
        st.success("**2025年3月** - 宜昌段放流四大家鱼 30万尾")
        st.success("**2025年2月** - 武汉段放流中华鲟 500尾")
        st.success("**2025年1月** - 南京段放流珍稀鱼类 2000尾")
        st.progress(68, text="鱼类栖息地修复工程")
        st.progress(45, text="产卵场生态重建")
        st.markdown('</div>', unsafe_allow_html=True)
