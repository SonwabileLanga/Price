import requests
import time
import re
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.conf import settings


class BaseScraper(ABC):
    """Base class for all store scrapers."""
    
    def __init__(self, store_name: str, base_url: str):
        self.store_name = store_name
        self.base_url = base_url
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_session()
    
    def setup_session(self):
        """Setup session with headers and configuration."""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def normalize_product_name(self, name: str) -> str:
        """Normalize product name for comparison."""
        # Remove extra spaces and convert to lowercase
        normalized = re.sub(r'\s+', ' ', name.strip().lower())
        
        # Remove common words that don't affect comparison
        common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        words = normalized.split()
        filtered_words = [word for word in words if word not in common_words]
        
        return ' '.join(filtered_words)
    
    def extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text."""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group())
            except ValueError:
                return None
        return None
    
    def get_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Get page content with retries."""
        for attempt in range(retries):
            try:
                response = self.session.get(
                    url, 
                    timeout=settings.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                # Add delay between requests
                time.sleep(settings.SCRAPING_DELAY)
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return None
        
        return None
    
    def cache_key(self, query: str) -> str:
        """Generate cache key for search query."""
        return f"scraper_{self.store_name}_{query.lower()}"
    
    def get_cache(self, key: str):
        """Get value from cache."""
        try:
            from django.core.cache import cache
            return cache.get(key)
        except:
            return None
    
    def set_cache(self, key: str, value, timeout: int = 1800):
        """Set value in cache."""
        try:
            from django.core.cache import cache
            cache.set(key, value, timeout)
        except:
            pass
    
    @abstractmethod
    def search_products(self, query: str) -> List[Dict]:
        """Search for products and return list of product data."""
        pass
    
    @abstractmethod
    def extract_product_data(self, product_element) -> Optional[Dict]:
        """Extract product data from a product element."""
        pass
