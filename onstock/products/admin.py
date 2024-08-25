from django.contrib import admin

from .models import Product
from .models import Stock


class StockInline(admin.StackedInline):
    model = Stock
    extra = 1
    min_num = 0
    max_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "sku",
        "price",
        "stock__quantity",
        "created",
        "modified",
    )
    list_filter = ("created", "modified")
    search_fields = ("name",)
    # inlines = [StockInline]
