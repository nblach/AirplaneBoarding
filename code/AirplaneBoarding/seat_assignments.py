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
                for j in range(0, len(i)):
                    seats[index] = i[j]
                    index -= 1
        elif sequence_index == 1:  # blocks in alternating, decreasing order
            # (first all odd index, then even index) (zero based)
            index = len(seats) - 1
            j = 1
            for i in blocks:
                if j % 2 == 1:
                    for k in range(0, len(i)):
                        seats[index] = i[k]
                        index -= 1
                j += 1

            j = 1
            for i in blocks:
                if j % 2 == 0:
                    for k in range(0, len(i)):
                        seats[index] = i[k]
                        index -= 1
                j += 1
        else:  # blocks in random order
            shuffle(blocks)
            index = 0
            for i in blocks:
                for k in range(0, len(i)):
                    seats[index] = i[k]
                    index += 1
        return seats

    @staticmethod
    def generate_half_row_block_assignment(plane, number_of_blocks_per_side, sequence_index, alternation):
        seats = np.empty(plane.rows * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        blocks_left = list()
        blocks_right = list()
        for i in range (0, number_of_blocks_per_side - 1):
            new_left_block =  np.empty(int(plane.rows / number_of_blocks_per_side) * plane.seatsLeft, dtype=Seat)
            new_right_block =  np.empty(int(plane.rows / number_of_blocks_per_side) * plane.seatsRight, dtype=Seat)
            for j in range(0, int(plane.rows / number_of_blocks_per_side)):
                for k in range(0, plane.seatsLeft):
                    new_left_block[j * plane.seatsLeft + k] = Seat(i * int(plane.rows / number_of_blocks_per_side) + j, k)
                for k in range(0, plane.seatsRight):
                    new_right_block[j*plane.seatsRight + k] = Seat(i * int(plane.rows / number_of_blocks_per_side) + j, k+plane.seatsLeft)
            np.random.shuffle(new_right_block)
            np.random.shuffle(new_left_block)
            blocks_left.append(new_left_block)
            blocks_right.append(new_right_block)
        new_left_block = np.empty((plane.rows - (number_of_blocks_per_side - 1) * int(plane.rows / number_of_blocks_per_side)) * plane.seatsLeft, dtype=Seat)
        new_right_block = np.empty((plane.rows - (number_of_blocks_per_side - 1) * int(plane.rows / number_of_blocks_per_side)) * plane.seatsRight, dtype=Seat)
        for j in range(0, (plane.rows - (number_of_blocks_per_side - 1) * int(plane.rows / number_of_blocks_per_side))):
            for k in range(0, plane.seatsLeft):
                new_left_block[j*plane.seatsLeft + k] = Seat((number_of_blocks_per_side - 1) * int(plane.rows / number_of_blocks_per_side) + j, k)
            for k in range(0, plane.seatsRight):
                new_right_block[j*plane.seatsRight + k] = Seat((number_of_blocks_per_side - 1) * int(plane.rows / number_of_blocks_per_side) + j, k+plane.seatsLeft)
        np.random.shuffle(new_left_block)
        np.random.shuffle(new_right_block)
        blocks_left.append(new_left_block)
        blocks_right.append(new_right_block)

        if sequence_index == 0:
            # Descending order first right side then left side
            index = len(seats) - 1
            for i in blocks_left:
                for j in range(0, len(i)):
                    seats[index] = i[j]
                    index -= 1
            for i in blocks_right:
                for j in range(0, len(i)):
                    seats[index] = i[j]
                    index -= 1
        elif sequence_index == 1:
            index = len(seats) - 1
            for i in range(0, alternation):
                j = 1
                for k in blocks_left:
                    if j % alternation == i:
                        for m in range(0, len(k)):
                            seats[index] = k[m]
                            index -= 1
                    j += 1
            for i in range(0, alternation):
                j = 1
                for k in blocks_right:
                    if j % alternation == i:
                        for m in range(0, len(k)):
                            seats[index] = k[m]
                            index -= 1
                    j += 1

        else:
            index = 0
            for n in range(0, 2):
                side = n
                for i, j in zip(reversed(blocks_right), reversed(blocks_left)):
                    if side:
                        for k in range(0, len(j)):
                            seats[index] = j[k]
                            index += 1
                    else:
                        for k in range(0, len(i)):
                            seats[index] = i[k]
                            index += 1
        for a in seats:
            print(a.row_number, '  ', a.col_numbner)
        return seats

    @staticmethod
    def generate_by_row_assignment(plane, alternation):
        seats = np.empty(plane.rows * (plane.seatsRight + plane.seatsLeft), dtype=Seat)
        rows = list()
        for i in range(0, plane.rows):
            new_row = np.empty((plane.seatsRight + plane.seatsLeft), dtype=Seat)
            for j in range(0, plane.seatsRight + plane.seatsLeft):
                new_row[j] = Seat(i, j)
            np.random.shuffle(new_row)
            rows.append(new_row)
        index = len(seats) - 1
        for i in range(0, alternation):
            j = 1
            for k in rows:
                if j % alternation == i:
                    for m in range(0, plane.seatsRight + plane.seatsLeft):
                        seats[index] = k[m]
                        index -= 1
                j += 1
        return seats
