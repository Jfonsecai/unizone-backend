from django.urls import path
from .views import PasswordResetRequestView, RegisterAPIView, CustomTokenObtainPairView, PasswordResetConfirmView
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
     path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Vistas para el reestablecimiento de contraseña
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]