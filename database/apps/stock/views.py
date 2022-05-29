from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import CategoryUOM, Inventory, Product, Uom
from .serializers import (
    CategoryUomSerializer,
    InventorySerializer,
    ProductSerializer,
    UomSerializer,
)


class ProductPagination(PageNumberPagination):
    page_size = 17


class UomCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryUomSerializer
    queryset = CategoryUOM.objects.all()


class UomViewSet(viewsets.ModelViewSet):
    serializer_class = UomSerializer
    queryset = Uom.objects.all()


class AllProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(isArchived=False).order_by("name")


class POSViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(isArchived=False).order_by("name")[:12]
    filter_backends = [filters.SearchFilter]
    search_fields = ("code", "name", "category", "providers")


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(isArchived=False).order_by("name")
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("code", "name", "category", "providers")

    @action(detail=False)
    def all_products(self, request):
        all_products = Product.objects.filter(isArchived=False).order_by(
            "name"
        )

        serializer = self.get_serializer(all_products, many=True)
        return Response(serializer.data)

        serializer = self.get_serializer(pos_products, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user, modified_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class AlertProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(
        isArchived=False, real_quantity__lte=F("alert_stock")
    ).order_by("name")
    pagination_class = ProductPagination


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ("name", "date", "items__article__name")

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user, modified_by=self.request.user
        )

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied("Wrong object owner")

        serializer.save(modified_by=self.request.user)


""" 
@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def multiple_product_creator(request):
    operation = get_object_or_404(
        Operation, pk=operation_id, created_by=request.user
    )
    items = Item.objects.filter(operation=operation_id)

    try:
        if operation.state != "done":
            # decrease current product quantity if operation_type is 'out'
            if operation.m_type == "out":
                for item in items:
                    product = Product.objects.get(id=item.article.id)
                    product.real_quantity -= item.quantity
                    product.save()

            # increase else
            else:
                for item in items:
                    product = Product.objects.get(id=item.article.id)
                    product.real_quantity += item.quantity
                    product.save()

            operation.state = "done"
            operation.save()
        else:
            AssertionError("INTERNAL ERROR: This operation is currently done!")

    except:
        AssertionError("INTERNAL ERROR: Cannot update stock now!")

    return Response()
 """
