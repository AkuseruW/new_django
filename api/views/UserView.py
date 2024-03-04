from django.contrib.gis.measure import D
from django.db.models import Q
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes

from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.handlers.swipe_filter import filter_profiles as filter_profiles_func
from api.models.User import CustomUser, UserPreference
from api.models.Match import Match
from api.serializers.UserSerialize import UserSerializer, UserPreferencesSerializer


class FindMatchingUsersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(tags=["Find Matching Users"], methods=["GET"], responses={200: UserSerializer})
    def get(self, request):
        current_user = request.user
        profiles = CustomUser.objects.exclude(id=current_user.id)
        user_preferences = UserPreference.objects.get(user=current_user)

        user_by_distance = profiles.filter(
            location__distance_lt=(
                current_user.location, D(km=user_preferences.location_max_distance)
            )
        )

        if not user_by_distance:
            return Response({"message": "No matching user found."}, status=status.HTTP_200_OK)

        filtered = filter_profiles_func(current_user, user_preferences, user_by_distance)

        return Response(UserSerializer(filtered, many=True).data, status=status.HTTP_200_OK)
    

class UserPreferencesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(tags=["User Preferences"], methods=["GET"], responses={200: UserPreferencesSerializer})
    def get(self, request):
        user = request.user
        user_preference, created = UserPreference.objects.get_or_create(user=user)
        serializer = UserPreferencesSerializer( user_preference )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(tags=["User Preferences"], methods=["PATCH"], request=UserPreferencesSerializer, responses={200: UserPreferencesSerializer})
    def patch(self, request):
        user = request.user
        user_preference, created = UserPreference.objects.get_or_create(user=user)
        serializer = UserPreferencesSerializer( user_preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
