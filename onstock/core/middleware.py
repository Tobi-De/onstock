from django.shortcuts import redirect

from onstock.core.types import HttpRequest


class NextURLMiddleware:

    def __init__(self, get_response: callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        if next_url := request.GET.get("next-url"):
            return redirect(next_url)
        return response
