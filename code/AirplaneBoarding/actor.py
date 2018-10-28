from seat import Seat
from passenger_type import Passenger_Type

class Actor:
    def __init__(self, actor_id, number_of_bags, passenger_size, passenger_moving_speed, row_number, col_number,
                 starting_action, starting_position):
        self.id = actor_id;
        self.passenger_type = Passenger_Type(self, number_of_bags, passenger_size, passenger_moving_speed)
        self.seat = Seat(self, row_number, col_number)
        self.action = starting_action
        self.position = starting_position
