from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JSON Web Tokens (JWT) with additional user data.

    This serializer extends the TokenObtainPairSerializer provided by the
    `django-rest-framework-simplejwt` library. It adds the user's email to the
    JWT payload, providing additional information along with the standard token.
    """

    @classmethod
    def get_token(cls, user):
        """
        Override the base method to include the user's email in the token payload.

        Args:
            - user: The user instance for whom the token is being generated.

        Returns:
            - Token: The JSON Web Token containing the standard payload and the
              additional 'email' field.
        """
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used to handle user registration by validating and processing
    the incoming data. It extends the base ModelSerializer provided by the
    `django-rest-framework` library and includes additional validation for the email,
    password, and password confirmation fields.
    """

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    profile = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'profile')

    def validate(self, attrs):
        """
        Custom validation method to ensure that the 'password' and 'password2' fields match.
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Custom method to create a new user instance with the validated data.
        """

        user = User.objects.create(
            email=validated_data['email'],
            profile=validated_data['profile'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

