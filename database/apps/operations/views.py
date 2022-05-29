import django
import pdfkit
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from xhtml2pdf import pisa
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.stock.models import Product

from .models import Item, Operation
from .serializers import ItemSerializer, OperationSerializer


class OperationPagination(PageNumberPagination):
    page_size = 17


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = [DjangoFilterBackend]
    search_fields = "article"


class OperationViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()
    pagination_class = OperationPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "contact__id",
        "contact__name",
        "state",
        "date",
        "m_type",
        "items__article",
        "items__article__name",
    ]
    # search_fields = (
    #     "contact__id",
    #     "contact__name",
    #     "state",
    #     "date",
    #     "m_type",
    #     "items__article__name",
    # )

    @action(detail=True, methods=["get"])
    def traceability(self, request):
        ops = self.get_object()
        # print(ops)
        recent_products = Operation.objects.all()

        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)

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

        serializer.save(
            modified_by=self.request.user,
        )


class PowerFilterApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Operation.objects.all()

        # custum filter
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        total_sale = queryset.filter(m_type="out", state="done").aggregate(
            total=Sum(F("items__quantity") * F("items__article__unit_cost"))
        )

        stock_value = Product.objects.aggregate(
            total=Sum(F("real_quantity") * F("unit_cost"))
        )

        daily_client = f"{len(queryset.filter(m_type='out', state='done', date=end_date))} / {len(queryset.filter(m_type='out', date=end_date))}"

        if start_date and end_date:
            tot_amount = (
                queryset.filter(
                    m_type="out",
                    state="done",
                    date__range=(start_date, end_date),
                )
                .values("date")
                .annotate(
                    sub_total=Sum(
                        F("items__quantity") * F("items__article__unit_cost")
                    )
                )
                .order_by("date")
            )

        serializer = OperationSerializer(queryset, many=True)

        return Response(
            {
                "queryset": serializer.data,
                "daily_performance": tot_amount,
                "stock_value": stock_value,
                "total_sale": total_sale,
                "daily_client": daily_client,
            }
        )


class UndoneApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Operation.objects.filter(state="draft")

        undone = queryset.annotate(Count("state"))

        serializer = OperationSerializer(queryset, many=True)
        return Response({"queryset": serializer.data, "undone": undone})


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, operation_id):
    operation = get_object_or_404(
        Operation, pk=operation_id, created_by=request.user
    )

    template_name = "pdf.html"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="stock.pdf"'
    template = get_template(template_name)
    html = template.render({"operation": operation})

    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def update__stock_qty(request, operation_id):
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
