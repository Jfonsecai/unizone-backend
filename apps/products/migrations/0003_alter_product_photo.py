# Generated by Django 5.1 on 2024-12-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='foto (URL)'),
        ),
    ]
