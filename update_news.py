import os
import feedparser
from datetime import datetime
import subprocess

# ===== CONFIGURATION =====
GITHUB_USERNAME = "pv7644356-rgb"
GITHUB_REPO = "blog"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Must be set in GitHub Actions secrets

# RSS feeds for categories
categories = {
    "prime_minister": "https://news.google.com/rss/search?q=prime+minister&hl=en-IN&gl=IN&ceid=IN:en",
    "accident": "https://news.google.com/rss/search?q=accident&hl=en-IN&gl=IN&ceid=IN:en",
    "sports": "https://news.google.com/rss/search?q=sports&hl=en-IN&gl=IN&ceid=IN:en",
    "events": "https://news.google.com/rss/search?q=events&hl=en-IN&gl=IN&ceid=IN:en"
}

# ===== FUNCTIONS =====
def fetch_and_save():
    os.makedirs("news_blog", exist_ok=True)
    updated = False

    for name, url in categories.items():
        feed = feedparser.parse(url)
        html_content = f"""
        <html>
        <head>
            <meta charset='UTF-8'>
            <meta http-equiv='refresh' content='120'>  <!-- Auto-refresh every 2 minutes -->
            <title>{name.capitalize()} News</title>
        </head>
        <body>
            <h1>{name.capitalize()} News - Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        """
        
        for entry in feed.entries[:10]:
            html_content += f"<p><a href='{entry.link}' target='_blank'>{entry.title}</a></p>"

        html_content += "</body></html>"

        file_path = f"news_blog/{name}.html"
        # Only write file if content changed
        if not os.path.exists(file_path) or open(file_path, "r", encoding="utf-8").read() != html_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Updated {file_path}")
            updated = True
        else:
            print(f"No changes for {file_path}")

    return updated

def git_push():
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
    subprocess.run(["git", "add", "."], check=True)
    
    # Only commit if there are changes
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode != 0:  # changes exist
        subprocess.run(
            ["git", "commit", "-m", f"Updated news at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
            check=True
        )
        subprocess.run(["git", "push", remote_url, "main"], check=True)
        print("Changes pushed to GitHub.")
    else:
        print("No changes to commit.")

# ===== MAIN =====
if __name__ == "__main__":
    if fetch_and_save():
        git_push()
    else:
        print("No updates fetched; nothing to push.")
