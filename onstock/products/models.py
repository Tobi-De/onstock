from django.db import models
from django_lifecycle import AFTER_CREATE
from django_lifecycle import hook
from django_lifecycle import LifecycleModel
from model_utils.models import TimeStampedModel


class Product(TimeStampedModel, LifecycleModel):
    name = models.CharField(verbose_name="Nom", max_length=100, unique=True, db_index=True)
    description = models.TextField(verbose_name="Description", blank=True)
    sku = models.CharField(verbose_name="SKU", max_length=50, unique=True, db_index=True, blank=True, null=True)
    price = models.PositiveSmallIntegerField(verbose_name="Prix")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name

    @hook(AFTER_CREATE)
    def create_stock(self):
        Stock.objects.create(product=self, quantity=0, min_quantity=0)


class Stock(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Produit", related_name="stock")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    min_quantity = models.PositiveIntegerField(verbose_name="Quantité minimale", default=0)
    max_quantity = models.PositiveSmallIntegerField(verbose_name="Quantité maximale", null=True, blank=True)
    last_restocked = models.DateTimeField(verbose_name="Dernier réapprovisionnement", null=True, blank=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    @classmethod
    def restock(cls):
        pass
