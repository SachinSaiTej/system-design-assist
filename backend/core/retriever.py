"""Web search retriever for finding relevant system design references."""
import os
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv

from core.web_searcher import WebSearcher
from core.searchers import PerplexitySearcher

load_dotenv()
logger = logging.getLogger(__name__)


class WebRetriever:
    """Retriever for searching the web for system design references using Perplexity only."""
    
    def __init__(self):
        """Initialize the retriever with Perplexity searcher."""
        self.searcher = PerplexitySearcher()
        
        if not self.searcher.is_available():
            logger.warning("⚠️  Perplexity API key not configured. Web search will be skipped.")
        else:
            logger.info(f"✅ Using {self.searcher.get_name()} as web search provider")
    
    def is_available(self) -> bool:
        """
        Check if web search is available.
        
        Returns:
            True if Perplexity is configured, False otherwise
        """
        return self.searcher.is_available()
    
    def get_active_provider(self) -> Optional[str]:
        """
        Get the name of the currently active search provider.
        
        Returns:
            Provider name or None if no provider is active
        """
        return self.searcher.get_name() if self.searcher.is_available() else None
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for relevant references using Perplexity.
        Returns empty list if Perplexity is not available or fails.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results, or empty list if search fails
        """
        if not self.searcher.is_available():
            logger.info("ℹ️  Perplexity not available, skipping web search")
            return []
        
        # Enhance query for system design search (if not already enhanced)
        enhanced_query = query
        if "system design" not in query.lower() and "architecture" not in query.lower():
            enhanced_query = f"{query} system design architecture"
        
        try:
            results = self.searcher.search(enhanced_query, num_results)
            
            if not results:
                logger.warning(f"⚠️  Perplexity returned no results for query: {query}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error during Perplexity search: {str(e)}")
            return []
