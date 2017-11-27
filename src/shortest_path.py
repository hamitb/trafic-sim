from map import *

a_map = Map()
a_map.add_node(0, 0, 5)
a_map.add_node(1, 0, 0)
a_map.add_node(2, 3, 0)
a_map.add_node(3, 15, 5)

a_map.add_road(0, 1)
a_map.add_road(0, 3)
a_map.add_road(1, 2)
a_map.add_road(3, 2)

a_map.get_shortest_path(1, 0)