"""
All possible states an actor can be in:
    1. looking for seat, with/without luggage, currently stationary -> waiting
    2. looking for seat, with/without luggage, currently moving forward towards the back/front of the airplane -> moving
    3. looking for luggage storage room (no space at seating position), currently stationary/currently moving towards 
    the back/front of the airplane -> waiting/moving
    4. placing luggage -> stationary + moving luggage
    
"""
class Actor:
    def __init__(self, actor_id, passenger_type, seat, starting_action, starting_aisle_position):
        self.id = actor_id;
        self.passenger_type = passenger_type
        self.seat = seat
        self.action = starting_action
        self.position = starting_aisle_position

    """
    id := a unique ID (Integer) give to this actor upon initialization
    passenger_type := An object, which contains information on the size of the actor, the moving speed and information 
        on luggage
    seat := an object containing the row number and the column number of the assigned seat.
    action := an integer, which indicates the current action this actor is undertaking (possibilities can be found above
    position := an object inside a linked list representing the isle and possibly the overhead compartments 
    """

    def act(self):
        return


