import pytz

from datetime import datetime

ISO_PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'
TRACCAR_PATTERN = '%Y-%m-%dT%H:%M:%SZ'


def get_date_from_str_utc(str_date=None, pattern=ISO_PATTERN):
    if str_date in [None, '']:
        return None
    date = datetime.strptime(str_date, pattern)
    date = datetime(date.year,
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