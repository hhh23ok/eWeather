import json
from pathlib import Path
from datetime import datetime, timedelta
import requests


# Fetch news from the API
def fetch_news(api_key, location="London"):
    url = f"https://api.worldnewsapi.com/search-news?text={location}&api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('news', [])[:4]  # Return only 4 articles
    else:
        print(response.status_code, "Broke pipe can apear because of problem of fetching data")
        return None


# Get yesterday's date as a fallback
def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime("%Y-%m-%d")


# Format the publish date
def format_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return get_yesterday_date()


# Get news articles
def get_news(location="London"):
    api_key = key
    news_data = fetch_news(api_key, location)

    # If no news data is fetched, load mock data
    if not news_data:
        print("Falling back to mock news data.")
        return None
        # news_data = load_mock_news()

    articles = []
    for article in news_data:
        articles.append({
            'title': article.get('title'),
            'text': article.get('text', 'No content available.'),
            'date': format_date(article.get('publish_date', get_yesterday_date())),  # Format date
            'source': article.get('source'),
            'url': article.get('url'),
            'summary': article.get('summary'),
            'image': article.get('image'),
        })
    return articles
