"""Web search retriever for finding relevant system design references."""
import os
import requests
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class WebRetriever:
    """Retriever for searching the web for system design references."""
    
    def __init__(self):
        """Initialize the retriever with API keys."""
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        self.bing_api_key = os.getenv("BING_API_KEY")
        self.bing_search_url = os.getenv("BING_SEARCH_URL", "https://api.bing.microsoft.com/v7.0/search")
        
        if not self.serpapi_key and not self.bing_api_key:
            logger.warning("⚠️  No search API key found (SERPAPI_KEY or BING_API_KEY)")
    
    def search_serpapi(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using SerpAPI.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        if not self.serpapi_key:
            return []
        
        try:
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "engine": "google",
                "num": num_results,
                "gl": "us",
                "hl": "en"
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=15)
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
    
    def search_bing(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using Bing Search API.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        if not self.bing_api_key:
            return []
        
        try:
            headers = {
                "Ocp-Apim-Subscription-Key": self.bing_api_key
            }
            params = {
                "q": query,
                "count": num_results,
                "offset": 0,
                "mkt": "en-US",
                "safeSearch": "Moderate"
            }
            
            response = requests.get(self.bing_search_url, headers=headers, params=params, timeout=15)
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
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for relevant references.
        Tries SerpAPI first, then falls back to Bing.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        # Enhance query for system design search
        enhanced_query = f"{query} system design architecture"
        
        # Try SerpAPI first
        if self.serpapi_key:
            results = self.search_serpapi(enhanced_query, num_results)
            if results:
                return results
        
        # Fallback to Bing
        if self.bing_api_key:
            results = self.search_bing(enhanced_query, num_results)
            if results:
                return results
        
        logger.warning("⚠️  No search results found. Both APIs may be unavailable.")
        return []

