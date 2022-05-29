from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ItemViewSet,
    OperationViewSet,
    PowerFilterApiView,
    UndoneApiView,
    generate_pdf,
    update__stock_qty,
)

router = DefaultRouter()
router.register("operations", OperationViewSet, basename="operations")
router.register("items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
    path("power_filter/", PowerFilterApiView.as_view(), name="power_filter"),
    path("undone/", UndoneApiView.as_view(), name="undone"),
    path(
        "operations/<int:operation_id>/generate_pdf/",
        generate_pdf,
        name="generate_pdf",
    ),
    path(
        "operations/<int:operation_id>/update__stock_qty/",
        update__stock_qty,
        name="update__stock_qty",
    ),
]
