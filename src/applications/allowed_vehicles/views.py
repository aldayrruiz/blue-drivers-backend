import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from applications.allowed_vehicles.services.updater import AllowedVehiclesUpdater
from applications.users.services.queryset import get_user_queryset
from shared.permissions import ONLY_ADMIN_OR_SUPER_ADMIN

logger = logging.getLogger(__name__)


class AllowedVehicleViewSet(viewsets.ViewSet):
    @swagger_auto_schema()
    def update(self, request, pk=None):
        """
        Update list of allowed vehicles of a user.
        """
        requester = self.request.user
        logger.info('Update user allowed vehicles request received.')
        user_queryset = get_user_queryset(requester, even_disabled=True)
        user = get_object_or_404(user_queryset, pk=pk)

        # Get new vehicles allowed replacing older ones (vehicles_queryset == vehicles in same tenant as admin)
        vehicle_ids = self.request.data
        updater = AllowedVehiclesUpdater(requester)
        updater.update(user, vehicle_ids)
        return Response(status=HTTP_200_OK)

    def get_permissions(self):
        """
        Only admin can modify vehicle privileges of users.
        """
        return [permission() for permission in ONLY_ADMIN_OR_SUPER_ADMIN]
