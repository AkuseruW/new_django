from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema

from api.models import Relationship, InterestedInRelation
from api.serializers.RelationshipSerializer import (RelationshipSerializer, InterestedInRelationSerializer, GetInterestedInRelationSerializer)

@extend_schema(tags=["Relationship"])
class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

@extend_schema(tags=["Interested In Relation"])
class InterestedInRelationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InterestedInRelation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetInterestedInRelationSerializer
        return InterestedInRelationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)