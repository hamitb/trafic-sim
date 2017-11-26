from map import *
from rsegment import *


a_map = Map()
a_map.add_node(1, 3, 5)
a_map.add_node(2, 4, 7)
a_map.add_node(3, 6, 5)

a_map.add_road(1, 2, 2)
a_map.add_road(3, 1, 1)
a_map.add_road(2, 3, 1, bidir=True)


segment_1=Rsegment(3.5 , 4 , a_map.children[1][2] )

first_vehicle=Vehicle(segment_1)
second_vehicle=Vehicle(segment_1)



print ( "Rsegment count =>"+str(segment_1.get_vehicles_count()) )
print("Rsegment_length , nlanes , ( start_node, end_node  ) =>"+ str(segment_1.get_info()) )
print("is segment full ? =>"+ str(segment_1.full()) )

print(" (capactity , avg_speed , vehicle_count) =>  " + str( segment_1.get_stats() ) )


print("is first_vehicle is part of segment =>"+str (segment_1==first_vehicle.Rsegment) )

