from aisle import Aisle
from compartment import Compartment
import numpy as np

class Plane:

    def __init__(self, seats_left, seats_right, rows, length_of_row, row_entry_size, compartment_size, compartment_length, actors):

        self.seatsLeft = seats_left
        self.seatsRight = seats_right
        self.seat_occupance = np.full((rows, seats_left + seats_right), 0, dtype=int)
        self.rows = rows
        self.aisle = Aisle(self, length_of_row, row_entry_size)
        self.compartments = []
        self.length = rows * length_of_row
        self.compartment_length = compartment_length
        self.actors = actors

        # initialize compartments
        self.nr_compartments = self.length/compartment_length
        for i in range(0, self.nr_compartments):
            self.compartments[i] = Compartment(compartment_size*2, i*compartment_size, (i+1)*compartment_size)

    def get_start_of_row(self, row_number):
        return row_number * self.length_of_row

    def get_compartment_at_pos(self, position):
        return self.compartments[math.floor(position/self.compartment_length)]
