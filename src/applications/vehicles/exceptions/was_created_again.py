from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN


class VehicleCreatedAgainError(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = 'El vehículo estaba eliminado y fue creado de nuevo con sus anteriores datos'
