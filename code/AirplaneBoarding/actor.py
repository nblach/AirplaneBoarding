from seat import Seat
from passenger_type import Passenger_Type

class Actor:
    def __init__(self, actor_id, passenger_type, seat, starting_action, starting_position):
        self.id = actor_id;
        self.passenger_type = passenger_type
        self.seat = seat
        self.action = starting_action
        self.position = starting_position
