import math
"""
All possible states (actions) an actor can be in:
    0. Not yet in plane
    1. looking for free compartment: 0. near seat
                                     1. first free towards the back (if nothing free by seat)
                                     2. towards front of plane (if nothing free near or behind seat)
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
        self.switch_forward_request = False
        self.switch_backwards_request = False
        self.switch_front_limit = -1
        self.switch_back_limit = -1
        self.switch_partner = None
        self.switch_done = False

        # fields needed for storing
        self.storing = False
        self.store_timer = 0

        # fields needed to move into seat
        self.seat_waiting = False
        self.seat_wait_counter = 0

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
                # we stop switching at 1 because mathematically speaking we already completed all required cycles.
                if self.switch_timer <= 1:
                    self.set_position(self.position_after_switch)
                    self.switching = False

                self.switch_timer -= 1
                return 0

            else:

                position_seat = self.plane.get_start_of_row(self.seat.row_number)
                compartment_current_position = self.plane.get_compartment_at_pos(self.position)
                # if because python does not have proper switch statements
                if self.action == 0:

                    # for action = 0, act is only called when self (this actor) is next in order to board plane
                    for i in range(0, self.size):
                        if self.plane.aisle.occupance[i] != 0:
                            return 1 # cannot enter plane yet

                    # can enter plane
                    self.set_position(0)
                    if self.luggage > 0:
                        self.action = 1
                    else:
                        self.action = 3
                    return 0

                if self.action == 1:
                    if self.action_1 == 0:
                        # Can we see our seat?
                        if  position_seat > (self.passenger_type.field_of_view + self.position):
                            # We cannot see our seat, move forward
                            self.move_forward(None)  # limit would be position_seat, but in this case, the limit can
                                                     # be dropped due to constraints speed<row_length<fov
                            return 0
                        else:
                            # We can see our seat
                            compartment_at_seat = self.plane.get_compartment_at_pos(position_seat)
                            # can we store all our luggage in the compartment at our seat?
                            if compartment_at_seat.free_space < self.luggage:
                                # not enough space, therefore store in next free compartment (fall through to next case)
                                self.action_1 = 1;
                            else:
                                # try to store luggage at seat
                                if compartment_at_seat == compartment_current_position:
                                    # we are at the compartment at our seat, fall through to store
                                    self.action = 2
                                else:
                                    # we are not yet at the compartment at our seat
                                    self.move_forward(position_seat)
                                    return 0

                    if self.action_1 == 1:
                        if compartment_current_position.free_space > 0:
                            # we are at a free compartment, fall through to store
                            self.action = 2
                        else:
                            # if at last compartment of plane
                            if compartment_current_position == self.plane.compartments[-1]:
                                # turn around
                                self.action_1 = 2
                            else:
                                self.move_forward(None)
                                return 0

                    if self.action_1 == 2:
                        if compartment_current_position.free_space > 0:
                            # we are at a free compartment, fall through to store
                            self.action = 2
                        else:
                            # if at first compartment of plane
                            if compartment_current_position == self.plane.compartments[0]:
                                # should not happen because the hand luggage exceeds storage room (not covered)
                                raise ValueError('ERROR: The amount of hand luggage exceeds the amount of storage room')
                            else:
                                self.move_backward(None)
                                return 0

                if self.action == 2:
                    # did we already start storing
                    if not self.storing:
                        # start storing
                        self.storing = True
                        # how many items can we store in this compartment
                        items_to_store = min(compartment_current_position.free_space, self.luggage)
                        # how long do we take to store
                        self.store_timer = self.storing_time(compartment_current_position, items_to_store)
                        # update capacities
                        self.luggage -= items_to_store
                        compartment_current_position.free_space -= items_to_store

                    # continue storing
                    if self.store_timer <= 1:
                        # finish storing
                        self.storing = False
                        if self.luggage > 0:
                            self.action = 1
                        else:
                            self.action = 3
                    self.store_timer -= 1
                    return 0

                if self.action == 3:
                    if self.can_enter_seat():
                        # falling through to state moving into seat
                        self.action = 4
                    else:
                        # move in direction of seat
                        if self.position < position_seat:
                            self.move_forward(position_seat)
                        else:
                            self.move_backward(position_seat + self.plane.aisle.row_entry_size - self.passenger_type.size)
                        return 0

                if self.action == 4:
                    # currently waiting?
                    if not self.seat_waiting:
                        self.set_seat_wait_counter()
                        self.seat_waiting = True

                    if self.seat_wait_counter <= 1:
                        self.action = 5
                        self.seat_waiting = False
                        self.sit_down()

                    self.seat_wait_counter -= 1
                    return 0
                if self.action == 5:
                    raise ValueError('ERROR: Actor is in state 5, but was called to act, '
                                     'which means he is still in the aisle (impossible)')

    def sit_down(self):
        # in our seat we store the sum of the times we need to leaf and enter that seat again
        self.plane.seat_occupance[self.seat.row_number][self.seat.col_numbner] = \
            self.passenger_type.moving_speed[2] + self.passenger_type.moving_speed[1]
        # TODO

    def move_forward(self, limit):
        # limit is inclusive
        # limit might equal None
        if not limit:
            limit = len(self.plane.aisle.occupance)- self.passenger_type.size

        if not self.switching:
            # can i move forward
            if self.plane.aisle.occupance[self.position+self.passenger_type.size]!= 0:
                # is the actor in front of me requesting to switch with me?
                next_field_actor = self.plane.actors[self.plane.aisle.occupance[self.position+self.passenger_type.size]-1]
                if next_field_actor.switch_backwards_request:
                    # Lets switch, set both actors to switching
                    self.switching = True
                    next_field_actor.switching = True
                    next_field_actor.switch_backwards_request = False
                    # set limits
                    self.switch_front_limit = next_field_actor.position + next_field_actor.passenger_type.size - self.passenger_type.size
                    next_field_actor.switch_front_limit = next_field_actor.position
                    self.switch_back_limit = self.position
                    next_field_actor.switch_back_limit = self.position
                    # set switching partners
                    self.switch_partner = next_field_actor
                    next_field_actor.switch_partner = self
                    # reset switch done variables
                    self.switch_done = False
                    next_field_actor.switch_done = False

                else:
                    # request switch
                    self.switch_forward_request = True
            else:
                # move forward
                limit = min(limit, self.passenger_type.moving_speed[0] + self.position)
                # we can move forward at least 1 spot
                furthest_free_pos = self.position + 1
                # calculate the furthest position we can get to
                while self.plane.aisle.occupance[furthest_free_pos + self.passenger_type.size] == 0 \
                        and furthest_free_pos < limit:
                    furthest_free_pos += 1

                # reset possible switch request
                self.switch_forward_request = False
                self.switch_backwards_request = False
                # set new position
                self.reset_position()
                self.set_position(furthest_free_pos)
            return 0

        else:
            # can we finish switching
            if self.position == self.switch_front_limit:
                self.switch_done = True
                if self.switch_partner.switch_done:
                    # we can finish switching
                    self.switching = False
                    self.switch_partner.switching = False
                    self.switch_done = False
                    self.switch_partner.switch_done = False
                    # is our partner at the other end
                    if self.switch_partner.position == self.switch_partner.switch_back_limit:
                        # at other end
                        self.set_position(self.position)
                        self.switch_partner.set_position(self.switch_partner.position)

                    else:
                        # at the same limit
                        # the other actor was first, so we move ourselves back
                        self.switch_partner.set_position(self.switch_partner.position)
                        self.set_position(self.switch_back_limit)

                    self.switch_partner.switch_partner = None
                    self.switch_partner = None
                return 0
            else:
                # move to new position
                limit = min(limit, self.switch_front_limit)
                self.position = min(limit, self.position + self.switch_speed())


    def move_backward(self, limit):
        # limit is inclusive
        # limit might equal None
        if not limit:
            limit = 0

        if not self.switching:
            # can I move forward
            if self.plane.aisle.occupance[self.position -1] != 0:
                # is the actor in front of me requesting to switch with me?
                prev_field_actor = self.plane.actors[self.plane.aisle.occupance[self.position -1] - 1]
                if prev_field_actor.switch_forward_request:
                    # Lets switch, set both actors to switching
                    self.switching = True
                    prev_field_actor.switching = True
                    prev_field_actor.switch_forward_request = False
                    # set limits
                    self.switch_front_limit = self.position
                    prev_field_actor.switch_front_limit = self.position - prev_field_actor.passenger_type.size + self.passenger_type.size
                    self.switch_back_limit = prev_field_actor.position
                    prev_field_actor.switch_back_limit = prev_field_actor.position
                    # set switching partners
                    self.switch_partner = prev_field_actor
                    prev_field_actor.switch_partner = self
                    # reset switch done variables
                    self.switch_done = False
                    prev_field_actor.switch_done = False

                else:
                    # request switch
                    self.switch_backwards_request = True
            else:
                # move backwards
                limit = max(limit, self.position - self.passenger_type.moving_speed[0])
                # we can move backwards at least 1 spot
                furthest_free_pos = self.position - 1
                # calculate the furthest position we can get to
                while self.plane.aisle.occupance[furthest_free_pos - 1] == 0 \
                        and furthest_free_pos > limit:
                    furthest_free_pos -= 1

                # reset possible switch request
                self.switch_forward_request = False
                self.switch_backwards_request = False
                # set new position
                self.reset_position()
                self.set_position(furthest_free_pos)
            return 0

        else:
            # can we finish switching
            if self.position == self.switch_back_limit:
                self.switch_done = True
                if self.switch_partner.switch_done:
                    # we can finish switching
                    self.switching = False
                    self.switch_partner.switching = False
                    self.switch_done = False
                    self.switch_partner.switch_done = False
                    # is our partner at the other end
                    if self.switch_partner.position == self.switch_partner.switch_front_limit:
                        # at other end
                        self.set_position(self.position)
                        self.switch_partner.set_position(self.switch_partner.position)

                    else:
                        # at the same limit
                        # the other actor was first, so we move ourselves forward
                        self.switch_partner.set_position(self.switch_partner.position)
                        self.set_position(self.switch_front_limit)

                    self.switch_partner.switch_partner = None
                    self.switch_partner = None
                return 0
            else:
                # move to new position
                limit = max(limit, self.switch_back_limit)
                self.position = max(limit, self.position - self.switch_speed())


    def switch_speed(self, other_actor):
        # TODO
        return math.ceil(self.passenger_type.moving_speed[0]/2)


    def set_seat_wait_counter(self):
        self.seat_wait_counter = self.passenger_type.moving_speed[1]
        # we count from left to right, are we sitting on the left?
        if self.seat.col_numbner <= self.plane.seatsLeft - 1:
            for i in range(0, self.seat.col_numbner):
                self.seat_wait_counter += self.plane.seat_occupance[self.seat.row_number][i]
        else:
            for i in range(self.seat.col_numbner + 1, self.plane.seatsLeft + self.plane.seatsRight):
                self.seat_wait_counter += self.plane.seat_occupance[self.seat.row_number][i]


    def can_enter_seat(self, seat_pos):
        return (self.position >= seat_pos) and ((self.position + self.passenger_type.size-1) <= (seat_pos + self.plane.aisle.row_entry_size-1))


    def set_position(self, position):
        self.position = position
        # mark occupied space in aisle
        for i in range(self.position, self.position + self.passenger_type.size):
            self.plane.aisle.occupance[i] = self.id


    def reset_position(self):
        # unmark occupied space in aisle
        for i in range(self.position, self.position + self.passenger_type.size):
            self.plane.aisle.occupance[i] = 0


    def storing_time(self, compartment, items):
        # TODO
        return items*self.passenger_type.storing_time
