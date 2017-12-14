import threading
import time
import numpy as np
from map import *
from rsegment import *
 
class Generator(object):
    def __init__(self, gen_id, _map, period, number, source_list, target_list, sim):
        self.map = _map
        self.gen_id = "gen{}".format(gen_id)
        self.vehicles = []
        self.sim = sim
        self.period = period
        self.number = number
        self.created_vehicle_count = 0
        self.clock = 0
        self.source_list = source_list
        self.target_list = target_list
        self.gen_on = threading.Event()
        self.tick_on = threading.Event()
        self.clock_thread = threading.Thread(target=self.set_clock, name="gen_clock_thread")
        self.gen_thread = threading.Thread(target=self.generate, name="gen_thread")
        self.completed = False
        self.terminated = False

    def get_start_end_nodes(self):
        start_node = np.random.choice(self.source_list)
        end_node = np.random.choice(self.target_list)

        return start_node, end_node

    def start_threads(self):
        self.clock_thread.start()
        self.gen_thread.start()

    def get_tick(self):
        self.tick_on.set()

    def reset_gen(self):
        self.vehicles = []
        self.created_vehicle_count = 0
        self.clock = 0
        self.gen_on.clear()
        self.tick_on.clear()
        self.completed = False
        self.terminated = False
        self.clock_thread = threading.Thread(target=self.set_clock, name="gen_clock_thread")
        self.gen_thread = threading.Thread(target=self.generate, name="gen_thread")
    
    def terminate(self):
        self.terminated = True

    def thread_status(self):
        return self.clock_thread.isAlive()
    
    def set_clock(self):
        while self.tick_on.wait():
            self.clock += 1
            self.tick_on.clear()

            if self.terminated:
                print("{} Terminated!".format(self.gen_id))
                self.gen_on.set()
                break
            
            if self.clock % self.period == 0:
                self.gen_on.set()

            if len(self.vehicles) > 0 and self.created_vehicle_count == self.number:
                is_completed = True
                for vehicle in self.vehicles:
                    is_completed = is_completed and vehicle.finish_path

                self.completed = is_completed
                
                if self.completed:
                    print('\x1b[5;37;44m' + \
                    "{} Done!\n".format(self.gen_id)+ \
                    '\x1b[0m')
                    break
            
        
    def generate(self):
        for _ in range(self.number):
            if self.gen_on.wait():
                if self.terminated:
                    return
                self.insert_new_vehicle()
                self.gen_on.clear()
        return

    def describe(self):
        return {
                'period': self.period, 
                'number': self.number, 
                'sources': self.source_list, 
                'targets': self.target_list,
               }
            
    def insert_new_vehicle(self):
        edge_path = []
        while edge_path == [] or edge_path == None:
            start_node, end_node = self.get_start_end_nodes()
            edge_path = self.map.get_shortest_path(start_node, end_node)
        
        rsegment_path = self.sim.edge_to_rsegment(edge_path)
        vhcl_id = "{}_vhcl{}".format(self.gen_id, self.created_vehicle_count)
        vhcl = Vehicle(rsegment_path, vhcl_id)
        print('\x1b[6;37;44m' + \
              "{}: New vehicle created!\n".format(vhcl_id)\
              + '\x1b[0m')
        self.created_vehicle_count += 1
        self.vehicles.append(vhcl)

