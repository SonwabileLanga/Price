from django.core.management.base import BaseCommand
from apps.scrapers.advanced_scraper_manager import AdvancedScraperManager


class Command(BaseCommand):
    help = 'Perform deep scraping with advanced techniques'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='iPhone 15',
            help='Search query to scrape (default: iPhone 15)'
        )
        parser.add_argument(
            '--store',
            type=str,
            choices=['takealot', 'game', 'makro', 'all'],
            default='all',
            help='Store to scrape (default: all)'
        )
        parser.add_argument(
            '--pages',
            type=int,
            default=3,
            help='Number of pages to scrape per store (default: 3)'
        )
        parser.add_argument(
            '--retry',
            type=int,
            default=2,
            help='Number of retry attempts (default: 2)'
        )

    def handle(self, *args, **options):
        query = options['query']
        store = options['store']
        pages = options['pages']
        retry = options['retry']
        
        self.stdout.write(f"🚀 Starting deep scraping for: '{query}'")
        self.stdout.write(f"📄 Pages per store: {pages}")
        self.stdout.write(f"🔄 Retry attempts: {retry}")
        self.stdout.write("=" * 50)
        
        scraper_manager = AdvancedScraperManager()
        
        try:
            if store == 'all':
                self.stdout.write("🔍 Deep searching all stores...")
                results = scraper_manager.search_all_stores_deep(query, pages)
            else:
                self.stdout.write(f"🔍 Deep searching {store}...")
                results = scraper_manager.search_specific_store_deep(store, query, pages)
            
            if results:
                self.stdout.write(f"\n✅ Deep scraping completed!")
                self.stdout.write(f"📊 Total results found: {len(results)}")
                self.stdout.write("\n📱 Sample Results:")
                
                # Group results by store
                by_store = {}
                for result in results:
                    store_name = result['store']
                    if store_name not in by_store:
                        by_store[store_name] = []
                    by_store[store_name].append(result)
                
                for store_name, store_results in by_store.items():
                    self.stdout.write(f"\n🏪 {store_name} ({len(store_results)} results):")
                    for i, result in enumerate(store_results[:5], 1):  # Show first 5 per store
                        self.stdout.write(f"  {i}. {result['title'][:60]}...")
                        self.stdout.write(f"     Price: R{result.get('price', 'N/A')}")
                        self.stdout.write(f"     URL: {result['url']}")
                        if result.get('image_url'):
                            self.stdout.write(f"     Image: {result['image_url']}")
                        self.stdout.write()
            else:
                self.stdout.write("❌ No results found from deep scraping.")
                self.stdout.write("💡 This might be due to:")
                self.stdout.write("   - Anti-bot protection on the websites")
                self.stdout.write("   - Network connectivity issues")
                self.stdout.write("   - Website structure changes")
                self.stdout.write("   - Rate limiting")
        
        except Exception as e:
            self.stdout.write(f"❌ Deep scraping failed: {e}")
            self.stdout.write("💡 Try running with fewer pages or different query")
        
        finally:
            # Cleanup
            scraper_manager.close_all_scrapers()
            self.stdout.write("\n🧹 Cleanup completed")
        
        self.stdout.write(self.style.SUCCESS('Deep scraping test completed!'))
