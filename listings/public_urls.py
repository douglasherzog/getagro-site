from django.urls import path

from . import views

app_name = "public_listings"

urlpatterns = [
    path("", views.public_offers, name="offers"),
    path("<int:pk>/", views.public_offer_detail, name="offer_detail"),
]
