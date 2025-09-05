#!/usr/bin/env python
"""
Test script to verify the price comparison application setup.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_comparison.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Test imports
try:
    from apps.products.models import Store, Product, ProductListing
    from apps.scrapers.scraper_manager import ScraperManager
    print("✅ Model imports successful")
except Exception as e:
    print(f"❌ Model imports failed: {e}")
    sys.exit(1)

# Test scraper manager
try:
    scraper_manager = ScraperManager()
    stores = scraper_manager.get_available_stores()
    print(f"✅ Scraper manager initialized with stores: {stores}")
except Exception as e:
    print(f"❌ Scraper manager failed: {e}")
    sys.exit(1)

# Test database connection
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! The application is ready to run.")
print("\nNext steps:")
print("1. Run: python manage.py makemigrations")
print("2. Run: python manage.py migrate")
print("3. Run: python manage.py createsuperuser")
print("4. Run: python manage.py runserver")
print("5. Visit: http://127.0.0.1:8000/")
