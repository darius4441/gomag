from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Item, Operation


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = ("operation", "old_qty")
        fields = (
            "id",
            "article",
            "quantity",
            "unit",
            "old_qty",
            "get_article_name",
            "get_article_available_qty",
        )


class OperationSerializer(
    WritableNestedModelSerializer, serializers.ModelSerializer
):
    items = ItemSerializer(many=True)

    class Meta:
        model = Operation
        read_only_fields = (
            "operation_number",
            "getContactName",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
        )
        fields = (
            "id",
            "contact",
            "m_type",
            "date",
            "annexe",
            "state",
            "items",
            "getContactName",
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        operation = Operation.objects.create(**validated_data)

        for item in items_data:
            Item.objects.create(operation=operation, **item)

        return operation
