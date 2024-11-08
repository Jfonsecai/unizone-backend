# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import path
# from .views import RegisterView

# urlpatterns = [
#     path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
#     path("logout/", LogoutView.as_view(), name="logout"),
#     path("registro/", RegisterView.as_view(), name="register"),
# ]

from django.urls import path
from .views import RegisterAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
]