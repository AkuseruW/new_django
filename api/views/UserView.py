import os
import binascii

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from api import redis_connect

from api.serializers.UserSerializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from rest_framework import status

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        user = request.user
        if user:
            return Response("Already logged in", status=status.HTTP_200_OK)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data=serializer.validated_data)
            if user:
                return Response("User created", status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.user
        if user:
            return Response("Already logged in", status=status.HTTP_200_OK)
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            token = binascii.hexlify(os.urandom(20)).decode()
            redis_connect.set(token, str(user.id), 3600)
            response = Response({"token": token, "message": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie(
            "__session", token, max_age=2592000, httponly=True, secure=True, samesite="None"
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.headers["Authorization"].split(" ")[1]
        redis_connect.delete(token)
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("__session")
        return response


class WhoamiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user:
            user = UserProfileSerializer(user)
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)