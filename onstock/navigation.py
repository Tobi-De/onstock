from django.urls import reverse
from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavItem


class MainNav(Nav):
    template_name = "navigation.html"
    items = [
        NavItem(
            title="Accueil",
            url="home",
            extra_context={"icon": "home"},
        ),
        NavItem(
            title="Produits",
            url=reverse("products:index"),
            extra_context={"icon": "store"},
        ),
        NavItem(
            title="Ventes",
            url=reverse("sales:index"),
            extra_context={"icon": "shopping_cart"},
        ),
        NavItem(
            title="Achats",
            url=reverse("purchases:index"),
            extra_context={"icon": "shopping_cart"},
        ),
        NavItem(
            title="Fournisseurs",
            url=reverse("suppliers:index"),
            extra_context={"icon": "store"},
        ),
    ]
