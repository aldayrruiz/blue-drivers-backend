import calendar
import datetime

import pytz
from django.db import models
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta

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


def now_utc():
    """
    Returns the current datetime in UTC timezone. This must be used to store in database.
    """
    return datetime.datetime.utcnow().astimezone(datetime.timezone.utc)


def is_after_now(date):
    now = get_now_utc()
    return now < date


def get_first_and_last_day_of(year, month):
    (_, last_day) = calendar.monthrange(year, month)
    first_datetime = datetime.datetime(year, month, 1, 0, 0, 0, 0)
    last_datetime = first_datetime + relativedelta(months=1)
    return first_datetime, last_datetime


def get_number_of_days_in_month(month, year):
    return calendar.monthrange(year, month)[1]


def get_hours_duration(start, end):
    duration = relativedelta(end, start)
    hours = duration.days * 24 + duration.minutes / 60 + duration.hours
    return hours


def from_date_to_utc(year, month, day, hour, minute=0, second=0):
    """
    Returns a datetime object in UTC timezone. For example, if the server is in UTC+2, and the
    parameters are 2020, 1, 1, 0, 0, 0, the returned datetime will be 2019-12-31 22:00:00.
    """
    local = pytz.timezone('Europe/Madrid')
    naive = datetime.datetime(year, month, day, hour, minute, second)
    local_dt = local.localize(naive)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt
