from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse

from blog.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "leads:sell",
            "leads:buy",
            "leads:contact",
            "blog:post_list",
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return (
            Post.objects.filter(is_published=True)
            .filter(published_at__lte=timezone.now())
            .order_by("-published_at", "-created_at")
        )

    def lastmod(self, obj: Post):
        return obj.updated_at or obj.published_at or obj.created_at

    def location(self, obj: Post):
        return reverse("blog:post_detail", kwargs={"slug": obj.slug})


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogPostSitemap,
}
