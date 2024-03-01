import os
import binascii

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from api import redis_connect
from drf_spectacular.utils import extend_schema

from api.serializers.AuthSerializer import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from rest_framework import status


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @extend_schema(tags=["Authentication"], request=UserRegisterSerializer, responses={201: UserProfileSerializer}, methods=["POST"])
    def post(request):
        if request.user.is_authenticated:
            return Response("Already logged in", status=status.HTTP_200_OK)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data=serializer.validated_data)
            if user:
                return Response("User created", status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @extend_schema(tags=["Authentication"], request=UserLoginSerializer, responses={200: UserProfileSerializer}, methods=["POST"])
    def post(request):
        if request.user.is_authenticated:
            return Response("Already logged in", status=status.HTTP_200_OK)
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            token = binascii.hexlify(os.urandom(20)).decode()
            redis_connect.set(token, str(user.id), 2592000)
            response = Response({"token": token, "message": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie(
            "__session", token, max_age=2592000, httponly=True, secure=True, samesite="None"
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(tags=["Authentication"], methods=["POST"], request=None, responses={200: {"message": "Logout successful"}})
    def post(request):
        token = request.headers["Authorization"].split(" ")[1]
        redis_connect.delete(token)
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("__session")
        return response

class WhoamiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(tags=["Authentication"], methods=["GET"], responses={200: UserProfileSerializer})
    def get(request):
        user = request.user
        if user:
            user = UserProfileSerializer(user)
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)