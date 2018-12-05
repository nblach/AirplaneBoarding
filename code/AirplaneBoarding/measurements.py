import numpy as np
from simulation import Simulation
from plane import Plane

def comparison_to_paper():

    plane = Plane(3, 0, 0, 0, 0, 0, 0, 0)
    load = #TODO
    number_of_actors = 138
    luggage_distribution_index = 1 #TODO
    random_seat_deletion = 1


    labels = []
    times_total = np.array((47, 5), dtype=float)
    times_individual = np.array((47, 5), dtype=float)

    f = open("test_methods.txt", "r+")
    lines = f.readlines()

    for i in range(0, 48):
        ind = i*5
        labels.append(lines[ind])
        for j in range(0,5):
            sim = Simulation(number_of_actors, plane, luggage_distribution_index, lines[ind+1], lines[ind +2], lines[ind+3], lines[ind+4], random_seat_deletion)
            sim.simulate()
            times_total[i, j] = sim.boarding_time_total
            acc = 0
            for x in sim.actors:
               acc += x.personal_boarding_duration
            times_individual[i,j] = acc*(1/600)/number_of_actors











    f.close()
