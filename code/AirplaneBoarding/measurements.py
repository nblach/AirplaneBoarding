import numpy as np
from simulation import Simulation
from plane import Plane
import csv
#import graphics

def comparison_to_paper(start, number):

    load = 90
    number_of_actors = 138
    random_seat_deletion = 1

    nr_of_methods_total = 47
    nr_of_methods =  number #47
    offset = start

    labels = []
    times_total = np.zeros((nr_of_methods_total, 5), dtype=float)
    times_individual = np.zeros((nr_of_methods_total, 5), dtype=float)

    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    print(len(lines))

    for i in range(offset, nr_of_methods+offset):
        line = lines[i].split()
        print(line)
        labels.append(line[0])
        for j in range(0,5):
            plane = Plane(3, 0, 0, 0, 0, 0, 0, 0)
            sim = Simulation(number_of_actors, plane, load, int(line[1]), int(line[2]), int(line[3]), int(line[4]), random_seat_deletion)
            sim.simulate()
            times_total[i][j] = sim.boarding_time_total
            acc = 0
            for x in sim.actors:
               acc += x.personal_boarding_duration
            times_individual[i][j] = acc*(1/600)/number_of_actors

    f.close()
    return [times_total, times_individual]


def write_results_methods_test(times_total, times_individual, nr_of_methods, offset, filename):
    with open(filename, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Method', 'Boarding Time 1','Boarding Time 2', 'Boarding Time 3', 'Boarding Time 4', 'Boarding Time 5',  'Individual Time 1',  'Individual Time 2',  'Individual Time 3',  'Individual Time 4',  'Individual Time 5'])

        for i in range(0, nr_of_methods):
            i = i+offset
            output_writer.writerow([times_total[i][0], times_total[i][1], times_total[i][2], times_total[i][3], times_total[i][4], times_individual[i][0], times_individual[i][1], times_individual[i][2], times_individual[i][3], times_individual[i][4]])



def comparison_both(start, number, load, number_actors_1, number_actors_2):


    random_seat_deletion = 1

    nr_of_methods_total = 47
    nr_of_methods =  number #47
    offset = start

    labels = []
    times_total = [np.zeros((nr_of_methods_total, 5), dtype=float), np.zeros((nr_of_methods_total, 5), dtype=float)]
    times_individual = [np.zeros((nr_of_methods_total, 5), dtype=float), np.zeros((nr_of_methods_total, 5), dtype=float)]

    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    print(len(lines))

    for i in range(0, nr_of_methods):
        i = i+offset
        line = lines[i].split()
        print(line)
        labels.append(line[0])
        for j in range(0,5):
            plane_1 = Plane(1, 0, 0, 0, 0, 0, 0, 0)
            plane_2 = Plane(2, 0, 0, 0, 0, 0, 0, 0)
            sim_1 = Simulation(number_actors_1, plane_1, load, int(line[1]), int(line[2]), int(line[3]), int(line[4]), random_seat_deletion)
            sim_2 = Simulation(number_actors_2, plane_2, load, int(line[1]), int(line[2]), int(line[3]), int(line[4]), random_seat_deletion)
            sim_1.simulate()
            sim_2.simulate()


            times_total[0][i][j] = sim_1.boarding_time_total
            acc = 0
            for x in sim_1.actors:
               acc += x.personal_boarding_duration
            times_individual[0][i][j] = acc*(1/600)/number_actors_1

            times_total[1][i][j] = sim_2.boarding_time_total
            acc = 0
            for x in sim_2.actors:
               acc += x.personal_boarding_duration
            times_individual[1][i][j] = acc*(1/600)/number_actors_2

        f.close()
        return [times_total, times_individual]


def write_results_methods_both(times_total, times_individual, nr_of_methods, offset, filename_1, filename_2):
    with open(filename_1, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Method', 'Boarding Time 1','Boarding Time 2', 'Boarding Time 3', 'Boarding Time 4', 'Boarding Time 5',  'Individual Time 1',  'Individual Time 2',  'Individual Time 3',  'Individual Time 4',  'Individual Time 5'])

        for i in range(0, nr_of_methods):
            i = i+offset
            output_writer.writerow([times_total[0][i][0], times_total[0][i][1], times_total[0][i][2], times_total[0][i][3], times_total[0][i][4], times_individual[0][i][0], times_individual[0][i][1], times_individual[0][i][2], times_individual[0][i][3], times_individual[0][i][4]])



    with open(filename_2, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Method', 'Boarding Time 1','Boarding Time 2', 'Boarding Time 3', 'Boarding Time 4', 'Boarding Time 5',  'Individual Time 1',  'Individual Time 2',  'Individual Time 3',  'Individual Time 4',  'Individual Time 5'])

        for i in range(0, nr_of_methods):
            i = i+offset
            output_writer.writerow([times_total[1][i][0], times_total[1][i][1], times_total[1][i][2], times_total[1][i][3], times_total[1][i][4], times_individual[1][i][0], times_individual[1][i][1], times_individual[1][i][2], times_individual[1][i][3], times_individual[1][i][4]])



