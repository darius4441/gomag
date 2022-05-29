from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AlertProductViewSet,
    InventoryViewSet,
    POSViewSet,
    ProductViewSet,
    UomCategoryViewSet,
    UomViewSet,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("pos", POSViewSet, basename="pos")
router.register(
    "alert_products", AlertProductViewSet, basename="alert_products"
)
router.register(
    "uom-categories", UomCategoryViewSet, basename="uom-categories"
)
router.register("uom", UomViewSet, basename="uom")
router.register("inventory", InventoryViewSet, basename="inventory")

urlpatterns = [
    path("stock/", include(router.urls)),
]
