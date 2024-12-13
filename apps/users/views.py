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
        user = User.objects.filter(email=email).first()
        if user:
            # Generar el token de restablecimiento
            token = default_token_generator.make_token(user)

            # Crear el enlace de restablecimiento
            reset_link = f"https://unizonevercel.vercel.app/password-reset/confirm/?token={token}&user={user.pk}"
            subject = 'Recuperación de contraseña'
            message = f'Por favor, sigue este enlace para restablecer tu contraseña: {reset_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            # Enviar el correo
            try:
                send_mail(
                    subject='Password Reset',
                    message=f'Click the following link to reset your password: {reset_link}',
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False
                )
                print("Correo de restablecimiento enviado")
                return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                return Response({"error": "Failed to send reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Si el usuario no existe
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



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
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({
            'access': token['access'],  # El token de acceso
            'refresh': token['refresh'],  # El token de refresco
            'username': token['username'],  # Nombre de usuario
            'role': token['role'],  # Rol del usuario
        })


