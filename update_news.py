import os
import feedparser
from datetime import datetime
import subprocess

# ===== CONFIGURATION =====
GITHUB_USERNAME = "pv7644356-rgb"
GITHUB_REPO = "blog"

# Google News RSS feeds for categories
categories = {
    "prime_minister": "https://news.google.com/rss/search?q=prime+minister&hl=en-IN&gl=IN&ceid=IN:en",
    "accident": "https://news.google.com/rss/search?q=accident&hl=en-IN&gl=IN&ceid=IN:en",
    "sports": "https://news.google.com/rss/search?q=sports&hl=en-IN&gl=IN&ceid=IN:en",
    "events": "https://news.google.com/rss/search?q=events&hl=en-IN&gl=IN&ceid=IN:en"
}

# ===== FUNCTIONS =====
def fetch_and_save():
    os.makedirs("news_blog", exist_ok=True)
    for name, url in categories.items():
        feed = feedparser.parse(url)
        html_content = f"<html><head><meta charset='UTF-8'><title>{name.capitalize()} News</title></head><body>"
        html_content += f"<h1>{name.capitalize()} News - Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>"
        for entry in feed.entries[:10]:
            html_content += f"<p><a href='{entry.link}' target='_blank'>{entry.title}</a></p>"
        html_content += "</body></html>"
        with open(f"news_blog/{name}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Saved news_blog/{name}.html")

def git_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Updated news at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

# ===== MAIN =====
if __name__ == "__main__":
    fetch_and_save()
    git_push()
