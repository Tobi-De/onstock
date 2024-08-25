# Generated by Django 5.1 on 2024-08-25 13:36

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=100, unique=True, verbose_name="Nom"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                (
                    "sku",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="SKU",
                    ),
                ),
                ("price", models.PositiveSmallIntegerField(verbose_name="Prix")),
            ],
            options={
                "verbose_name": "Produit",
                "verbose_name_plural": "Produits",
            },
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(verbose_name="Quantité")),
                (
                    "min_quantity",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Quantité minimale"
                    ),
                ),
                (
                    "max_quantity",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Quantité maximale"
                    ),
                ),
                (
                    "last_restocked",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Dernier réapprovisionnement",
                    ),
                ),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stock",
                        to="products.product",
                        verbose_name="Produit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
            },
        ),
    ]
