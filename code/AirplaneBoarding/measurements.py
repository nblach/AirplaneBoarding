import numpy as np
from simulation import Simulation
from plane import Plane
import csv

def comparison_to_paper():

    plane = Plane(3, 0, 0, 0, 0, 0, 0, 0)
    load = 100#TODO
    number_of_actors = 138
    luggage_distribution_index = 1 #TODO
    random_seat_deletion = 1

    nr_of_methods =  13 #48

    labels = []
    times_total = np.zeros((48, 5), dtype=float)
    times_individual = np.zeros((48, 5), dtype=float)

    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    print(len(lines))

    for i in range(0, nr_of_methods):
        i = i+36
        line = lines[i].split()
        print(line)
        labels.append(line[0])
        for j in range(0,5):
            sim = Simulation(number_of_actors, plane, load, line[1], line[2], line[3], line[4], random_seat_deletion)
            sim.simulate()
            times_total[i][j] = sim.boarding_time_total
            acc = 0
            for x in sim.actors:
               acc += x.personal_boarding_duration
            times_individual[i][j] = acc*(1/600)/number_of_actors


    with open('output_test_methods.csv', mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Method', 'Boarding Time 1','Boarding Time 2', 'Boarding Time 3', 'Boarding Time 4', 'Boarding Time 5',  'Individual Time 1',  'Individual Time 2',  'Individual Time 3',  'Individual Time 4',  'Individual Time 5'])

        for i in range(0, nr_of_methods):
            i = i+36
            output_writer.writerow([times_total[i][0], times_total[i][1], times_total[i][2], times_total[i][3], times_total[i][4], times_individual[i][0], times_individual[i][1], times_individual[i][2], times_individual[i][3], times_individual[i][4]])











    f.close()
