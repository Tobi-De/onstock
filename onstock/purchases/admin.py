from django.contrib import admin

from .models import Item
from .models import Purchase


class ItemInline(admin.TabularInline):
    model = Item
    min_num = 1
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "status",
        "total_cost",
        "order_date",
        "received_date",
        "created",
        "modified",
    )
    list_filter = (
        "created",
        "modified",
        "supplier",
        "order_date",
        "received_date",
    )
    inlines = [ItemInline]
