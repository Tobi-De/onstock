from django.db import models
from model_utils.models import TimeStampedModel


class Sale(TimeStampedModel):
    total_amount = models.PositiveIntegerField(verbose_name="Montant total")

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ["-created"]


class Item(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Vente", related_name="items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="Produit", related_name="sales"
    )
    quantity_sold = models.PositiveIntegerField(verbose_name="Quantité vendue")
    unit_price = models.PositiveIntegerField(verbose_name="Prix unitaire")
    total_price = models.PositiveIntegerField(verbose_name="Prix total")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"{self.sale} - {self.product} - {self.quantity_sold} - {self.total_price}"
