from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q, Min
from django.utils import timezone
from django.core.cache import cache
import json
from typing import List, Dict

from .models import Product, ProductListing, Store, SearchQuery, PriceHistory
from apps.scrapers.hybrid_scraper_manager import HybridScraperManager


def home(request):
    """Home page with search functionality."""
    return render(request, 'products/home.html')


def search_results(request):
    """Display search results."""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'products/search_results.html', {
            'query': '',
            'results': [],
            'message': 'Please enter a search term.'
        })
    
    # Record search query
    SearchQuery.objects.create(
        query=query,
        user_ip=request.META.get('REMOTE_ADDR')
    )
    
    # Check cache first
    cache_key = f"search_results_{query.lower()}"
    cached_results = cache.get(cache_key)
    
    if cached_results:
        results = cached_results
    else:
        # Search all stores using hybrid approach
        scraper_manager = HybridScraperManager()
        scraped_results = scraper_manager.search_all_stores_hybrid(query)
        
        # Process and save results
        results = process_and_save_results(scraped_results, query)
        
        # Cache results for 30 minutes
        cache.set(cache_key, results, 1800)
    
    # Update search query with results count
    SearchQuery.objects.filter(query=query).update(results_count=len(results))
    
    # Paginate results
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/search_results.html', {
        'query': query,
        'results': page_obj,
        'total_results': len(results)
    })


def process_and_save_results(scraped_results: List[Dict], query: str) -> List[Dict]:
    """Process scraped results and save to database."""
    processed_results = []
    
    for result in scraped_results:
        try:
            # Normalize product name
            normalized_name = normalize_product_name(result['title'])
            
            # Get or create product
            product, created = Product.objects.get_or_create(
                normalized_name=normalized_name,
                defaults={
                    'name': result['title'],
                    'brand': extract_brand(result['title']),
                    'model': extract_model(result['title']),
                }
            )
            
            # Get or create store
            store, created = Store.objects.get_or_create(
                name=result['store'],
                defaults={'base_url': get_store_url(result['store'])}
            )
            
            # Get or create product listing
            listing, created = ProductListing.objects.get_or_create(
                product=product,
                store=store,
                defaults={
                    'title': result['title'],
                    'url': result['url'],
                    'image_url': result.get('image_url', ''),
                    'current_price': result.get('price', 0) or 0,
                    'is_available': result.get('price') is not None,
                }
            )
            
            # Update listing if price changed
            if result.get('price') and listing.current_price != result['price']:
                # Save price history
                PriceHistory.objects.create(
                    listing=listing,
                    price=listing.current_price,
                    is_available=listing.is_available
                )
                
                # Update current price
                listing.current_price = result['price']
                listing.is_available = True
                listing.last_updated = timezone.now()
                listing.save()
            
            # Add to processed results
            processed_results.append({
                'id': listing.id,
                'title': listing.title,
                'url': listing.url,
                'price': float(listing.current_price) if listing.current_price else None,
                'image_url': listing.image_url,
                'store': store.name,
                'store_url': store.base_url,
                'is_available': listing.is_available,
                'last_updated': listing.last_updated,
            })
            
        except Exception as e:
            print(f"Error processing result: {e}")
            continue
    
    return processed_results


def normalize_product_name(name: str) -> str:
    """Normalize product name for comparison."""
    import re
    
    # Remove extra spaces and convert to lowercase
    normalized = re.sub(r'\s+', ' ', name.strip().lower())
    
    # Remove common words that don't affect comparison
    common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    words = normalized.split()
    filtered_words = [word for word in words if word not in common_words]
    
    return ' '.join(filtered_words)


def extract_brand(name: str) -> str:
    """Extract brand from product name."""
    # Common brand patterns
    brands = ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'NVIDIA', 'AMD', 'Intel']
    
    for brand in brands:
        if brand.lower() in name.lower():
            return brand
    
    return ''


def extract_model(name: str) -> str:
    """Extract model from product name."""
    import re
    
    # Look for model patterns like "iPhone 15 Pro", "Galaxy S24", etc.
    model_patterns = [
        r'iPhone\s+\d+[A-Za-z\s]*',
        r'Galaxy\s+[A-Za-z0-9\s]+',
        r'MacBook\s+[A-Za-z0-9\s]+',
        r'Dell\s+[A-Za-z0-9\s]+',
        r'HP\s+[A-Za-z0-9\s]+',
    ]
    
    for pattern in model_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return match.group().strip()
    
    return ''


def get_store_url(store_name: str) -> str:
    """Get base URL for store."""
    store_urls = {
        'Takealot': 'https://www.takealot.com',
        'Game': 'https://www.game.co.za',
        'Makro': 'https://www.makro.co.za',
    }
    return store_urls.get(store_name, '')


@csrf_exempt
def api_search(request):
    """API endpoint for search."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if not query:
            return JsonResponse({'error': 'Query parameter required'}, status=400)
        
        # Search all stores using hybrid approach
        scraper_manager = HybridScraperManager()
        results = scraper_manager.search_all_stores_hybrid(query)
        
        # Process results
        processed_results = process_and_save_results(results, query)
        
        return JsonResponse({
            'query': query,
            'results': processed_results,
            'total': len(processed_results)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def product_detail(request, product_id):
    """Product detail page with price history."""
    listing = get_object_or_404(ProductListing, id=product_id)
    
    # Get price history
    price_history = PriceHistory.objects.filter(listing=listing).order_by('-recorded_at')[:30]
    
    # Get similar products
    similar_products = ProductListing.objects.filter(
        product__normalized_name=listing.product.normalized_name
    ).exclude(id=product_id).order_by('current_price')
    
    return render(request, 'products/product_detail.html', {
        'listing': listing,
        'price_history': price_history,
        'similar_products': similar_products,
    })


def compare_products(request):
    """Compare multiple products."""
    product_ids = request.GET.getlist('products')
    
    if not product_ids:
        return render(request, 'products/compare.html', {
            'products': [],
            'message': 'No products selected for comparison.'
        })
    
    products = ProductListing.objects.filter(id__in=product_ids).order_by('current_price')
    
    return render(request, 'products/compare.html', {
        'products': products,
    })
