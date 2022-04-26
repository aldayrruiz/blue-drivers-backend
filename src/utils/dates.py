import datetime

import pytz
from django.db import models
from django.utils.translation import gettext_lazy as _

ISO_PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'
TRACCAR_PATTERN = '%Y-%m-%dT%H:%M:%SZ'
TIMEZONE = 'UTC'
utc = pytz.UTC


class WeekDay(models.IntegerChoices):
    MONDAY = 0, _('MONDAY')
    TUESDAY = 1, _('TUESDAY')
    WEDNESDAY = 2, _('WEDNESDAY')
    THURSDAY = 3, _('THURSDAY')
    FRIDAY = 4, _('FRIDAY')
    SUNDAY = 5, _('SUNDAY')
    SATURDAY = 6, _('SATURDAY')


def get_date_from_str_utc(str_date=None, pattern=ISO_PATTERN):
    if str_date in [None, '']:
        return None
    date = datetime.datetime.strptime(str_date, pattern)
    date = datetime.datetime(date.year,
                             date.month,
                             date.day,
                             date.hour,
                             date.minute,
                             date.second,
                             date.microsecond,
                             tzinfo=pytz.utc)
    return date


def from_date_to_str_date_traccar(date):
    return date.strftime(TRACCAR_PATTERN)


def from_naive_to_aware(date):
    return date.replace(tzinfo=utc)


def get_now_utc():
    timezone = pytz.timezone(TIMEZONE)
    return datetime.datetime.now().astimezone(timezone)


def is_after_now(date):
    now = get_now_utc()
    return now < date