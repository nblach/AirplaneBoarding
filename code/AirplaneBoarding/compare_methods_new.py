from multiprocessing import Process, Array
import numpy as np
import measurements
import ctypes as c
from plane import Plane
from simulation import Simulation

cap_plane_1 = 125
cap_plane_2 = 180
nr_of_actors = [[cap_plane_1,cap_plane_2],[int(0.625 * cap_plane_1), int(0.625*cap_plane_2)]]
loads = [100, 70]
random_seat_deletion = 1
nr_of_methods_total = 4
size = (nr_of_methods_total, 5)



def simul(array_total_in, array_individual_in, i, j, plane_nr, line, load_id):
    np.random.seed() #required in order to obtain different seeds for different processes
    array_total = np.reshape(np.frombuffer(array_total_in.get_obj()), size)
    array_individual = np.reshape(np.frombuffer(array_individual_in.get_obj()), size)

    plane = Plane(plane_nr, 0,0,0,0,0,0,0)
    sim = Simulation(nr_of_actors[load_id][plane_nr-1], plane, loads[load_id], int(line[1]), int(line[2]), int(line[3]), int(line[4]), random_seat_deletion)
    sim.simulate()

    array_total[i][j] = sim.boarding_time_total
    print(sim.boarding_time_total)

    acc = 0
    for x in sim.actors:
        acc += x.personal_boarding_duration
    array_individual[i][j] = acc*(1/600)/nr_of_actors[load_id][plane_nr-1]


if __name__ == '__main__':
    processes = []
    p_counter = 0


    times_load_100_passengers_100_plane_1_total = Array(c.c_double, size[0]*size[1])
    times_load_70_passengers_625_plane_1_total= Array(c.c_double, size[0]*size[1])
    times_load_100_passengers_100_plane_2_total= Array(c.c_double, size[0]*size[1])
    times_load_70_passengers_625_plane_2_total= Array(c.c_double, size[0]*size[1])
    times_load_100_passengers_100_plane_1_individual = Array(c.c_double, size[0]*size[1])
    times_load_70_passengers_625_plane_1_individual= Array(c.c_double, size[0]*size[1])
    times_load_100_passengers_100_plane_2_individual= Array(c.c_double, size[0]*size[1])
    times_load_70_passengers_625_plane_2_individual= Array(c.c_double, size[0]*size[1])


    f = open("error_correction.txt", "r+")
    lines = f.readlines()

    for i in range(0, size[0]):
        line = lines[i].split()
        for j in range(0,size[1]):

            processes.append(Process(target=simul, args=(times_load_100_passengers_100_plane_1_total, times_load_100_passengers_100_plane_1_individual, i, j, 1, line, 0)))
            processes.append(Process(target=simul, args=(times_load_100_passengers_100_plane_2_total, times_load_100_passengers_100_plane_2_individual, i, j, 2, line, 0)))
            processes.append(Process(target=simul, args=(times_load_70_passengers_625_plane_1_total, times_load_70_passengers_625_plane_1_individual, i, j, 1, line, 1)))
            processes.append(Process(target=simul, args=(times_load_70_passengers_625_plane_2_total, times_load_70_passengers_625_plane_2_individual, i, j, 2, line, 1)))
            for p in range(p_counter, p_counter+1): #4
                processes[p].start()
            p_counter += 1#4



    f.close()

    for p in processes:
        p.join()


    times_load_100_passengers_100_plane_1_total = np.reshape(np.frombuffer((times_load_100_passengers_100_plane_1_total.get_obj())), size)
    times_load_70_passengers_625_plane_1_total = np.reshape(np.frombuffer((times_load_70_passengers_625_plane_1_total.get_obj())), size)
    times_load_100_passengers_100_plane_2_total = np.reshape(np.frombuffer((times_load_100_passengers_100_plane_2_total.get_obj())), size)
    times_load_70_passengers_625_plane_2_total = np.reshape(np.frombuffer((times_load_70_passengers_625_plane_2_total.get_obj())), size)
    times_load_100_passengers_100_plane_1_individual = np.reshape(np.frombuffer((times_load_100_passengers_100_plane_1_individual.get_obj())), size)
    times_load_70_passengers_625_plane_1_individual = np.reshape(np.frombuffer((times_load_70_passengers_625_plane_1_individual.get_obj())), size)
    times_load_100_passengers_100_plane_2_individual = np.reshape(np.frombuffer((times_load_100_passengers_100_plane_2_individual.get_obj())), size)
    times_load_70_passengers_625_plane_2_individual = np.reshape(np.frombuffer((times_load_70_passengers_625_plane_2_individual.get_obj())), size)


    np.savetxt('times_load_100_passengers_100_plane_1_total.csv', times_load_100_passengers_100_plane_1_total, delimiter=',')
    np.savetxt('times_load_70_passengers_625_plane_1_total.csv',times_load_70_passengers_625_plane_1_total , delimiter=',')
    np.savetxt('times_load_100_passengers_100_plane_2_total.csv', times_load_100_passengers_100_plane_2_total, delimiter=',')
    np.savetxt('times_load_70_passengers_625_plane_2_total.csv', times_load_70_passengers_625_plane_2_total, delimiter=',')
    np.savetxt('times_load_100_passengers_100_plane_1_individual.csv', times_load_100_passengers_100_plane_1_individual, delimiter=',')
    np.savetxt('times_load_70_passengers_625_plane_1_individual.csv', times_load_70_passengers_625_plane_1_individual, delimiter=',')
    np.savetxt('times_load_100_passengers_100_plane_2_individual.csv', times_load_100_passengers_100_plane_2_individual, delimiter=',')
    np.savetxt('times_load_70_passengers_625_plane_2_individual.csv', times_load_70_passengers_625_plane_2_individual, delimiter=',')
