from django.urls import path

from api.views.AuthView import LoginView, LogoutView, RegisterView, WhoamiView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="register"),
    path("signin/", LoginView.as_view(), name="login"),
    path("signout/", LogoutView.as_view(), name="logout"),
    path("whoami/", WhoamiView.as_view(), name="whoami"),
]
