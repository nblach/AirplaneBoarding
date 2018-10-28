class Aisle:

    def __init__(self, plane, units_per_row, row_entry_size):
        self.plane = plane
        self.units_per_row = units_per_row
        self.row_entry_size = row_entry_size
        self.occupance = []
        for i in range(0, plane.length):
            self.occupance[i] = 0;
