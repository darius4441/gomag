from rest_framework import serializers

from .models import CategoryUOM, Inventory, InventoryItem, Product, Uom


class CategoryUomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryUOM
        fields = "__all__"


class UomSerializer(serializers.ModelSerializer):
    category_id = CategoryUomSerializer(many=False)

    class Meta:
        model = Uom
        read_only_fields = ("category_id",)
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = (
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "getUom",
        )
        fields = (
            "id",
            "name",
            "prod_type",
            "category",
            "code",
            "description",
            "providers",
            "uom",
            "slug",
            "getReplenish",
            "alert_stock",
            "optimal_stock",
            "real_quantity",
            "virtual_quantity",
            "unit_price",
            "unit_cost",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "getUom",
        )

    def create(self, validated_data):
        operation = Product.objects.create(**validated_data)

        return operation


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        read_only_fields = ("inventory",)
        fields = (
            "id",
            "article",
            "initial_quantity",
            "getArticleName",
            "getArticleUom",
        )


class InventorySerializer(serializers.ModelSerializer):
    items_inventory = InventoryItemSerializer(many=True)
    read_only_fields = (
        "created_at",
        "created_by",
        "modified_at",
        "modified_by",
    )

    class Meta:
        model = Inventory
        fields = (
            "id",
            "name",
            "date",
            "items_inventory",
        )

    def create(self, validated_data):
        items_inventory_data = validated_data.pop("items_inventory")
        inventory = Inventory.objects.create(**validated_data)

        for item in items_inventory_data:
            InventoryItem.objects.create(inventory=inventory, **item)

        return inventory
