from multiprocessing import Process, Array
import numpy as np
import measurements
import ctypes as c

size = (21,5)



def f(start, number, times_random_in, times_steffen_in, x):

    temp_times = measurements.compare_by_load(start, number)
    times_random_local = np.frombuffer(times_random_in.get_obj())
    times_random_local = np.reshape(times_random_local, size)
    times_steffen_local = np.frombuffer(times_steffen_in.get_obj())
    times_steffen_local = np.reshape(times_steffen_local, size)

    for i in range(start, start+number):
        for j in range(0, 5):
            times_random_local[i][j] = temp_times[0][i][j]
            times_steffen_local[i][j] = temp_times[1][i][j]

if __name__ == '__main__':

    processes = []

    times_random = Array(c.c_double, 21 * 5)
    times_steffen = Array(c.c_double, 21 * 5)

    for i in range(0, 21):
        processes.append(Process(target=f, args=(i, 1, times_random, times_steffen, 0)))
        processes[i].start()

    for p in processes:
        p.join()

    times_steffen = np.reshape(np.frombuffer((times_steffen.get_obj())), size)
    times_random = np.reshape(np.frombuffer((times_random.get_obj())), size)

    np.savetxt('loads_random.csv', times_random, delimiter=',')
    np.savetxt('loads_steffen.csv', times_steffen, delimiter=',')



