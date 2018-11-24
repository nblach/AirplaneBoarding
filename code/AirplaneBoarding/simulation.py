import numpy as np
import math
from passenger_type import Passenger_Type
from actor import Actor
from seat_assignments import Assignments

PASSENGER_SIZE = 0.4
UNIT_LENGTH = 0.001  # meter
UNIT_TIME = 0.1  # seconds


MAXIMUM_MOVING_SPEED = 3  # m/s
MINIMUM_MOVING_SPEED = 0.3  # m/s
MODE_MOVING_SPEED = 1

MAXIMUM_ROW_ENTER_TIME = 10  # m/s
MINIMUM_ROW_ENTER_TIME = 2.5  # m/s
MODE_ROW_ENTER_TIME = 4

MAXIMUM_EXIT_ROW_TIME = 15  # m/s
MINIMUM_EXIT_ROW_TIME = 5  # m/s
MODE_EXIT_ROW_TIME = 7.5

MAXIMUM_STORE_TIME = 14.5  # s
MINIMUM_STORE_TIME = 1.5  # s
MODE_STORING_TIME = 4



class Simulation:

    def __init__(self, number_of_actors, plane, seat_assignment_id):
        self.seat_assignment = Assignments.generate_assignment(plane, number_of_actors, seat_assignment_id)
        self.actors = []
        self.plane = plane
        self.number_of_actors = number_of_actors

        #fill actors[] with random actors
        for i in range(1, self.number_of_actors+1):
            actor = Actor(i, self.get_random_passenger(), self.seat_assignment[i], 0, plane)
            self.actors.append(actor)
        self.plane.actors = self.actors


        #simulation[] will contain all states observed during simulation (in order)
        self.simulation = list()

    """
    Passenger moving speed data is given in from of a triangular distribution (it was recoded for Short Haul airplanes):
        passing_one_row_seconds = [1.8, 2.4, 3.0] seconds per row - average row size around 2002 was 0.87m
        install_in_seat_seconds = [6.0, 9.0, 30.0] seconds
        exit_from_seat_into_aisle = [3.0, 3.6, 4.2] seconds
    Passenger luggage load is chosen by us, so we can have different set ups. 
    In the paper they had two options normal and high load. 
    """

    @staticmethod
    def get_random_passenger():
        # test data
        moving_speed = [Simulation.m_per_s_to_speed_unit(np.random.triangular(MINIMUM_MOVING_SPEED, MODE_MOVING_SPEED, MAXIMUM_MOVING_SPEED)), Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_ROW_ENTER_TIME, MODE_ROW_ENTER_TIME, MAXIMUM_ROW_ENTER_TIME)),
                        Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_EXIT_ROW_TIME, MODE_EXIT_ROW_TIME, MAXIMUM_EXIT_ROW_TIME))]
        number_of_bags_possibilities = [0, 1, 1]
        load_probabilities = [[0.6, 0.3, 0.1], [0.2, 0.6, 0.2]]
        number_of_bags = np.random.choice(number_of_bags_possibilities, p=load_probabilities[0])
        storing_time = Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_STORE_TIME, MODE_STORING_TIME, MAXIMUM_STORE_TIME))
        return Passenger_Type(number_of_bags, moving_speed, storing_time,  Simulation.meter_to_space_unit(PASSENGER_SIZE))

    def simulate(self):
        done = False
        i = 0
        next_actor_in = 0

        while not done:
            if i%100 == 0:
                print('still going strong ', i)
            j = 0
            actors_seated = 0
            prev_actor = -1
            # loop backwards through aisle and store order of actors in list
            acting_order = list()
            for x in reversed(range(0, self.plane.length)):
                if self.plane.aisle.occupance[x] != prev_actor and self.plane.aisle.occupance[x] > 0:
                    #print(self.plane.aisle.occupance[x])
                    acting_order.append(self.actors[self.plane.aisle.occupance[x]-1])
                    prev_actor = self.plane.aisle.occupance[x]
            # let the actors do their magic
            for a in acting_order:
                a.act()
            # try letting the next actor enter the plane
            if next_actor_in < len(self.actors) and self.actors[next_actor_in].act() != 1:
                #print('actor just entered the plane: ' , next_actor_in)
                next_actor_in += 1

            frame = np.zeros((self.number_of_actors,4), dtype=int)
            for a in self.actors:
                frame[j, 0] = a.position
                frame[j, 1] = a.action
                frame[j, 2] = a.seat.row_number
                frame[j, 3] = a.seat.col_numbner
                if a.action == 5:
                    actors_seated += 1
                j += 1
            self.simulation.append(frame)
            i += 1
            if actors_seated == self.number_of_actors:
                done = True

    @staticmethod
    def m_per_s_to_speed_unit(speed):
        return round(speed / (UNIT_LENGTH/UNIT_TIME))

    @staticmethod
    def sec_to_time_unit(seconds):
        return round(seconds / UNIT_TIME)

    @staticmethod
    def meter_to_space_unit(meters):
        return round(meters / UNIT_LENGTH)

