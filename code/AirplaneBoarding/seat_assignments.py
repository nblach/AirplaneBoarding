from seat import Seat
import numpy as np
class Assignments:

    @staticmethod
    def generate_assignment(plane, number_of_actors, seat_assignment_id):
        if seat_assignment_id == 1:
            return Assignments.generate_random_assignment(plane)

    @staticmethod
    def generate_random_assignment(plane):
        seats = np.empty(plane.rows * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        for i in range(0, plane.rows):
            for j in range(0, plane.seatsRight + plane.seatsLeft):
                seats[i * (plane.seatsRight + plane.seatsLeft) + j] = Seat(i,j)
        np.random.shuffle(seats)
        return seats

