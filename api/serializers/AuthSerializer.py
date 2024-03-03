from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError

from api.models import Gender, UserPreference

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password", "gender")

    def validate(self, data):
        if UserModel.objects.filter(email=data["email"]).exists():
            raise ValidationError("User with this email already exists")
        if not data["password"] or len(data["password"]) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not data["gender"]:
            raise ValidationError("Gender is required")
        return data
    
    def create(self, data):
        user = UserModel.objects.create_user(**data)
        UserPreference.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise ValidationError("Invalid credentials")
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "email", "gender")