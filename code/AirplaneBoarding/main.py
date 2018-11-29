from simulation import Simulation
from plane import Plane
from graphics import Animation

p = Plane(4, 3, 20, 0.9, 0.6, 3, 1.6)
sim = Simulation(140, p, 1, 0,0)
sim.simulate()
animation = Animation(sim)
animation.animate(20)
