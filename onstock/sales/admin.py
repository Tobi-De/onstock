from django.contrib import admin

from .models import Item
from .models import Sale


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    min_num = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "total_amount")
    list_filter = ("created", "modified")
    inlines = [ItemInline]
