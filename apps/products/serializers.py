from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'available', 'photo']

    def validate_name(self, value):
        if ";" in value or "--" in value or "'" in value:
            raise serializers.ValidationError("Input contains invalid characters.")
        return value