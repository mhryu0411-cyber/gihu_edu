import streamlit as st
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from utils.sample_data import get_sample_sst, OCEAN_BUOYS, AIRMASSES

st.set_page_config(page_title="해양관측", page_icon="🌊", layout="wide")

easy_mode = st.sidebar.toggle("😊 쉬운 설명 모드", value=True)

st.markdown("## 🌊 해양관측 — 해수면 온도와 기단")

if easy_mode:
    st.info("바다의 온도가 기단의 성질을 결정해요! 따뜻한 바다 위의 공기는 따뜻하고 습하고, 차가운 바다 위의 공기는 차갑고 습해요.")
else:
    st.info("해양성 기단(mP, mT)의 특성은 발원지 해수면 온도(SST)에 의해 결정됩니다. 오호츠크해와 북태평양의 SST 차이가 두 기단의 성질 차이를 만듭니다.")

month = st.slider("📅 월 선택", 1, 12, 7, format="%d월")
sst_df = get_sample_sst(month)

col1, col2 = st.columns([1.5, 1])

with col1:
    m = folium.Map(location=[34, 130], zoom_start=5, tiles="CartoDB positron")
    for _, row in sst_df.iterrows():
        sst = row["sst"]
        if sst <= 10: color = "#3B82F6"
        elif sst <= 18: color = "#60A5FA"
        elif sst <= 24: color = "#FBBF24"
        else: color = "#EF4444"
        folium.CircleMarker(
            [row["lat"], row["lon"]], radius=12,
            color=color, fill=True, fill_color=color, fill_opacity=0.7,
            tooltip=f"{row['name']}: {sst}°C",
            popup=f"<b>{row['name']}</b><br>해수면온도: {sst}°C<br>해역: {row['region']}"
        ).add_to(m)

    # 오호츠크해, 북태평양 표시
    folium.Marker([55, 150], icon=folium.DivIcon(html='<div style="font-size:20px">🌧️ 오호츠크해</div>')).add_to(m)
    folium.Marker([25, 140], icon=folium.DivIcon(html='<div style="font-size:20px">🌞 북태평양</div>')).add_to(m)

    st_folium(m, use_container_width=True, height=450)

with col2:
    st.markdown("#### 📊 연간 해수면온도 변화")
    fig = go.Figure()
    for bname in OCEAN_BUOYS:
        sst_vals = [get_sample_sst(m).query(f"name=='{bname}'")["sst"].values[0] for m in range(1,13)]
        fig.add_trace(go.Scatter(
            x=list(range(1,13)), y=sst_vals,
            name=bname, mode="lines+markers",
        ))
    fig.add_vline(x=month, line_dash="dash", line_color="gray")
    fig.update_layout(height=400, xaxis=dict(tickmode="array", tickvals=list(range(1,13)),
                      ticktext=[f"{m}월" for m in range(1,13)]),
                      yaxis_title="SST (°C)", margin=dict(l=0,r=0,t=10,b=0),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💡 오호츠크해 vs 북태평양")
    if easy_mode:
        st.markdown("""
        - 🌧️ **오호츠크해**: 차가운 바다 → 차갑고 습한 공기 (장마!)
        - 🌞 **북태평양**: 따뜻한 바다 → 뜨겁고 습한 공기 (무더위!)
        - 이 두 기단이 만나면 **장마전선**이 생겨요!
        """)
    else:
        st.markdown("""
        - **오호츠크해 기단 (mP)**: SST ~5~15°C → 한랭 습윤
        - **북태평양 기단 (mT)**: SST ~25~30°C → 고온 다습
        - 두 기단의 세력이 비슷할 때 정체전선 형성 → 장마
        """)
