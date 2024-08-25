from django.db import models
from django_lifecycle import AFTER_CREATE
from django_lifecycle import BEFORE_CREATE
from django_lifecycle import hook
from django_lifecycle import LifecycleModel
from model_utils.models import TimeStampedModel
from onstock.products.models import Stock


class Sale(TimeStampedModel):
    total_amount = models.PositiveIntegerField(verbose_name="Montant total")

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ["-created"]


class Item(TimeStampedModel, LifecycleModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Vente", related_name="items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="Produit", related_name="sales"
    )
    quantity_sold = models.PositiveIntegerField(verbose_name="Quantité vendue")
    unit_price = models.PositiveIntegerField(verbose_name="Prix unitaire", blank=True)
    total_price = models.PositiveIntegerField(verbose_name="Prix total", blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"{self.sale} - {self.product} - {self.quantity_sold} - {self.total_price}"

    @hook(BEFORE_CREATE)
    def calculate_total_price(self):
        if not self.unit_price:
            self.unit_price = self.product.price
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity_sold

    @hook(AFTER_CREATE)
    def decrease_stock(self):
        stock = Stock.objects.select_for_update().get(product=self.product)
        stock.quantity = models.F("quantity") - self.quantity_sold
        stock.save()
