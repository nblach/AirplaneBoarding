import numpy as np
import random
from passenger_type import Passenger_Type
from actor import Actor
from seat_assignments import Assignments

PASSENGER_SIZE = 0.5
PASSENGER_PERSONAL_SPACE = 0.45

UNIT_LENGTH = 0.001  # meter
UNIT_TIME = 0.1  # seconds


MAXIMUM_MOVING_SPEED = 1.7  # m/s
MINIMUM_MOVING_SPEED = 0.2  # m/s
MODE_MOVING_SPEED = 0.8

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

    def __init__(self, number_of_actors, plane, seat_assignment_id, luggage_distribution_index, random_seat_deletion):
        #TODO automate seat_assignment using seat_assignment_id
        self.seat_assignment = Assignments.generate_full_row_block_assignment(plane, 6, 1, 1)
        if random_seat_deletion:
            adapted_seat_assignment = list(self.seat_assignment)
            for i in range(0, len(self.seat_assignment) - number_of_actors):
                index = random.randint(0, len(self.seat_assignment)-i-1)
                del adapted_seat_assignment[index]
            self.seat_assignment = adapted_seat_assignment
        self.actors = []
        self.plane = plane
        self.number_of_actors = number_of_actors
        self.luggage_distribution_index = luggage_distribution_index

        # fill actors[] with random actors
        luggage_distribution = self.get_luggage_distribution()
        for i in range(1, self.number_of_actors+1):
            actor = Actor(i, self.get_random_passenger(luggage_distribution[i-1]), self.seat_assignment[i-1], 0, plane)
            self.actors.append(actor)
        self.plane.actors = self.actors
        # simulation[] will contain all states observed during simulation (in order)
        self.simulation = list()

    """
    Passenger moving speed data is given in from of a triangular distribution (it was recoded for Short Haul airplanes):
        passing_one_row_seconds = [1.8, 2.4, 3.0] seconds per row - average row size around 2002 was 0.87m
        install_in_seat_seconds = [6.0, 9.0, 30.0] seconds
        exit_from_seat_into_aisle = [3.0, 3.6, 4.2] seconds
    Passenger luggage load is chosen by us, so we can have different set ups. 
    In the paper they had two options normal and high load. 
    """

    def get_luggage_distribution(self):
        load_distribution = [[0.6, 0.3, 0.1], [0.2, 0.6, 0.2]]
        total_number_of_pieces = 0
        maximum_luggage_capacity = self.plane.nr_compartments * self.plane.compartment_size * 2
        luggage_distribution = np.zeros(self.number_of_actors, dtype=int)
        count = 0
        j = 0
        for i in range(0, self.number_of_actors):
            if j < len(load_distribution[self.luggage_distribution_index]):
                if count < int(load_distribution[self.luggage_distribution_index][j] * self.number_of_actors):
                    luggage_distribution[i] = j
                    count += 1
                    total_number_of_pieces += j
                elif count == int(load_distribution[self.luggage_distribution_index][j] * self.number_of_actors):
                    count = 0
                    j += 1
                    total_number_of_pieces += j
                    luggage_distribution[i] = j
            else:
                luggage_distribution[i] = 0

        if total_number_of_pieces > maximum_luggage_capacity:
            raise ValueError('ERROR: The luggage distribution, number of passengers and plane specifications '
                             'will result in more hand luggage than available space in the compartments. '
                             'This is not allowed. The total number of pieces amounts to: ', total_number_of_pieces,
                             ' and the available space is: ', maximum_luggage_capacity)
        np.random.shuffle(luggage_distribution)
        return luggage_distribution




    @staticmethod
    def get_random_passenger(number_of_bags):
        # test data
        moving_speed = [Simulation.m_per_s_to_speed_unit(np.random.triangular(MINIMUM_MOVING_SPEED, MODE_MOVING_SPEED, MAXIMUM_MOVING_SPEED)), Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_ROW_ENTER_TIME, MODE_ROW_ENTER_TIME, MAXIMUM_ROW_ENTER_TIME)),
                        Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_EXIT_ROW_TIME, MODE_EXIT_ROW_TIME, MAXIMUM_EXIT_ROW_TIME))]
        storing_time = Simulation.sec_to_time_unit(np.random.triangular(MINIMUM_STORE_TIME, MODE_STORING_TIME, MAXIMUM_STORE_TIME))
        return Passenger_Type(number_of_bags, moving_speed, storing_time,  Simulation.meter_to_space_unit(PASSENGER_SIZE), Simulation.meter_to_space_unit(PASSENGER_PERSONAL_SPACE))

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
            for x in reversed(range(0, len(self.plane.aisle.occupance))):
                if self.plane.aisle.occupance[x] != prev_actor and self.plane.aisle.occupance[x] > 0:
                    acting_order.append(self.actors[self.plane.aisle.occupance[x]-1])
                    prev_actor = self.plane.aisle.occupance[x]
            # let the actors do their magic
            for a in acting_order:
                a.act()
            # try letting the next actor enter the plane
            if next_actor_in < len(self.actors) and self.actors[next_actor_in].act() != 1:
                next_actor_in += 1

            frame = (np.zeros((self.number_of_actors,4), dtype=int), np.zeros(self.plane.nr_compartments, dtype=int))
            for a in self.actors:
                frame[0][j, 0] = a.position
                frame[0][j, 1] = a.action
                frame[0][j, 2] = a.luggage
                frame[0][j, 3] = a.switching
                if a.action == 5:
                    actors_seated += 1
                j += 1
            n = 0
            for c in self.plane.compartments:
                frame[1][n] = c.free_space
                n += 1
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

