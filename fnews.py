import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# OpenAI 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from urllib.parse import urljoin

from urllib.parse import parse_qs, urlparse

import urllib.parse

def get_bank_news():
    url = "https://www.reuters.com/business/finance/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        news_data = []
        items = soup.select("a.story-title, a.media-story-card__heading__link")[:10]

        for item in items:
            title = item.get_text(strip=True)
            link = item.get("href")

            if link and link.startswith("/"):
                link = "https://www.reuters.com" + link

            if title and link:
                news_data.append({
                    "title": title,
                    "link": link
                })

        return news_data

    except Exception as e:
        print("Reuters 뉴스 수집 에러:", e)
        return []



def get_ai_summary(news_list):
    if not news_list: return "뉴스를 가져오지 못했습니다."
    titles = [n['title'] for n in news_list]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
    "role": "user",
    "content": f"""
다음은 오늘의 주요 금융 뉴스 헤드라인 목록입니다.

이 뉴스들을 바탕으로,
- 오늘 금융 시장의 핵심 이슈를 2~3줄로 요약하고
- 추가로 밑에 규칙으로 투자자 관점에서 주목할 만한 흐름을 정리해 주세요.

투자자 주목 흐름 정리시에는 작성 규칙:
- 반드시 아래 형식으로 작성
1. 첫 번째 핵심 이슈 요약
2. 두 번째 핵심 이슈 요약
3. 세 번째 핵심 이슈 요약
- 각 항목은 한 문장으로 간결하게
- 불필요한 설명 없이 핵심만
- 문장마다 소제목+한 문장 정리 형식으로 번호 매겨서

헤드라인:
{titles}
"""
}]
    )
    return response.choices[0].message.content

def make_headline_table(news_list):
    lines = []
    for i, news in enumerate(news_list, 1):
        lines.append(f"| {i} | [{news['title']}]({news['link']}) |")
    return "\n".join(lines)

def update_readme():
    # [중요] 여기서 news_list를 먼저 만들어야 아래에서 쓸 수 있습니다!
    news_list = get_bank_news()
    ai_briefing = get_ai_summary(news_list)
    headline_table = make_headline_table(news_list)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    badge_py = "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)"
    badge_ai = "![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)"
    badge_gh = "![Github Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)"

    
    readme_content = f"""# 🏦 Bank News AI Analyzer
{badge_py} {badge_ai} {badge_gh}

> **💡 공지:** 본 리포트는 매일 아침 AI가 최신 금융 뉴스를 요약하여 업데이트합니다.

## 🕒 Last Update: `{now}` (KST)

## 🤖 AI 애널리스트 오늘의 브리핑

{ai_briefing}

## 📰 실시간 주요 헤드라인
| 번호 | 뉴스 제목 (클릭 시 이동) |
| --- | --- |
{headline_table}

© {datetime.now()}
"""



    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
