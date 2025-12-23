from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

# Create your views here.

from .forms import BuyerLeadForm, ContactForm, SellerLeadForm
from .models import Lead


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
