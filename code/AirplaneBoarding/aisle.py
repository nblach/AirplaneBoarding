import numpy as np
import simulation


class Aisle:

    def __init__(self, plane, units_per_row, row_entry_size):
        self.plane = plane
        self.units_per_row = units_per_row
        self.row_entry_size = row_entry_size
        self.occupance = np.full(plane.length + simulation.PASSENGER_PERSONAL_SPACE, 0, dtype=int)

    """
    plane := ???????
    units_per_row := The length of a row in terms of our specified unit
    row_entry_size := The size of the entry to a row in terms of our unit 
    """