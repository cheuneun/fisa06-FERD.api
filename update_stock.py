import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# 한국 대표 종목 10개 (종목코드.KS 또는 .KQ)
# 005930: 삼성전자, 000660: SK하이닉스, 005490: POSCO홀딩스 등
SYMBOLS = [
    "005930.KS", "000660.KS", "373220.KS", "207940.KS", 
    "005380.KS", "068270.KS", "005490.KS", "051910.KS", 
    "035420.KS", "006400.KS"
]

# 종목코드와 매칭되는 한글 이름 (딕셔너리)
NAMES = {
    "005930.KS": "삼성전자", "000660.KS": "SK하이닉스", "373220.KS": "LG에너지솔루션",
    "207940.KS": "삼성바이오로직스", "005380.KS": "현대차", "068270.KS": "셀트리온",
    "005490.KS": "POSCO홀딩스", "051910.KS": "LG화학", "035420.KS": "NAVER", "006400.KS": "삼성SDI"
}

README_PATH = "README.md"

def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("Global Quote", {})

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_rows = ""

    print(f"한국 주식 업데이트 시작: {now}")
    
    for i, symbol in enumerate(SYMBOLS):
        # 5개마다 65초 대기 (무료 API 제한)
        if i > 0 and i % 5 == 0:
            print("API 제한 방지를 위해 잠시 대기 중...")
            time.sleep(65) 
            
        quote = get_stock_data(symbol)
        name = NAMES.get(symbol, symbol)
        
        if quote:
            # 한국 주식은 소수점 없이 원화(KRW)로 표시되므로 정수 처리
            price = quote.get("05. price", "0")
            change = quote.get("10. change percent", "0%")
            formatted_price = format(int(float(price)), ',') # 세 자리마다 콤마
            stock_rows += f"| {name} | {formatted_price}원 | {change} |\n"
            print(f"{name} 완료!")
        else:
            stock_rows += f"| {name} | 데이터 없음 | - |\n"

    readme_content = f"""
# 🇰🇷 실시간 국내 주요 종목 (KOSPI Top 10)

이 대시보드는 Alpha Vantage API를 통해 한국 시장의 주요 종목 주가를 자동으로 업데이트합니다.

| 종목명 | 현재가 | 변동률 |
| :--- | :--- | :--- |
{stock_rows}

---
⏳ **최종 업데이트 시간:** {now} (KST/UTC)  
*참고: Alpha Vantage의 한국 데이터는 실시간보다 15~20분 정도 지연될 수 있습니다.*
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
