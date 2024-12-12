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
        fields = [
            'username', 'first_name', 'last_name', 'dni', 'phone_number', 'email',
            'password', 'role', 'street', 'city', 'state', 'country'
        ]
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dni=validated_data['dni'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            street=validated_data.get('street'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            country=validated_data.get('country'),
            role=validated_data.get('role', User.BUYER) # Si no se pasa el rol, por defecto será 'buyer'
        )
        user.set_password(validated_data['password'])  # Guarda la contraseña de forma segura
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role # Se pasa el rol del usuario para que el front sepa dónde redireccionarlo
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        # Incluye los campos personalizados en la respuesta del serializer
        data['username'] = self.user.username
        data['role'] = self.user.role  # Ajusta según tu modelo
        return data
