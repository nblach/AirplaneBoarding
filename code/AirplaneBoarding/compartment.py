# a compartment object stands for the compartments on one level at both sides of the aisle


class Compartment:
    def __init__(self, size, start, end):
        self.size = size
        self.start = start
        self.end = end
        self.free_space = size


