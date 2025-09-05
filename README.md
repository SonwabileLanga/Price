# 🛒 Price Comparison Application

A comprehensive Django-based web application that compares prices from South African online stores including **Takealot**, **Game**, and **Makro**. The application features advanced web scraping capabilities, beautiful responsive design, and intelligent fallback systems to ensure reliable price comparison data.

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.35.0-orange.svg)](https://selenium.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-purple.svg)](https://getbootstrap.com/)

## 🚀 Live Demo

**Application URL**: http://127.0.0.1:8000/  
**Admin Panel**: http://127.0.0.1:8000/admin/ (admin/admin123)

## ✨ Key Features

### 🔍 **Advanced Web Scraping**
- **Selenium WebDriver**: Handles JavaScript-heavy websites
- **Anti-Bot Detection Bypass**: Advanced techniques to avoid detection
- **Dynamic Content Loading**: Scrolls and loads all product data
- **Pagination Support**: Scrapes multiple pages per store
- **Cookie Consent Handling**: Automatically handles popups

### 🛒 **Price Comparison**
- **Multi-Store Search**: Search across Takealot, Game, and Makro simultaneously
- **Real-Time Data**: Live scraping with intelligent fallback to sample data
- **Product Images**: Display product images from all stores
- **Price History**: Track price changes over time
- **Side-by-Side Comparison**: Easy price comparison interface

### 🎨 **User Experience**
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Product Details**: Comprehensive product information and specifications
- **Search Functionality**: Smart search with autocomplete suggestions
- **Admin Interface**: Full Django admin for data management

### ⚡ **Performance & Reliability**
- **Intelligent Caching**: Reduces scraping load and improves performance
- **Hybrid Scraping**: Multiple fallback strategies ensure reliable results
- **Error Handling**: Robust error handling and retry mechanisms
- **Database Optimization**: Efficient data storage and retrieval

## Tech Stack

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: SQLite (default) / PostgreSQL
- **Web Scraping**: BeautifulSoup4 + Selenium
- **Frontend**: Bootstrap 5 + HTML/CSS/JavaScript
- **Caching**: Django cache framework
- **Image Handling**: Pillow

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd price-comparison
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### Basic Search
1. Go to the home page
2. Enter a product name (e.g., "iPhone 15", "Dell laptop")
3. Click search to see results from all stores
4. Click on any product for detailed information

### Product Comparison
1. Search for products
2. Click "Add to Compare" on products you want to compare
3. Go to the Compare page to see side-by-side comparison

### Admin Features
- View and manage all scraped products
- Monitor price history
- Track search queries
- Manage store configurations

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string (optional)
- `REDIS_URL`: Redis cache URL (optional)

### Scraping Settings
- `SCRAPING_DELAY`: Delay between requests (seconds)
- `MAX_RETRIES`: Maximum retry attempts
- `REQUEST_TIMEOUT`: Request timeout (seconds)

## Project Structure

```
price_comparison/
├── apps/
│   ├── products/          # Main app for products and listings
│   └── scrapers/          # Web scraping modules
├── price_comparison/      # Django project settings
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS)
├── media/                # Media files (images)
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## 🏗️ Scraping Architecture

The application uses a sophisticated **hybrid scraping approach** with multiple layers:

### **Level 1: Advanced Scraping (Selenium)**
- **AdvancedScraper**: Base class with Selenium WebDriver
- **Store-specific advanced scrapers**: Handle JavaScript and dynamic content
- **Anti-bot techniques**: User agent rotation, random delays, headless browsing
- **Dynamic loading**: Scrolls pages to load all content

### **Level 2: Basic Scraping (BeautifulSoup)**
- **BaseScraper**: BeautifulSoup4 for static HTML parsing
- **Store-specific basic scrapers**: Fallback for simple sites
- **Fast parsing**: Quick extraction when JavaScript isn't needed

### **Level 3: Sample Data Fallback**
- **Enhanced sample data**: Realistic product data for demonstration
- **Intelligent matching**: Returns relevant products based on search query
- **Always available**: Ensures users always get results

### **Hybrid Manager**
- **HybridScraperManager**: Orchestrates all scraping levels
- **Intelligent fallback**: Automatically switches between methods
- **Performance optimization**: Caches results and manages resources

## Database Models

- **Store**: Online store information
- **Product**: Product details and normalization
- **ProductListing**: Store-specific product listings
- **PriceHistory**: Historical price data
- **SearchQuery**: Search query tracking

## API Endpoints

- `GET /`: Home page
- `GET /search/`: Search results page
- `GET /product/<id>/`: Product detail page
- `GET /compare/`: Product comparison page
- `POST /api/search/`: API search endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Scraping fails**: Check if websites have changed their structure
2. **Images not loading**: Verify image URLs and CORS settings
3. **Database errors**: Run migrations and check database configuration
4. **Slow performance**: Adjust caching settings and scraping delays

### Debug Mode

Enable debug mode in settings.py to see detailed error messages and enable Django's debug toolbar.

## Future Enhancements

- [ ] Add more South African stores
- [ ] Implement price alerts
- [ ] Add product reviews and ratings
- [ ] Mobile app development
- [ ] Advanced filtering and sorting
- [ ] Export comparison results
- [ ] User accounts and favorites
