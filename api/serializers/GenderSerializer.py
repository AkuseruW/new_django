from rest_framework import serializers
from api.models import Gender

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


# class InterestedInGenderSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = InterestedInGender
#         fields = ('user', 'gender')
        


# class GetInterestedInGenderSerializer(serializers.ModelSerializer):
#     gender = serializers.SlugRelatedField(slug_field='name', read_only=True)

#     class Meta:
#         model = InterestedInGender
#         fields = ('gender',)

