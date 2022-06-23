from django.db import models

from applications.reports.models.abstract_report import AbstractReport
from applications.tenants.models import Tenant


class UseWithoutReservation(AbstractReport):
    hours = models.DecimalField()
    tenant = models.ForeignKey(Tenant, related_name='use_without_reservation_reports', on_delete=models.CASCADE)

    class Meta:
        db_table = 'UseWithoutReservation'
