import pandas as pd
import numpy as np

# 주요 ASOS 관측소 정보
STATIONS = {
    "108": {"name": "서울", "lat": 37.5714, "lon": 126.9658},
    "159": {"name": "부산", "lat": 35.1046, "lon": 129.0319},
    "143": {"name": "대구", "lat": 35.8714, "lon": 128.6014},
    "156": {"name": "광주", "lat": 35.1728, "lon": 126.8914},
    "133": {"name": "대전", "lat": 36.3690, "lon": 127.3743},
    "152": {"name": "울산", "lat": 35.5597, "lon": 129.3200},
    "184": {"name": "제주", "lat": 33.5141, "lon": 126.5297},
    "105": {"name": "강릉", "lat": 37.7514, "lon": 128.8910},
    "112": {"name": "인천", "lat": 37.4775, "lon": 126.6249},
    "119": {"name": "수원", "lat": 37.2700, "lon": 126.9875},
    "146": {"name": "전주", "lat": 35.8214, "lon": 127.1547},
    "192": {"name": "진주", "lat": 35.1641, "lon": 128.0403},
    "101": {"name": "춘천", "lat": 37.9026, "lon": 127.7357},
    "90":  {"name": "속초", "lat": 38.2509, "lon": 128.5649},
    "168": {"name": "여수", "lat": 34.7392, "lon": 127.7406},
    "201": {"name": "강화", "lat": 37.7075, "lon": 126.4467},
    "170": {"name": "목포", "lat": 34.8171, "lon": 126.3817},
    "131": {"name": "청주", "lat": 36.6372, "lon": 127.4414},
}

# 5대 기단 정보
AIRMASSES = {
    "시베리아 기단": {
        "origin": [50, 100], "type": "cP", "property": "한랭 건조",
        "color": "#3B82F6", "emoji": "❄️",
        "months": [11, 12, 1, 2],
        "desc_easy": "시베리아는 러시아의 아주 추운 곳이에요. 겨울에 이곳에서 차갑고 건조한 공기가 한반도로 내려와요. 그래서 겨울이 춥고 건조한 거예요!",
        "desc_detail": "시베리아 내륙의 강한 복사냉각으로 형성되는 한랭 건조한 대륙성 극기단(cP)입니다. 겨울철 시베리아 고기압이 확장하면서 한반도에 강한 북서풍과 한파를 가져옵니다.",
        "wind_dir": "북서", "wind_angle": 315,
    },
    "양쯔강 기단": {
        "origin": [30, 115], "type": "cT", "property": "온난 건조",
        "color": "#F59E0B", "emoji": "🌤️",
        "months": [3, 4, 5, 9, 10],
        "desc_easy": "중국의 양쯔강 근처에서 만들어지는 따뜻하고 건조한 공기예요. 봄과 가을에 한반도로 와서 맑고 선선한 날씨를 만들어줘요!",
        "desc_detail": "양쯔강 유역에서 발원하는 온난 건조한 기단으로, 이동성 고기압의 형태로 봄·가을에 한반도를 통과합니다. 맑고 건조한 날씨를 가져오며, 일교차가 큰 특징이 있습니다.",
        "wind_dir": "남서~서", "wind_angle": 240,
    },
    "오호츠크해 기단": {
        "origin": [55, 150], "type": "mP", "property": "한랭 습윤",
        "color": "#8B5CF6", "emoji": "🌧️",
        "months": [6, 7],
        "desc_easy": "오호츠크해는 러시아 동쪽의 차가운 바다예요. 초여름에 이 바다에서 차갑고 습한 공기가 내려와요. 북태평양 기단과 만나면 장마가 시작돼요!",
        "desc_detail": "오호츠크해 상의 한랭 습윤한 해양성 극기단(mP)입니다. 초여름 북태평양 기단과 만나 정체전선(장마전선)을 형성하며, 동해안에 냉기류를 가져와 농업 피해를 유발하기도 합니다.",
        "wind_dir": "북동", "wind_angle": 45,
    },
    "북태평양 기단": {
        "origin": [25, 140], "type": "mT", "property": "고온 다습",
        "color": "#EF4444", "emoji": "🌞",
        "months": [7, 8],
        "desc_easy": "북태평양은 한반도 남동쪽의 따뜻한 바다예요. 여름에 이 바다에서 뜨겁고 습한 공기가 올라와서 무더위와 열대야를 만들어요!",
        "desc_detail": "북태평양 아열대 고기압에서 발원하는 고온 다습한 해양성 열대기단(mT)입니다. 한여름 한반도를 지배하며 폭염, 열대야, 집중호우의 주요 원인이 됩니다.",
        "wind_dir": "남~남동", "wind_angle": 160,
    },
    "적도 기단": {
        "origin": [10, 135], "type": "eT", "property": "고온 다습",
        "color": "#EC4899", "emoji": "🌀",
        "months": [8, 9, 10],
        "desc_easy": "적도 근처의 아주 따뜻한 바다에서 만들어진 공기예요. 이 공기가 모여서 소용돌이를 만들면 태풍이 돼요! 늦여름~가을에 한반도로 올라오기도 해요.",
        "desc_detail": "적도 부근 해양에서 발원하는 고온 다습한 적도기단(eT)으로, 열대저기압(태풍)의 형태로 한반도에 영향을 미칩니다. 강풍과 폭우를 동반하며 늦여름~초가을에 주로 나타납니다.",
        "wind_dir": "남", "wind_angle": 180,
    },
}

