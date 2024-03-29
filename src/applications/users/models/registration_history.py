import uuid

from django.conf import settings
from django.db import models

from applications.tenants.models import Tenant
from applications.users.models.history_action_type import ActionType


class UserRegistrationHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ActionType.choices, default=ActionType.CREATED)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='registration_history', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, related_name='user_registration_history', on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserRegistrationHistory'
        ordering = ['-date']

    def __str__(self):
        return '{} - {}'.format(self.user, self.action)
