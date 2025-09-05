from django.core.management.base import BaseCommand
from apps.scrapers.hybrid_scraper_manager import HybridScraperManager


class Command(BaseCommand):
    help = 'Test hybrid scraping with enhanced sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='iPhone',
            help='Search query to test (default: iPhone)'
        )
        parser.add_argument(
            '--store',
            type=str,
            choices=['takealot', 'game', 'makro', 'all'],
            default='all',
            help='Store to test (default: all)'
        )

    def handle(self, *args, **options):
        query = options['query']
        store = options['store']
        
        self.stdout.write(f"🚀 Testing Hybrid Scraping for: '{query}'")
        self.stdout.write("=" * 50)
        
        scraper_manager = HybridScraperManager()
        
        try:
            if store == 'all':
                self.stdout.write("🔍 Testing hybrid search across all stores...")
                results = scraper_manager.search_all_stores_hybrid(query)
            else:
                self.stdout.write(f"🔍 Testing hybrid search for {store}...")
                results = scraper_manager.search_specific_store_hybrid(store, query)
            
            if results:
                self.stdout.write(f"\n✅ Hybrid scraping completed!")
                self.stdout.write(f"📊 Total results found: {len(results)}")
                self.stdout.write("\n📱 Results by Store:")
                
                # Group results by store
                by_store = {}
                for result in results:
                    store_name = result['store']
                    if store_name not in by_store:
                        by_store[store_name] = []
                    by_store[store_name].append(result)
                
                for store_name, store_results in by_store.items():
                    self.stdout.write(f"\n🏪 {store_name} ({len(store_results)} results):")
                    for i, result in enumerate(store_results, 1):
                        self.stdout.write(f"  {i}. {result['title']}")
                        price = result.get('price', 0)
                        if price and price > 0:
                            self.stdout.write(f"     💰 Price: R{price:,.2f}")
                        else:
                            self.stdout.write(f"     💰 Price: N/A")
                        self.stdout.write(f"     🔗 URL: {result['url']}")
                        if result.get('image_url'):
                            self.stdout.write(f"     🖼️ Image: {result['image_url']}")
                        self.stdout.write()
                
                # Show price comparison
                if len(results) > 1:
                    self.stdout.write("💰 Price Comparison:")
                    sorted_results = sorted(results, key=lambda x: x.get('price', 0))
                    for i, result in enumerate(sorted_results, 1):
                        price = result.get('price', 0)
                        if price > 0:
                            self.stdout.write(f"  {i}. {result['store']}: R{price:,.2f}")
                
            else:
                self.stdout.write("❌ No results found from hybrid scraping.")
        
        except Exception as e:
            self.stdout.write(f"❌ Hybrid scraping failed: {e}")
        
        finally:
            # Cleanup
            scraper_manager.close_all_scrapers()
            self.stdout.write("\n🧹 Cleanup completed")
        
        self.stdout.write(self.style.SUCCESS('Hybrid scraping test completed!'))
