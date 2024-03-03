from django.urls import path
from api.views.UserView import FindMatchingUsersView, UserPreferencesView

urlpatterns = [
    path('find_matching_users/', FindMatchingUsersView.as_view(), name='find_matching_users'),
    path('user_preferences/', UserPreferencesView.as_view(), name='user_preferences'),
]