from allauth.urls import urlpatterns as allauth_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_not_required  # type: ignore
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views import defaults as default_views
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from health_check.views import MainView
from onstock.core import views as core_views
from onstock.core.utils import decorate_urls

admin_header = "Administration de FATUM"
admin.site.enable_nav_sidebar = False
admin.site.site_header = admin_header
admin.site.site_title = admin_header

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("", RedirectView.as_view(url=reverse_lazy("admin:index")), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(".well-known/security.txt", core_views.security_txt),
    path("robots.txt", core_views.robots_txt),
    path("android-chrome-192x192.png", core_views.favicon),
    path("android-chrome-512x512.png", core_views.favicon),
    path("apple-touch-icon.png", core_views.favicon),
    path("browserconfig.xml", core_views.favicon),
    path("favicon-16x16.png", core_views.favicon),
    path("favicon-32x32.png", core_views.favicon),
    path("favicon.ico", core_views.favicon),
    path("mstile-150x150.png", core_views.favicon),
    path("safari-pinned-tab.svg", core_views.favicon),
    path("health/", MainView.as_view()),
    path("accounts/", include(decorate_urls(allauth_patterns, [login_not_required]))),
    path(settings.ADMIN_URL, admin.site.urls),
    path("products/", include("onstock.products.urls", namespace="products")),
    path("purchases/", include("onstock.purchases.urls", namespace="purchases")),
    path("sales/", include("onstock.sales.urls", namespace="sales")),
    path("suppliers/", include("onstock.suppliers.urls", namespace="suppliers")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
