from django.shortcuts import get_object_or_404, render
from django.utils import timezone

# Create your views here.

from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True).filter(published_at__lte=timezone.now()).order_by("-published_at", "-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug: str):
    post = get_object_or_404(
        Post.objects.filter(is_published=True).filter(published_at__lte=timezone.now()),
        slug=slug,
    )
    return render(request, "blog/post_detail.html", {"post": post})
