import os
import requests
import telebot
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")

def gnews_api(keyword=None, category=None,country=None):
    URL = "https://gnews.io/api/v4/top-headlines"
    URL2 = "https://gnews.io/api/v4/search"
    params = {
        "lang": "en",  # Language of the articles
        "max": 10,  # Maximum", number of articles to return
        "apikey": API_KEY  # Authentication parameter
    }
    try:
        if keyword:
            params['q'] = keyword
        if category:
            params['category'] = category
        if country:
            params['country'] = country

        if keyword:
            url=URL2
        else:
            url=URL
        response = requests.get(url, params=params,timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            source_name = (article.get("source") or {}).get("name", "Unknown Source")
            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "source": source_name,
                "url": article.get("url"),
                "content": article.get("content")
            })

        return articles
    except Exception as e:
        print(e)
    except requests.exceptions.ConnectionError:
        print("No internet connection or server is down.")

gnews_api()