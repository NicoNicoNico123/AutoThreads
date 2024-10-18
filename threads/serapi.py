from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

class SerpAPI:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_KEY environment variable is not set")

    def get_trending_now(self): 
        params = {
            "engine": "google_trends_trending_now",
            "geo": "HK",
            "hl":"zh-tw",
            "api_key": self.api_key
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            trending_searches = results.get("trending_searches", [])
            if trending_searches and isinstance(trending_searches[0], dict):
                return trending_searches[0].get("query", "")
            return ""
        except Exception as e:
            print(f"Error in get_trending_now: {e}")
            return ""

    def get_news(self, query: str):
        params = {
            "engine": "google_news",
            "q": query,
            "geo": "HK",
            "hl":"zh-tw",
            "api_key": self.api_key
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            return results
        except Exception as e:
            print(f"Error in get_news: {e}")
            return {}

    def main(self):
        query = self.get_trending_now()
        if not query:
            print("No trending topics found")
            return []

        news = self.get_news(query)
        if not news:
            print("No news found")
            return []

        main_titles = [item.get('title', '') for item in news.get('news_results', [])]
        
        story_titles = []
        for item in news.get('news_results', []):
            if 'stories' in item:
                story_titles.extend([story.get('title', '') for story in item['stories']])

        all_titles = main_titles + story_titles
        result = all_titles[:10]
        return result

if __name__ == "__main__":
    try:
        result = SerpAPI().main()
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
