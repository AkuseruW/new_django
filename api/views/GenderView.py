from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema

from api.models import Gender, InterestedInGender
from api.serializers.GenderSerializer import (
    GenderSerializer, InterestedInGenderSerializer, GetInterestedInGenderSerializer
)

@extend_schema(tags=["Gender"])
class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

@extend_schema(tags=["Interested In Gender"])
class InterestedInGenderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InterestedInGender.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetInterestedInGenderSerializer
        return InterestedInGenderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @staticmethod
    def handle_integrity_error():
        return Response({"detail": "You have already expressed interest in this gender."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return self.handle_integrity_error()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
            return Response(serializer.data)
        except IntegrityError:
            return self.handle_integrity_error()