from simulation import Simulation
from plane import Plane
from graphics import Animation

p = Plane(3, 3, 23, 0.9, 0.6, 3, 1.6)
sim = Simulation(120, p, 1, 0,1)
sim.simulate()
animation = Animation(sim)
animation.animate(4)
