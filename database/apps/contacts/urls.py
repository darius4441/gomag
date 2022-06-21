from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactViewSet

router = DefaultRouter()
router.register("contacts", ContactViewSet, basename="contacts")

urlpatterns = [
    path("", include(router.urls)),
]
