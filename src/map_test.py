from map import *

a_map = Map()
a_map.add_node(1, 3, 5)
a_map.add_node(2, 4, 7)
a_map.add_node(3, 6, 5)

a_map.add_road(1, 2, 2)
a_map.add_road(3, 1, 1)
a_map.add_road(2, 3, 1, bidir=True)

print(a_map.get_shortest_path(1, 3))