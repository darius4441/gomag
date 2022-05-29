from rest_framework import serializers

from .models import Company, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        read_only_fields = (
            "company",
            "getCompanyName",
            "created_at",
            "modified_at",
            "created_by",
            "modified_by",
        )
        fields = (
            "id",
            "name",
            "gender",
            "company",
            "getCompanyName",
            "c_type",
            "is_archived",
        )


class CompanySerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Company
        read_only_fields = (
            "operation_number",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
        )
        fields = (
            "id",
            "name",
            "phone",
            "email",
            "contacts",
        )
