from django.db import models
from django.db.models import Manager
from django_lifecycle import AFTER_CREATE
from django_lifecycle import AFTER_UPDATE
from django_lifecycle import BEFORE_CREATE
from django_lifecycle import hook
from django_lifecycle import LifecycleModel
from django_lifecycle.conditions import WhenFieldValueChangesTo
from django_lifecycle.conditions import WhenFieldValueIs
from django_lifecycle.conditions import WhenFieldValueWas
from model_utils.models import TimeStampedModel
from onstock.products.models import Stock


class Purchase(TimeStampedModel, LifecycleModel):
    items: Manager["Item"]

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        RECEIVED = "RECEIVED", "Reçu"
        CANCELED = "CANCELED", "Annulé"

    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.CASCADE,
        verbose_name="Fournisseur",
        related_name="purchases",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RECEIVED)
    total_cost = models.PositiveIntegerField(verbose_name="Coût total")
    order_date = models.DateField(verbose_name="Date de commande", blank=True, null=True)
    received_date = models.DateField(verbose_name="Date de réception", null=True, blank=True)

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
        ordering = ["-created"]

    @property
    def product_display(self):
        return ", ".join(self.items.values_list("product__name", flat=True))

    @hook(
        AFTER_UPDATE,
        condition=WhenFieldValueWas("status", Status.PENDING) & WhenFieldValueChangesTo("status", Status.RECEIVED),
    )
    def increase_stock(self):
        for item in self.items.all():
            stock = Stock.objects.select_for_update().get(product=item.product)
            stock.quantity = models.F("quantity") + item.quantity_received
            stock.save()


class Item(TimeStampedModel, LifecycleModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name="Achat", related_name="items")
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name="Produit",
        related_name="purchases",
    )
    quantity_ordered = models.PositiveIntegerField(verbose_name="Quantité commandée", blank=True)
    quantity_received = models.PositiveIntegerField(verbose_name="Quantité reçue")
    unit_price = models.PositiveIntegerField(verbose_name="Prix unitaire")
    total_cost = models.PositiveIntegerField(verbose_name="Coût total", blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"{self.purchase} - {self.quantity_received} - {self.total_cost}"

    @hook(BEFORE_CREATE)
    def calculate_total_cost(self):
        if not self.total_cost:
            self.total_cost = self.unit_price * self.quantity_received

    @hook(BEFORE_CREATE)
    def set_quantity_ordered(self):
        if not self.quantity_ordered:
            self.quantity_ordered = self.quantity_received

    @hook(AFTER_CREATE, condition=WhenFieldValueIs("purchase.status", Purchase.Status.RECEIVED))
    def increase_stock(self):
        stock = Stock.objects.select_for_update().get(product=self.product)
        stock.quantity = models.F("quantity") + self.quantity_received
        stock.save()
