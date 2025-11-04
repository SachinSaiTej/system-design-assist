"""Abstract interface and implementations for web search providers."""
from abc import ABC, abstractmethod
from typing import List, Dict
import logging
import os

logger = logging.getLogger(__name__)


class WebSearcher(ABC):
    """Abstract base class for web search providers."""
    
    @abstractmethod
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for relevant references.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', 'snippet' keys
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this searcher is available (has required API keys).
        
        Returns:
            True if available, False otherwise
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this search provider.
        
        Returns:
            Provider name
        """
        pass

