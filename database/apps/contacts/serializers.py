from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',
'name',
'street',
'street_2',
'city',
'phone',
'email',
'is_customer',
'is_provider',
'is_for_invoice',
'note',
'has_not_email',
'parent_id',
        )


# class CompanySerializer(serializers.ModelSerializer):
#     contacts = ContactSerializer(many=True)

#     class Meta:
#         model = Company
#         read_only_fields = (
#             "operation_number",
#             "created_at",
#             "created_by",
#             "modified_at",
#             "modified_by",
#         )
#         fields = (
#             "id",
#             "name",
#             "phone",
#             "email",
#             "contacts",
#         )
