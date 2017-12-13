from simulation import *
from map import *
import time

points = { 
1 : (6.4145, 112.0495), 2 : (35.2796, 110.9804), 3 : (50.7812, 167.9088), 4 : (51.0485, 228.3117), 
5 : (40.6250, 260.9186), 6 : (21.6488, 274.8166), 7 : (75.9045, 220.8282), 8 : (75.9045, 198.1103), 
9 : (75.9045, 251.0296), 10 : (62.2738, 164.4343), 11 : (76.7064, 149.7345), 12 : (54.7903, 110.1786), 
13 : (144.8601, 104.8332), 14 : (140.0492, 156.6835), 15 : (125.8839, 167.3743), 16 : (105.5715, 168.1761), 
17 : (94.6134, 162.5634), 18 : (149.4037, 213.6119), 19 : (174.0455, 223.4780), 20 : (182.8124, 232.5881), 
21 : (200.9867, 228.0445), 22 : (94.8807, 211.2065), 23 : (91.9407, 198.3776), 24 : (108.5114, 237.1316), 
25 : (116.5295, 244.6152), 26 : (121.3404, 261.1859), 27 : (131.2293, 255.8405), 28 : (128.8239, 229.6481), 
29 : (127.4876, 199.4466), 30 : (127.2203, 176.7287), 31 : (144.5928, 251.8314), 32 : (144.0583, 220.5609), 
33 : (170.5180, 216.0173), 34 : (100.7306, 236.2403), 35 : (93.8326, 221.7827), 36 : (86.4621, 222.2552), 
37 : (84.3832, 228.7753), 38 : (85.8951, 242.6659), 39 : (93.4546, 245.9732), 40 : (95.4152, 278.8257), 
41 : (108.3778, 276.6875), 42 : (111.0505, 268.4022), 43 : (75.3700, 233.5235), 44 : (96.2170, 192.3640), 
45 : (95.1480, 171.5170), 46 : (4.4012, 290.1460), 47 : (9.4494, 255.4226), 48 : (10.5833, 220.6488), 
49 : (41.1994, 168.1101), 50 : (4.5357, 227.0744), 51 : (284.6161, 253.9107), 52 : (224.8958, 241.0595), 
53 : (173.4911, 173.0238), 54 : (155.7262, 104.2322), 55 : (155.7262, 91.7589), 56 : (243.4167, 205.9077), 
57 : (221.4941, 209.6875), 58 : (207.5089, 162.8185), 59 : (244.1726, 143.5417), 60 : (223.7619, 100.8304),
61 : (323.7619, 100.8304), 62 : (123.7619, 100.8304)
}

# edges for one way road segments. direction is from first to second point
diredges = [(19, 18),(18, 33),(33, 19), (7, 4), (3, 10), (2, 3), (11, 12), (38, 39),(35, 36)] 

# edges for two way road segments. There is one lane per direction. 
# simply represented as to edges. ie. (52,57) implies (57,52) 
bidirsinglelane = [(52, 57), (8, 23), (37, 43), (5, 6), (8, 9), (34, 35),
(22, 23), (16, 24), (6, 47), (24, 42), (54, 55), (16, 17), (25, 26),
(58, 59), (44, 45), (31, 32), (15, 30), (14, 18), (8, 10), (56, 57),
(28, 29), (24, 34), (4, 5), (23, 44), (17, 45), (47, 48), (24, 25),
(36, 37), (34, 39), (53, 58), (18, 32), (29, 30), (41, 42), (27, 31),
(7, 22), (37, 38), (19, 20), (22, 35), (40, 41), (11, 17), (26, 27),
(48, 49), (27, 28), (57, 58), (20, 21), (10, 11), (3, 49), (3, 4),
(48, 50), (6, 46)]


# edges for two way road segments. There are two lanes per direction. 
# corressponds to a wider roads
bidir2lane = [ (1, 2), (2, 12), (12, 13), (13, 54), (54, 60),
   (54, 53), (53, 21),  (21, 52), (52, 51), (13, 14), (14, 15), (15, 16) ]

# points with only one edge connects. They are like dead ends, or source/sink nodes
endpoints = [ 51, 56, 59, 60, 1, 55, 9, 40, 46, 50 ]

## MAP TESTS
print("## MAP TESTS ##")

# Create map
print("## Create map ##")

a_map = Map()

# Add nodes
print("## Add nodes ##")

for node_id, point in points.items():
    a_map.add_node(node_id, point[0], point[1])

# Add directed edges with single lane
print("## Add directed edges with single lane ##")

for diredge in diredges:
    a_map.add_road(diredge[0], diredge[1])

# Add bidir edges with single lane
print("## Add bidir edges with single lane ##")

for bidiredge in bidirsinglelane:
    a_map.add_road(bidiredge[0], bidiredge[1], bidir=True)

# Add bidir edges with 2 lanes
print("## Add bidir edges with 2 lanes ##")

for bidir2 in bidir2lane:
    a_map.add_road(bidir2[0], bidir2[1], nlanes=2, bidir=True)

# Delete nodes
print("## Delete nodes ##")

a_map.delete_node(61)
a_map.delete_node(62)

# Delete edges
print("## Delete edges ##")

a_map.delete_road(12, 13, bidir=True)

# Shortest path
print("## Shortest path ##")

path = a_map.get_shortest_path(8, 44)
print([(edge.start_node.node_id, edge.end_node.node_id) for edge in path])

## DB TESTS
print("## DB TESTS ##")
time.sleep(1)
print("## INSPECT THE 'map.db' file created at the root folder of project with sqlite ##")
time.sleep(1)
print("## <INFO> ##")
print("## To not insert same data with exact same id's which would violate the unique contsraints, ##")
print("## if you get any errors caused by unique constraints delete the 'map.db' file  ##")
print("## The new 'map.db' file automatically will be created each time the tests run ##")
print("## </INFO> ##")
time.sleep(3)
# Save map to db
print("## Save map to db ##")

try:
    a_map.save_map("Happy Map")
except:
    pass

# # Create new map
print("## Create new map ##")

another_map = Map()

# Load "Happy Map" that we created before from db
print("## Load 'Happy Map' that we created before from db ##")

another_map.load_map("Happy Map")

# Save this map as a new map to db
print("## Save this map as a new map to db ##")

try:
    another_map.save_map("Funny Map")
except:
    pass


## Simulation tests
print("## SIMULATION TESTS ##")

# Create simulation
print("## Create simulation ##")

s = Simulation()

# Set map
print("## Set map ##")

s.set_map(a_map)

# Add generators
print("## Add generators ##")

s.add_generator(range(60), range(60), 3, 10)
s.add_generator(range(60), range(60), 5, 5)

# Get generators
# print("## Get generators ##")

print (s.get_generators())

# Start simulation
print("## Start simulation ##")

s.start_simulation(1000)
time.sleep(10)

# Terminate simulation
print("## Terminate simulation ##")

# Total number of vehicles
print("## Total number of vehicles ##")
print(s.get_stats())

s.terminate()

# Proceed with ticks
for _ in range(10):
    s.tick()
    time.sleep(1)