from django.conf import settings
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "core/home.html", {"whatsapp_url": getattr(settings, "WHATSAPP_URL", "")})
