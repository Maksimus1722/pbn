from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if host.startswith('www.'):
            new_host = host[4:]
            return HttpResponsePermanentRedirect(
                f"{request.scheme}://{new_host}{request.path}"
            )
        return self.get_response(request)