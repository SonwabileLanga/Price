from django.db import models
from django.utils import timezone


class Store(models.Model):
    """Model representing different online stores."""
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(max_length=500)
    normalized_name = models.CharField(max_length=500, db_index=True)
    category = models.CharField(max_length=200, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['normalized_name']
        indexes = [
            models.Index(fields=['normalized_name']),
            models.Index(fields=['brand', 'model']),
        ]
    
    def __str__(self):
        return self.name


class ProductListing(models.Model):
    """Model representing a product listing from a specific store."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='listings')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='listings')
    store_product_id = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=500)
    url = models.URLField()
    image_url = models.URLField(blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'store']
        ordering = ['current_price']
        indexes = [
            models.Index(fields=['store', 'is_available']),
            models.Index(fields=['current_price']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.store.name}"


class PriceHistory(models.Model):
    """Model for storing historical price data."""
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['listing', 'recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.listing} - R{self.price} ({self.recorded_at})"


class SearchQuery(models.Model):
    """Model for tracking search queries."""
    query = models.CharField(max_length=500)
    results_count = models.PositiveIntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['searched_at']),
        ]
    
    def __str__(self):
        return f"{self.query} ({self.searched_at})"
