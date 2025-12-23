from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, "CANONICAL_HOST", "get.agr.br")
        host = (request.get_host() or "").split(":")[0]

        if host == f"www.{canonical_host}":
            return HttpResponsePermanentRedirect(
                f"{request.scheme}://{canonical_host}{request.get_full_path()}"
            )

        return self.get_response(request)
