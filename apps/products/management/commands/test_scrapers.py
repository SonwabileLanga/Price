from django.core.management.base import BaseCommand
from apps.scrapers.scraper_manager import ScraperManager


class Command(BaseCommand):
    help = 'Test web scrapers with a sample search query'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='iPhone 15',
            help='Search query to test (default: iPhone 15)'
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
        
        self.stdout.write(f"Testing scrapers with query: '{query}'")
        
        scraper_manager = ScraperManager()
        
        if store == 'all':
            self.stdout.write("Searching all stores...")
            results = scraper_manager.search_all_stores(query)
        else:
            self.stdout.write(f"Searching {store}...")
            results = scraper_manager.search_specific_store(store, query)
        
        if results:
            self.stdout.write(f"\nFound {len(results)} results:")
            for i, result in enumerate(results[:5], 1):  # Show first 5 results
                self.stdout.write(f"\n{i}. {result['title']}")
                self.stdout.write(f"   Store: {result['store']}")
                self.stdout.write(f"   Price: R{result.get('price', 'N/A')}")
                self.stdout.write(f"   URL: {result['url']}")
                if result.get('image_url'):
                    self.stdout.write(f"   Image: {result['image_url']}")
        else:
            self.stdout.write("No results found.")
        
        self.stdout.write(self.style.SUCCESS('Scraper test completed!'))
