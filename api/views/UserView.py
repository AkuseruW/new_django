from rest_framework.views import APIView

from rest_framework.response import Response
from api.models.Gender import InterestedInGender
from api.models.Relationship import InterestedInRelation
from rest_framework import permissions
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from api.models.User import CustomUser
from api.serializers.UserSerialize import UserSerializer

class FindMatchingUsersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(tags=["Find Matching Users"], methods=["GET"], responses={200: UserSerializer})
    def get(self, request):
        current_user = request.user
        
        current_user_interested_in_genders = InterestedInGender.objects.filter(user=current_user).values_list('gender', flat=True)
        current_user_interested_in_relations = InterestedInRelation.objects.filter(user=current_user).values_list('relationship', flat=True)
        
        matching_users = CustomUser.objects.filter(
            Q(id__in=InterestedInGender.objects.filter(gender__in=current_user_interested_in_genders).values_list('user', flat=True)) &
            Q(id__in=InterestedInRelation.objects.filter(relationship__in=current_user_interested_in_relations).values_list('user', flat=True))
        ).exclude(id=current_user.id).order_by("?").first()
        
        if matching_users:
            serializer = UserSerializer(matching_users)
            return Response(serializer.data)
        else:
            return Response({"message": "No matching user found."}, status=404)