from rest_framework import serializers
from api.models.User import CustomUser, Profile, UserPreference


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'profile', 'gender', 'location')

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ('interested_in', 'relationship', 'location_max_distance', 'age_min', 'age_max')