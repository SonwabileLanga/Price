from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('compare/', views.compare_products, name='compare_products'),
]
