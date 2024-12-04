from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'first_name', 'last_name', 'dni', 'phone_number']

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             dni=validated_data['dni'],
#             phone_number=validated_data['phone_number']
#         )
#         user.set_password(validated_data['password'])  # Encripta la contraseña
#         user.save()
#         return user


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'phone_number', 'password', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            dni=validated_data['dni'],
            phone_number=validated_data['phone_number'],
            role=validated_data.get('role', User.BUYER)  # Si no se pasa el rol, por defecto será 'buyer'
        )
        user.set_password(validated_data['password'])  # Guarda la contraseña de forma segura
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id # Opcional: agregar información adicional al token
        token['role'] = user.role # Se pasa el rol del usuario para que el front sepa dónde redireccionarlo
        return token