import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.sample_data import AIRMASSES, get_monthly_strength, get_sample_station_data, STATIONS

st.set_page_config(page_title="계절별 탐구", page_icon="🌸", layout="wide")

easy_mode = st.sidebar.toggle("😊 쉬운 설명 모드", value=True)

st.markdown("## 🌸 계절별 기단 탐구")

seasons = {
    "🌸 봄 (3~5월)": {"months": [3,4,5], "main": "양쯔강 기단",
        "easy": "봄에는 양쯔강 기단이 이동성 고기압을 몰고 와서 맑고 따뜻한 날이 많아요! 하지만 가끔 시베리아 기단이 찾아오면 꽃샘추위가 오기도 해요.",
        "detail": "봄철에는 양쯔강 기단에서 발원한 이동성 고기압이 주기적으로 통과하며 맑고 건조한 날씨를 가져옵니다. 시베리아 기단의 간헐적 남하로 꽃샘추위가 나타나며, 늦봄으로 갈수록 북태평양 기단의 세력이 점차 확장됩니다."},
    "☀️ 여름 (6~8월)": {"months": [6,7,8], "main": "북태평양 기단",
        "easy": "6월에는 오호츠크해 기단과 북태평양 기단이 만나서 장마가 시작돼요! 7~8월에는 북태평양 기단이 강해져서 무더운 여름이 찾아와요.",
        "detail": "초여름(6월)에는 오호츠크해 기단(mP)과 북태평양 기단(mT)이 한반도 부근에서 충돌하여 정체전선(장마전선)을 형성합니다. 7월 중순 이후 북태평양 고기압이 확장하면서 장마가 끝나고 고온 다습한 한여름 날씨가 지속됩니다."},
    "🍂 가을 (9~11월)": {"months": [9,10,11], "main": "양쯔강 기단",
        "easy": "가을에는 다시 양쯔강 기단이 찾아와서 맑고 시원한 날씨를 만들어줘요. 하늘이 높고 파란 '천고마비'의 계절이에요!",
        "detail": "가을에는 북태평양 기단이 후퇴하고 양쯔강 기단의 이동성 고기압이 다시 우세해집니다. 맑고 건조한 날씨가 지속되며, 늦가을로 갈수록 시베리아 기단의 영향이 증가합니다."},
    "⛄ 겨울 (12~2월)": {"months": [12,1,2], "main": "시베리아 기단",
        "easy": "겨울에는 시베리아에서 아주 차갑고 건조한 공기가 내려와요. 삼한사온이라고 해서, 3일은 춥고 4일은 따뜻한 패턴이 반복돼요!",
        "detail": "겨울철에는 시베리아 고기압에서 확장한 한랭 건조한 cP 기단이 한반도를 지배합니다. 약 3~4일 주기로 기단이 강약을 반복하며 삼한사온 현상이 나타납니다. 서해안 지역은 해기차(해수면-기온 차이)로 인한 대설이 발생하기도 합니다."},
}

tabs = st.tabs(list(seasons.keys()))

for tab, (season_name, info) in zip(tabs, seasons.items()):
    with tab:
        desc = info["easy"] if easy_mode else info["detail"]
        main_am = AIRMASSES[info["main"]]
        st.info(f"{main_am['emoji']} **대표 기단: {info['main']}** ({main_am['property']})")
        st.markdown(desc)

        col1, col2 = st.columns(2)
        with col1:
            months = info["months"]
            all_data = []
            for m in months:
                df = get_sample_station_data(m)
                df["month"] = f"{m}월"
                all_data.append(df)
            combined = __import__("pandas").concat(all_data)
            fig = px.box(combined, x="month", y="temp", color="month",
                         title=f"{season_name.split('(')[0].strip()} 전국 기온 분포",
                         labels={"temp":"기온 (°C)","month":"월"})
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = go.Figure()
            for m in months:
                strengths = get_monthly_strength(m)
                names = list(strengths.keys())
                vals = list(strengths.values())
                fig2.add_trace(go.Bar(name=f"{m}월", x=names, y=[v*100 for v in vals]))
            fig2.update_layout(title="월별 기단 세력 비교", barmode="group",
                               yaxis_title="세력 (%)", height=400)
            st.plotly_chart(fig2, use_container_width=True)
