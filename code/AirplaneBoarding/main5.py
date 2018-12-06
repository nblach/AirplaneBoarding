from simulation import Simulation
from plane import Plane
#from graphics import Animation
import measurements
import threading
import numpy as np

class MyThread(threading.Thread):
    def __init__(self, id, array_total, array_individual):
        threading.Thread.__init__(self)
        self.id = id
        self.array_total = array_total
        self.array_individual = array_individual

    def run(self):
        result = measurements.comparison_to_paper(self.id, 1)
        for j in range(0,5):
            self.array_total[self.id][j] = result[0][self.id][j]
            self.array_individual[self.id][j] = result[1][self.id][j]





nr_of_methods_total = 47
nr_of_methods = 7
offset = 40
filename = 'output_methods_oldplane_5.txt'

result = []
result = measurements.comparison_to_paper(offset, nr_of_methods)

measurements.write_results_methods_test(result[0], result[1], nr_of_methods, offset, filename)









