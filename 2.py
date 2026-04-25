import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
   # 如果你需要模拟最近30天的数据（为了防止报错，先加这一段）：
import pandas as pd
import numpy as np
   

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
    st.markdown('<p class="section-title">💧 智能水质监测系统</p>', unsafe_allow_html=True)

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

    # 生成近30天水质趋势数据
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    trend_data = pd.DataFrame({
        "日期": dates,
        "溶解氧": np.random.uniform(6.0, 8.5, 30),
        "pH": np.random.uniform(7.0, 8.0, 30)
    })
    
    # 绘制趋势图
    fig = px.line(
        trend_data,
        x="日期",
        y=["溶解氧", "pH"],
        title="水质指标趋势（近30天）",
        markers=True,
        color_discrete_map={"溶解氧": "#00ffff", "pH": "#ffaa00"}
    )
    
    # 图表样式美化
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#cccccc",
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickformat="%m月%d日"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_traces(line_width=3)
    st.plotly_chart(fig, use_container_width=True)
   # 生成基础折线图
# --- 1. 先准备数据（这是你漏掉的一步） ---
# 假设你的总数据表叫 water_data，我们需要筛选出最近的数据或者模拟一下
# 如果你的 water_data 里已经有足够的数据，直接用：
# trend_data = water_data  <-- 如果你的数据本身就是最近的，直接用这句





# --------------------------
# 1. 更新到2026年的鱼类数据（带合理增长趋势）
# --------------------------
fish_data = pd.DataFrame({
    "年份": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
    "四大家鱼(万尾)": [120, 135, 150, 170, 195, 230, 270],
    "珍稀鱼类(万尾)": [10, 15, 20, 25, 30, 38, 48],
    "洄游性鱼类(万尾)": [20, 25, 30, 35, 40, 52, 68],
    "底栖鱼类(万尾)": [30, 35, 40, 45, 50, 65, 82]
})


