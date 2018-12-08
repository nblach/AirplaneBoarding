import ctypes as c
from multiprocessing import Process, Array
from plane import Plane
from simulation import Simulation
import numpy as np

nr_of_actors = 138
load = 90
random_seat_deletion = 1
nr_of_methods_total = 2#49
size = (nr_of_methods_total, 5)



def simul(array_total_in, array_individual_in, i, j, plane_nr, line, load_id):
    np.random.seed() #required in order to obtain different seeds for different processes
    array_total = np.reshape(np.frombuffer(array_total_in.get_obj()), size)
    array_individual = np.reshape(np.frombuffer(array_individual_in.get_obj()), size)

    plane = Plane(plane_nr, 0,0,0,0,0,0,0)
    sim = Simulation(nr_of_actors, plane, load, int(line[1]), int(line[2]), int(line[3]), int(line[4]), random_seat_deletion)
    sim.simulate()

    array_total[i][j] = sim.boarding_time_total

    acc = 0
    for x in sim.actors:
        acc += x.personal_boarding_duration
    array_individual[i][j] = acc*(1/600)/nr_of_actors


if __name__ == '__main__':
    processes = []
    p_counter = 0


    times_load_90_passengers_100_plane_3_total = Array(c.c_double, size[0]*size[1])
    times_load_90_passengers_100_plane_3_individual = Array(c.c_double, size[0]*size[1])


    f = open("mix_method.txt", "r+")  #change@!!!!!!!!!!!!!
    lines = f.readlines()

    for i in range(0, size[0]):
        line = lines[i].split()
        for j in range(0,size[1]):

            processes.append(Process(target=simul, args=(times_load_90_passengers_100_plane_3_total, times_load_90_passengers_100_plane_3_individual, i, j, 3, line, 0)))


            processes[p_counter].start()
            p_counter += 1



    f.close()

    for p in processes:
        p.join()


    times_load_90_passengers_100_plane_3_total = np.reshape(np.frombuffer((times_load_90_passengers_100_plane_3_total.get_obj())), size)
    times_load_90_passengers_100_plane_3_individual = np.reshape(np.frombuffer((times_load_90_passengers_100_plane_3_individual.get_obj())), size)


    np.savetxt('times_load_90_passengers_100_plane_3_total.csv', times_load_90_passengers_100_plane_3_total, delimiter=',')
    np.savetxt('times_load_90_passengers_100_plane_3_individual.csv', times_load_90_passengers_100_plane_3_individual, delimiter=',')
