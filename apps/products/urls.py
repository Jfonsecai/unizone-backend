# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/products/', views.ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
]
