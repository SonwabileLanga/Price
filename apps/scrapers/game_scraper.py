import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class GameScraper(BaseScraper):
    """Scraper for Game.co.za"""
    
    def __init__(self):
        super().__init__("Game", "https://www.game.co.za")
    
    def search_products(self, query: str) -> List[Dict]:
        """Search for products on Game."""
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
        
        # Look for product containers - Game uses different class names
        product_containers = soup.find_all('div', class_=re.compile(r'product.*item|product.*card|item.*product'))
        
        if not product_containers:
            # Try alternative selectors
            product_containers = soup.find_all('div', {'data-testid': re.compile(r'product.*')})
        
        if not product_containers:
            # Try looking for product links
            product_links = soup.find_all('a', href=re.compile(r'/product/|/item/'))
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
            
            # Extract price - Game might use different price class names
            price_element = product_element.find('span', class_=re.compile(r'price|amount|cost'))
            if not price_element:
                # Try alternative price selectors
                price_element = product_element.find('div', class_=re.compile(r'price|amount'))
            
            if not price_element:
                # Try looking for text that looks like a price
                price_text = product_element.get_text()
                price_match = re.search(r'R\s*[\d,]+\.?\d*', price_text)
                if price_match:
                    price_element = type('obj', (object,), {'get_text': lambda: price_match.group()})
            
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
            elif img_element and img_element.get('data-src'):
                image_url = img_element['data-src']
                if not image_url.startswith('http'):
                    image_url = self.base_url + image_url
            
            # Extract product ID from URL
            product_id = None
            if '/product/' in url or '/item/' in url:
                product_id = url.split('/')[-1].split('?')[0]
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'image_url': image_url,
                'product_id': product_id,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Error extracting product data from Game: {e}")
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
                    price_element = parent.find('span', class_=re.compile(r'price|amount|cost'))
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
            if img_element:
                if img_element.get('src'):
                    image_url = img_element['src']
                elif img_element.get('data-src'):
                    image_url = img_element['data-src']
                
                if image_url and not image_url.startswith('http'):
                    image_url = self.base_url + image_url
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'image_url': image_url,
                'product_id': url.split('/')[-1].split('?')[0] if '/product/' in url or '/item/' in url else None,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Error extracting from link: {e}")
            return None
