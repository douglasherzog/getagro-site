from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from blog.models import Post
from leads.models import Lead


@login_required
def dashboard(request):
    lead_count = Lead.objects.count()
    post_count = Post.objects.filter(is_published=True).count()
    return render(
        request,
        "accounts/dashboard.html",
        {"lead_count": lead_count, "post_count": post_count},
    )
