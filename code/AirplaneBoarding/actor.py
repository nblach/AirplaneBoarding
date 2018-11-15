"""
All possible states (actions) an actor can be in:
    0. Not yet in plane
    1. looking for free compartment     (moving/standing)
    2. storing luggage
    3. looking for seat (without luggage)
    4. moving into seat
    5. Seated
    6. Moving out of the seat in order to allow another actor to take their seat
"""


class Actor:

    def __init__(self, actor_id, passenger_type, seat, starting_action, starting_aisle_position):
        self.id = actor_id
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