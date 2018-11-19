"""
All possible states (actions) an actor can be in:
    0. Not yet in plane
    1. looking for free compartment: a. near seat
                                     b. further back (if nothing free by seat)
                                     c. towards front of plane (if nothing free near or behind seat)
    2. storing luggage
    3. moving to seat (without luggage)
    4. moving into seat
    5. Seated

   Also, instead of moving regularly, an actor can be switching its position with another actor
"""


class Actor:

    def __init__(self, actor_id, passenger_type, seat, starting_action, plane):
        self.id = actor_id
        self.passenger_type = passenger_type
        self.seat = seat
        self.action = starting_action
        self.action_1 = 0
        self.position = -1
        self.luggage = passenger_type.number_of_bags
        self.plane = plane

        # fields needed for switching
        self.switching = False
        self.switch_timer = 0
        self.position_after_switch

    """
    id := a unique ID (Integer) give to this actor upon initialization
    passenger_type := An object, which contains information on the size of the actor, the moving speed and information 
        on luggage
    seat := an object containing the row number and the column number of the assigned seat.
    action := an integer, which indicates the current action this actor is undertaking (possibilities can be found above
    action_1 := indicating, which substate of action 1 is being done (0 = a, 1 = b, 2 = c)
    position := index of position in the aisle (-1 if not yet in plane/aisle)
    luggage := current number of luggage pieces
    plane := plane object that is boarded. Containing aisle, etc.
    
    """

    # returns 1 if the actor is not in the plane yet
    def act(self):

            # treat switch separately
            if self.switching:
                if(self.switch_timer > 0):
                    self.switch_timer -= 1
                else:
                    self.set_position(self.position_after_switch)
                    self.switching = False
                return 0

            else:

                # if because python does not have proper switch statements
                if self.action == 0:

                    # for action = 0, act is only called when self (this actor) is next in order to board plane
                    for i in range(0, self.size):
                        if self.plane.aisle.occupance[i] != 0:
                            return 1 #cannot enter plane yet

                    # can enter plane
                    self.set_position(0)
                    if self.luggage > 0:
                        self.action = 1
                    else:
                        self.action = 3
                    return 0

                if self.action == 1:
                    if self.action_1 == 0:





    def set_position(self, position):
        self.position = position
        # mark occupied space in aisle
        for i in range(self.position, self.position + self.size):
            self.plane.aisle.occupance[i] = self.id

