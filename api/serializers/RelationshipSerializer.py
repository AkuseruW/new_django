from rest_framework import serializers
from api.models import Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


# class InterestedInRelationSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     class Meta:
#         model = InterestedInRelation
#         fields = ('relationship', 'user')

# class GetInterestedInRelationSerializer(serializers.ModelSerializer):
#     relationship = serializers.SlugRelatedField(slug_field='name', read_only=True)
#     class Meta:
#         model = InterestedInRelation
#         fields = ('relationship',)