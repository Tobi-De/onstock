from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from onstock.products.models import Product
from onstock.products.models import Stock
from onstock.purchases.models import Item as PurchaseItem
from onstock.purchases.models import Purchase
from onstock.sales.models import Item as SaleItem
from onstock.sales.models import Sale
from onstock.suppliers.models import Supplier


class Command(BaseCommand):
    help = "Create shop owner and shop employee groups with specific permissions."

    def handle(self, *_, **__):
        # Define models and their permissions
        models_permissions = {
            Product: ["add", "change", "delete", "view"],
            Stock: ["add", "change", "delete", "view"],
            Sale: ["add", "change", "delete", "view"],
            SaleItem: ["add", "change", "delete", "view"],
            Purchase: ["add", "change", "delete", "view"],
            PurchaseItem: ["add", "change", "delete", "view"],
            Supplier: ["add", "change", "delete", "view"],
        }

        # Create shop owner group
        shop_owner_group, created = Group.objects.get_or_create(name="shop_owner")
        if created:
            self.stdout.write(self.style.SUCCESS("Created group shop_owner"))
        else:
            self.stdout.write(self.style.WARNING("Group shop_owner already exists"))

        # Assign all permissions to shop owner
        for model, actions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                perm = Permission.objects.get(codename=f"{action}_{content_type.model}", content_type=content_type)
                shop_owner_group.permissions.add(perm)

        # Create shop employee group
        shop_employee_group, created = Group.objects.get_or_create(name="shop_employee")
        if created:
            self.stdout.write(self.style.SUCCESS("Created group shop_employee"))
        else:
            self.stdout.write(self.style.WARNING("Group shop_employee already exists"))

        # Assign specific permissions to shop employee
        employee_permissions = {
            Product: ["view"],
            Stock: ["view"],
            Sale: ["add", "view"],
            SaleItem: ["add", "view"],
        }

        for model, actions in employee_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                perm = Permission.objects.get(codename=f"{action}_{content_type.model}", content_type=content_type)
                shop_employee_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS("Successfully assigned permissions to groups"))
