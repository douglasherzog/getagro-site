"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.templatetags.static import static
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from .sitemaps import sitemaps

from accounts.views import BuyGateView, SellGateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url=static("core/logo.jpg"), permanent=True)),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
    ),
    path("comprar/", BuyGateView.as_view(), name="buy_gate"),
    path("vender/", SellGateView.as_view(), name="sell_gate"),
    path("accounts/publicacoes/", include(("listings.urls", "listings"), namespace="listings")),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('', include('leads.urls')),
]
