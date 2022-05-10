from simulation import Simulation
from plane import Plane
from graphics import Animation

plane = Plane(2, 0, 0, 0, 0, 0, 0, 0)
sim = Simulation(160, plane, 100, 7, 1, 0, 0, 1)
sim.simulate()
a = Animation(sim)
a.animate(20)







