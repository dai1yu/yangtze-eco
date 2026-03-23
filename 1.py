import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# 页面配置
st.set_page_config(page_title="长江生态保护平台", page_icon="🌊", layout="wide")

# ==================== 侧边栏导航 ====================
st.sidebar.title("🌿 长江生态保护平台")
page = st.sidebar.radio("导航", ["🏠 首页", "💧 水质监测", "🐟 鱼类修复", "📚 生态科普", "👥 团队介绍"])

# ==================== 模拟数据（假数据，后期换成真实数据）====================
# 水质监测数据
water_data = pd.DataFrame({
    "监测点": ["宜昌", "武汉", "南京", "上海", "岳阳"],
    "pH值": [7.2, 7.5, 7.1, 7.3, 7.4],
    "溶解氧(mg/L)": [6.8, 6.5, 6.9, 6.7, 6.6],
    "浊度(NTU)": [12, 15, 11, 14, 13],
    "水质等级": ["II类", "II类", "I类", "II类", "II类"]
})

# 鱼类种群趋势数据
fish_data = pd.DataFrame({
    "年份": [2020, 2021, 2022, 2023, 2024, 2025],
    "四大家鱼(万尾)": [120, 135, 150, 170, 195, 220],
    "珍稀鱼类(万尾)": [8, 10, 13, 17, 22, 28]
})

# 科普文章数据
articles = [
    {"title": "长江十年禁渔成效显著", "summary": "禁渔以来，江豚数量首次止跌回升...", "date": "2025-03-15"},
    {"title": "水质监测技术新突破", "summary": "智能传感器实时监测pH、溶解氧...", "date": "2025-03-10"},
    {"title": "鱼类增殖放流活动启动", "summary": "今年计划放流四大家鱼100万尾...", "date": "2025-03-05"},
]

# ==================== 首页 ====================
if page == "🏠 首页":
    st.title("🌊 长江生态保护平台")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 监测点位", "50+", "新增10个")
    with col2:
        st.metric("🐟 鱼类恢复率", "+32%", "近3年")
    with col3:
        st.metric("🌿 水质达标率", "94%", "提升8%")

    st.markdown("### 📖 项目背景")
    st.write("""
    长江是中华民族的母亲河，但长期面临水污染、生物多样性下降等问题。
    本项目通过**智能水质监测终端**、**鱼类生态修复系统**和**智慧科普平台**，
    构建长江生态保护一体化解决方案，助力长江大保护战略。
    """)

    st.markdown("### 🎯 核心价值")
    st.write("- **生态效益**：恢复鱼类种群，提升水质达标率")
    st.write("- **社会价值**：提升公众环保意识，带动绿色就业")
    st.write("- **经济价值**：环保数据服务、生态旅游衍生收益")

# ==================== 水质监测 ====================
elif page == "💧 水质监测":
    st.title("💧 智能水质监测系统")

    st.markdown("### 📊 实时监测数据")
    st.dataframe(water_data, use_container_width=True)

    # 水质趋势图（模拟）
    st.markdown("### 📈 水质指标趋势")
    trend_data = pd.DataFrame({
        "日期": pd.date_range(start="2025-01-01", periods=30, freq="D"),
        "溶解氧": np.random.uniform(6.0, 7.5, 30),
        "pH": np.random.uniform(7.0, 7.8, 30)
    })
    fig = px.line(trend_data, x="日期", y=["溶解氧", "pH"], title="主要水质指标变化趋势")
    st.plotly_chart(fig, use_container_width=True)

    st.info("🔍 数据说明：实时数据来自智能监测终端，每15分钟更新一次")

# ==================== 鱼类修复 ====================
elif page == "🐟 鱼类修复":
    st.title("🐟 长江鱼类生态修复系统")

    st.markdown("### 📈 鱼类种群恢复趋势")
    fig = px.bar(fish_data, x="年份", y=["四大家鱼(万尾)", "珍稀鱼类(万尾)"],
                 title="主要鱼类种群数量变化", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🎣 近期放流活动")
    col1, col2 = st.columns(2)
    with col1:
        st.success("**2025年3月**\n\n宜昌段放流四大家鱼30万尾")
    with col2:
        st.success("**2025年2月**\n\n武汉段放流中华鲟500尾")

    st.markdown("### 📋 修复项目进度")
    st.progress(68, text="鱼类栖息地修复工程 - 68%")
    st.progress(45, text="产卵场生态重建 - 45%")

# ==================== 生态科普 ====================
elif page == "📚 生态科普":
    st.title("📚 长江生态智慧科普平台")

    st.markdown("### 📰 最新科普文章")
    for article in articles:
        with st.expander(f"📄 {article['title']} ({article['date']})"):
            st.write(article["summary"])
            st.button("阅读全文", key=article["title"])

    st.markdown("### 🎥 科普视频推荐")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # 替换成真实视频链接

    st.markdown("### 💬 互动问答")
    question = st.text_input("你有什么关于长江生态保护的问题？")
    if question:
        st.success("感谢提问！我们的专家会尽快回复你。")

# ==================== 团队介绍 ====================
elif page == "👥 团队介绍":
    st.title("👥 项目团队")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("改")
        st.write("项目负责人 | 环境工程博士")
        st.write("5年水环境治理经验")
    with col2:
        st.subheader("改")
        st.write("技术总监 | 物联网专家")
        st.write("智能硬件开发经验")
    with col3:
        st.subheader("改")
        st.write("运营总监 | 生态学硕士")
        st.write("科普教育推广经验")

    st.markdown("### 🤝 合作资源")
    st.write("- 长江水利委员会（技术支持）")
    st.write("- 中科院水生所（科研合作）")
    st.write("- 阿拉善SEE生态协会（公益支持）")

    st.markdown("### 📞 联系方式")
    st.write("邮箱：改")
    st.write("电话：改")