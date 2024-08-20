from django.http import HttpRequest as HttpRequestBase
from django_htmx.middleware import HtmxDetails
from stockon.users.models import User


class HttpRequest(HttpRequestBase):
    htmx: HtmxDetails


class AuthenticatedHttpRequest(HttpRequest):
    user: User
