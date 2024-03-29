from applications.reservations.models import Reservation
from applications.tenants.models import Tenant
from applications.users.models import Role, User
from applications.vehicles.models import Vehicle
from utils.dates import get_now_utc


def get_reservation_queryset(requester, take_all=False, owner_id=None, vehicle_id=None, _from=None, _to=None):
    tenant = requester.tenant
    if requester.role in [Role.ADMIN, Role.SUPER_ADMIN] and take_all:
        # For admin web - All reservations
        queryset = Reservation.objects.filter(tenant=tenant)
    else:
        # For mobile (Users or Admins) - All reservations made by requester
        # Filter by tenant is not needed because of own requester
        queryset = Reservation.objects.filter(tenant=tenant, owner=requester)

    if owner_id:
        # If reservations of user is specified
        queryset = queryset.filter(owner_id=owner_id)

    if vehicle_id:
        # If reservations of vehicle is specified
        queryset = queryset.filter(vehicle_id=vehicle_id)

    if _from and _to:
        # Not needed, but useful in future
        queryset = queryset.filter(start__gte=_from, start__lte=_to)
    return queryset


def get_recurrent_queryset(requester):
    queryset = requester.recurrences
    return queryset.all()


def get_future_reservations():
    future_reservations = Reservation.objects.exclude(end__lt=get_now_utc())
    return future_reservations


def get_future_reservations_of(requester):
    future_reservations = get_future_reservations()
    return future_reservations.filter(owner_id=requester.id)
