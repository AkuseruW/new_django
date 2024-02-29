import os
import binascii

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from api import redis_connect
from drf_spectacular.utils import extend_schema

from api.serializers.AuthSerializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from rest_framework import status


@extend_schema(tags=["Authentication"], request=UserRegisterSerializer)
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            return Response("Already logged in", status=status.HTTP_200_OK)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data=serializer.validated_data)
            if user:
                return Response("User created", status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Authentication"], request=UserLoginSerializer, responses={200: UserProfileSerializer})
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
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

@extend_schema(tags=["Authentication"], methods=["POST"])
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        token = request.headers["Authorization"].split(" ")[1]
        redis_connect.delete(token)
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("__session")
        return response

@extend_schema(tags=["Authentication"], methods=["GET"], responses={200: UserProfileSerializer})
class WhoamiView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        user = request.user
        if user:
            user = UserProfileSerializer(user)
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)