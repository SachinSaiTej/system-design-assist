"""SerpAPI web search implementation."""
import os
import requests
from typing import List, Dict
import logging
from dotenv import load_dotenv
from ..web_searcher import WebSearcher

load_dotenv()
logger = logging.getLogger(__name__)


class SerpAPISearcher(WebSearcher):
    """SerpAPI web search provider."""
    
    def __init__(self):
        """Initialize the SerpAPI searcher."""
        self.api_key = os.getenv("SERPAPI_KEY")
        self.api_url = "https://serpapi.com/search"
    
    def is_available(self) -> bool:
        """Check if SerpAPI key is configured."""
        return bool(self.api_key)
    
    def get_name(self) -> str:
        """Get the name of this search provider."""
        return "SerpAPI"
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using SerpAPI.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        if not self.is_available():
            logger.warning("SerpAPI key not configured")
            return []
        
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": num_results,
                "gl": "us",
                "hl": "en"
            }
            
            response = requests.get(self.api_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            organic_results = data.get("organic_results", [])
            
            for result in organic_results[:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            logger.info(f"✅ SerpAPI returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ SerpAPI error: {str(e)}")
            return []

