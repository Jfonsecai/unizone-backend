from django.contrib import admin
from .models import User

#Lógica de admin en user
class UserAdmin(admin.ModelAdmin):
    list_display =  ('username', 'first_name', 'last_name', 'email', 'dni', 'phone_number', 'country', 'city', 'state', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'phone_number', 'country', 'city', 'state')
    list_filter = ('is_staff', 'is_active', 'country', 'date_joined')
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'dni', 'phone_number', 'country', 'street', 'city', 'state')
        }),
        ('Permisos', {
            'fields': ('is_staff', 'is_active')
        }),
    )

admin.site.register(User, UserAdmin)