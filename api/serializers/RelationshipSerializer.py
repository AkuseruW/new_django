from rest_framework import serializers
from api.models import Relationship, InterestedInRelation


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


class InterestedInRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedInRelation
        fields = ('relationship', 'user')