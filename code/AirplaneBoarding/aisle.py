class Aisle:

    def __init__(self, plane, units_per_row, row_entry_size):
        self.plane = plane
        self.units_per_row = units_per_row
        self.row_entry_size = row_entry_size
        self.occupance = []
        for i in range(0, plane.length):
            self.occupance.append(0)

    """
    plane := ???????
    units_per_row := The length of a row in terms of our specified unit
    row_entry_size := The size of the entry to a row in terms of our unit 
    """