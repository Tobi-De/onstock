from django.db import models
from model_utils.models import TimeStampedModel


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    contact_info = models.TextField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.name