def get_monthly_strength(month):
    """월별 각 기단의 상대적 세력(0~1)"""
    strengths = {
        "시베리아 기단":   [0.95, 0.85, 0.4, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.5, 0.9],
        "양쯔강 기단":     [0.1, 0.2, 0.7, 0.9, 0.8, 0.3, 0.1, 0.1, 0.6, 0.8, 0.5, 0.15],
        "오호츠크해 기단": [0.0, 0.0, 0.0, 0.1, 0.3, 0.8, 0.7, 0.2, 0.0, 0.0, 0.0, 0.0],
        "북태평양 기단":   [0.0, 0.0, 0.0, 0.0, 0.1, 0.4, 0.9, 0.95, 0.5, 0.1, 0.0, 0.0],
        "적도 기단":       [0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.1, 0.5, 0.6, 0.3, 0.05, 0.0],
    }
    result = {}
    for name, vals in strengths.items():
        result[name] = vals[month - 1]
    return result

def get_sample_station_data(month):
    """월별 관측소 샘플 데이터 생성 (데모용)"""
    np.random.seed(month)
    base_temps = {
        1: -5, 2: -2, 3: 5, 4: 12, 5: 18, 6: 22, 7: 26, 8: 27, 9: 22, 10: 14, 11: 6, 12: -1
    }
    wind_dirs = {
        1: 315, 2: 315, 3: 250, 4: 240, 5: 230,
        6: 50, 7: 170, 8: 160, 9: 200, 10: 270, 11: 300, 12: 320
    }
    base_t = base_temps[month]
    base_wd = wind_dirs[month]
    records = []
    for stn_id, info in STATIONS.items():
        lat_effect = (info["lat"] - 36) * (-1.5 if month in [12,1,2] else -0.8)
        temp = base_t + lat_effect + np.random.normal(0, 1.5)
        humidity = 60 + (month in [6,7,8]) * 20 + np.random.normal(0, 8)
        wind_speed = 2 + np.random.exponential(1.5)
        wind_dir = (base_wd + np.random.normal(0, 25)) % 360
        records.append({
            "stn_id": stn_id,
            "name": info["name"],
            "lat": info["lat"],
            "lon": info["lon"],
            "temp": round(temp, 1),
            "humidity": round(min(max(humidity, 20), 99), 1),
            "wind_speed": round(wind_speed, 1),
            "wind_dir": round(wind_dir, 0),
        })
    return pd.DataFrame(records)

OCEAN_BUOYS = {
    "동해부이": {"lat": 37.5, "lon": 131.0, "region": "동해"},
    "서해부이": {"lat": 36.0, "lon": 124.5, "region": "서해"},
    "남해부이": {"lat": 33.5, "lon": 128.0, "region": "남해"},
    "제주남부": {"lat": 32.0, "lon": 126.5, "region": "남해"},
}

def get_sample_sst(month):
    """월별 부이 해수면온도 샘플"""
    base_sst = {1:8, 2:7, 3:9, 4:12, 5:16, 6:20, 7:24, 8:26, 9:24, 10:20, 11:15, 12:10}
    records = []
    for name, info in OCEAN_BUOYS.items():
        lat_adj = (info["lat"] - 35) * (-0.5)
        sst = base_sst[month] + lat_adj + np.random.normal(0, 0.8)
        records.append({"name": name, "lat": info["lat"], "lon": info["lon"],
                        "sst": round(sst, 1), "region": info["region"]})
    return pd.DataFrame(records)

SEASON_NAMES = {1:"겨울", 2:"겨울", 3:"봄", 4:"봄", 5:"봄",
                6:"여름(장마)", 7:"여름", 8:"여름", 9:"가을", 10:"가을", 11:"가을", 12:"겨울"}
