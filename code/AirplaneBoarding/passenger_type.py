class Passenger_Type:

    def __init__(self, number_of_bags, moving_speed, storing_time, physical_size, personal_space, field_of_view):
        self.number_of_bags = number_of_bags
        self.size = physical_size + personal_space
        self.physical_size = physical_size
        self.personal_space = personal_space
        self.moving_speed = moving_speed
        self.field_of_view = field_of_view
        self.storing_time = storing_time

