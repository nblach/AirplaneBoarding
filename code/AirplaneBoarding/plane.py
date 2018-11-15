from aisle import Aisle
from compartment import Compartment

class Plane:

    def __init__(self, seats_left, seats_right, rows, length_of_row, row_entry_size, compartment_size, compartment_length):

        self.seatsLeft = seats_left
        self.seatsRight = seats_right
        self.rows = rows
        self.aisle = Aisle(self, length_of_row, row_entry_size)
        self.compartments = []
        self.length = rows * length_of_row

        # initialize compartments
        self.nr_compartments = self.length/compartment_length
        for i in range(0, self.nr_compartments):
            self.compartments[i] = Compartment(compartment_size*2, i*compartment_size, (i+1)*compartment_size)


