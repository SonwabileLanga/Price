from typing import List, Dict
from django.core.cache import cache
from .takealot_advanced_scraper import TakealotAdvancedScraper
from .game_advanced_scraper import GameAdvancedScraper
from .makro_advanced_scraper import MakroAdvancedScraper


class AdvancedScraperManager:
    """Advanced manager class to coordinate all deep scrapers."""
    
    def __init__(self):
        self.scrapers = {
            'takealot': TakealotAdvancedScraper(),
            'game': GameAdvancedScraper(),
            'makro': MakroAdvancedScraper(),
        }
    
    def search_all_stores_deep(self, query: str, max_pages: int = 3) -> List[Dict]:
        """Deep search all stores for a given query with pagination."""
        all_results = []
        
        for store_name, scraper in self.scrapers.items():
            try:
                print(f"🔍 Deep searching {store_name} for: {query}")
                results = scraper.search_products_deep(query, max_pages)
                all_results.extend(results)
                print(f"✅ Found {len(results)} results from {store_name}")
            except Exception as e:
                print(f"❌ Error deep searching {store_name}: {e}")
                continue
        
        return all_results
    
    def search_specific_store_deep(self, store_name: str, query: str, max_pages: int = 3) -> List[Dict]:
        """Deep search a specific store with pagination."""
        if store_name not in self.scrapers:
            return []
        
        try:
            print(f"🔍 Deep searching {store_name} for: {query}")
            results = self.scrapers[store_name].search_products_deep(query, max_pages)
            print(f"✅ Found {len(results)} results from {store_name}")
            return results
        except Exception as e:
            print(f"❌ Error deep searching {store_name}: {e}")
            return []
    
    def search_with_retry(self, query: str, max_retries: int = 2) -> List[Dict]:
        """Search with retry mechanism for better reliability."""
        all_results = []
        
        for attempt in range(max_retries):
            print(f"🔄 Search attempt {attempt + 1}/{max_retries}")
            
            for store_name, scraper in self.scrapers.items():
                try:
                    print(f"🔍 Searching {store_name} (attempt {attempt + 1})")
                    results = scraper.search_products_deep(query, max_pages=2)
                    all_results.extend(results)
                    print(f"✅ {store_name}: {len(results)} results")
                except Exception as e:
                    print(f"❌ {store_name} failed (attempt {attempt + 1}): {e}")
                    continue
            
            if all_results:
                break  # If we got results, no need to retry
        
        return all_results
    
    def get_available_stores(self) -> List[str]:
        """Get list of available store names."""
        return list(self.scrapers.keys())
    
    def close_all_scrapers(self):
        """Close all scraper instances to free resources."""
        for scraper in self.scrapers.values():
            try:
                scraper.close()
            except:
                pass
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.close_all_scrapers()
