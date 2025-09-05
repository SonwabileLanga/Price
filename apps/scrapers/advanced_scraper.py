import requests
import time
import re
import json
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import random


class AdvancedScraper:
    """Advanced scraper with Selenium for JavaScript-heavy sites and anti-bot bypass."""
    
    def __init__(self, store_name: str, base_url: str):
        self.store_name = store_name
        self.base_url = base_url
        self.ua = UserAgent()
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with anti-detection measures."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Faster loading
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            self.driver = None
    
    def random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Add random delay to mimic human behavior."""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page(self, scroll_pause_time: float = 2.0):
        """Scroll page to load dynamic content."""
        if not self.driver:
            return
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def search_products_deep(self, query: str, max_pages: int = 3) -> List[Dict]:
        """Deep search with pagination and dynamic content loading."""
        if not self.driver:
            return []
        
        all_products = []
        
        try:
            # Navigate to search page
            search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
            self.driver.get(search_url)
            self.random_delay(2, 4)
            
            # Handle cookie consent if present
            self.handle_cookie_consent()
            
            # Scroll to load dynamic content
            self.scroll_page()
            
            # Extract products from current page
            products = self.extract_products_from_page()
            all_products.extend(products)
            
            # Try to find and click pagination
            for page in range(2, max_pages + 1):
                if self.go_to_next_page(page):
                    self.random_delay(2, 4)
                    self.scroll_page()
                    products = self.extract_products_from_page()
                    all_products.extend(products)
                else:
                    break
            
            return all_products[:50]  # Limit to 50 results
            
        except Exception as e:
            print(f"Error in deep search: {e}")
            return all_products
    
    def handle_cookie_consent(self):
        """Handle cookie consent popups."""
        if not self.driver:
            return
        
        try:
            # Common cookie consent selectors
            cookie_selectors = [
                "button[data-testid*='cookie']",
                "button[class*='cookie']",
                "button[class*='accept']",
                "button[class*='consent']",
                "button:contains('Accept')",
                "button:contains('OK')",
                "button:contains('I agree')",
                ".cookie-accept",
                "#cookie-accept",
                "[data-testid='cookie-accept']"
            ]
            
            for selector in cookie_selectors:
                try:
                    if selector.startswith("button:contains"):
                        # Use XPath for text-based selectors
                        text_content = selector.split('contains(')[1].split(')')[0].strip("'")
                        xpath = f"//button[contains(text(), '{text_content}')]"
                        element = self.driver.find_element(By.XPATH, xpath)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        self.random_delay(1, 2)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Cookie consent handling failed: {e}")
    
    def go_to_next_page(self, page_num: int) -> bool:
        """Navigate to next page of results."""
        if not self.driver:
            return False
        
        try:
            # Common pagination selectors
            pagination_selectors = [
                f"a[href*='page={page_num}']",
                f"button[data-page='{page_num}']",
                f"a:contains('{page_num}')",
                ".pagination a",
                ".pager a",
                "[data-testid*='pagination'] a",
                ".next-page",
                "#next-page"
            ]
            
            for selector in pagination_selectors:
                try:
                    if selector.endswith("a"):
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if str(page_num) in element.text or str(page_num) in element.get_attribute('href'):
                                element.click()
                                return True
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        element.click()
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Pagination failed: {e}")
            return False
    
    def extract_products_from_page(self) -> List[Dict]:
        """Extract products from current page using multiple strategies."""
        if not self.driver:
            return []
        
        products = []
        
        try:
            # Strategy 1: Look for product containers
            product_containers = self.driver.find_elements(By.CSS_SELECTOR, 
                "div[data-testid*='product'], .product-item, .product-card, .product-container, [class*='product']")
            
            if not product_containers:
                # Strategy 2: Look for product links
                product_containers = self.driver.find_elements(By.CSS_SELECTOR, 
                    "a[href*='/product/'], a[href*='/item/'], a[href*='/p/']")
            
            if not product_containers:
                # Strategy 3: Look for any clickable elements that might be products
                product_containers = self.driver.find_elements(By.CSS_SELECTOR, 
                    "div[class*='item'], div[class*='card'], div[class*='listing']")
            
            for container in product_containers[:20]:  # Limit to 20 per page
                try:
                    product_data = self.extract_product_data_advanced(container)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error extracting products: {e}")
            return products
    
    def extract_product_data_advanced(self, container) -> Optional[Dict]:
        """Advanced product data extraction with multiple fallback strategies."""
        try:
            # Extract title
            title = self.extract_title(container)
            if not title:
                return None
            
            # Extract URL
            url = self.extract_url(container)
            if not url:
                return None
            
            # Extract price
            price = self.extract_price_advanced(container)
            
            # Extract image
            image_url = self.extract_image_url(container)
            
            # Extract product ID
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
            print(f"Error extracting product data: {e}")
            return None
    
    def extract_title(self, container) -> Optional[str]:
        """Extract product title with multiple strategies."""
        title_selectors = [
            "h1", "h2", "h3", "h4", "h5", "h6",
            "[data-testid*='title']",
            "[class*='title']",
            "[class*='name']",
            "a[href*='/product/']",
            ".product-title",
            ".product-name"
        ]
        
        for selector in title_selectors:
            try:
                element = container.find_element(By.CSS_SELECTOR, selector)
                title = element.text.strip()
                if title and len(title) > 3:
                    return title
            except:
                continue
        
        # Fallback: get text from container
        try:
            title = container.text.strip()
            if title and len(title) > 3:
                return title.split('\n')[0]  # Get first line
        except:
            pass
        
        return None
    
    def extract_url(self, container) -> Optional[str]:
        """Extract product URL with multiple strategies."""
        url_selectors = [
            "a[href*='/product/']",
            "a[href*='/item/']",
            "a[href*='/p/']",
            "a[href]"
        ]
        
        for selector in url_selectors:
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
    
    def extract_price_advanced(self, container) -> Optional[float]:
        """Advanced price extraction with multiple strategies."""
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
                    # Use XPath for text-based selectors
                    xpath = "//span[contains(text(), 'R')] | //div[contains(text(), 'R')]"
                    elements = container.find_elements(By.XPATH, xpath)
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
        
        # Fallback: search in all text
        try:
            text = container.text
            price = self.parse_price(text)
            if price:
                return price
        except:
            pass
        
        return None
    
    def parse_price(self, text: str) -> Optional[float]:
        """Parse price from text with multiple patterns."""
        if not text:
            return None
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Price patterns
        patterns = [
            r'R\s*([\d,]+\.?\d*)',
            r'R\s*([\d,]+)',
            r'([\d,]+\.?\d*)\s*R',
            r'([\d,]+)\s*R',
            r'([\d,]+\.?\d*)',
            r'([\d,]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    price_str = match.group(1).replace(',', '')
                    return float(price_str)
                except ValueError:
                    continue
        
        return None
    
    def extract_image_url(self, container) -> Optional[str]:
        """Extract product image URL with multiple strategies."""
        img_selectors = [
            "img[src]",
            "img[data-src]",
            "img[data-lazy]",
            "img[data-original]",
            "[class*='image'] img",
            "[class*='photo'] img"
        ]
        
        for selector in img_selectors:
            try:
                element = container.find_element(By.CSS_SELECTOR, selector)
                img_url = element.get_attribute('src') or element.get_attribute('data-src') or element.get_attribute('data-lazy')
                if img_url and not img_url.startswith('data:'):
                    if not img_url.startswith('http'):
                        img_url = self.base_url + img_url
                    return img_url
            except:
                continue
        
        return None
    
    def extract_product_id(self, url: str) -> Optional[str]:
        """Extract product ID from URL."""
        if not url:
            return None
        
        # Extract ID from various URL patterns
        patterns = [
            r'/product/([^/?]+)',
            r'/item/([^/?]+)',
            r'/p/([^/?]+)',
            r'/([^/?]+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.close()
