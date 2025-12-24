from django.urls import path

from . import views

app_name = "interesses"

urlpatterns = [
    path("oferta/<int:pk>/", views.interest_offer, name="offer"),
    path("procura/<int:pk>/", views.interest_procura, name="procura"),
]