# ==================== 鱼类修复中心 ====================
if page == "🐟 鱼类修复中心":
    st.markdown('<p class="section-title">🐟 长江鱼类生态修复系统</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 种群恢复趋势")
        fig = px.area(
            fish_data,
            x="年份",
            y=["四大家鱼(万尾)", "珍稀鱼类(万尾)", "洄游性鱼类(万尾)", "底栖鱼类(万尾)"],
            title="鱼类资源总量变化（2020-2026）",
            color_discrete_sequence=["#00ffff", "#ffaa00", "#00ff00", "#ff6699"]
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#cccccc",
            legend_title="鱼类类别",
            xaxis=dict(tickmode="linear", dtick=1)  # 让年份按1年间隔显示
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏙️ 近期放流活动")
        st.success("**2026年3月20日**\n\n宜昌段**春季增殖放流：投放四大家鱼 45 万尾**，配套投放滤食性鱼类（鲢、鳙）净化水质。")
        st.success("**2026年3月5日**\n\n荆州段**珍稀鱼类放流：中华鲟 800 尾**（全人工繁殖子二代）、**长江江豚 10 头**（迁地保护后野化放归）。")
        st.success("**2026年2月14日**\n\n武汉段**洄游性鱼类放流：胭脂鱼 1.2 万尾**、**长吻鮠 5000 尾**，恢复洄游通道生态。")
        st.success("**2026年1月25日**\n\n南京段**底栖鱼类放流：铜鱼 3 万尾**、**鳊鱼 2 万尾**，修复底栖生物链。")
        st.success("**2026年1月10日**\n\n上海段**河口鱼类放流：刀鲚 5 万尾**、**凤鲚 3 万尾**，助力河口渔业资源恢复。")

    st.markdown("### 🏗️ 修复项目进度")
    st.progress(75, text="**鱼类栖息地修复工程**（已完成75%，新增人工鱼巢 500 处）")
    st.progress(55, text="**产卵场生态重建**（已完成55%，修复产卵场面积 200 公顷）")
    st.progress(40, text="**洄游通道畅通工程**（已完成40%，拆除小型坝闸 12 座）")
    st.progress(60, text="**珍稀物种保育计划**（已完成60%，人工繁育珍稀鱼类 10 万尾）")


# ==================== 科普教育平台 ====================
elif page == "📚 科普教育平台":
    st.markdown('<p class="section-title">📚 长江生态智慧科普平台</p >', unsafe_allow_html=True)

    articles = [
    {
        "title": "长江江豚种群数量实现历史性逆转",
        "date": "2026-01-15",
        "content": "据农业农村部最新发布的2025年度长江全流域生态监测报告显示，长江江豚种群数量已稳定回升至1500头以上，较2026年首次突破1000头大关具有里程碑意义。报告指出，随着十年禁渔的深入推进，长江干流及洞庭湖、鄱阳湖的水域生态环境显著改善，江豚栖息地质量大幅提升，目击频率较五年前增加了40%。"
    },
    {
        "title": "数字孪生长江系统全面上线运行",
        "date": "2026-02-20",
        "content": "长江水利委员会宣布，历时三年建设的'数字孪生长江'核心系统正式投入业务化运行。该系统利用卫星遥感、水下声呐及AI大数据模型，实现了对长江流域水雨情、工情、险情的毫秒级实时推演。在刚刚过去的2026年汛前准备中，该系统成功预测了上游三次洪峰过程，为流域防洪调度提供了精准的数字化支撑。"
    },
    {
        "title": "中华鲟全人工繁殖技术取得重大突破",
        "date": "2026-03-10",
        "content": "中国长江三峡集团中华鲟研究所传来喜讯，2026年春季中华鲟全人工繁殖工作圆满结束，成功培育子二代幼苗超过5万尾，存活率创下历史新高。科研人员首次成功应用了新型激素诱导技术，解决了子二代亲本性腺发育不同步的世界级难题，这标志着长江珍稀特有鱼类的种质资源保护迈上了新台阶。"
    }
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
# 3. 数据分析报告 (elif 分支)
# ==========================================
elif page == "📊 数据分析报告":
    st.markdown('<p class="section-title">📊 深度数据分析报告</p>', unsafe_allow_html=True)

    # 1. 关键指标看板 (使用列布局)
    st.subheader("📈 核心生态指标")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="平均溶解氧 (mg/L)", value="6.8", delta="1.2 ↗️")
    with col2:
        st.metric(label="监测到的鱼类种类", value="42 种", delta="3 种 ↗️")
    with col3:
        st.metric(label="水质综合评分", value="85", delta="良好")

    st.divider()

    # 2. 深度分析部分
    st.subheader("🔬 溶解氧与鱼类多样性相关性分析")

    # 这里使用两列布局：左边放图，右边放文字结论
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("##### 数据分布散点图")
        # 模拟生成一些数据用于展示 (实际项目中请使用你的真实数据 df)
        import numpy as np
        import pandas as pd
        import altair as alt

        # 生成模拟数据
        chart_data = pd.DataFrame({
            '溶解氧': np.random.uniform(4, 10, 50),
            '鱼类数量': np.random.uniform(10, 60, 50)
        })

        # 使用 Altair 绘制散点图 (Streamlit 原生图表也可以，Altair 更美观)
        scatter_chart = alt.Chart(chart_data).mark_circle(size=60).encode(
            x='溶解氧',
            y='鱼类数量',
            color='鱼类数量',
            tooltip=['溶解氧', '鱼类数量']
        ).interactive()

        st.altair_chart(scatter_chart, use_container_width=True)

    with c2:
        st.markdown("##### 分析结论")
        st.info("""
        - **正相关性强**：数据显示，随着溶解氧含量的提升，鱼类物种丰富度呈现明显的上升趋势。
        - **关键阈值**：当溶解氧低于 **5mg/L** 时，鱼类数量显著减少。
        - **建议**：应重点监测枯水期的溶解氧水平，以保护敏感鱼类种群。
        """)

    st.divider()

    # 3. 保留你之前的互动问答 (记得保持缩进！)
    st.markdown("### 🗣️ 互动问答")
    question = st.text_input("你有什么关于长江生态保护的问题？")
    if question:
        st.success("感谢提问！问题已记录，专家会尽快回复。")


# ================================== 新增：系统设置 ==================================
elif page == "⚙️ 系统设置":
    st.markdown('<p class="section-title">⚙️ 系统全局设置</p>', unsafe_allow_html=True)

   
    st.slider("设置数据刷新频率（分钟）", 1, 60, 5)
   
    st.toggle("开启实时报警推送")
    st.markdown('<p class="section-title">亮度设置', unsafe_allow_html=True)

    # ✅ 在这里粘贴滑块
    brightness = st.slider("调节背景亮度", 0, 100, 91)
    st.session_state.brightness = brightness

    # ... 其他设置 ...
   
