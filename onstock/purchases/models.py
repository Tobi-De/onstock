from django.db import models
from model_utils.models import TimeStampedModel


class Purchase(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        RECEIVED = "RECEIVED", "Reçu"
        CANCELED = "CANCELED", "Annulé"

    supplier = models.ForeignKey(
        "suppliers.Supplier", on_delete=models.CASCADE, verbose_name="Fournisseur", related_name="purchases"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="Produit", related_name="purchases"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    total_cost = models.PositiveIntegerField(verbose_name="Coût total")
    order_date = models.DateField(verbose_name="Date de commande", blank=True, null=True)
    received_date = models.DateField(verbose_name="Date de réception", null=True, blank=True)

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
        ordering = ["-created"]


class Item(TimeStampedModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name="Achat", related_name="items")
    quantity_ordered = models.PositiveIntegerField(verbose_name="Quantité commandée")
    quantity_received = models.PositiveIntegerField(verbose_name="Quantité reçue")
    unit_price = models.PositiveIntegerField(verbose_name="Prix unitaire")
    total_cost = models.PositiveIntegerField(verbose_name="Coût total")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"{self.purchase} - {self.quantity_received} - {self.total_cost}"
