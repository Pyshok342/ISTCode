# -*- coding: utf-8 -*-
"""
Иллюстрация парсинга веб-страницы с использованием Python.

Демонстрируется три подхода:
  1) Парсинг локального HTML-файла (mock_news.html) — основной пример;
  2) Парсинг HTML с удалённого URL через requests + BeautifulSoup;
  3) Парсинг через API (на примере api.github.com).

Установка зависимостей:
    pip install requests beautifulsoup4 lxml

Запуск:
    python web_scraper.py
"""
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup


# =====================================================================
# ПРИМЕР 1. Парсинг локальной HTML-страницы (рекомендуемый для обучения)
# =====================================================================
def parse_local_html(filename: str = "mock_news.html") -> list[dict]:
    """Прочитать локальный HTML и извлечь карточки новостей."""
    html = Path(filename).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    print(f"Заголовок страницы: {soup.title.string}\n")

    # Извлекаем меню навигации
    print("Главное меню:")
    for link in soup.select("nav.main-nav a, nav .main-nav a, .main-nav a"):
        print(f"  • {link.text} → {link['href']}")
    print()

    articles = []
    for card in soup.find_all("article", class_="article-card"):
        title = card.find("h3", class_="article-title").text.strip()
        slug = card["data-slug"]
        url = card.find("a", class_="article-link")["href"]

        meta = card.find("div", class_="article-meta")
        category = meta.find("span", class_="category").text.strip()
        author = meta.find("span", class_="author").text.replace("Автор:", "").strip()
        date = meta.find("time")["datetime"]

        summary = card.find("p", class_="article-summary").text.strip()

        stats = card.find("div", class_="article-stats")
        views = int(stats.find("span", class_="views").text.split(":")[1].strip())
        comments = int(stats.find("span", class_="comments").text.split(":")[1].strip())

        articles.append({
            "title": title, "slug": slug, "url": url,
            "category": category, "author": author, "date": date,
            "summary": summary, "views": views, "comments": comments,
        })
    return articles


# =====================================================================
# ПРИМЕР 2. Парсинг удалённой HTML-страницы (рабочий шаблон)
# =====================================================================
def parse_remote_url(url: str) -> dict | None:
    """Шаблон парсинга реальной страницы через requests + BeautifulSoup."""
    headers = {
        # Обязательно представляться — это вежливо и снижает риск 403
        "User-Agent": (
            "Mozilla/5.0 (compatible; ResearchBot/1.0; "
            "+https://example.com/contact)"
        ),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return {
            "url": url,
            "status": response.status_code,
            "title": soup.title.string.strip() if soup.title else None,
            "headings": [h.text.strip() for h in soup.find_all(["h1", "h2"])][:5],
            "links_count": len(soup.find_all("a")),
            "encoding": response.encoding,
        }
    except requests.RequestException as exc:
        print(f"Ошибка сети: {exc}")
        return None


# =====================================================================
# ПРИМЕР 3. Парсинг через API (альтернатива парсингу HTML)
# =====================================================================
def parse_via_github_api(owner: str, repo: str) -> dict | None:
    """Получение информации о репозитории через GitHub REST API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ResearchBot/1.0",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "name":        data.get("full_name"),
            "description": data.get("description"),
            "language":    data.get("language"),
            "stars":       data.get("stargazers_count"),
            "forks":       data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "license":     data.get("license", {}).get("name") if data.get("license") else None,
            "created_at":  data.get("created_at"),
        }
    except requests.RequestException as exc:
        print(f"Ошибка API: {exc}")
        return None


# =====================================================================
# Точка входа
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("ПРИМЕР 1. Парсинг локальной HTML-страницы (mock_news.html)")
    print("=" * 70)
    articles = parse_local_html()
    print(f"Извлечено статей: {len(articles)}\n")

    for i, art in enumerate(articles, 1):
        print(f"{i}. [{art['category']}] {art['title']}")
        print(f"   Автор: {art['author']}  |  Дата: {art['date']}")
        print(f"   {art['summary']}")
        print(f"   👁 {art['views']} просмотров, 💬 {art['comments']} комментариев")
        print(f"   URL: {art['url']}\n")

    # Аналитика
    print("=" * 70)
    print("Аналитика по парсингу:")
    print("=" * 70)
    total_views = sum(a["views"] for a in articles)
    total_comments = sum(a["comments"] for a in articles)
    print(f"Всего просмотров:    {total_views:,}".replace(",", " "))
    print(f"Всего комментариев:  {total_comments}")

    top = max(articles, key=lambda a: a["views"])
    print(f"Самая популярная:    «{top['title']}» ({top['views']} просмотров)")

    categories = {}
    for a in articles:
        categories[a["category"]] = categories.get(a["category"], 0) + 1
    print(f"Распределение по категориям:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")

    # Сохранение результата в JSON
    with open("parsed_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"\nРезультат сохранён в parsed_articles.json")

    # Пример 3 — парсинг через API (демонстрация, если есть сеть)
    print("\n" + "=" * 70)
    print("ПРИМЕР 3. Парсинг через API (api.github.com)")
    print("=" * 70)
    repo_info = parse_via_github_api("python", "cpython")
    if repo_info:
        print(f"Репозиторий:     {repo_info['name']}")
        print(f"Описание:        {repo_info['description']}")
        print(f"Основной язык:   {repo_info['language']}")
        print(f"Звёзд:           {repo_info['stars']:,}".replace(",", " "))
        print(f"Форков:          {repo_info['forks']:,}".replace(",", " "))
        print(f"Открытых issues: {repo_info['open_issues']}")
        print(f"Лицензия:        {repo_info['license']}")
        print(f"Создан:          {repo_info['created_at']}")
