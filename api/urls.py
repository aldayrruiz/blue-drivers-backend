from django.urls import path
from api.views import VehicleViewSet, VehicleTypeViewSet, ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'vehicletypes', VehicleTypeViewSet, basename='vehicletype')
router.register(r'reservations', ReservationViewSet, basename='reservation')
urlpatterns = router.urls
