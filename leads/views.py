from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

from accounts.models import Profile
from listings.models import Listing

from .forms import BuyerLeadForm, ContactForm, ProcuraForm, SellerLeadForm
from .models import Lead, Procura


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            lead = form.save()

            if settings.CONTACT_TO_EMAIL:
                subject = f"[GetAgro] Novo contato: {lead.name}"
                body = (
                    f"Interesse: {lead.get_interest_display()}\n"
                    f"Nome: {lead.name}\n"
                    f"Email: {lead.email}\n"
                    f"Telefone: {lead.phone}\n\n"
                    f"Mensagem:\n{lead.message}\n"
                )
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_TO_EMAIL], fail_silently=False)

            messages.success(request, "Mensagem enviada com sucesso.")
            return redirect("leads:contact")
    else:
        form = ContactForm()

    return render(
        request,
        "leads/contact.html",
        {"form": form, "whatsapp_url": getattr(settings, "WHATSAPP_URL", "")},
    )


def sell(request):
    if request.method == "POST":
        form = SellerLeadForm(request.POST)
        if form.is_valid():
            lead = form.save()

            if settings.CONTACT_TO_EMAIL:
                subject = f"[GetAgro] Novo lead (Vender): {lead.name}"
                body = (
                    f"Interesse: {lead.get_interest_display()}\n"
                    f"Nome: {lead.name}\n"
                    f"Email: {lead.email}\n"
                    f"Telefone: {lead.phone}\n"
                    f"Cidade/UF: {lead.city_state}\n"
                    f"Cabeças: {lead.heads}\n"
                    f"Peso médio (kg): {lead.avg_weight_kg}\n"
                    f"Categoria: {lead.animal_category}\n"
                    f"Raça: {lead.breed}\n"
                    f"Prazo: {lead.timeframe}\n\n"
                    f"Detalhes:\n{lead.message}\n"
                )
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_TO_EMAIL], fail_silently=False)

            messages.success(request, "Recebemos seus dados. Vamos retornar o quanto antes.")
            return redirect("leads:sell")
    else:
        form = SellerLeadForm()

    return render(
        request,
        "leads/sell.html",
        {"form": form, "whatsapp_url": getattr(settings, "WHATSAPP_URL", "")},
    )


def buy(request):
    if request.method == "POST":
        form = BuyerLeadForm(request.POST)
        if form.is_valid():
            lead = form.save()

            if settings.CONTACT_TO_EMAIL:
                subject = f"[GetAgro] Novo lead (Comprar): {lead.name}"
                body = (
                    f"Interesse: {lead.get_interest_display()}\n"
                    f"Nome: {lead.name}\n"
                    f"Email: {lead.email}\n"
                    f"Telefone: {lead.phone}\n"
                    f"Cidade/UF: {lead.city_state}\n"
                    f"Volume desejado: {lead.desired_volume}\n"
                    f"Especificações:\n{lead.specs}\n\n"
                    f"Janela de compra: {lead.timeframe}\n\n"
                    f"Observações:\n{lead.message}\n"
                )
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_TO_EMAIL], fail_silently=False)

            messages.success(request, "Recebemos sua demanda. Vamos retornar o quanto antes.")
            return redirect("leads:buy")
    else:
        form = BuyerLeadForm()

    return render(
        request,
        "leads/buy.html",
        {"form": form, "whatsapp_url": getattr(settings, "WHATSAPP_URL", "")},
    )


def public_procuras(request):
    procuras = Procura.objects.filter(is_active=True).select_related("buyer_profile").order_by("-created_at")
    return render(request, "leads/public_procuras.html", {"procuras": procuras})


def public_procura_detail(request, pk: int):
    procura = get_object_or_404(Procura, pk=pk, is_active=True)
    return render(request, "leads/public_procura_detail.html", {"procura": procura})


@login_required
def procura_create(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if profile is None or profile.role not in (Profile.ROLE_BUYER, Profile.ROLE_BOTH):
        return redirect(f"/accounts/cadastro/?role=buyer&next=/procuras/nova/")

    if request.method == "POST":
        form = ProcuraForm(request.POST)
        if form.is_valid():
            procura = form.save(commit=False)
            procura.buyer_profile = profile
            procura.save()
            messages.success(request, "Procura publicada.")
            return redirect(f"/procuras/{procura.pk}/")
    else:
        form = ProcuraForm()

    return render(request, "leads/procura_form.html", {"form": form})


def _get_profile_safe(user):
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None


def _notify_admin_new_lead(lead: Lead):
    if not settings.CONTACT_TO_EMAIL:
        return

    if lead.source == Lead.Source.LISTING and lead.listing:
        subject = f"[GetAgro] Interesse em oferta: {lead.listing.title}"
        ref = f"Oferta #{lead.listing_id} - {lead.listing.title}"
    elif lead.source == Lead.Source.PROCURA and lead.procura:
        subject = f"[GetAgro] Interesse em procura: {lead.procura.title}"
        ref = f"Procura #{lead.procura_id} - {lead.procura.title}"
    else:
        subject = "[GetAgro] Novo lead"
        ref = "(sem referência)"

    body = (
        f"Referência: {ref}\n"
        f"Lead ID: {lead.pk}\n"
        f"Status: {lead.get_status_display()}\n"
        f"Nome: {lead.name}\n"
        f"Email: {lead.email}\n"
        f"Telefone: {lead.phone}\n\n"
        f"Mensagem:\n{lead.message}\n\n"
        f"Admin: /admin/leads/lead/{lead.pk}/change/\n"
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_TO_EMAIL], fail_silently=False)


@login_required
def interest_offer(request, pk: int):
    if request.method != "POST":
        return redirect(f"/ofertas/{pk}/")

    listing = get_object_or_404(Listing, pk=pk)
    profile = _get_profile_safe(request.user)

    msg = (request.POST.get("message") or "").strip()
    lead_message = msg or "(sem mensagem)"

    lead = Lead.objects.create(
        source=Lead.Source.LISTING,
        user=request.user,
        listing=listing,
        interest=Lead.Interest.BUYER,
        name=(profile.full_name if profile else request.user.get_username()),
        email=(profile.email if profile and profile.email else (request.user.email or "")),
        phone=(profile.phone if profile else ""),
        message=lead_message,
    )
    _notify_admin_new_lead(lead)
    messages.success(request, "Interesse enviado. Vamos retornar o quanto antes.")
    return redirect(f"/ofertas/{pk}/")


@login_required
def interest_procura(request, pk: int):
    if request.method != "POST":
        return redirect(f"/procuras/{pk}/")

    procura = get_object_or_404(Procura, pk=pk, is_active=True)
    profile = _get_profile_safe(request.user)

    msg = (request.POST.get("message") or "").strip()
    lead_message = msg or "(sem mensagem)"

    lead = Lead.objects.create(
        source=Lead.Source.PROCURA,
        user=request.user,
        procura=procura,
        interest=Lead.Interest.SELLER,
        name=(profile.full_name if profile else request.user.get_username()),
        email=(profile.email if profile and profile.email else (request.user.email or "")),
        phone=(profile.phone if profile else ""),
        message=lead_message,
    )
    _notify_admin_new_lead(lead)
    messages.success(request, "Interesse enviado. Vamos retornar o quanto antes.")
    return redirect(f"/procuras/{pk}/")
