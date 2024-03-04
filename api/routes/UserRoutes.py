from django.urls import path
from api.views.UserView import FindMatchingUsersView, UserPreferencesView, like_user

urlpatterns = [
    path('find_matching_users/', FindMatchingUsersView.as_view(), name='find_matching_users'),
    path('user_preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('like/<uuid:user_id>/', like_user, name='like_user'),
]