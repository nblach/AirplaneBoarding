from aisle import Aisle
import math
from compartment import Compartment
from simulation import Simulation
import numpy as np

class Plane:

    def __init__(self, id):
        if id == 0:
            return self.bombardier_cs_100()
        elif id == 1:
            return self.airbus_a_320_200()
        else:
            return self.plane_from_paper()

    def __init__(self, id, seats_left, seats_right, rows, length_of_row, row_entry_size, compartment_size, compartment_length):

        if id == 1:
            # Bombardier CS100
            seats_left = 2
            seats_right = 3
            rows = 25
            length_of_row = 0.787
            row_entry_size = (2/5) * 0.787
            compartment_size = 3
            compartment_length = 1.35
        elif id == 2:
            # Airbus A320-200
            seats_left = 3
            seats_right = 3
            rows = 30
            length_of_row = 0.787
            row_entry_size = (2/5) * 0.787
            compartment_size = 5
            compartment_length = 2.2
        elif id == 3:
            # Plane from paper
            seats_left = 3
            seats_right = 3
            rows = 23
            length_of_row = 0.813
            row_entry_size = (2/5) * 0.813
            compartment_size = 3
            compartment_length = 1.35

        #else create custom plane
        row_entry_size = Simulation.meter_to_space_unit(row_entry_size)
        length_of_row = Simulation.meter_to_space_unit(length_of_row)
        compartment_length = Simulation.meter_to_space_unit(compartment_length)
        self.seatsLeft = seats_left
        self.seatsRight = seats_right
        self.seat_occupance = np.full((rows, seats_left + seats_right), 0, dtype=int)
        self.rows = rows
        self.length = rows * length_of_row
        self.aisle = Aisle(self, length_of_row, row_entry_size)
        self.compartments = []
        self.compartment_length = compartment_length
        self.actors = None
        self.length_of_row = length_of_row
        self.compartment_size = compartment_size

        # initialize compartments
        self.nr_compartments = math.ceil(self.length/compartment_length)
        for i in range(0, self.nr_compartments):
            self.compartments.append(Compartment(compartment_size*2, i*compartment_length, min(self.length -1, (i+1)*compartment_length)))

    def get_start_of_row(self, row_number):
        return row_number * self.length_of_row

    def get_compartment_at_pos(self, position):
        return self.compartments[int(position/self.compartment_length)]




