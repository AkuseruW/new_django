from django.urls import path
from api.views.GenderView import GenderViewSet

urlpatterns = [
    path('gender/', GenderViewSet.as_view({'get': 'list', 'post': 'create'}), name='gender_list'),
    path('gender/<int:pk>/', GenderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='gender_detail'),
]