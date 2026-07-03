import streamlit as st

st.set_page_config(
    page_title="한반도의 사계절과 기단",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #3B82F6, #EF4444, #F59E0B, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .airmass-card {
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        margin-bottom: 0.5rem;
        text-align: center;
        transition: transform 0.2s;
    }
    .airmass-card:hover { transform: scale(1.03); }
    .stSlider > div { padding: 0 1rem; }
</style>
""", unsafe_allow_html=True)

import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from utils.sample_data import (
    STATIONS, AIRMASSES, get_monthly_strength,
    get_sample_station_data, SEASON_NAMES,
)

st.markdown('<div class="main-title">🌏 한반도의 사계절과 기단</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">슬라이더를 움직여 계절마다 어떤 기단이 한반도에 영향을 미치는지 알아보세요!</div>', unsafe_allow_html=True)

easy_mode = st.sidebar.toggle("😊 쉬운 설명 모드", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 기단이란?")
if easy_mode:
    st.sidebar.info("**기단**은 넓은 지역에 걸쳐 비슷한 온도와 습도를 가진 커다란 공기 덩어리예요! 계절마다 다른 기단이 한반도로 찾아와서 날씨가 바뀐답니다. 🌈")
else:
    st.sidebar.info("**기단(氣團, Air Mass)**은 수평 방향으로 기온·습도 등의 물리적 성질이 거의 균일한 대규모 공기 덩어리입니다. 발원지의 위도(한대/열대)와 지표면 특성(대륙/해양)에 따라 분류됩니다.")

month = st.slider(
    "📅 월을 선택하세요 (1월~12월)",
    min_value=1, max_value=12, value=1,
    format="%d월"
)
season = SEASON_NAMES[month]
strengths = get_monthly_strength(month)
station_df = get_sample_station_data(month)

dominant = max(strengths, key=strengths.get)
dom_info = AIRMASSES[dominant]

st.markdown(f"### 🗓️ {month}월 ({season}) — 현재 가장 강한 기단: {dom_info['emoji']} **{dominant}**")

col_left, col_center, col_right = st.columns([1.2, 2.5, 1.2])

with col_center:
    m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles="CartoDB positron",
                   width="100%", height=520)

    for _, row in station_df.iterrows():
        t = row["temp"]
        if t <= 0: color = "#3B82F6"
        elif t <= 10: color = "#60A5FA"
        elif t <= 20: color = "#FBBF24"
        elif t <= 25: color = "#F97316"
        else: color = "#EF4444"

        wd = row["wind_dir"]
        arrows = {0: "↓", 45: "↙", 90: "←", 135: "↖", 180: "↑", 225: "↗", 270: "→", 315: "↘"}
        closest = min(arrows.keys(), key=lambda x: min(abs(wd-x), 360-abs(wd-x)))
        arrow = arrows[closest]

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color, fill=True, fill_color=color, fill_opacity=0.8,
            popup=folium.Popup(
                f"<b>{row['name']}</b><br>"
                f"🌡️ {row['temp']}°C<br>"
                f"💧 습도 {row['humidity']}%<br>"
                f"🌬️ 풍속 {row['wind_speed']}m/s<br>"
                f"🧭 풍향 {int(row['wind_dir'])}°",
                max_width=200
            ),
            tooltip=f"{row['name']} {row['temp']}°C {arrow}",
        ).add_to(m)

    for name, info in AIRMASSES.items():
        s = strengths[name]
        if s < 0.1:
            continue
        origin = info["origin"]
        folium.Marker(
            location=origin,
            icon=folium.DivIcon(html=f'<div style="font-size:{14+s*16}px;text-align:center">{info["emoji"]}</div>'),
        ).add_to(m)
        if s > 0.2:
            folium.PolyLine(
                [origin, [36.5, 127.8]],
                color=info["color"],
                weight=int(1 + s * 7),
                opacity=min(s + 0.2, 0.9),
                dash_array="10" if s < 0.5 else None,
            ).add_to(m)

    st_folium(m, use_container_width=True, height=520, returned_objects=[])

with col_left:
    st.markdown("#### 📊 기단 세력")
    for name, s in sorted(strengths.items(), key=lambda x: -x[1]):
        info = AIRMASSES[name]
        pct = int(s * 100)
        bar_color = info["color"]
        st.markdown(
            f"{info['emoji']} **{name}**"
        )
        st.progress(s, text=f"{pct}%")

with col_right:
    st.markdown(f"#### {dom_info['emoji']} {dominant}")
    desc = dom_info["desc_easy"] if easy_mode else dom_info["desc_detail"]
    st.info(desc)
    st.markdown(f"- **성질:** {dom_info['property']}")
    st.markdown(f"- **분류:** {dom_info['type']}")
    st.markdown(f"- **주요 바람:** {dom_info['wind_dir']}풍")

st.markdown("---")
st.markdown("### 🌡️ 전국 관측소 데이터")

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    sorted_df = station_df.sort_values("temp")
    colors = ["#3B82F6" if t <= 0 else "#60A5FA" if t <= 10 else "#FBBF24" if t <= 20 else "#F97316" if t <= 25 else "#EF4444" for t in sorted_df["temp"]]
    fig1 = go.Figure(go.Bar(
        x=sorted_df["temp"], y=sorted_df["name"],
        orientation="h", marker_color=colors,
        text=[f"{t}°C" for t in sorted_df["temp"]], textposition="outside",
    ))
    fig1.update_layout(title=f"{month}월 전국 기온", height=450,
                       xaxis_title="기온 (°C)", yaxis_title="", margin=dict(l=0,r=40,t=40,b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    fig2 = go.Figure()
    for name, info in AIRMASSES.items():
        monthly = [get_monthly_strength(m)[name] * 100 for m in range(1, 13)]
        fig2.add_trace(go.Scatter(
            x=list(range(1, 13)), y=monthly,
            name=f"{info['emoji']} {name}",
            line=dict(color=info["color"], width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
    fig2.add_vline(x=month, line_dash="dash", line_color="gray", annotation_text=f"{month}월")
    fig2.update_layout(title="연간 기단 세력 변화", height=450,
                       xaxis=dict(title="월", tickmode="array", tickvals=list(range(1,13)), ticktext=[f"{m}월" for m in range(1,13)]),
                       yaxis_title="세력 (%)", margin=dict(l=0,r=0,t=40,b=0),
                       legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("### 🧠 퀴즈 타임!")
with st.expander("문제를 풀어보세요!", expanded=False):
    q_map = {
        1: ("겨울철 한반도에 한파를 가져오는 기단은?", ["시베리아 기단","북태평양 기단","양쯔강 기단","오호츠크해 기단"], 0),
        2: ("장마전선은 어떤 두 기단이 만나서 형성되나요?", ["시베리아+양쯔강","오호츠크해+북태평양","양쯔강+적도","시베리아+오호츠크해"], 1),
        3: ("봄·가을에 맑고 건조한 날씨를 가져오는 기단은?", ["북태평양 기단","오호츠크해 기단","양쯔강 기단","적도 기단"], 2),
        4: ("태풍은 어떤 기단과 관련이 있나요?", ["시베리아 기단","양쯔강 기단","적도 기단","오호츠크해 기단"], 2),
        5: ("한여름 무더위와 열대야의 원인이 되는 기단은?", ["양쯔강 기단","시베리아 기단","오호츠크해 기단","북태평양 기단"], 3),
    }
    for qnum, (q, opts, ans) in q_map.items():
        st.markdown(f"**Q{qnum}. {q}**")
        sel = st.radio("", opts, key=f"q{qnum}", index=None, label_visibility="collapsed")
        if sel:
            if opts.index(sel) == ans:
                st.success("🎉 정답이에요!")
            else:
                st.error(f"아쉬워요! 정답은 **{opts[ans]}**이에요.")

st.markdown("---")
st.caption("🌏 한반도의 사계절과 기단 | 기상자료개방포털 API 활용 | 기후변화원리사이트")
