from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "name",
        "contact_info",
        "address",
    )
    list_filter = ("created", "modified")
    search_fields = ("name",)
