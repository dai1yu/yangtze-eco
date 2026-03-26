import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 页面配置
st.set_page_config(page_title="长江生态保护大屏", layout="wide", page_icon="🌊")

# ==================== 自定义CSS - 参考图风格 ====================
st.markdown("""
<style>
    /* 整体背景 - 深色科技感 */
    .stApp {
        background: linear-gradient(135deg, #0a0c15 0%, #0f1725 100%);
    }
    
    /* 卡片样式 */
    .card {
        background: rgba(10, 20, 35, 0.75);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(0, 200, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    /* 大数字卡片 - 顶部 */
    .metric-card {
        background: linear-gradient(135deg, rgba(0,40,60,0.8), rgba(0,20,40,0.9));
        border-radius: 16px;
        padding: 15px 20px;
        border: 1px solid rgba(0, 255, 255, 0.3);
        text-align: center;
    }
    .metric-value {
        font-size: 42px;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0,255,255,0.5);
    }
    .metric-label {
        font-size: 14px;
        color: #88aaff;
        letter-spacing: 1px;
    }
    .metric-trend {
        font-size: 12px;
        color: #44ff44;
    }
    
    /* 标题样式 */
    .section-title {
        font-size: 18px;
        font-weight: bold;
        color: #00ffff;
        border-left: 3px solid #00ffff;
        padding-left: 12px;
        margin: 0 0 15px 0;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: rgba(5, 15, 25, 0.95);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* 表格样式 */
    .stDataFrame {
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
    }
    
    /* 排行榜列表 */
    .rank-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(0,255,255,0.1);
        color: #ddd;
    }
    .rank-number {
        color: #00ffff;
        font-weight: bold;
        width: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 模拟数据 ====================
water_data = pd.DataFrame({
    "监测点": ["宜昌", "武汉", "南京", "上海", "岳阳", "九江", "芜湖", "重庆"],
    "pH值": [7.2, 7.5, 7.1, 7.3, 7.4, 7.2, 7.3, 7.1],
    "溶解氧(mg/L)": [6.8, 6.5, 6.9, 6.7, 6.6, 6.8, 6.7, 6.4],
    "水质等级": ["Ⅱ类", "Ⅱ类", "Ⅰ类", "Ⅱ类", "Ⅱ类", "Ⅱ类", "Ⅱ类", "Ⅱ类"]
})

fish_data = pd.DataFrame({
    "年份": [2020, 2021, 2022, 2023, 2024, 2025],
    "四大家鱼(万尾)": [120, 135, 150, 170, 195, 220],
    "珍稀鱼类(万尾)": [8, 10, 13, 17, 22, 28]
})

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("# 🌊 长江生态保护")
    st.markdown("### 数据可视化驾驶舱")
    st.markdown("---")
    page = st.selectbox("选择模块", ["📊 总览大屏", "💧 水质监测", "🐟 鱼类修复"])
    st.markdown("---")
    st.caption("数据实时更新 | 长江水利委员会")

# ==================== 总览大屏（参考图布局）====================
if page == "📊 总览大屏":
    
    # ========== 第一行：顶部大数字卡片（4个） ==========
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">52</div>
            <div class="metric-label">📡 监测点位</div>
            <div class="metric-trend">↑ 新增 8个</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">+32%</div>
            <div class="metric-label">🐟 鱼类恢复率</div>
            <div class="metric-trend">↑ 近3年累计</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">94.2%</div>
            <div class="metric-label">💧 水质达标率</div>
            <div class="metric-trend">↑ 提升 8.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1,280</div>
            <div class="metric-label">🌿 修复面积</div>
            <div class="metric-trend">km² ↑ 156</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== 第二行：左右分栏 ==========
    col_left, col_right = st.columns([1, 1])
    
    # 左侧：环形图 + 趋势图
    with col_left:
        with st.container():
            st.markdown('<div class="section-title">📊 水质等级占比</div>', unsafe_allow_html=True)
            fig = go.Figure(data=[go.Pie(
                labels=["Ⅰ类", "Ⅱ类", "Ⅲ类"],
                values=[1, 6, 1],
                hole=0.65,
                marker_colors=["#00ffaa", "#44aaff", "#ffaa44"],
                textinfo="label+percent",
                textfont=dict(color="white")
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#ffffff",
                height=280,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with st.container():
            st.markdown('<div class="section-title">📈 鱼类恢复趋势</div>', unsafe_allow_html=True)
            fig = px.line(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                          color_discrete_sequence=["#00ffff", "#ffaa00"])
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#cccccc",
                height=280,
                margin=dict(t=30, b=0, l=0, r=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 右侧：排行榜（监测点水质排名）
    with col_right:
        st.markdown('<div class="section-title">🏆 监测点水质排名</div>', unsafe_allow_html=True)
        
        # 按溶解氧排序
        ranking = water_data.sort_values("溶解氧(mg/L)", ascending=False).head(8)
        
        for i, row in ranking.iterrows():
            st.markdown(f"""
            <div class="rank-item">
                <div><span class="rank-number">{ranking.index.get_loc(i)+1}</span> {row['监测点']}</div>
                <div>溶解氧: {row['溶解氧(mg/L)']} mg/L</div>
                <div style="color:#00ffff;">{row['水质等级']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        
        # 实时监测数据卡片
        st.markdown('<div class="section-title">⏱️ 实时监测数据</div>', unsafe_allow_html=True)
        
        # 模拟实时数据
        realtime_data = pd.DataFrame({
            "时间": ["14:32:25", "14:31:20", "14:30:15"],
            "宜昌 pH": [7.21, 7.19, 7.22],
            "武汉 pH": [7.52, 7.50, 7.51],
            "南京 pH": [7.08, 7.10, 7.09]
        })
        st.dataframe(realtime_data, use_container_width=True, hide_index=True)
    
    # ========== 第三行：详细数据表格 ==========
    st.markdown('<div class="section-title">📋 全流域监测数据</div>', unsafe_allow_html=True)
    st.dataframe(water_data, use_container_width=True)
    
    # ========== 第四行：项目价值卡片 ==========
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div class="metric-label">🌱 生态效益</div>
            <div>恢复鱼类种群 +32%<br>水质达标率 94.2%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div class="metric-label">👥 社会价值</div>
            <div>公众环保意识提升<br>带动绿色就业 2000+</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div class="metric-label">💰 经济价值</div>
            <div>环保数据服务<br>生态旅游收益</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== 水质监测页面 ====================
elif page == "💧 水质监测":
    st.markdown('<div class="section-title">💧 水质监测中心</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">7.3</div>
            <div class="metric-label">📊 平均pH</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">6.7 mg/L</div>
            <div class="metric-label">💨 平均溶解氧</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">20%</div>
            <div class="metric-label">🏆 Ⅰ类水质占比</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📋 实时监测数据")
    st.dataframe(water_data, use_container_width=True)

# ==================== 鱼类修复页面 ====================
elif page == "🐟 鱼类修复":
    st.markdown('<div class="section-title">🐟 鱼类生态修复系统</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 种群恢复趋势")
        fig = px.area(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                      color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cccccc")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎣 近期放流活动")
        st.success("**2025年3月** - 宜昌段放流四大家鱼 30万尾")
        st.success("**2025年2月** - 武汉段放流中华鲟 500尾")
        st.success("**2025年1月** - 南京段放流珍稀鱼类 2000尾")
        st.progress(68, text="鱼类栖息地修复工程")
        st.progress(45, text="产卵场生态重建")
