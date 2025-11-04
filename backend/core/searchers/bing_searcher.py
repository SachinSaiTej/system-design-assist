"""Bing Search API web search implementation."""
import os
import requests
from typing import List, Dict
import logging
from dotenv import load_dotenv
from ..web_searcher import WebSearcher

load_dotenv()
logger = logging.getLogger(__name__)


class BingSearcher(WebSearcher):
    """Bing Search API web search provider."""
    
    def __init__(self):
        """Initialize the Bing searcher."""
        self.api_key = os.getenv("BING_API_KEY")
        self.api_url = os.getenv("BING_SEARCH_URL", "https://api.bing.microsoft.com/v7.0/search")
    
    def is_available(self) -> bool:
        """Check if Bing API key is configured."""
        return bool(self.api_key)
    
    def get_name(self) -> str:
        """Get the name of this search provider."""
        return "Bing"
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using Bing Search API.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        if not self.is_available():
            logger.warning("Bing API key not configured")
            return []
        
        try:
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key
            }
            params = {
                "q": query,
                "count": num_results,
                "offset": 0,
                "mkt": "en-US",
                "safeSearch": "Moderate"
            }
            
            response = requests.get(self.api_url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            web_pages = data.get("webPages", {}).get("value", [])
            
            for page in web_pages[:num_results]:
                results.append({
                    "title": page.get("name", ""),
                    "url": page.get("url", ""),
                    "snippet": page.get("snippet", "")
                })
            
            logger.info(f"✅ Bing API returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Bing API error: {str(e)}")
            return []

