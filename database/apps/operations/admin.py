from django.contrib import admin

from .models import Item, Operation


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = [
        "operation",
        "article",
        "quantity",
        "unit",
    ]


class OperationAdmin(admin.ModelAdmin):
    fields = ["contact", "m_type", "date", "annexe", "state"]
    inlines = [ItemInline]
    list_display = ("contact", "m_type", "date", "state")
    list_filter = ("m_type", "state")


admin.site.register(Operation, OperationAdmin)
