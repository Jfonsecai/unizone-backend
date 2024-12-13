from django.db import models

class Product(models.Model):
    name = models.TextField(max_length=200, verbose_name="nombre")
    description = models.TextField(max_length=300, verbose_name="descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    available = models.BooleanField(default=True, verbose_name="disponible")
    # photo = models.ImageField(
    #     upload_to="logos/", null=True, blank=True, verbose_name="foto"
    # )
    photo = models.URLField(max_length=500, null=True, blank=True, verbose_name="foto (URL)")


    def __str__(self):
        return f"Producto: {self.name} {self.price:.2f}" 
