import json

import requests
from decouple import config

base_url = '{}:{}/api/'.format(config('TRACCAR_URL'), config('TRACCAR_PORT'))
auth = (config('TRACCAR_USER'), config('TRACCAR_PASSWORD'))

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


def get(target, params, pk=None, timeout=1200):
    url = _get_url(target, pk)
    return requests.get(url, headers=headers, params=params, auth=auth, timeout=timeout)


def post(target, data):
    url = _get_url(target)
    payload = json.dumps(data)
    return requests.post(url, headers=headers, data=payload, auth=auth, timeout=10)


def put(target, data):
    url = f'{base_url}{target}'
    payload = json.dumps(data)
    return requests.put(url, headers=headers, data=payload, auth=auth, timeout=10)


def delete(target, pk):
    url = _get_url(target, pk)
    return requests.delete(url, headers=headers, auth=auth, timeout=10)


def _get_url(target, pk=None):
    if pk is None:
        return '{}{}'.format(base_url, target)
    else:
        return '{}{}/{}'.format(base_url, target, pk)


def report_units_converter(report):
    return {
        'deviceId': report['deviceId'],
        'deviceName': report['deviceName'],
        'maxSpeed': report['maxSpeed'] * 1.85,
        'averageSpeed': report['averageSpeed'] * 1.85,
        'distance': report['distance'] / 1000,
        'spentFuel': report['spentFuel'],
        'engine_hours': report['engineHours']  # milliseconds
    }
