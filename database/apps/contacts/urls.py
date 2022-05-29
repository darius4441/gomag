from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, ContactViewSet

router = DefaultRouter()
router.register("contacts", ContactViewSet, basename="contacts")
router.register("company", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
]
