from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile

from .forms import ListingForm
from .models import Listing


def _require_seller(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return None

    if profile.role not in (Profile.ROLE_SELLER, Profile.ROLE_BOTH):
        return None

    return profile


@login_required
def my_listings(request):
    profile = _require_seller(request)
    if profile is None:
        return HttpResponseForbidden("Acesso restrito.")

    listings = Listing.objects.filter(seller_profile=profile).order_by("-created_at")
    return render(request, "listings/my_listings.html", {"listings": listings})


@login_required
def listing_create(request):
    profile = _require_seller(request)
    if profile is None:
        return HttpResponseForbidden("Acesso restrito.")

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller_profile = profile
            listing.save()
            messages.success(request, "Publicação criada.")
            return redirect("listings:my_listings")
    else:
        form = ListingForm()

    return render(request, "listings/listing_form.html", {"form": form, "mode": "create"})


@login_required
def listing_edit(request, pk: int):
    profile = _require_seller(request)
    if profile is None:
        return HttpResponseForbidden("Acesso restrito.")

    listing = get_object_or_404(Listing, pk=pk, seller_profile=profile)

    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Publicação atualizada.")
            return redirect("listings:my_listings")
    else:
        form = ListingForm(instance=listing)

    return render(request, "listings/listing_form.html", {"form": form, "mode": "edit", "listing": listing})


@login_required
def listing_delete(request, pk: int):
    profile = _require_seller(request)
    if profile is None:
        return HttpResponseForbidden("Acesso restrito.")

    listing = get_object_or_404(Listing, pk=pk, seller_profile=profile)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Publicação removida.")
        return redirect("listings:my_listings")

    return render(request, "listings/listing_confirm_delete.html", {"listing": listing})


@login_required
def admin_listings(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Acesso restrito.")

    listings = Listing.objects.select_related("seller_profile", "seller_profile__user").order_by("-created_at")
    return render(request, "listings/admin_listings.html", {"listings": listings})
