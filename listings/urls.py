from django.urls import path

from . import views

app_name = "listings"

urlpatterns = [
    path("", views.my_listings, name="my_listings"),
    path("novo/", views.listing_create, name="listing_create"),
    path("<int:pk>/editar/", views.listing_edit, name="listing_edit"),
    path("<int:pk>/excluir/", views.listing_delete, name="listing_delete"),
    path("admin/", views.admin_listings, name="admin_listings"),
]
