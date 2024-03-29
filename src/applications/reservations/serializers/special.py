from rest_framework import serializers

from applications.reservations.models import Recurrent
from applications.reservations.serializers.validator import validate_reservation_dates


class CreateByRecurrentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(allow_blank=True, required=False, style={'base_template': 'textarea.html'})
    startTime = serializers.DateTimeField(required=True)
    endTime = serializers.DateTimeField(required=True)
    vehicles = serializers.ListField(child=serializers.UUIDField(), allow_empty=False)
    is_driver_needed = serializers.BooleanField(required=False)
    recurrent = serializers.PrimaryKeyRelatedField(queryset=Recurrent.objects.all())


class CreateByDateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(allow_blank=True, required=False, style={'base_template': 'textarea.html'})
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    vehicles = serializers.ListField(child=serializers.UUIDField(), allow_empty=False)
    is_driver_needed = serializers.BooleanField(required=False)

    def validate(self, data):
        validate_reservation_dates(data)
        return data
