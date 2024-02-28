from django.urls import path
from api.views.GenderView import GenderViewSet, InterestedInGenderViewSet

urlpatterns = [
    path('gender/', GenderViewSet.as_view({'get': 'list', 'post': 'create'}), name='gender_list'),
    path('gender/<int:pk>/', GenderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='gender_detail'),
    path('gender/interest/', InterestedInGenderViewSet.as_view({'get': 'list','post': 'create'}), name='gender_interest'),
    path('gender/interest/<int:pk>/', InterestedInGenderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='gender_interest_detail'),
]