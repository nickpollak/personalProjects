import requests
import json


newsapi_key = ""

# GET https://newsapi.org/v2/top-headlines?country=us&apiKey=

def get_relevant_news(company_name):
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "q": company_name,
                "country": "us",
                "pageSize": 5,
                "apiKey": newsapi_key
            }
        )
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        result = []
        for a in articles:
            result.append({
                "title": a["title"],
                "source": a["source"]["name"],
                "published_at": a["publishedAt"],
                "url": a["url"],
                "description": a.get("description", "")
            })

        print(f"Found {len(result)} articles for '{company_name}'")
        return result

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching news for '{company_name}': {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching news for '{company_name}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching news for '{company_name}': {e}")
        return []