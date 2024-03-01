from django.urls import path
from api.views.UserView import FindMatchingUsersView

urlpatterns = [
    path('find_matching_users/', FindMatchingUsersView.as_view(), name='find_matching_users'),
]