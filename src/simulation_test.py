from simulation import *
from map import *
import time

a_map = Map()
a_map.load_map("Happy Map")
print("## SIMULATION TESTS ##")

# Create simulation
print("## Create simulation ##")

s = Simulation()

# Set map
print("## Set map ##")

s.set_map(a_map)

# Add generators
print("## Add generators ##")

s.add_generator(range(60), range(60), 2, 10)
s.add_generator(range(60), range(60), 3, 5)

print("## Start simulation ##")

s.start_simulation(200)
s.wait()