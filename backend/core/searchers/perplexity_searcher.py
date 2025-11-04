"""Perplexity API web search implementation."""
import os
from typing import List, Dict
import logging
from dotenv import load_dotenv
from ..web_searcher import WebSearcher

load_dotenv()
logger = logging.getLogger(__name__)

try:
    from perplexity import Perplexity
    PERPLEXITY_AVAILABLE = True
except ImportError:
    PERPLEXITY_AVAILABLE = False
    logger.warning("perplexity package not installed. Install with: pip install perplexityai")


class PerplexitySearcher(WebSearcher):
    """Perplexity API web search provider."""
    
    def __init__(self):
        """Initialize the Perplexity searcher."""
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.client = None
        
        if self.is_available() and PERPLEXITY_AVAILABLE:
            try:
                # Perplexity SDK reads PERPLEXITY_API_KEY from environment automatically
                # But we can also pass it explicitly if needed
                if self.api_key:
                    # Set environment variable for SDK to pick up
                    os.environ["PERPLEXITY_API_KEY"] = self.api_key
                
                self.client = Perplexity()
            except Exception as e:
                logger.error(f"Failed to initialize Perplexity client: {str(e)}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if Perplexity API key is configured."""
        return bool(self.api_key) and PERPLEXITY_AVAILABLE
    
    def get_name(self) -> str:
        """Get the name of this search provider."""
        return "Perplexity"
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using Perplexity API SDK.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        if not self.is_available() or not self.client:
            logger.warning("Perplexity API key not configured or SDK not available")
            return []
        
        try:
            # Enhance query for system design search
            enhanced_query = f"{query} system design architecture"
            
            # Create search query list (Perplexity SDK accepts a list)
            search_query = [enhanced_query]
            
            # Perform search using Perplexity SDK
            search = self.client.search.create(query=search_query)
            
            results = []
            
            # Extract results from search.results
            if hasattr(search, 'results') and search.results:
                for result in search.results[:num_results]:
                    # Each result should have title and url attributes
                    title = getattr(result, 'title', '') or getattr(result, 'text', 'Untitled')
                    url = getattr(result, 'url', '')
                    snippet = getattr(result, 'snippet', '') or getattr(result, 'description', '')
                    
                    if url:  # Only add if we have a URL
                        results.append({
                            "title": title[:200] if title else "Untitled",
                            "url": url,
                            "snippet": snippet[:300] if snippet else ""
                        })
            
            logger.info(f"✅ Perplexity API returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Perplexity API error: {str(e)}")
            return []

