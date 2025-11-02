import os
from duckduckgo_search import DDGS
import requests

class ResearchTool:
    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_KEY")

    def search(self, q: str, k: int = 5):
        results = []
        if self.serpapi_key:
            try:
                r = requests.get("https://serpapi.com/search.json", params={
                    "engine": "google", "q": q, "num": k, "api_key": self.serpapi_key
                }, timeout=20)
                for item in r.json().get("organic_results", [])[:k]:
                    results.append({
                        "title": item.get("title"),
                        "url": item.get("link"),
                        "snippet": item.get("snippet","")
                    })
            except Exception:
                pass

        if not results:
            with DDGS() as ddgs:
                for r in ddgs.text(q, max_results=k):
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body")
                    })
        return results
