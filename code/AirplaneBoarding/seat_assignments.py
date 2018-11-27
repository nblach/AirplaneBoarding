from seat import Seat
import numpy as np
from random import shuffle
from math import gcd
from math import ceil


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



    @staticmethod
    def generate_by_letter_assignment(plane, alternating, back_to_front):
        seats = np.empty(plane.rows*(plane.seatsRight + plane.seatsLeft), dtype = Seat)
        cols = list()
        for i in range(0, plane.seatsLeft + plane.seatsRight):
            new_col = np.empty(plane.rows, dtype = Seat)
            for j in range(0, plane.rows):
                new_col[j] = Seat(j, i)
            if not back_to_front:
                np.random.shuffle(new_col)
            cols.append(new_col)

        if alternating:
            #From window to aisle alternating
            if plane.seatsLeft > plane.seatsRight:
                #start from left
                side_1 = plane.seatsRight+plane.seatsLeft-1
                side_2 = 0
                side_1_inc = -1
                side_2_inc = 1
                side_1_limit = plane.seatsRight-1
                side_2_limit = plane.seatsRight
            else:
                side_1 = 0
                side_2 = plane.seatsRight+plane.seatsLeft-1
                side_1_inc = 1
                side_2_inc = -1
                side_1_limit = plane.seatsRight
                side_2_limit = plane.seatsRight-1


            index = 0
            for j in range(0, len(cols)):
                if j % 2 == 0:
                    if side_1 != side_1_limit:
                        col = cols[side_1]
                        side_1 += side_1_inc
                else:
                    if side_2 != side_2_limit:
                        col = cols[side_2]
                        side_2 += side_2_inc
                for i in range(0, plane.rows):
                    seats[index] = col[i]
                    index += 1
        else:
            #From A to ...
            index = 0
            for col in cols:
                for i in range(0, plane.rows):
                    seats[index] = col[i]
                    index += 1
        return seats


    @staticmethod
    def generate_steffen_assignment(plane):
        return Assignments.generate_by_seat_assignment(plane, 1, 1, 1)


    @staticmethod
    def generate_by_seat_assignment(plane, overall_alternate, letter_alternate, row_alternation):
        # overall alternate = True /False:   GO A... B... C... or A... F... B...
        # letter alternate = True / False    GO AAAAAA ..... or AFAFAF .....
        # row alternation integer


        row_alternation += 1
        seats = np.empty(plane.rows*(plane.seatsRight + plane.seatsLeft), dtype = Seat)

        index = 0
        for i in range(0, row_alternation):
            for j in range(0, plane.seatsLeft + plane.seatsRight):
                if overall_alternate:
                        if j % 2 == 1:
                            j = plane.seatsRight+plane.seatsLeft -1 - int(j/2)
                        else:
                            j = int(j/2)
                for k in range(0, ceil((plane.rows - i)/row_alternation)):
                    row = plane.rows-1-i-k*row_alternation

                    if letter_alternate:
                        if k % 2 == 0:
                            col = j
                        else:
                            col = plane.seatsRight+plane.seatsLeft -1 - j
                    else:
                        col = j

                    seats[index] = Seat(row,col)
                    index += 1


        return seats











