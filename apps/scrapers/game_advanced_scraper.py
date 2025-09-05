import time
import re
from typing import List, Dict, Optional
from .advanced_scraper import AdvancedScraper


class GameAdvancedScraper(AdvancedScraper):
    """Advanced scraper for Game.co.za with deep scraping capabilities."""
    
    def __init__(self):
        super().__init__("Game", "https://www.game.co.za")
    
    def search_products_deep(self, query: str, max_pages: int = 3) -> List[Dict]:
        """Deep search on Game with specific optimizations."""
        if not self.driver:
            return []
        
        all_products = []
        
        try:
            # Navigate to search page
            search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
            self.driver.get(search_url)
            self.random_delay(3, 5)  # Longer delay for Game
            
            # Handle Game-specific elements
            self.handle_game_specifics()
            
            # Scroll to load all products
            self.scroll_page(scroll_pause_time=2.5)
            
            # Extract products with Game-specific selectors
            products = self.extract_game_products()
            all_products.extend(products)
            
            # Try pagination
            for page in range(2, max_pages + 1):
                if self.go_to_game_next_page(page):
                    self.random_delay(3, 5)
                    self.scroll_page(scroll_pause_time=2.5)
                    products = self.extract_game_products()
                    all_products.extend(products)
                else:
                    break
            
            return all_products[:50]
            
        except Exception as e:
            print(f"Error in Game deep search: {e}")
            return all_products
    
    def handle_game_specifics(self):
        """Handle Game-specific popups and elements."""
        if not self.driver:
            return
        
        try:
            # Handle cookie consent
            self.handle_cookie_consent()
            
            # Handle Game-specific popups
            popup_selectors = [
                "button[data-testid='close-button']",
                ".modal-close",
                "[class*='close']",
                "[class*='dismiss']",
                "button:contains('Close')",
                "button:contains('×')",
                "[class*='popup'] button",
                "[class*='overlay'] button"
            ]
            
            for selector in popup_selectors:
                try:
                    if selector.endswith("×')"):
                        elements = self.driver.find_elements(By.XPATH, "//button[contains(text(), '×')]")
                    elif selector.endswith("Close')"):
                        elements = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Close')]")
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            self.random_delay(1, 2)
                            break
                except:
                    continue
                    
        except Exception as e:
            print(f"Game-specific handling failed: {e}")
    
    def go_to_game_next_page(self, page_num: int) -> bool:
        """Navigate to next page on Game."""
        if not self.driver:
            return False
        
        try:
            # Game-specific pagination selectors
            pagination_selectors = [
                f"a[href*='page={page_num}']",
                f"button[data-page='{page_num}']",
                ".pagination a",
                ".pager a",
                "[data-testid*='pagination'] a",
                ".next-page",
                "#next-page",
                "button:contains('Next')",
                "a:contains('Next')",
                "[class*='pagination'] a",
                "[class*='pager'] a"
            ]
            
            for selector in pagination_selectors:
                try:
                    if selector.endswith("Next')"):
                        elements = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //button[contains(text(), 'Next')]")
                        for element in elements:
                            if element.is_displayed():
                                element.click()
                                return True
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if str(page_num) in element.text or str(page_num) in element.get_attribute('href'):
                                if element.is_displayed():
                                    element.click()
                                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Game pagination failed: {e}")
            return False
    
    def extract_game_products(self) -> List[Dict]:
        """Extract products using Game-specific selectors."""
        if not self.driver:
            return []
        
        products = []
        
        try:
            # Game-specific product selectors
            product_selectors = [
                "div[data-testid*='product']",
                ".product-item",
                ".product-card",
                ".product-container",
                "[class*='product-item']",
                "[class*='product-card']",
                "div[data-testid='product-item']",
                "article[data-testid*='product']",
                "[class*='item']",
                "[class*='card']",
                "[class*='listing']"
            ]
            
            product_containers = []
            for selector in product_selectors:
                try:
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    product_containers.extend(containers)
                except:
                    continue
            
            # Remove duplicates
            product_containers = list(set(product_containers))
            
            for container in product_containers[:20]:
                try:
                    product_data = self.extract_game_product_data(container)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error extracting Game products: {e}")
            return products
    
    def extract_game_product_data(self, container) -> Optional[Dict]:
        """Extract product data with Game-specific logic."""
        try:
            # Title extraction
            title = self.extract_game_title(container)
            if not title:
                return None
            
            # URL extraction
            url = self.extract_game_url(container)
            if not url:
                return None
            
            # Price extraction
            price = self.extract_game_price(container)
            
            # Image extraction
            image_url = self.extract_game_image(container)
            
            # Product ID
            product_id = self.extract_product_id(url)
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'image_url': image_url,
                'product_id': product_id,
                'store': self.store_name
            }
            
        except Exception as e:
            print(f"Error extracting Game product data: {e}")
            return None
    
    def extract_game_title(self, container) -> Optional[str]:
        """Extract title with Game-specific selectors."""
        title_selectors = [
            "h3[data-testid*='title']",
            "h4[data-testid*='title']",
            "[data-testid*='product-title']",
            "[class*='product-title']",
            "[class*='product-name']",
            "a[href*='/product/']",
            "a[href*='/item/']",
            "h3", "h4", "h5",
            "[class*='title']",
            "[class*='name']"
        ]
        
        for selector in title_selectors:
            try:
                element = container.find_element(By.CSS_SELECTOR, selector)
                title = element.text.strip()
                if title and len(title) > 3:
                    return title
            except:
                continue
        
        return None
    
    def extract_game_url(self, container) -> Optional[str]:
        """Extract URL with Game-specific logic."""
        try:
            # Look for product links
            link_selectors = [
                "a[href*='/product/']",
                "a[href*='/item/']",
                "a[href*='/p/']",
                "a[href]"
            ]
            
            for selector in link_selectors:
                try:
                    element = container.find_element(By.CSS_SELECTOR, selector)
                    url = element.get_attribute('href')
                    if url and ('/product/' in url or '/item/' in url or '/p/' in url):
                        if not url.startswith('http'):
                            url = self.base_url + url
                        return url
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None
    
    def extract_game_price(self, container) -> Optional[float]:
        """Extract price with Game-specific selectors."""
        price_selectors = [
            "[data-testid*='price']",
            "[class*='price']",
            "[class*='amount']",
            "[class*='cost']",
            ".price",
            ".amount",
            ".cost",
            "span:contains('R')",
            "div:contains('R')"
        ]
        
        for selector in price_selectors:
            try:
                if selector.endswith("R')"):
                    elements = container.find_elements(By.XPATH, "//span[contains(text(), 'R')] | //div[contains(text(), 'R')]")
                    for element in elements:
                        price_text = element.text.strip()
                        price = self.parse_price(price_text)
                        if price:
                            return price
                else:
                    element = container.find_element(By.CSS_SELECTOR, selector)
                    price_text = element.text.strip()
                    price = self.parse_price(price_text)
                    if price:
                        return price
            except:
                continue
        
        return None
    
    def extract_game_image(self, container) -> Optional[str]:
        """Extract image with Game-specific selectors."""
        img_selectors = [
            "img[data-testid*='image']",
            "img[class*='product-image']",
            "img[class*='item-image']",
            "img[src]",
            "img[data-src]",
            "img[data-lazy]",
            "img[data-original]"
        ]
        
        for selector in img_selectors:
            try:
                element = container.find_element(By.CSS_SELECTOR, selector)
                img_url = element.get_attribute('src') or element.get_attribute('data-src') or element.get_attribute('data-lazy') or element.get_attribute('data-original')
                if img_url and not img_url.startswith('data:'):
                    if not img_url.startswith('http'):
                        img_url = self.base_url + img_url
                    return img_url
            except:
                continue
        
        return None
