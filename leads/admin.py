from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

# Register your models here.

from .models import Lead, MessageTemplate, Procura


def _profile_contact_lines(profile):
    if profile is None:
        return []
    lines = []
    if profile.full_name:
        lines.append(f"Nome: {profile.full_name}")
    if profile.email:
        lines.append(f"E-mail: {profile.email}")
    if profile.phone:
        lines.append(f"Telefone/WhatsApp: {profile.phone}")
    if profile.city and profile.state:
        lines.append(f"Cidade/UF: {profile.city}/{profile.state}")
    return lines


def _release_contact_for_lead(request, lead: Lead, mode: str):
    if not settings.DEFAULT_FROM_EMAIL:
        raise ValueError("DEFAULT_FROM_EMAIL não configurado")

    if lead.source == Lead.Source.LISTING and lead.listing:
        seller_profile = lead.listing.seller_profile
        buyer_profile = None
        try:
            buyer_profile = lead.user.profile if lead.user else None
        except Exception:
            buyer_profile = None
        ref = f"Oferta: {lead.listing.title} (#{lead.listing_id})"
    elif lead.source == Lead.Source.PROCURA and lead.procura:
        buyer_profile = lead.procura.buyer_profile
        seller_profile = None
        try:
            seller_profile = lead.user.profile if lead.user else None
        except Exception:
            seller_profile = None
        ref = f"Procura: {lead.procura.title} (#{lead.procura_id})"
    else:
        buyer_profile = None
        seller_profile = None
        ref = "Referência não encontrada"

    seller_lines = _profile_contact_lines(seller_profile)
    buyer_lines = _profile_contact_lines(buyer_profile)

    if not seller_profile or not buyer_profile:
        raise ValueError("Não foi possível identificar comprador e vendedor para liberar contato")

    buyer_email_to = buyer_profile.email or ""
    seller_email_to = seller_profile.email or ""
    if not buyer_email_to or not seller_email_to:
        raise ValueError("E-mail do comprador ou vendedor ausente no perfil")

    subject = f"[GetAgro] Contato liberado - {ref}"

    if mode == Lead.ContactRelease.BOTH:
        body_to_buyer = "\n".join([ref, "", "Contato do vendedor:"] + seller_lines)
        body_to_seller = "\n".join([ref, "", "Contato do comprador:"] + buyer_lines)
    elif mode == Lead.ContactRelease.SELLER_ONLY:
        body_to_buyer = "\n".join([ref, "", "Contato do vendedor:"] + seller_lines)
        body_to_seller = "\n".join([ref, "", "Contato liberado apenas do vendedor.", "Aguarde o comprador entrar em contato."])
    elif mode == Lead.ContactRelease.BUYER_ONLY:
        body_to_buyer = "\n".join([ref, "", "Contato liberado apenas do comprador.", "Aguarde o vendedor entrar em contato."])
        body_to_seller = "\n".join([ref, "", "Contato do comprador:"] + buyer_lines)
    else:
        raise ValueError("Modo inválido")

    send_mail(subject, body_to_buyer, settings.DEFAULT_FROM_EMAIL, [buyer_email_to], fail_silently=False)
    send_mail(subject, body_to_seller, settings.DEFAULT_FROM_EMAIL, [seller_email_to], fail_silently=False)

    lead.contact_release = mode
    lead.contact_released_at = timezone.now()
    lead.status = Lead.Status.CONTACT_RELEASED
    lead.save(update_fields=["contact_release", "contact_released_at", "status"])


@admin.action(description="Liberar contato: A) ambos")
def release_contact_both(modeladmin, request, queryset):
    ok = 0
    for lead in queryset:
        try:
            _release_contact_for_lead(request, lead, Lead.ContactRelease.BOTH)
            ok += 1
        except Exception as e:
            messages.error(request, f"Lead {lead.pk}: {e}")
    if ok:
        messages.success(request, f"Contatos liberados (ambos) para {ok} lead(s).")


@admin.action(description="Liberar contato: B) só do vendedor")
def release_contact_seller_only(modeladmin, request, queryset):
    ok = 0
    for lead in queryset:
        try:
            _release_contact_for_lead(request, lead, Lead.ContactRelease.SELLER_ONLY)
            ok += 1
        except Exception as e:
            messages.error(request, f"Lead {lead.pk}: {e}")
    if ok:
        messages.success(request, f"Contatos liberados (só vendedor) para {ok} lead(s).")


@admin.action(description="Liberar contato: C) só do comprador")
def release_contact_buyer_only(modeladmin, request, queryset):
    ok = 0
    for lead in queryset:
        try:
            _release_contact_for_lead(request, lead, Lead.ContactRelease.BUYER_ONLY)
            ok += 1
        except Exception as e:
            messages.error(request, f"Lead {lead.pk}: {e}")
    if ok:
        messages.success(request, f"Contatos liberados (só comprador) para {ok} lead(s).")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "source", "status", "interest", "listing", "procura", "name", "email", "phone")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("source", "status", "interest", "created_at")
    actions = [release_contact_both, release_contact_seller_only, release_contact_buyer_only]


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("channel", "title", "is_active", "updated_at")
    list_filter = ("channel", "is_active", "updated_at")
    search_fields = ("title", "subject", "body")


@admin.register(Procura)
class ProcuraAdmin(admin.ModelAdmin):
    list_display = ("created_at", "title", "buyer_profile", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "specs", "buyer_profile__full_name", "buyer_profile__document")
