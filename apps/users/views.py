from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import User
from rest_framework.exceptions import NotFound, ValidationError
from django.conf import settings


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica para restablecer la contraseña, enviar correo, etc.
        # Ejemplo simple de enviar correo:
        user = User.objects.filter(email=email).first()
        if user:
            # Generar el token de restablecimiento
            token = default_token_generator.make_token(user)

            # Crear el enlace de restablecimiento
            reset_link = f"http://127.0.0.1:8000/api/password-reset/confirm/?token={token}&user={user.pk}"

            # Enviar el enlace de restablecimiento por correo electrónico
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,  # Asegúrate de configurar el correo en settings.py
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        user_id = request.data.get('username')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not user_id or not token or not new_password:
            return Response({'error': 'username, token, and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound('User not found.')

        # Verificamos si el token es válido
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password successfully reset.'}, status=status.HTTP_200_OK)
        else:
            raise ValidationError('Invalid or expired token.')

