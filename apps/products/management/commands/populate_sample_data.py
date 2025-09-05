from django.core.management.base import BaseCommand
from apps.products.models import Store, Product, ProductListing
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")
        
        # Create stores
        stores_data = [
            {'name': 'Takealot', 'base_url': 'https://www.takealot.com'},
            {'name': 'Game', 'base_url': 'https://www.game.co.za'},
            {'name': 'Makro', 'base_url': 'https://www.makro.co.za'},
        ]
        
        stores = {}
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                defaults={'base_url': store_data['base_url']}
            )
            stores[store.name] = store
            if created:
                self.stdout.write(f"Created store: {store.name}")
        
        # Sample products
        sample_products = [
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'brand': 'Apple',
                'model': 'iPhone 15 Pro Max',
                'category': 'Smartphones',
                'listings': [
                    {'store': 'Takealot', 'price': 24999.00, 'title': 'Apple iPhone 15 Pro Max 256GB - Natural Titanium'},
                    {'store': 'Game', 'price': 25999.00, 'title': 'Apple iPhone 15 Pro Max 256GB Natural Titanium'},
                    {'store': 'Makro', 'price': 24499.00, 'title': 'iPhone 15 Pro Max 256GB Natural Titanium'},
                ]
            },
            {
                'name': 'Samsung Galaxy S24 Ultra 512GB',
                'brand': 'Samsung',
                'model': 'Galaxy S24 Ultra',
                'category': 'Smartphones',
                'listings': [
                    {'store': 'Takealot', 'price': 22999.00, 'title': 'Samsung Galaxy S24 Ultra 512GB - Titanium Black'},
                    {'store': 'Game', 'price': 23999.00, 'title': 'Samsung Galaxy S24 Ultra 512GB Titanium Black'},
                    {'store': 'Makro', 'price': 22499.00, 'title': 'Galaxy S24 Ultra 512GB Titanium Black'},
                ]
            },
            {
                'name': 'Dell XPS 15 Laptop',
                'brand': 'Dell',
                'model': 'XPS 15',
                'category': 'Laptops',
                'listings': [
                    {'store': 'Takealot', 'price': 32999.00, 'title': 'Dell XPS 15 9530 Laptop - Intel i7, 16GB RAM, 512GB SSD'},
                    {'store': 'Game', 'price': 33999.00, 'title': 'Dell XPS 15 9530 Intel i7 16GB 512GB SSD'},
                    {'store': 'Makro', 'price': 31999.00, 'title': 'Dell XPS 15 9530 Laptop Intel i7 16GB 512GB'},
                ]
            },
            {
                'name': 'MacBook Pro 14-inch M3',
                'brand': 'Apple',
                'model': 'MacBook Pro 14-inch',
                'category': 'Laptops',
                'listings': [
                    {'store': 'Takealot', 'price': 29999.00, 'title': 'Apple MacBook Pro 14-inch M3 Chip 8GB RAM 512GB SSD'},
                    {'store': 'Game', 'price': 30999.00, 'title': 'MacBook Pro 14-inch M3 8GB 512GB SSD Space Gray'},
                    {'store': 'Makro', 'price': 28999.00, 'title': 'MacBook Pro 14-inch M3 8GB 512GB Space Gray'},
                ]
            },
            {
                'name': 'Sony WH-1000XM5 Headphones',
                'brand': 'Sony',
                'model': 'WH-1000XM5',
                'category': 'Audio',
                'listings': [
                    {'store': 'Takealot', 'price': 4999.00, 'title': 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones'},
                    {'store': 'Game', 'price': 5199.00, 'title': 'Sony WH-1000XM5 Noise Cancelling Wireless Headphones'},
                    {'store': 'Makro', 'price': 4799.00, 'title': 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones Black'},
                ]
            }
        ]
        
        for product_data in sample_products:
            # Create product
            product, created = Product.objects.get_or_create(
                normalized_name=product_data['name'].lower(),
                defaults={
                    'name': product_data['name'],
                    'brand': product_data['brand'],
                    'model': product_data['model'],
                    'category': product_data['category'],
                }
            )
            
            if created:
                self.stdout.write(f"Created product: {product.name}")
            
            # Create listings
            for listing_data in product_data['listings']:
                store = stores[listing_data['store']]
                listing, created = ProductListing.objects.get_or_create(
                    product=product,
                    store=store,
                    defaults={
                        'title': listing_data['title'],
                        'url': f"{store.base_url}/product/{product.id}",
                        'image_url': f"https://via.placeholder.com/300x200?text={product.name.replace(' ', '+')}",
                        'current_price': Decimal(str(listing_data['price'])),
                        'is_available': True,
                    }
                )
                
                if created:
                    self.stdout.write(f"Created listing: {listing.title} - R{listing.current_price}")
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write("You can now visit http://127.0.0.1:8000/ to see the application with sample data.")
