from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# Vista para listar y crear productos
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Vista para obtener, actualizar y eliminar un producto específico
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
