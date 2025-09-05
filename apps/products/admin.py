from django.contrib import admin
from .models import Store, Product, ProductListing, PriceHistory, SearchQuery


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'base_url']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model', 'category', 'created_at']
    list_filter = ['brand', 'category', 'created_at']
    search_fields = ['name', 'normalized_name', 'brand', 'model']
    readonly_fields = ['normalized_name']


@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'current_price', 'is_available', 'last_updated']
    list_filter = ['store', 'is_available', 'last_updated']
    search_fields = ['product__name', 'title', 'store__name']
    readonly_fields = ['last_updated', 'created_at']


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['listing', 'price', 'is_available', 'recorded_at']
    list_filter = ['is_available', 'recorded_at']
    search_fields = ['listing__product__name', 'listing__store__name']
    readonly_fields = ['recorded_at']


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'results_count', 'searched_at', 'user_ip']
    list_filter = ['searched_at']
    search_fields = ['query']
    readonly_fields = ['searched_at']
