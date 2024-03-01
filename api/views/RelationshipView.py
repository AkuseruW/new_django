from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError

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
        
    @staticmethod
    def handle_integrity_error():
        return Response({"detail": "You have already expressed interest in this relationship."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return self.handle_integrity_error()