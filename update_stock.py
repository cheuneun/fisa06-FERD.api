import requests
import os
from datetime import datetime

# FRED API 설정 (GitHub Secrets에 FRED_API_KEY 등록 필수)
API_KEY = os.getenv("FRED_API_KEY")

# 금융권 핵심 거시 경제 지표 (기준금리, 물가, 실업률, 장단기 금리차)
INDICATORS = {
    "FEDFUNDS": "🇺🇸 미국 기준 금리 (Fed Funds Rate)",
    "CPIAUCSL": "🍎 소비자 물가 지수 (CPI)",
    "UNRATE": "👷 실업률 (Unemployment Rate)",
    "T10Y2Y": "📉 장단기 금리차 (10Y-2Y Spread)"
}

README_PATH = "README.md"

def get_fred_data(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={API_KEY}&file_type=json&sort_order=desc&limit=1"
    try:
        response = requests.get(url)
        data = response.json()
        if "observations" in data and len(data["observations"]) > 0:
            value = data["observations"][0]["value"]
            date = data["observations"][0]["date"]
            return value, date
    except Exception as e:
        print(f"Error fetching {series_id}: {e}")
    return None, None

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""

    print("FRED 거시 경제 데이터 수집 중...")
    for s_id, name in INDICATORS.items():
        value, date = get_fred_data(s_id)
        if value:
            rows += f"| {name} | **{value}%** | {date} |\n"
            print(f"{name} 완료")
        else:
            rows += f"| {name} | 데이터 없음 | - |\n"

    readme_content = f"""
# 🏛️ Global Macro Economic Dashboard

이 리포지토리는 **FRED API**와 **GitHub Actions**를 사용하여 글로벌 거시 경제 지표를 실시간으로 모니터링하는 금융 데이터 파이프라인입니다.

## 📊 주요 거시 경제 지표
| 지표명 | 수치 | 마지막 발표일 |
| :--- | :--- | :--- |
{rows}

---
⏳ **최종 업데이트:** {now} (KST)  
*출처: Federal Reserve Bank of St. Louis (FRED API)*
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    if not API_KEY:
        print("FRED_API_KEY가 없습니다. Secrets 설정을 확인하세요.")
    else:
        update_readme()
