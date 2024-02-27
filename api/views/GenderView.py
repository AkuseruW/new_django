from rest_framework import viewsets

from api.models import Gender
from api.serializers.GenderSerializer import GenderSerializer

from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:

            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(GenderViewSet, self).get_permissions()