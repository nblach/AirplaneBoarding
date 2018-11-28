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
            for i in blocks_right:
                for j in range(0, len(i)):
                    seats[index] = i[j]
                    index -= 1
            for i in blocks_left:
                for j in range(0, len(i)):
                    seats[index] = i[j]
                    index -= 1
        elif sequence_index == 1:
            index = 0
            for start in reversed(range(len(blocks_left)-1-alternation, len(blocks_left))):
                i = start
                while i >= 0:
                    for k in range(0, len(blocks_left[i])):
                        seats[index] = blocks_left[i][k]
                        index += 1
                    i -= (alternation + 1)
            for start in reversed(range(len(blocks_right)-1-alternation, len(blocks_right))):
                i = start
                while i >= 0:
                    for k in range(0, len(blocks_right[i])):
                        seats[index] = blocks_right[i][k]
                        index += 1
                    i -= (alternation + 1)

        else:
            index = 0
            i = len(blocks_left)-1
            j = len(blocks_right)-2
            while i >= 0 or j >= 0:
                if i >= 0:
                    for k in range(0, len(blocks_left[i])):
                        seats[index] = blocks_left[i][k]
                        index += 1
                    i -= 2
                if j >= 0:
                    for k in range(0, len(blocks_right[j])):
                        seats[index] = blocks_right[j][k]
                        index += 1
                    j -= 2
            i = len(blocks_left) - 2
            j = len(blocks_right) - 1
            while i >= 0 or j >= 0:
                if j >= 0:
                    for k in range(0, len(blocks_right[j])):
                        seats[index] = blocks_right[j][k]
                        index += 1
                    j -= 2
                if i >= 0:
                    for k in range(0, len(blocks_left[i])):
                        seats[index] = blocks_left[i][k]
                        index += 1
                    i -= 2
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
        index = 0
        for start in reversed(range(len(rows)-1-alternation, len(rows))):
            i = start
            while i >= 0:
                for k in range(0, len(rows[i])):
                    seats[index] = rows[i][k]
                    index += 1
                i -= (alternation + 1)
        return seats



    @staticmethod
    def generate_by_letter_assignment(plane, alternating, back_to_front):
        seats = np.empty(plane.rows*(plane.seatsRight + plane.seatsLeft), dtype = Seat)
        cols = list()
        for i in range(0, plane.seatsLeft + plane.seatsRight):
            new_col = np.empty(plane.rows, dtype = int)
            for j in range(0, plane.rows):
                new_col[plane.rows-j-1] = j
            if not back_to_front:
                np.random.shuffle(new_col)
            cols.append(new_col)



        index = 0
        for j in range(0, len(cols)):
            if alternating:
                if j%2 == 0:
                    j = int(j/2)
                else:
                    j = plane.seatsLeft + plane.seatsRight - 1 - int(j/2)
            for i in range(0, plane.rows):
                seats[index] = Seat(cols[j][i], j)
                index += 1
        return seats


    @staticmethod
    def generate_steffen_assignment(plane):

        return Assignments.generate_by_seat_assignment(plane, 1, 1, 1)

    @staticmethod
    def generate_by_half_row_assignment(plane, row_alternation, alternate_sides):
        row_alternation += 1
        seats = np.empty(plane.rows*(plane.seatsRight + plane.seatsLeft), dtype = Seat)

        index = 0
        seats_on_side = plane.seatsLeft
        for h in range(0, 2):
            for i in range(0, row_alternation):
                for j in range(0, ceil((plane.rows - i)/row_alternation)):
                    if alternate_sides:
                        h_temp = (h+j)%2
                    if h_temp == 0:
                        seats_on_side = plane.seatsLeft
                    else:
                        seats_on_side = plane.seatsRight
                    half_row = np.empty(seats_on_side, dtype = int)
                    for k in range(0, seats_on_side):
                        half_row[k] = k+h_temp*plane.seatsLeft
                    np.random.shuffle(half_row)
                    for k in range(0, seats_on_side):
                        seats[index] = Seat(plane.rows-1 - (i+j*row_alternation),half_row[k])
                        index += 1



        return seats



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











