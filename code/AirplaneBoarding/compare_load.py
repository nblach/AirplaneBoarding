from multiprocessing import Process, Array
import numpy as np
import measurements
import ctypes as c

size = (21,5)



def f(start, number, arr, x):

    temp_times = measurements.compare_by_load(start, number)
    times = np.frombuffer(arr.get_obj())
    times = np.reshape(times, size)

    for i in range(start, start+number):
        for j in range(0, 5):
            times[i][j] = temp_times[x][i][j]

if __name__ == '__main__':

    processes = []

    times_random = Array(c.c_double, 21 * 5)
    times_steffen = Array(c.c_double, 21 * 5)

    for i in range(0, 1):
        processes.append(Process(target=f, args=(i, 1, times_random, 0)))
        processes[i*2].start()
        processes.append(Process(target=f, args=(i, 1, times_steffen, 1)))
        processes[i*2+1].start()

    for p in processes:
        p.join()

    times_steffen = np.reshape(np.frombuffer((times_steffen.get_obj())), size)
    times_random = np.reshape(np.frombuffer((times_random.get_obj())), size)

    np.savetxt('loads_random.csv', times_random, delimiter=',')
    np.savetxt('loads_steffen.csv', times_steffen, delimiter=',')



