from seat import Seat
import numpy as np
from random import shuffle


class Assignments:

    @staticmethod
    def generate_random_assignment(plane):
        seats = np.empty(plane.rows * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        for i in range(0, plane.rows):
            for j in range(0, plane.seatsRight + plane.seatsLeft):
                seats[i * (plane.seatsRight + plane.seatsLeft) + j] = Seat(i, j)
        np.random.shuffle(seats)
        return seats

    @staticmethod
    def generate_full_row_block_assignment(plane, number_of_blocks, sequence_index):
        seats = np.empty(plane.rows * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        blocks = list()
        for i in range(0, number_of_blocks-1):
            new_block = np.empty(int(plane.rows/number_of_blocks) * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
            for j in range(0, int(plane.rows/number_of_blocks)):
                for k in range(0, plane.seatsRight + plane.seatsLeft):
                    new_block[j * (plane.seatsRight + plane.seatsLeft) + k] = \
                        Seat(i*int(plane.rows/number_of_blocks)+j, k)
            np.random.shuffle(new_block)
            blocks.append(new_block)
        new_block = np.empty((plane.rows-(number_of_blocks-1)*int(plane.rows / number_of_blocks)) *
                             (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        for j in range(0, (plane.rows-(number_of_blocks-1)*int(plane.rows / number_of_blocks))):
            for k in range(0, plane.seatsRight + plane.seatsLeft):
                new_block[j * (plane.seatsRight + plane.seatsLeft) + k] = \
                    Seat((number_of_blocks-1)*int(plane.rows / number_of_blocks) + j, k)
        np.random.shuffle(new_block)
        blocks.append(new_block)
        if sequence_index == 0:  # blocks in decreasing order
            index = len(seats)-1
            for i in blocks:
                for j in np.nditer(i, ['refs_ok']):
                    seats[index] = j
                    index -= 1
        elif sequence_index == 1:  # blocks in alternating, decreasing order (first all even index, then odd index)
            index = len(seats) - 1
            j = 0
            for i in blocks:
                if j % 2 == 1:
                    for k in np.nditer(i):
                        seats[index] = k
                        index -= 1
                j += 1

            j = 0
            for i in blocks:
                if j % 2 == 0:
                    for k in np.nditer(i):
                        seats[index] = k
                        index -= 1
                j += 1
        else:  # blocks in random order
            shuffle(blocks)
            index = 0
            for i in blocks:
                for k in np.nditer(i):
                    seats[index] = k
                    index += 1
        return seats
