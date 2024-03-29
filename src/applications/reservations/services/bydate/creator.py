from operator import itemgetter

from applications.allowed_vehicles.services.queryset import get_vehicles_ordered_by_ids
from applications.reservations.exceptions.already_posses_reservation_at_the_same_time import \
    YouAlreadyPossesOtherReservationAtSameTime
from applications.reservations.models import Reservation
from applications.reservations.services.validator import ReservationValidator
from utils.dates import from_naive_to_aware


class ReservationByDateCreator:
    def __init__(self, title, description, start, end, vehicles, owner, is_driver_needed):
        self.title = title
        self.description = description
        self.start = from_naive_to_aware(start)
        self.end = from_naive_to_aware(end)
        self.vehicles = vehicles
        self.owner = owner
        self.is_driver_needed = is_driver_needed

    def create(self):
        """
        Return reservation created. Otherwise, None is returned.
        """

        for vehicle in self.vehicles:
            possible_reservation = self.__get_reservation__(self.owner, vehicle)
            validator = ReservationValidator(vehicle, self.owner)
            [is_valid, r_conflict] = validator.is_reservation_valid(possible_reservation)
            if is_valid:
                possible_reservation.save()
                return possible_reservation
            if r_conflict.owner == self.owner:
                raise YouAlreadyPossesOtherReservationAtSameTime()
        return None

    def __get_reservation__(self, requester, vehicle):
        reservation = Reservation(
            title=self.title,
            description=self.description,
            start=self.start,
            end=self.end,
            vehicle=vehicle,
            owner=requester,
            tenant=requester.tenant,
            is_driver_needed=self.is_driver_needed
        )
        return reservation

    @staticmethod
    def from_serializer(serializer, owner):
        # Just taking all variables from body request
        (
            title,
            description,
            start,
            end,
            vehicles_ids,
            is_driver_needed
        ) = itemgetter('title',
                       'description',
                       'start',
                       'end',
                       'vehicles',
                       'is_driver_needed')(serializer.validated_data)

        # Get vehicles ordered by user preference
        vehicles = get_vehicles_ordered_by_ids(vehicles_ids, owner)

        return ReservationByDateCreator(title, description, start, end, vehicles, owner, is_driver_needed)
