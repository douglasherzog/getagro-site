from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, "CANONICAL_HOST", "")
        if canonical_host:
            current_host = request.get_host() or ""
            host_no_port = current_host.split(":", 1)[0]
            if host_no_port.lower() == f"www.{canonical_host}".lower():
                new_url = f"{request.scheme}://{canonical_host}{request.path}"
                if request.GET:
                    new_url += "?" + urlencode(request.GET, doseq=True)
                return HttpResponsePermanentRedirect(new_url)

        response = self.get_response(request)

        if not settings.DEBUG:
            x_robots_tag = response.headers.get("X-Robots-Tag")
            if x_robots_tag and "noindex" in x_robots_tag.lower():
                response.headers.pop("X-Robots-Tag", None)

        return response
