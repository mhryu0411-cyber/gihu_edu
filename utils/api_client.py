import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = ""  # 기상자료개방포털에서 발급받은 인증키 입력

def get_asos_data(stn_id="108", start_date=None, end_date=None):
    """지상관측(ASOS) 일별 데이터 조회"""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    if not end_date:
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd.php"
    params = {
        "tm1": start_date,
        "tm2": end_date,
        "stn": stn_id,
        "help": 0,
        "authKey": API_KEY,
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            return _parse_asos(res.text)
    except:
        pass
    return None

def get_aws_realtime():
    """AWS 실시간 관측 데이터"""
    url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm.php"
    params = {"help": 0, "authKey": API_KEY}
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            return res.text
    except:
        pass
    return None

def get_ocean_buoy():
    """해양기상부이 관측 데이터"""
    url = "https://apihub.kma.go.kr/api/typ01/url/sea_obsbuoy.php"
    params = {"help": 0, "authKey": API_KEY}
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            return res.text
    except:
        pass
    return None

def get_satellite_image(band="ir1", time=None):
    """천리안2A 위성영상 URL 반환"""
    if not time:
        time = datetime.utcnow().strftime("%Y%m%d%H%M")
    url = f"https://apihub.kma.go.kr/api/typ01/cgi/dfs/nph-qpf_ana_img.cgi"
    return url

def _parse_asos(text):
    lines = text.strip().split("\n")
    data_lines = [l for l in lines if l and not l.startswith("#")]
    if not data_lines:
        return None
    records = []
    for line in data_lines:
        parts = line.split(",") if "," in line else line.split()
        if len(parts) >= 10:
            records.append(parts)
    return records
