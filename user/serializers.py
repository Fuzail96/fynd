from rest_framework import  serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=200)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, max_length=17, allow_blank=True, allow_null=True)
    password_1= serializers.CharField(required=True, max_length=200)
    password_2= serializers.CharField(required=True, max_length=200)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password= serializers.CharField(required=True, max_length=200)

class TokenSerializer(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField(required=True)
