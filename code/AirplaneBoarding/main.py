from simulation import Simulation
from plane import Plane
from graphics import Animation

plane = Plane(1, 0, 0, 0, 0, 0, 0, 0)
sim = Simulation(125, plane, 80, 7, 1, 0, 0, 1)
sim.simulate()
a = Animation(sim)
a.animate(10)







