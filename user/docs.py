from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, LoginSerializer, TokenSerializer
from .models import User

register = {
    "operation_description": "Register",
    "method": "POST",
    "request_body": RegisterSerializer,
    "responses": {
        201 : 'User successfully registered.',
        400 : 'Email already in use.'
    }
}

login = {
    "operation_description": "User Login",
    "method": "POST",
    "request_body": LoginSerializer,
    "responses": {
        200 : TokenSerializer,
        401 : 'Invalid credentials.'
    }
}