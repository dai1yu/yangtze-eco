import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 初始化亮度，如果之前没设置过，默认为 100
if 'brightness' not in st.session_state:
   st.session_state.brightness = 91
# ==========================================
# ✅ 粘贴在这里：负责真正变色的代码
# ==========================================

# 1. 获取当前亮度值（从 session_state 里拿，不管你在哪个页面）
current_brightness = st.session_state.brightness

# 2. 计算颜色
gray_val = int(255 - (current_brightness * 2.55))
bg_color = f"rgb({gray_val}, {gray_val}, {gray_val})" if gray_val < 128 else f"rgb({gray_val}, {gray_val}, {gray_val})"

# 3. 注入 CSS (把你截图里第 23-49 行的内容粘贴在这里)
st.markdown(f"""
<style>
    /* 1. 修改页面整体背景 */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        background-image: none;
    }}

    /* 2. 修改主内容区背景 */
    .main .block-container {{
        background-color: {bg_color};
    }}

    /* 3. 修改侧边栏背景 */
    [data-testid="stSidebar"] {{
        background-color: {bg_color};
    }}

    /* 4. 增加过渡动画 */
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
        transition: background-color 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)
# 页面配置 - 宽屏模式
st.set_page_config(page_title="长江生态保护平台", layout="wide", page_icon="🌊")

# ==================== 自定义CSS - 深色大屏风格 ====================
st.markdown("""
<style>
    /* 深色主题 */
    .stApp {
        background: linear-gradient(135deg, #0a1a2f 0%, #0c2a3b 100%);
    }

    /* 卡片样式 */
    .metric-card {
        background: rgba(20, 40, 55, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ffff;
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
    .section-title {
        font-size: 28px;
        font-weight: bold;
        color: #00ffff;
        border-left: 4px solid #00ffff;
        padding-left: 20px;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(0,255,255,0.3);
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: rgba(10, 25, 35, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }

    /* 表格样式 */
    .stDataFrame {
        background: rgba(20, 40, 55, 0.6);
        border-radius: 15px;
        padding: 10px;
    }

    /* 指标卡片文字 */
    .metric-label {
        color: #88aaff;
        font-size: 14px;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #00ffff;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏导航 ====================
with st.sidebar:
    st.markdown("# 🌊 长江生态保护")
    st.markdown("### 智慧监测 · 生态修复 · 科普教育")
    st.markdown("---")

with st.sidebar:
    # ... 你的标题和其他内容 ...

    # 加入这个滑块（或者把它放在“系统设置”页面里，但必须在 session_state 中保存）
    # 这里为了演示全局控制，建议直接放侧边栏，或者在“系统设置”里修改 st.session_state.brightness
   
   
    page = st.selectbox(
    "选择驾驶舱",
    ["🏠 总览驾驶舱", "💧 水质监测中心", "🐟 鱼类修复中心", "📚 科普教育平台", "📊 数据分析报告", "⚙️ 系统设置"],
    key="nav"
)
    st.markdown("---")
    st.caption("实时数据更新中 | 数据来源：长江水利委员会")

# ==================== 模拟数据 ====================
water_data = pd.DataFrame({
    "监测点": ["宜昌", "武汉", "南京", "上海", "岳阳"],
    "pH值": [7.2, 7.5, 7.1, 7.3, 7.4],
    "溶解氧(mg/L)": [6.8, 6.5, 6.9, 6.7, 6.6],
    "浊度(NTU)": [12, 15, 11, 14, 13],
    "水质等级": ["Ⅱ类", "Ⅱ类", "Ⅰ类", "Ⅱ类", "Ⅱ类"]
})

fish_data = pd.DataFrame({
    "年份": [2020, 2021, 2022, 2023, 2024, 2025],
    "四大家鱼(万尾)": [120, 135, 150, 170, 195, 220],
    "珍稀鱼类(万尾)": [8, 10, 13, 17, 22, 28]
})

# ==================== 总览驾驶舱 ====================
if page == "🏠 总览驾驶舱":
    st.markdown('<p class="section-title">📊 长江生态保护总览</p >', unsafe_allow_html=True)

    # 第一行：核心指标卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📡 监测点位</div>
            <div class="metric-value">52</div>
            <div style="color:#44ff44; font-size:12px;">↑ 新增 8 个</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🐟 鱼类恢复率</div>
            <div class="metric-value">+32%</div>
            <div style="color:#44ff44; font-size:12px;">近3年累计增长</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">💧 水质达标率</div>
            <div class="metric-value">94.2%</div>
            <div style="color:#44ff44; font-size:12px;">↑ 提升 8.5%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🌿 生态修复面积</div>
            <div class="metric-value">1,280</div>
            <div style="color:#44ff44; font-size:12px;">平方公里 ↑ 156</div>
        </div>
        """, unsafe_allow_html=True)

    # 第二行：图表
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 鱼类种群恢复趋势")
        fig = px.line(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                      title="主要鱼类种群数量变化",
                      color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#cccccc", title_font_color="#00ffff")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🗺️ 监测点水质分布")
        fig = px.bar(water_data, x="监测点", y=["pH值", "溶解氧(mg/L)"],
                     title="各监测点水质指标",
                     barmode="group",
                     color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font_color="#cccccc", title_font_color="#00ffff")
        st.plotly_chart(fig, use_container_width=True)

    # 第三行：项目背景
    st.markdown("### 🎯 项目使命")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🌱 **生态效益**\n\n恢复鱼类种群，提升水质达标率，重建长江生态平衡")
    with col2:
        st.success("👥 **社会价值**\n\n提升公众环保意识，带动绿色就业，共建美丽长江")
    with col3:
        st.warning("💰 **经济价值**\n\n环保数据服务，生态旅游衍生收益，可持续发展")

# ==================== 水质监测中心 ====================
elif page == "💧 水质监测中心":
    st.markdown('<p class="section-title">💧 智能水质监测系统</p >', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">📊 平均pH</div><div class="metric-value">7.3</div><div style="color:#44ff44;">正常范围 6.5-8.5</div></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">💨 平均溶解氧</div><div class="metric-value">6.7 mg/L</div><div style="color:#44ff44;">≥5.0 达标</div></div>',
            unsafe_allow_html=True)
    with col3:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">🏆 Ⅰ类水质占比</div><div class="metric-value">20%</div><div style="color:#ffaa00;">目标提升至 35%</div></div>',
            unsafe_allow_html=True)

    st.markdown("### 📋 实时监测数据")
    st.dataframe(water_data, use_container_width=True)

    # 水质趋势模拟
    trend_data = pd.DataFrame({
        "日期": pd.date_range(start="2025-03-01", periods=30, freq="D"),
        "溶解氧": [6.2 + i * 0.03 for i in range(30)],
        "pH": [7.1 + i * 0.01 for i in range(30)]
    })
    fig = px.line(trend_data, x="日期", y=["溶解氧", "pH"], title="水质指标趋势（近30天）")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cccccc")
    st.plotly_chart(fig, use_container_width=True)

# ==================== 鱼类修复中心 ====================
elif page == "🐟 鱼类修复中心":
    st.markdown('<p class="section-title">🐟 长江鱼类生态修复系统</p >', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 种群恢复趋势")
        fig = px.area(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                      title="鱼类资源总量变化",
                      color_discrete_sequence=["#00ffff", "#ffaa00"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cccccc")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎣 近期放流活动")
        st.success("**2025年3月**\n\n宜昌段放流四大家鱼 30 万尾")
        st.success("**2025年2月**\n\n武汉段放流中华鲟 500 尾")
        st.success("**2025年1月**\n\n南京段放流珍稀鱼类 2000 尾")

        st.markdown("### 📋 修复项目进度")
        st.progress(68, text="鱼类栖息地修复工程")
        st.progress(45, text="产卵场生态重建")

# ==================== 科普教育平台 ====================
elif page == "📚 科普教育平台":
    st.markdown('<p class="section-title">📚 长江生态智慧科普平台</p >', unsafe_allow_html=True)

    articles = [
        {"title": "长江十年禁渔成效显著", "date": "2025-03-15",
         "content": "自2021年长江十年禁渔全面实施以来，长江流域鱼类资源显著恢复。监测数据显示，江豚种群数量从2017年的1012头增加到2024年的1249头，实现了历史性转折。四大家鱼产卵量同比增长超过30%。"},
        {"title": "水质监测技术新突破", "date": "2025-03-10",
         "content": "新型智能水质监测传感器可实现pH值、溶解氧、浊度、氨氮等多项指标实时监测，数据每15分钟上传一次，精度达到实验室级别。该技术已在宜昌、武汉等5个城市试点应用。"},
        {"title": "鱼类增殖放流活动启动", "date": "2025-03-05",
         "content": "2025年春季增殖放流活动在宜昌启动，计划放流四大家鱼100万尾、中华鲟2000尾。活动现场有200余名志愿者参与，共同见证长江生态修复的重要时刻。"},
    ]

    for article in articles:
        with st.expander(f"📄 {article['title']} ({article['date']})"):
            st.write(article["content"])

    st.markdown("### 🎥 科普视频推荐")
        # 使用 HTML iframe 嵌入视频，兼容性更好
    # 注意：我们将 watch?v= 后面的 ID 提取出来，放入 embed 链接中
    # --- 视频部分 ---
    # ==========================================
    # 第一部分：科普视频推荐（放在设置判断之前）
    # ==========================================
    video_html_1 = """
    <div style="text-align: center; margin: 20px 0;">
        <iframe 
            src="//player.bilibili.com/player.html?isOutside=true&aid=255524604&bvid=BV1TY411E7JV&cid=572934280&p=1" 
            scrolling="no" 
            border="0" 
            frameborder="no" 
            framespacing="0" 
            allowfullscreen="true"
            style="width: 100%; height: 500px; max-width: 800px;">
        </iframe>
    </div>
    """
    st.markdown(video_html_1, unsafe_allow_html=True)
    st.markdown("### 📺 科普视频推荐")
    
    # ==========================================
    # 1. 科普视频区域 (主页面内容)
    # ==========================================
    video_html = """
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <iframe
            src="//player.bilibili.com/player.html?isOutside=true&aid=112844863506780&bvid=BV1ebe9epEYX&cid=500001626552220&p=1"
            scrolling="no"
            border="0"
            frameborder="no"
            framespacing="0"
            allowfullscreen="true"
            width="800"
            height="450">
        </iframe>
    </div>
    """
    # 注意：这里只保留一次渲染
    
    st.markdown(video_html, unsafe_allow_html=True)

# ==========================================
# 2. 互动问答区域 (属于主页面)
# ==========================================
st.markdown("### 🙋 互动问答")
question = st.text_input("你有什么关于长江生态保护的问题？")
if question:
    st.success("感谢提问！问题已记录，专家会尽快回复。")

# ==========================================
# 3. 数据分析报告 (elif 分支)
# ==========================================
elif page == "📊 数据分析报告":
    st.markdown('<p class="section-title">📊 深度数据分析报告</p>', unsafe_allow_html=True)
    st.subheader("🐟 水质与鱼类相关性分析")
    st.write("通过皮尔逊相关系数分析，我们发现溶解氧含量与鱼类种群数量呈强正相关。")
    st.info("此处展示相关性热力图或散点图...")
    st.markdown('<p class="section-title">📊 深度数据分析报告</p>', unsafe_allow_html=True)

    st.subheader("📉 水质与鱼类相关性分析")
    st.write("通过皮尔逊相关系数分析，我们发现溶解氧含量与鱼类种群数量呈强正相关。")

    # 这里可以放一些图表
    st.info("此处展示相关性热力图或散点图...")

# ================================== 新增：系统设置 ==================================
elif page == "⚙️ 系统设置":
    st.markdown('<p class="section-title">⚙️ 系统全局设置</p>', unsafe_allow_html=True)

    st.toggle("开启实时报警推送")
    st.slider("设置数据刷新频率（分钟）", 1, 60, 5)
    st.markdown('<p class="section-title">...', unsafe_allow_html=True)

    # ✅ 在这里粘贴滑块
    brightness = st.slider("调节背景亮度", 0, 100, st.session_state.brightness)
    st.session_state.brightness = brightness

    st.toggle("开启实时报警推送")
    # ... 其他设置 ...
   
