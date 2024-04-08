from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

from .serializers import (
    MyTokenObtainPairSerializer, 
    RegisterSerializer,
    )
from auth_app.models import User


class MyObtainTokenPairView(TokenObtainPairView):
    """
    Custom API view for obtaining token pairs.

    This view extends the TokenObtainPairView provided by the Django Rest Framework's
    simplejwt library. It allows clients to obtain both access and refresh tokens
    by providing valid user credentials.
    """

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows users to register by providing the required information
    such as username, email, and password. Upon successful registration,
    a new user instance will be created and stored in the database.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]

