from simulation import Simulation
from plane import Plane
from graphics import Animation

p = Plane(4, 3, 30, 0.8, 0.5, 3, 1.6)
sim = Simulation(100, p, 1, 0)
sim.simulate()
animation = Animation(sim)
animation.animate(4)
