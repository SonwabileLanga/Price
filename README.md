# Price Comparison Application

A Django-based web application that compares prices from South African online stores including Takealot, Game, and Makro. The application scrapes product data including images and prices, stores them in a database, and provides a user-friendly interface for comparison.

## Features

- **Multi-Store Search**: Search across Takealot, Game, and Makro simultaneously
- **Product Images**: Display product images from all stores
- **Price Comparison**: Compare prices side-by-side
- **Price History**: Track price changes over time
- **Product Details**: Detailed product information and specifications
- **Responsive Design**: Mobile-friendly interface
- **Caching**: Intelligent caching to reduce scraping load
- **Admin Interface**: Django admin for managing data

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

## Scraping Architecture

The application uses a modular scraping approach:

1. **BaseScraper**: Abstract base class with common functionality
2. **Store-specific scrapers**: TakealotScraper, GameScraper, MakroScraper
3. **ScraperManager**: Coordinates all scrapers
4. **Caching**: Results are cached to avoid repeated scraping
5. **Error handling**: Robust error handling and retry logic

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
