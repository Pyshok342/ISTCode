# -*- coding: utf-8 -*-
"""
Генератор тестовой HTML-страницы новостного сайта.
Используется как «полигон» для иллюстрации парсинга веб-страниц.
"""
from datetime import datetime

articles = [
    ("ai-breakthrough-2026", "Прорыв в развитии искусственного интеллекта",
     "ИИ", "Алексей Иванов", "2026-05-25",
     "Учёные представили новую архитектуру нейросети, превосходящую GPT-4 по точности на 12 %.",
     "1247", "183"),
    ("quantum-computer-russia", "В России запущен квантовый компьютер на 50 кубитов",
     "Технологии", "Мария Петрова", "2026-05-24",
     "Российская команда МФТИ и Росатома представила свой первый 50-кубитный квантовый процессор.",
     "892", "97"),
    ("python-3-13-release", "Вышел Python 3.13 с GIL-free режимом",
     "Программирование", "Дмитрий Соколов", "2026-05-23",
     "Долгожданное обновление включает экспериментальный режим без GIL и улучшенный JIT-компилятор.",
     "2103", "324"),
    ("cyber-attack-banks", "Крупная DDoS-атака на банковский сектор",
     "Безопасность", "Анна Кузнецова", "2026-05-22",
     "Несколько крупных банков подверглись скоординированной атаке; работа сервисов восстановлена.",
     "567", "78"),
    ("5g-russia-2026", "5G-сети развернуты в 15 городах России",
     "Связь", "Сергей Морозов", "2026-05-21",
     "Минцифры объявило о завершении первого этапа развёртывания сетей пятого поколения.",
     "1456", "201"),
    ("opensource-foundation", "Создан российский Open Source Foundation",
     "Технологии", "Елена Васильева", "2026-05-20",
     "Сбер, Яндекс и VK объявили о запуске фонда поддержки российского открытого ПО.",
     "734", "112"),
]

html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Tech News — главная страница</title>
</head>
<body>
    <header class="site-header">
        <h1>Tech News</h1>
        <nav>
            <ul class="main-nav">
                <li><a href="/">Главная</a></li>
                <li><a href="/ai">ИИ</a></li>
                <li><a href="/tech">Технологии</a></li>
                <li><a href="/security">Безопасность</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h2>Последние новости</h2>
        <div class="articles-list">
"""

for slug, title, category, author, date, summary, views, comments in articles:
    html += f"""            <article class="article-card" data-slug="{slug}">
                <a href="/article/{slug}" class="article-link">
                    <h3 class="article-title">{title}</h3>
                </a>
                <div class="article-meta">
                    <span class="category">{category}</span>
                    <span class="author">Автор: {author}</span>
                    <time datetime="{date}">{date}</time>
                </div>
                <p class="article-summary">{summary}</p>
                <div class="article-stats">
                    <span class="views">Просмотров: {views}</span>
                    <span class="comments">Комментариев: {comments}</span>
                </div>
            </article>
"""

html += """        </div>
    </main>

    <footer>
        <p>© 2026 Tech News. Все права защищены.</p>
    </footer>
</body>
</html>
"""

with open("mock_news.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Файл mock_news.html сохранён ({len(articles)} статей)")
