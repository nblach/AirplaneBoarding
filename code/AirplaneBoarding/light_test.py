import ctypes as c
from multiprocessing import Process, Array
from plane import Plane
from simulation import Simulation
import numpy as np

nr_of_actors = 180
load = 100
random_seat_deletion = 1
nr_of_methods_total = 2
size = (nr_of_methods_total, 1)



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


    data_light_test_total = Array(c.c_double, size[0] * size[1])
    data_light_test_individual = Array(c.c_double, size[0] * size[1])


    f = open("light_test_in.txt", "r+")
    lines = f.readlines()

    for i in range(0, size[0]):
        line = lines[i].split()
        for j in range(0,size[1]):

            processes.append(Process(target=simul, args=(data_light_test_total, data_light_test_individual, i, j, 2, line, 0)))


            processes[p_counter].start()
            p_counter += 1



    f.close()

    for p in processes:
        p.join()


    data_light_test_total = np.reshape(np.frombuffer((data_light_test_total.get_obj())), size)
    data_light_test_individual = np.reshape(np.frombuffer((data_light_test_individual.get_obj())), size)


    #np.savetxt('data_light_test_total.csv', data_light_test_total, delimiter=',')
    #np.savetxt('data_light_test_indicidual.csv', data_light_test_individual, delimiter=',')

    print('Total boarding time with random seat assignment : ', data_light_test_total[0][0], ' min')
    print('Average individual boarding time with random seat assignment:', data_light_test_individual[0][0], ' min')
    print('Boarding time with the Steffen method: ', data_light_test_total[1][0], ' min')
    print('Average individual boarding time with the Steffen method:', data_light_test_individual[1][0], ' min')
