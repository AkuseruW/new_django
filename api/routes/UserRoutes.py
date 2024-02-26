from django.urls import path
from api.views.UserView import RegisterView, LoginView, LogoutView, WhoamiView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('whoami/', WhoamiView.as_view(), name='whoami'),
]