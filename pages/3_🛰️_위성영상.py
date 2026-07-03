import streamlit as st
from utils.sample_data import AIRMASSES, SEASON_NAMES, get_monthly_strength

st.set_page_config(page_title="위성영상", page_icon="🛰️", layout="wide")

easy_mode = st.sidebar.toggle("😊 쉬운 설명 모드", value=True)

st.markdown("## 🛰️ 위성영상 — 천리안 2A호로 보는 기단")

if easy_mode:
    st.info("천리안 2A호는 우리나라가 쏘아 올린 기상위성이에요! 우주에서 구름 사진을 찍어 보내주는데, 이 사진을 보면 기단이 어디에 있는지 알 수 있어요.")
else:
    st.info("천리안위성 2A호(GK-2A)의 적외·가시 채널 영상을 통해 기단의 분포, 전선의 위치, 구름 패턴을 관측할 수 있습니다. 기상자료개방포털 위성 API를 통해 영상을 조회합니다.")

st.markdown("### 🔗 위성영상 API 연동 안내")
st.warning("⚠️ 천리안 2A호 위성영상을 표시하려면 기상자료개방포털에서 API 인증키를 발급받아 `utils/api_client.py`에 입력해주세요.")

st.markdown("---")
st.markdown("### 📚 계절별 위성영상에서 보이는 특징")

season_satellite = {
    "❄️ 겨울": {
        "features": [
            "시베리아 고기압에서 불어오는 찬 공기가 서해를 지나며 구름띠(대류운) 형성",
            "서해안 지역에 눈구름이 발달하는 모습 관찰 가능",
            "대륙은 맑고 해양에 구름이 줄지어 나타남",
        ],
        "tip_easy": "겨울 위성사진에서 서해에 줄무늬 구름이 보이면, 시베리아에서 찬바람이 오고 있다는 뜻이에요!",
        "tip_detail": "한랭기류가 상대적으로 따뜻한 서해 해면을 지나면서 해기차(海氣差)에 의한 대류가 발생하여 구름줄이 형성됩니다.",
    },
    "🌸 봄": {
        "features": [
            "이동성 고기압 통과 시 한반도 전체가 맑게 보임",
            "중국에서 황사 발원 시 누런 먼지층 관찰 가능",
            "저기압 통과 시 나선형 구름 패턴",
        ],
        "tip_easy": "봄에 한반도가 깨끗하게 보이는 날은 양쯔강 기단 덕분이에요! 누렇게 보이면 황사가 온 거예요.",
        "tip_detail": "이동성 고기압의 하강기류로 구름이 소산되어 위성영상에서 한반도 지형이 명확하게 관측됩니다.",
    },
    "🌧️ 장마/여름": {
        "features": [
            "장마전선이 동서 방향으로 길게 걸쳐 있는 구름대 관찰",
            "장마전선 남북 이동을 며칠에 걸쳐 추적 가능",
            "태풍 접근 시 나선형 구름 구조가 뚜렷하게 보임",
        ],
        "tip_easy": "여름에 한반도를 가로지르는 긴 구름띠가 보이면 그게 바로 장마전선이에요! 오호츠크해 기단과 북태평양 기단이 부딪히는 곳이랍니다.",
        "tip_detail": "정체전선(장마전선)은 mP와 mT 기단의 경계에서 형성되며, 위성 적외영상에서 동서 방향의 밝은 구름대로 관측됩니다.",
    },
    "🍂 가을": {
        "features": [
            "이동성 고기압 영향으로 맑은 날이 많아 한반도가 선명하게 보임",
            "태풍 접근 시 위성영상으로 경로 추적 가능",
            "늦가을 시베리아 기단 남하 시 서해 구름줄 재출현",
        ],
        "tip_easy": "가을에는 하늘이 맑아서 위성사진에 한반도가 아주 예쁘게 보여요! 🍁",
        "tip_detail": "양쯔강 기단의 이동성 고기압이 우세하여 광범위한 쾌청 구역이 관측됩니다.",
    },
}

for season, info in season_satellite.items():
    with st.expander(season, expanded=False):
        for f in info["features"]:
            st.markdown(f"- {f}")
        tip = info["tip_easy"] if easy_mode else info["tip_detail"]
        st.success(f"💡 {tip}")

st.markdown("---")
st.markdown("### 🎯 위성영상 읽기 연습")
st.markdown("아래 상황에서 위성영상은 어떤 모습일지 상상해보세요!")

situations = [
    ("1월, 시베리아 기단이 강하게 남하 중", "서해에 줄무늬 구름, 대륙은 맑음"),
    ("7월 초, 장마전선이 한반도 중부에 위치", "동서 방향 구름대가 중부지방을 가로지름"),
    ("9월, 태풍이 제주도 남쪽에 접근 중", "나선형 구름 구조가 제주 남방 해상에 위치"),
    ("10월, 이동성 고기압 통과 중", "한반도 전체가 맑게 보임"),
]
for q, a in situations:
    with st.expander(f"🤔 {q}"):
        st.success(f"👉 {a}")
