# urls.py
from django.urls import path
from . import views
from .views import SimulatePurchaseView

urlpatterns = [
    path('api/products/', views.ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
    path('api/simulate-purchase/', SimulatePurchaseView.as_view(), name='simular-compra'),
]
