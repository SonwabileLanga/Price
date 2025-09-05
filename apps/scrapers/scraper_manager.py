from typing import List, Dict
from django.core.cache import cache
from .takealot_scraper import TakealotScraper
from .game_scraper import GameScraper
from .makro_scraper import MakroScraper


class ScraperManager:
    """Manager class to coordinate all scrapers."""
    
    def __init__(self):
        self.scrapers = {
            'takealot': TakealotScraper(),
            'game': GameScraper(),
            'makro': MakroScraper(),
        }
    
    def search_all_stores(self, query: str) -> List[Dict]:
        """Search all stores for a given query."""
        all_results = []
        
        for store_name, scraper in self.scrapers.items():
            try:
                print(f"Searching {store_name} for: {query}")
                results = scraper.search_products(query)
                all_results.extend(results)
                print(f"Found {len(results)} results from {store_name}")
            except Exception as e:
                print(f"Error searching {store_name}: {e}")
                continue
        
        return all_results
    
    def search_specific_store(self, store_name: str, query: str) -> List[Dict]:
        """Search a specific store."""
        if store_name not in self.scrapers:
            return []
        
        try:
            return self.scrapers[store_name].search_products(query)
        except Exception as e:
            print(f"Error searching {store_name}: {e}")
            return []
    
    def get_available_stores(self) -> List[str]:
        """Get list of available store names."""
        return list(self.scrapers.keys())
