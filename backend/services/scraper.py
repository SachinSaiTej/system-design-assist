"""Web content scraper for extracting readable text from URLs."""
import requests
from typing import Optional
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

# Whitelist of trusted domains
TRUSTED_DOMAINS = [
    "bytebytego.com",
    "github.com",
    "medium.com",
    "dev.to",
    "aws.amazon.com",
    "cloud.google.com",
    "microsoft.com",
    "engineering.fb.com",
    "blog.twitter.com",
    "highscalability.com",
]

# User agent for respectful scraping
USER_AGENT = "Mozilla/5.0 (compatible; SystemDesignAssistant/1.0; +https://system-design-assistant.com/bot)"


class WebScraper:
    """Scraper for extracting readable text from web pages."""
    
    def __init__(self):
        """Initialize the scraper."""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
    
    def is_trusted_domain(self, url: str) -> bool:
        """Check if URL is from a trusted domain."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            
            return any(domain.endswith(trusted) for trusted in TRUSTED_DOMAINS)
        except Exception as e:
            logger.warning(f"Error checking trusted domain for {url}: {str(e)}")
            return False
    
    def check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt."""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(USER_AGENT, url)
        except Exception as e:
            logger.debug(f"Could not check robots.txt for {url}: {str(e)}")
            # Default to allowing if robots.txt check fails
            return True
    
    def scrape_url(self, url: str, max_length: int = 10000) -> Optional[str]:
        """
        Scrape readable text from a URL.
        
        Args:
            url: URL to scrape
            max_length: Maximum length of content to return
            
        Returns:
            Extracted text content or None if scraping fails
        """
        try:
            # Check if domain is trusted
            if not self.is_trusted_domain(url):
                logger.warning(f"URL not from trusted domain: {url}")
                # Allow but log warning
            
            # Check robots.txt
            if not self.check_robots_txt(url):
                logger.warning(f"URL blocked by robots.txt: {url}")
                return None
            
            # Fetch the page with timeout
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Try using readability-lxml if available, otherwise fallback to simple extraction
            try:
                from readability import Document
                doc = Document(response.text)
                content = doc.summary()
                # Remove HTML tags for basic extraction
                from html import unescape
                import re
                text = re.sub(r'<[^>]+>', '', content)
                text = unescape(text)
            except ImportError:
                # Fallback: use newspaper3k if available
                try:
                    import newspaper
                    article = newspaper.Article(url, fetch_images=False)
                    article.download()
                    article.parse()
                    text = article.text
                except ImportError:
                    # Last resort: basic HTML tag removal
                    import re
                    from html import unescape
                    text = re.sub(r'<[^>]+>', '', response.text)
                    text = unescape(text)
                    # Remove excessive whitespace
                    text = ' '.join(text.split())
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return text.strip()
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

