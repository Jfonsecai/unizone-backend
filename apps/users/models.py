from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, User
from django_countries.fields import CountryField

# Create your models here.
        
class User(AbstractUser):
    ADMIN = 'admin'
    BUYER = 'buyer'
    ROLE_CHOICES = (
        (ADMIN, 'Administrador'),
        (BUYER, 'Comprador'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)

    phone_number = models.PositiveBigIntegerField(
        unique=False,blank=False,null=False,
        validators=[
            RegexValidator(
                regex=r'^(3|6)\d{9}$',
                message=('No es un número de teléfono válido'),
                code='invalid_phonenumber'
            )
        ],
        verbose_name='Número teléfono'
    )
    dni = models.PositiveBigIntegerField(
        unique=True, blank=False, null=False,
        validators=[
            RegexValidator(
                regex=r'^\d{7,10}$',
                message=('No es un número de documento válido'),
                code='invalid_dni'
            )
        ],
        verbose_name='Cédula ciudadania')
    street = models.CharField(max_length=255, verbose_name="Calle", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Ciudad", blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name="Departamento", blank=True, null=True)
    country = CountryField(verbose_name="País", blank=True, null=True)
    username = models.CharField(
        max_length=150, unique=True, primary_key=True, verbose_name='Nombre de usuario'
    ) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name','email','dni','phone_number']

    class Meta:
        db_table = 'USER'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.email = self.email.lower()
        super(User, self).save()
