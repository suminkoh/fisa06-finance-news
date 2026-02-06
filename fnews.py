import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import datetime

# 1. OpenAI 클라이언트 설정 (GitHub Secrets의 API 키 사용)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bank_news():
    """네이버 금융에서 은행/금융 뉴스 제목들을 가져옵니다."""
    url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=259"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    news_items = []
    # 최신 뉴스 제목 10개 추출
    items = soup.select('.articleSubject a')[:10] 
    for item in items:
        news_items.append(item.get_text(strip=True))
    return news_items

def analyze_news_with_gpt(news_list):
    """수집된 뉴스 제목들을 GPT가 분석하고 요약합니다."""
    news_text = "\n".join(news_list)
    
    prompt = f"""
    너는 베테랑 금융 애널리스트야. 아래 제공된 오늘자 은행/금융 뉴스 제목들을 보고 브리핑을 작성해줘.
    
    뉴스 제목 목록:
    {news_text}
    
    작성 가이드라인:
    1. 오늘 핵심 금융 이슈를 3가지로 압축해서 요약해줘.
    2. 현재 은행권의 시장 분위기가 어떤지(긍정/부정/관망) 한 문장으로 진단해줘.
    3. 일반인들이 참고하면 좋을 '오늘의 금융 팁'을 한 줄 추가해줘.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 실행 부분 ---
print("뉴스 수집 중...")
news_titles = get_bank_news()

print("AI 분석 중...")
ai_analysis = analyze_news_with_gpt(news_titles)

# 현재 시간 (한국 시간으로 맞추려면 아래 그대로 사용하거나 UTC 조정)
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# 2. README.md 파일 작성
now = datetime.now().strftime('%Y-%m-%d %H:%M')

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# 🏦 Bank News AI Analyzer\n\n")
    
    # 배지 (따옴표 에러 방지를 위해 변수로 따로 뺌)
    badge_py = "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)"
    badge_ai = "![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)"
    badge_gh = "![Github Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)"
    
    f.write(f"{badge_py} {badge_ai} {badge_gh}\n\n")
    f.write(f"> **💡 공지:** 본 리포트는 매일 AI가 최신 금융 뉴스를 요약하여 업데이트합니다.\n\n")
    f.write(f"## 🕒 업데이트 시간: `{now}`\n\n")
    f.write(f"## 🤖 AI 애널리스트 브리핑\n\n{ai_analysis}\n\n")
    f.write(f"## 📰 주요 뉴스 헤드라인\n")
    for i, title in enumerate(news_titles, 1):
        f.write(f"{i}. {title}\n")