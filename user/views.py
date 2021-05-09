from django.conf import settings
from django.contrib import auth
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from . import docs
import requests
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, TokenSerializer


@swagger_auto_schema(**docs.register)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        name = data['name']
        email = data['email']
        phone = data['phone']
        password1 = data['password_1']
        password2 = data['password_2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                return Response({'msg': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(email=email, password=password1, name=name, phone=phone)
                user.save()
                return Response({'msg': 'User successfully registered.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Password does not match.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(**docs.login)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def login(request):
    try:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data['email']
        password = data['password']
        user = auth.authenticate(username=email, password=password)
        if user:
            user = User.objects.get(email=email)
            data = {
                "user": user,
                "token": user.token()
            }

            return Response({'success': True, 'msg': 'Verification success', 'data': TokenSerializer(data).data}, status=200)
        else:
            return Response({'msg': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


