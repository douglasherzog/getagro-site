from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("vender/", views.sell, name="sell"),
    path("comprar/", views.buy, name="buy"),
    path("contato/", views.contact, name="contact"),
]
