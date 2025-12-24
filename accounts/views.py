from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView

# Create your views here.

from blog.models import Post
from leads.models import Lead

from .forms import DocumentAuthenticationForm, SignupForm
from .models import Profile


@login_required
def dashboard(request):
    lead_count = Lead.objects.count()
    post_count = Post.objects.filter(is_published=True).count()

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    return render(
        request,
        "accounts/dashboard.html",
        {"lead_count": lead_count, "post_count": post_count, "profile": profile},
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    role = request.GET.get("role") or request.POST.get("role")
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso.")
            if next_url:
                return redirect(next_url)
            return redirect("accounts:dashboard")
    else:
        initial = {}
        if role in (Profile.ROLE_BUYER, Profile.ROLE_SELLER):
            initial["role"] = role
        form = SignupForm(initial=initial)

    return render(request, "accounts/signup.html", {"form": form, "next": next_url, "role": role})


@login_required
def negociantes(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Acesso restrito.")

    profiles = Profile.objects.select_related("user").order_by("full_name")
    return render(request, "accounts/negociantes.html", {"profiles": profiles})


class DocumentLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = DocumentAuthenticationForm

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url

        role = self.request.POST.get("role") or self.request.GET.get("role")
        if role == Profile.ROLE_SELLER:
            return "/accounts/publicacoes/"
        if role == Profile.ROLE_BUYER:
            return reverse("accounts:dashboard")

        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            profile = None

        if profile and profile.role in (Profile.ROLE_SELLER, Profile.ROLE_BOTH):
            return "/accounts/publicacoes/"

        return reverse("accounts:dashboard")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["role"] = self.request.GET.get("role", "")
        ctx["next"] = self.request.GET.get("next", "")
        return ctx


class BuyGateView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse("accounts:dashboard")
        login_url = reverse("accounts:login")
        return f"{login_url}?role={Profile.ROLE_BUYER}"


class SellGateView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse("accounts:dashboard")
        login_url = reverse("accounts:login")
        return f"{login_url}?role={Profile.ROLE_SELLER}&next=/accounts/publicacoes/"