class Simulation(object):
    def __init__(self):
        '''
        Creates an empty simulation
        '''
        self.map = None
        self.sim_on = threading.Event()
        self.sim_thread = None
        self.generators = []
        self.next_gen_id = 0
        self.rsegments = dict()
        self.clock = 0
        self.completed = False
        self.terminated = False
        self.sub_comps_terminated = False
        self.manual = True
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
        gen_id = self.next_gen_id
        new_generator = Generator(gen_id, self.map, period, number, source_list, target_list, self)
        self.generators.append(new_generator)
        self.next_gen_id += 1
        
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
        if not self.completed:
            for gen in self.generators:
                if gen.thread_status() is False and not gen.completed:
                    gen.start_threads()
        
        self.terminated = False
        if tickperiod:
            self.manual = False
            self.sim_on.set()
            print('\x1b[5;30;42m' + \
                  "Simulation Started !" +\
                  '\x1b[0m')
            self.sim_thread = threading.Thread(target=self._simulation_thread, name="sim_thread" ,args=[tickperiod])
            self.sim_thread.start()
        else:
            self.tick()        

    def sim_completed(self):
        sim_completed = True
        for gen in self.generators:
            sim_completed = sim_completed and gen.completed
        
        self.completed = sim_completed
        return sim_completed

    def _simulation_thread(self, tickperiod):
        while self.sim_on.wait():
            # print("active threads ", threading.active_count())
            time.sleep(tickperiod * 1e-3)
            
            if self.sim_completed() or self.terminated:
                self.sim_on.clear()
                if not self.sub_comps_terminated:
                    for gen in self.generators:
                        if not gen.completed:
                            gen.terminate()
                            gen.get_tick()
                    for _,rsegment in self.rsegments.items():
                        rsegment.complete_segment()
                        rsegment.get_tick()
                    self.sub_comps_terminated = True
                    self.manual = True
                break

            self.tick()
        
        print('\x1b[5;30;41m' + \
              "Simulation terminated !" +\
              '\x1b[0m')
        return

    def edge_to_rsegment(self, path):
        rsegments = []
        for edge in path:
            x1, y1 = edge.start_node.x, edge.start_node.y 
            x2, y2 = edge.end_node.x, edge.end_node.y
            key = (x1, y1, x2, y2)
            if key in self.rsegments:
                existing_rs = self.rsegments[key]
                rsegments.append(existing_rs)
            else:
                new_rs = Rsegment(edge)
                self.rsegments[key] = new_rs
                rsegments.append(new_rs)
        return rsegments

    def tick(self):
        '''
        Explicit advance of simulation. tick() signal is
        generated (methods are called) for each generator and
        simulation component.
        '''
        if not self.completed:
            for gen in self.generators:
                if gen.thread_status() is False and not gen.completed:
                    gen.start_threads()

        if self.sim_completed() or self.terminated:
            if not self.sub_comps_terminated:
                for gen in self.generators:
                    if not gen.completed:
                        gen.terminate()
                for _,rsegment in self.rsegments.items():
                    rsegment.complete_segment()

        print('\x1b[6;30;42m' + "Tick #{}\n".format(self.clock) + '\x1b[0m')
        # print("Tick #{}".format(self.clock))
        self.clock += 1

        for gen in self.generators:
            gen.get_tick()
        for _,rsegment in self.rsegments.items():
            rsegment.get_tick()
            
    def terminate(self):
        '''
        End the simulation.
        '''
        self.terminated = True
        if not self.manual:
            self.sim_thread.join()
        else:
            self.stop_gen_threads()
            self.stop_rsegment_threads()
        self.reset_simulation()
    
    def stop_gen_threads(self):
        for gen in self.generators:
            gen_thread = gen.gen_thread
            gen_clock = gen.clock_thread
            gen.terminate()
            gen.get_tick()
            gen_thread.join()
            gen_clock.join()

    def stop_rsegment_threads(self):
        for _, rsegment in self.rsegments.items():
            segment_thread = rsegment.segment_thread
            rsegment.terminate_segment()
            rsegment.get_tick()
            segment_thread.join()

    def reset_simulation(self):
        self.sim_on.clear()
        self.rsegments = dict()
        self.clock = 0
        self.completed = False
        self.terminated = False
        self.sub_comps_terminated = False
        self.manual = True  
        for gen in self.generators:
            gen.reset_gen()
    
    def wait(self):
        '''
        Wait for the end of simulation. If manual tick it returns
        if simulation is over.
        '''
        if self.manual:
            return self.completed

        self.sim_thread.join()
        return

    def get_stats(self):
        '''
        Get simulation statistics. Total number of vehicles,
        number of vehicles completed, number of vehicles
        currently on map, average speed, maximum vehicles per
        road segment, current vehicles per road segment, average
        speed per segment. Road segment statistics need not to be
        complete in phase 1.
        '''
        total_num_of_vhcls = sum([len(gen.vehicles) for gen in self.generators])
        return total_num_of_vhcls