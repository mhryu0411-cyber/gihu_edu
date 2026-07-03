import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from utils.sample_data import (
    STATIONS, AIRMASSES, get_monthly_strength,
    get_sample_station_data, SEASON_NAMES,
)

# 1. 페이지 및 멀티페이지 네비게이션 설정 (★ 메뉴 실종 버그 완벽 해결 영역 ★)
# 원래 사용하시던 다른 페이지(해수면, 구름 등)의 정확한 파일명을 아래 'pages/파일명.py' 자리에 적어주세요.
pages = {
    "기후 탐구 대시보드": [
        st.Page(__file__, title="한반도의 사계절 기단", icon="🌏"), # 현재 이 페이지의 이름을 변경
        st.Page("pages/해수면.py", title="해수면 변화 분석", icon="🌊"), # 예시 (실제 파일명으로 수정)
        st.Page("pages/구름.py", title="구름 및 강수량", icon="☁️"),   # 예시 (실제 파일명으로 수정)
    ]
}
pg = st.navigation(pages)
pg.run()

# 2. 나눔고딕 반영 및 상단바 제거 커스텀 CSS
st.markdown("""
<style>
    /* 폰트: 나눔고딕 전체 강제 적용 */
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .stApp, * {
        font-family: 'Nanum Gothic', sans-serif !important;
    }
    
    /* 상단 기본 헤더(깃허브 로고, 메뉴 등) 완전히 숨기기 */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 메인 타이틀 디자인 */
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E40AF, #EF4444, #F59E0B, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        margin-top: 1rem;
        letter-spacing: -0.03em;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    
    /* 사이드바 은은하고 부드러운 그라데이션 적용 */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #EDF2F7 0%, #F7FAFC 100%) !important;
    }
    
    /* 카드형 컨테이너 보더 및 섀도우 마감 */
    div[data-testid="stContainer"] {
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        padding: 1.2rem !important;
    }
    
    /* 섹션 헤더 좌측 바 포인트 */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
        border-left: 4px solid #2563EB;
        padding-left: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. 사이드바 내용 구성 (쉬운 설명 모드 토글 완전 삭제)
with st.sidebar:
    st.markdown("### 📖 기단(Air Mass)이란?")
    # 기본적으로 상세한 설명(상세 모드)만 나오도록 고정
    st.info("**기단(氣團)**은 수평 방향으로 기온·습도 등의 물리적 성질이 거의 균일한 대규모 공기 덩어리입니다. 발원지의 위도와 지표면 특성에 따라 분류됩니다.")

# 4. 메인 대시보드 상단 헤더
st.markdown('<div class="main-title">한반도의 사계절 기단</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">슬라이더를 움직여 계절마다 어떤 기단이 한반도에 영향을 미치는가 탐구해 보세요!</div>', unsafe_allow_html=True)

# 5. 메인 컨트롤러 슬라이더
month = st.slider(
    "📅 분석할 월을 선택하세요 (1월~12월)",
    min_value=1, max_value=12, value=1,
    format="%d월"
)

# 데이터 바인딩
season = SEASON_NAMES[month]
strengths = get_monthly_strength(month)
station_df = get_sample_station_data(month)
dominant = max(strengths, key=strengths.get)
dom_info = AIRMASSES[dominant]

st.markdown(f"### 🗓️ {month}월 ({season}) — 현재 가장 우세한 기단: {dom_info['emoji']} **{dominant}**")
st.markdown("<br>", unsafe_allow_html=True)

# 6. 대시보드 3단 레이아웃
col_left, col_center, col_right = st.columns([1.3, 2.4, 1.3], gap="medium")

# [좌측] 기단 세력 그래프
with col_left:
    with st.container(border=True):
        st.markdown('<div class="section-header">📊 기단별 영향력 점유율</div>', unsafe_allow_html=True)
        for name, s in sorted(strengths.items(), key=lambda x: -x[1]):
            info = AIRMASSES[name]
            pct = int(s * 100)
            st.markdown(f"{info['emoji']} **{name}**")
            st.progress(s, text=f"{pct}%")

# [중앙] Folium 지도 시각화
with col_center:
    m = folium.Map(location=[36.3, 127.8], zoom_start=7, tiles="CartoDB positron", width="100%", height=530)

    # 관측소 매핑
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
                f"<b>{row['name']}</b><br>🌡️ {row['temp']}°C<br>💧 습도 {row['humidity']}%<br>🌬️ 풍속 {row['wind_speed']}m/s<br>🧭 풍향 {int(row['wind_dir'])}°",
                max_width=200
            ),
            tooltip=f"{row['name']} {row['temp']}°C {arrow}",
        ).add_to(m)

    # 기단 발원지 화살표 매핑
    for name, info in AIRMASSES.items():
        s = strengths[name]
        if s < 0.1:
            continue
        origin = info["origin"]
        folium.Marker(
            location=origin,
            icon=folium.DivIcon(html=f'<div style="font-size:{14+s*16}px; text-shadow: 1px 1px 2px white; text-align:center">{info["emoji"]}</div>'),
        ).add_to(m)
        
        if s > 0.2:
            folium.PolyLine(
                [origin, [36.5, 127.8]],
                color=info["color"],
                weight=int(2 + s * 8),
                opacity=min(s + 0.3, 0.9),
                dash_array="10" if s < 0.5 else None,
            ).add_to(m)

    st_folium(m, use_container_width=True, height=530, returned_objects=[])

# [우측] 우세 기단 상세분석
with col_right:
    with st.container(border=True):
        st.markdown(f'<div class="section-header">{dom_info["emoji"]} {dominant} 기단 정보</div>', unsafe_allow_html=True)
        
        # 상세 모드 설명문으로 고정 적용
        st.info(dom_info["desc_detail"])
        
        st.markdown(f"🧬 **기단의 성질:** {dom_info['property']}")
        st.markdown(f"🗂️ **지리적 분류:** {dom_info['type']}")
        st.markdown(f"🧭 **대표적인 바람:** {dom_info['wind_dir']}풍")

st.markdown("<br><hr>", unsafe_allow_html=True)

# 7. 하단 차트 섹션
st.markdown("### 📊 전국 기상 통계 및 기단 분석 그래프")

col_chart1, col_chart2 = st.columns(2, gap="large")
with col_chart1:
    sorted_df = station_df.sort_values("temp")
    colors = ["#3B82F6" if t <= 0 else "#60A5FA" if t <= 10 else "#FBBF24" if t <= 20 else "#F97316" if t <= 25 else "#EF4444" for t in sorted_df["temp"]]
    fig1 = go.Figure(go.Bar(
        x=sorted_df["temp"], y=sorted_df["name"],
        orientation="h", marker_color=colors,
        text=[f"{t}°C" for t in sorted_df["temp"]], textposition="outside",
    ))
    fig1.update_layout(
        title=f"📍 {month}월 주요 관측소 기온 분포", height=450,
        xaxis_title="기온 (°C)", yaxis_title="", margin=dict(l=0, r=40, t=50, b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    fig2 = go.Figure()
    for name, info in AIRMASSES.items():
        monthly = [get_monthly_strength(m)[name] * 100 for m in range(1, 13)]
        fig2.add_trace(go.Scatter(
            x=list(range(1, 13)), y=monthly,
            name=f"{info['emoji']} {name}",
            line=dict(color=info["color"], width=3),
            mode="lines+markers", marker=dict(size=6),
        ))
    fig2.add_vline(x=month, line_dash="dash", line_color="#64748B", line_width=2, annotation_text=f"현재 선택: {month}월")
    fig2.update_layout(
        title="📈 1년 주기 기단 세력 변동 추이", height=450,
        xaxis=dict(title="월", tickmode="array", tickvals=list(range(1,13)), ticktext=[f"{m}월" for m in range(1,13)]),
        yaxis_title="세력 영향도 (%)", margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(orientation="h", y=-0.2, x=0.05),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br><hr>", unsafe_allow_html=True)

# 8. 퀴즈 섹션
st.markdown("### 🧠 기후 원리 퀴즈 타임!")
with st.expander("💡 기단과 사계절에 대한 문제를 풀며 복습해보세요!", expanded=False):
    q_map = {
        1: ("겨울철 한반도에 매서운 한파와 삼한사온을 가져오는 기단은?", ["시베리아 기단","북태평양 기단","양쯔강 기단","오호츠크해 기단"], 0),
        2: ("초여름 장마전선(정체전선)은 주로 어떤 두 기단이 힘겨루기를 하며 형성되나요?", ["시베리아+양쯔강","오호츠크해+북태평양","양쯔강+적도","시베리아+오호츠크해"], 1),
        3: ("봄과 가을철에 유독 하늘이 맑고 건조한 날씨를 선사하는 기단은?", ["북태평양 기단","오호츠크해 기단","양쯔강 기단","적도 기단"], 2),
        4: ("막대한 에너지를 품고 우리에게 다가오는 '태풍'은 어느 기단의 고향과 관련이 깊을까요?", ["시베리아 기단","양쯔강 기단","적도 기단","오호츠크해 기단"], 2),
        5: ("한여름 숨 막히는 무더위와 밤잠을 설치게 하는 열대야의 주범이 되는 기단은?", ["양쯔강 기단","시베리아 기단","오호츠크해 기단","북태평양 기단"], 3),
    }
    for qnum, (q, opts, ans) in q_map.items():
        st.markdown(f"**Q{qnum}. {q}**")
        sel = st.radio("", opts, key=f"q{qnum}", index=None, label_visibility="collapsed")
        if sel:
            if opts.index(sel) == ans:
                st.success("🎉 완벽해요! 정답입니다.")
            else:
                st.error(f"아쉬워요! 정답은 **{opts[ans]}**입니다.")
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

# 9. 푸터 가독성 완화
st.markdown("<br>", unsafe_allow_html=True)
st.caption("🌏 한반도의 사계절 기단 시각화 시뮬레이터 | Designed for Premium UI | 나눔고딕 폰트 적용 완료")
