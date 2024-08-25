from django import forms

from .models import Purchase
from onstock.suppliers.models import Supplier
from onstock.products.models import Product
from .models import Item


class PurchaseForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects, initial=Supplier.objects.first, label="Fournisseur"
    )
    class Meta:
        model = Purchase
        fields = (
            "id",
            "supplier",
            "status",
            "total_cost",
            "order_date",
            "received_date",
        )
        widgets = {
            "order_date": forms.DateInput(attrs={"type": "date"}),
            "received_date": forms.DateInput(attrs={"type": "date"}),
        }


class ItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects, initial=Product.objects.first, label="Article"
    )
    class Meta:
        model =  Item
        fields = ("product", "quantity_ordered", "quantity_received", "unit_price", "total_cost")
