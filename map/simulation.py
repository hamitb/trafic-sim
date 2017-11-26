import threading
import time
import secrets
from map import *
from rsegment import *
 
class Generator(object):
    def __init__(self, _map, period, number, source_list, target_list):
        self.map = _map
        self.period = period
        self.number = number
        self.created_vehicle_count = 0
        self.clock = 0
        self.source_list = source_list
        self.target_list = target_list
        self.gen_on = threading.Event()
        self.tick_on = threading.Event()
        self.clock_thread = threading.Thread(target=self.set_clock)
        self.gen_thread = threading.Thread(target=self.generate)

        self.clock_thread.start()
        self.gen_thread.start()
    
    def get_start_end_nodes(self):
        start_node = secrets.choice(self.source_list)
        end_node = secrets.choice(self.target_list)

        return start_node, end_node

    def gen_tick(self):
        self.tick_on.set()
    
    def set_clock(self):
        while self.tick_on.wait():
            print("clock: {}".format(self.clock))
            self.clock += 1
            self.tick_on.clear()
            if self.clock % self.period == 0:
                self.gen_on.set()
        
    def generate(self):
        for i in range(self.number):
            if self.gen_on.wait():
                self.insert_new_vehicle()
                self.gen_on.clear()
        
        print("generated all")
        return

    def describe(self):
        return {
                'period': self.period, 
                'number': self.number, 
                'sources': self.source_list, 
                'targets': self.target_list,
               }
            
    def insert_new_vehicle(self):
        start_node, end_node = self.get_start_end_nodes()
        path = Map().get_shortest_path(1, 2)
        vhcl = Vehicle
        print("New car created at {}, {}".format(start_node, end_node))
        self.created_vehicle_count += 1

class Simulation(object):
    def __init__(self):
        '''
        Creates an empty simulation
        '''
        self.map = None
        self.sim_on = threading.Event()
        self.sim_thread = None
        self.generators = []
    def set_map(self, map_object):
        '''
        set Map object as the map for the simulation
        '''
        self.map = map_object
    def add_generator(self, source_list, target_list, period, number):
        ''' 
        Add a traffic generator. Generator generates a vehicle
        once in the given period. After generating number
        vehicles it stops generating
        '''
        new_generator = Generator(self.map, period, number, source_list, target_list)
        self.generators.append(new_generator)
        
    def get_generators(self):
        '''
        get a list of generators and their parameters 
        '''
        gens = [gen.describe() for gen in self.generators]
        return gens

    def del_generator(self, num):
        ''' 
        delete the generator in the given order of
        insertion (getGenerators() list order)
        '''
        for i in range(num):
            del self.generators[0]
    def start_simulation(self, tickperiod = 0):
        '''
        Start the simulation with each tick of clock lasts
        tickperiod milliseconds. A thread sends tick() signal to
        all generators and edges to advance simulation once in
        tickperiod milliseconds. If tickperiod is 0, tick() is
        explicit. The program/user calls Simulation.tick()
        that advances simulation clock explicitly.
        '''
        if tickperiod:
            self.sim_on.set()
            print("Simulation Started !")
            self.sim_thread = threading.Thread(target=self._simulation_thread, args=[tickperiod])
            self.sim_thread.start()
        else:
            self.tick()         

    def _simulation_thread(self, tickperiod):
        while self.sim_on.wait():
            time.sleep(tickperiod * 1e-3)
            self.tick() 
        print("Simulation terminated")

    def tick(self):
        '''
        Explicit advance of simulation. tick() signal is
        generated (methods are called) for each generator and
        simulation component.
        '''
        print("Tick!")
        for gen in self.generators:
            gen.get_tick()
        print("All generators informed")
            
    def terminate(self):
        '''
        End the simulation.
        '''
        self.sim_on.clear()
            
    def wait(self):
        '''
        Wait for the end of simulation. If manual tick it returns
        if simulation is over.
        '''
    def get_stats(self):
        '''
        Get simulation statistics. Total number of vehicles,
        number of vehicles completed, number of vehicles
        currently on map, average speed, maximum vehicles per
        road segment, current vehicles per road segment, average
        speed per segment. Road segment statistics need not to be
        complete in phase 1.
        '''

# s = Simulation()
# s.start_simulation(0)

# print("Something else happens here")

# time.sleep(5)
# s.terminate()

# g = Generator(None, 2, 3, [1,2,3], [3,4,5])
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)
# g.gen_tick()
# time.sleep(0.5)

