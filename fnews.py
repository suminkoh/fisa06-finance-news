import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import datetime

# OpenAI 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bank_news():
    url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=259"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_data = []
        items = soup.select('.articleSubject a')[:10] 
        for item in items:
            title = item.get_text(strip=True)
            link = "https://finance.naver.com" + item['href']
            news_data.append({"title": title, "link": link})
        return news_data
    except:
        return []

def get_ai_summary(news_list):
    if not news_list: return "뉴스를 가져오지 못했습니다."
    titles = [n['title'] for n in news_list]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"금융 뉴스 요약해줘:\n{titles}"}]
    )
    return response.choices[0].message.content

def update_readme():
    # [중요] 여기서 news_list를 먼저 만들어야 아래에서 쓸 수 있습니다!
    news_list = get_bank_news()
    ai_briefing = get_ai_summary(news_list)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    badge_py = "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)"
    badge_ai = "![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)"
    badge_gh = "![Github Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)"

    
    readme_content = f"""# 🏦 Bank News AI Analyzer
{badge_py} {badge_ai} {badge_gh}

> **💡 공지:** 본 리포트는 매일 아침 AI가 최신 금융 뉴스를 요약하여 업데이트합니다.

## 🕒 Last Update: `{now}` (KST)

## 🤖 AI 애널리스트 오늘의 브리핑
```text
{ai_briefing}

"""

    for i, news in enumerate(news_list, 1):
        readme_content += f"| {i} | [{news['title']}]({news['link']}) |\n"

        readme_content += f"\n---\n© {datetime.now().year} Finance Automation Project."


    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()