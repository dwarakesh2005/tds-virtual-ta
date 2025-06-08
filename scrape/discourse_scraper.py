import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_discourse(base_url: str, start_date: str, end_date: str):
    posts = []
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for post in soup.select('.topic-list-item'):
            post_date = datetime.strptime(post.select_one('.post-time')['title'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if post_date < datetime.strptime(start_date, '%Y-%m-%d'):
                return posts
            
            posts.append({
                "title": post.select_one('.topic-title').text.strip(),
                "url": post.select_one('.topic-title')['href'],
                "content": post.select_one('.topic-excerpt').text.strip(),
                "date": post_date.isoformat(),
                "keywords": ["model", "tokenizer"]  # Example keywords
            })
        
        page += 1

# Usage (run periodically)
data = scrape_discourse(
    "https://discourse.onlinedegree.iitm.ac.in/c/tds",
    "2025-01-01",
    "2025-04-14"
)
with open('../data/discourse_posts.json', 'w') as f:
    json.dump(data, f)
