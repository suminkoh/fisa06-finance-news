# ... (앞부분 뉴스 수집 및 GPT 분석 로직은 동일) ...

# 현재 시간 설정
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# 2. README.md 디자인 작성
with open("README.md", "w", encoding="utf-8") as f:
    # 헤더 부분: 배지를 넣어 전문적인 느낌 전달
    f.write(f"# 🏦 Bank News AI Analyzer\n\n")
    f.write(f"![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ")
    f.write(f"![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ")
    f.write(f"![Github Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)\n\n")
    
    f.write(f"> **💡 공지:** 본 리포트는 매일 아침 8시, AI가 최신 금융 뉴스를 요약하여 자동으로 업데이트합니다.\n\n")
    
    f.write(f"## 🕒 Last Update: `{now}`\n\n")
    
    f.write(f"## 🤖 AI 애널리스트 오늘의 브리핑\n")
    f.write(f"```text\n{ai_analysis}\n```\n\n") # 박스 안에 넣어 가독성 향상
    
    f.write(f"## 📰 실시간 주요 헤드라인\n")
    f.write(f"| 순번 | 뉴스 제목 |\n") # 표(Table) 형식으로 깔끔하게 정리
    f.write(f"| :--- | :--- |\n")
    for i, title in enumerate(news_titles, 1):
        f.write(f"| {i} | {title} |\n")
        
    f.write(f"\n\n---\n")
    f.write(f"© {datetime.now().year} Finance Automation Project. All rights reserved.")
