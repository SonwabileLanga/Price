from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.api_search, name='api_search'),
]
