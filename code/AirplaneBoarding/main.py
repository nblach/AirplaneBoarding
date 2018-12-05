from simulation import Simulation
from plane import Plane
from graphics import Animation

sim = Simulation(110, Plane(1, 0, 0, 0, 0, 0, 0, 0), 1, 0,1)
sim.simulate()
animation = Animation(sim)
animation.animate(5)
