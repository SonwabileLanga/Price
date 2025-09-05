import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class TakealotScraper(BaseScraper):
    """Scraper for Takealot.com"""
    
    def __init__(self):
        super().__init__("Takealot", "https://www.takealot.com")
    
    def search_products(self, query: str) -> List[Dict]:
        """Search for products on Takealot."""
        # Check cache first
        cache_key = self.cache_key(query)
        cached_results = self.get_cache(cache_key)
        if cached_results:
            return cached_results
        
        search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
        soup = self.get_page(search_url)
        
        if not soup:
            return []
        
        products = []
        
        # Look for product containers
        product_containers = soup.find_all('div', class_=re.compile(r'product.*container|product.*item'))
        
        if not product_containers:
            # Try alternative selectors
            product_containers = soup.find_all('div', {'data-testid': re.compile(r'product.*')})
        
        if not product_containers:
            # Try looking for product links
            product_links = soup.find_all('a', href=re.compile(r'/product/'))
            for link in product_links[:10]:  # Limit to first 10 results
                product_data = self.extract_from_link(link)
                if product_data:
                    products.append(product_data)
        else:
            for container in product_containers[:10]:  # Limit to first 10 results
                product_data = self.extract_product_data(container)
                if product_data:
                    products.append(product_data)
        
        # Cache results for 30 minutes
        self.set_cache(cache_key, products, 1800)
        return products
    
    def extract_product_data(self, product_element) -> Optional[Dict]:
        """Extract product data from a product element."""
        try:
            # Extract title
            title_element = product_element.find('h3') or product_element.find('h4') or product_element.find('a')
            if not title_element:
                return None
            
            title = title_element.get_text(strip=True)
            if not title:
                return None
            
            # Extract URL
            link_element = product_element.find('a', href=True)
            if not link_element:
                return None
            
            url = link_element['href']
            if not url.startswith('http'):
                url = self.base_url + url
            
            # Extract price
            price_element = product_element.find('span', class_=re.compile(r'price|amount'))
            if not price_element:
                # Try alternative price selectors
                price_element = product_element.find('div', class_=re.compile(r'price'))
            
            price = None
            if price_element:
                price_text = price_element.get_text(strip=True)
                price = self.extract_price(price_text)
            
            # Extract image
            img_element = product_element.find('img')
            image_url = None
            if img_element and img_element.get('src'):
                image_url = img_element['src']
                if not image_url.startswith('http'):
                    image_url = self.base_url + image_url
            
            # Extract product ID from URL
            product_id = None
            if '/product/' in url:
                product_id = url.split('/product/')[-1].split('?')[0]
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'image_url': image_url,
                'product_id': product_id,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Error extracting product data from Takealot: {e}")
            return None
    
    def extract_from_link(self, link_element) -> Optional[Dict]:
        """Extract product data from a product link."""
        try:
            title = link_element.get_text(strip=True)
            if not title:
                return None
            
            url = link_element['href']
            if not url.startswith('http'):
                url = self.base_url + url
            
            # Try to find price in parent elements
            price = None
            parent = link_element.parent
            for _ in range(3):  # Check up to 3 parent levels
                if parent:
                    price_element = parent.find('span', class_=re.compile(r'price|amount'))
                    if price_element:
                        price_text = price_element.get_text(strip=True)
                        price = self.extract_price(price_text)
                        break
                    parent = parent.parent
                else:
                    break
            
            # Try to find image
            image_url = None
            img_element = link_element.find('img')
            if img_element and img_element.get('src'):
                image_url = img_element['src']
                if not image_url.startswith('http'):
                    image_url = self.base_url + image_url
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'image_url': image_url,
                'product_id': url.split('/product/')[-1].split('?')[0] if '/product/' in url else None,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Error extracting from link: {e}")
            return None
