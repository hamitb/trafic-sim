from simulation import *
from map import *
import threading

a_map = Map()
a_map.add_node(0, 0, 5)
a_map.add_node(1, 0, 0)
a_map.add_node(2, 3, 0)
a_map.add_node(3, 15, 5)

a_map.add_road(0, 1)
a_map.add_road(0, 3)
a_map.add_road(1, 2)
a_map.add_road(3, 2)

s = Simulation()
s.set_map(a_map)
s.add_generator([0], [1], 2, 2)
