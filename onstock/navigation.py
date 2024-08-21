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
            url="products",
            extra_context={"icon": "store"},
        ),
        NavItem(
            title="Ventes",
            url="sales",
            extra_context={"icon": "shopping_cart"},
        ),
        NavItem(title="Achats", url="purchases", extra_context={"icon": "shopping_cart"}),
        NavItem(title="Fournisseurs", url="suppliers", extra_context={"icon": "store"}),
    ]
