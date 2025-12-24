from django.urls import path

from . import views

app_name = "procuras"

urlpatterns = [
    path("", views.public_procuras, name="list"),
    path("nova/", views.procura_create, name="create"),
    path("<int:pk>/", views.public_procura_detail, name="detail"),
]
