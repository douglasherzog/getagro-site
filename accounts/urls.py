from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.DocumentLoginView.as_view(), name="login"),
    path("cadastro/", views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("negociantes/", views.negociantes, name="negociantes"),
]
