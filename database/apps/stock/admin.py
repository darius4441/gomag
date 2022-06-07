from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import ParentUOM, Product, ProductCategory, Uom


class ProductCategoryResource(resources.ModelResource):
    class Meta:
        model = ProductCategory
        fields = (
            "id",
            "name",
            "parent",
        )
        export_order = (
            "id",
            "name",
            "parent",
        )


class ProductCategoryAdmin(ImportExportActionModelAdmin):
    resource_class = ProductCategoryResource


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
            "unit",
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
            "unit",
            "unit_cost",
            "unit_price",
            "alert_stock",
            "optimal_stock",
            "code",
            "description",
            "created_by",
            "modified_by",
        )


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = (
        "name",
        "category",
        "providers",
        "real_quantity",
        "unit_cost",
        "uom",
        "unit",
        "created_at",
        "modified_at",
    )
    list_filter = ("category", "providers", "uom")
    search_fields = ("code", "name", "providers")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "real_quantity",
                    "uom",
                    "unit",
                    ("unit_cost", "unit_price"),
                    ("semi_wholesale_price", "wholesale_price"),
                )
            },
        ),
        (
            "Donnée de filtre",
            {"fields": ("category", "providers", "code")},
        ),
        ("Suivie de stock", {"fields": ("alert_stock", "optimal_stock")}),
        ("Tracabilité", {"fields": ("created_by", "modified_by")}),
    )


class CategoryUomRessource(resources.ModelResource):
    class Meta:
        model = ParentUOM
        fields = (
            "id",
            "name",
        )


class UomInline(admin.TabularInline):
    model = Uom
    extra = 0
    fields = ["name", "ratio", "rouding", "type", "uom_parent"]


class CategoryUomAdmin(ImportExportActionModelAdmin):
    resource_class = CategoryUomRessource
    fields = ("name",)
    inlines = [UomInline]
    list_display = ("name",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ParentUOM, CategoryUomAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
