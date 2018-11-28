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
    def generate_full_row_block_assignment(plane, number_of_blocks, sequence_index, alternation):
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
            index = 0
            for start in reversed(range(len(blocks)-1-alternation, len(blocks))):
                i = start
                while i >= 0:
                    for k in range(0, len(blocks[i])):
                        seats[index] = blocks[i][k]
                        index += 1
                    i -= (alternation + 1)
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











