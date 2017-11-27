from simulation import *
from map import *

m = Map()
s = Simulation()
s.add_generator([1,2,3], [3,4,5], 2, 1)
s.start_simulation(500)