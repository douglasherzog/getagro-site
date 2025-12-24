from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseForbidden

# Create your views here.

from blog.models import Post
from leads.models import Lead

from .forms import SignupForm
from .models import Profile


@login_required
def dashboard(request):
    lead_count = Lead.objects.count()
    post_count = Post.objects.filter(is_published=True).count()
    return render(
        request,
        "accounts/dashboard.html",
        {"lead_count": lead_count, "post_count": post_count},
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("accounts:dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def negociantes(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Acesso restrito.")

    profiles = Profile.objects.select_related("user").order_by("full_name")
    return render(request, "accounts/negociantes.html", {"profiles": profiles})
