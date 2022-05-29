from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "code",
            "description",
            "uom",
            "providers",
            "uom",
            "real_quantity",
            "unit_price",
            "unit_cost",
            "alert_stock",
            "optimal_stock",
            "created_by",
            "modified_by",
        )
        export_order = (
            "id",
            "name",
            "category",
            "providers",
            "real_quantity",
            "uom",
            "unit_cost",
            "unit_price",
            "alert_stock",
            "optimal_stock",
            "code",
            "description",
            "created_by",
            "modified_by",
        )


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = (
        "name",
        "category",
        "providers",
        "real_quantity",
        "unit_cost",
        "uom",
        "created_at",
        "modified_at",
    )
    list_filter = ("category", "providers")
    search_fields = ("code", "name", "category", "providers")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "real_quantity",
                    "uom",
                    ("unit_cost", "unit_price"),
                )
            },
        ),
        ("Donnée de filtre", {"fields": ("category", "providers", "code")}),
        ("Suivie de stock", {"fields": ("alert_stock", "optimal_stock")}),
        ("Tracabilité", {"fields": ("created_by", "modified_by")}),
    )


admin.site.register(Product, ProductAdmin)
