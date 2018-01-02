import threading
import time
import numpy as np
from .rsegment import *
from .observer import Observed
from .printwc import  printwc
 
class Generator(object):
    def __init__(self, gen_id, _map, period, number, source_list, target_list, sim, lock):
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
        self.clock_thread = threading.Thread(target=self.set_clock, name="{}_clock_thread".format(self.gen_id))
        self.gen_thread = threading.Thread(target=self.generate, name="{}_thread".format(self.gen_id))
        self.completed = False
        self.terminated = False
        self.lock = lock

    def get_start_end_nodes(self):
        start_node = np.random.choice(self.source_list)
        end_node = np.random.choice(self.target_list)

        return start_node, end_node

    def start_threads(self):
        self.clock_thread.start()
        self.gen_thread.start()

    def get_tick(self):
        self.tick_on.set()
        if not self.clock_thread.isAlive():
            self.sim.check()

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

            if self.terminated:
                # printwc('blue_bg',"{} Terminated!".format(self.gen_id))
                self.sim.check()
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
                    self.sim.check()
                    # printwc('blue_bg',"{} Done!\n".format(self.gen_id))
                    break

            if not self.gen_on.isSet() or not self.gen_thread.isAlive():
                self.sim.check()

            self.tick_on.clear()

        
    def generate(self):
        for _ in range(self.number):
            if self.gen_on.wait():
                if self.terminated:
                    return
                self.insert_new_vehicle()

                if not self.tick_on.isSet():
                    self.sim.check()

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

        with self.lock:
            rsegment_path = self.sim.edge_to_rsegment(edge_path)

        vhcl_id = "{}_vhcl{}".format(self.gen_id, self.created_vehicle_count)
        vhcl = Vehicle(rsegment_path, vhcl_id, self.sim.k_speed)
        # printwc('blue_bg', "{}: New vehicle created!\n".format(vhcl_id))
        self.created_vehicle_count += 1
        self.vehicles.append(vhcl)

class Simulation(Observed):
    def __init__(self, k_speed=60.0):
        '''
        Creates an empty simulation
        '''
        self.map = None
        self.sim_on = threading.Event()
        self.notif_on = threading.Event()
        self.generators = []
        self.k_speed = k_speed
        self.next_gen_id = 0
        self.rsegments = dict()
        self.clock = 0
        self.completed = False
        self.terminated = False
        self.sub_comps_terminated = False
        self.manual = True
        self.final_notif_send = False
        self.lock = threading.Lock()
        self.check_lock = threading.Lock()
        self.comp_count = 0
        self.finished_comp_count = 0
        self.stats = []

        self.sim_thread = threading.Thread(target=self._simulation_thread, name="sim_thread" ,args=[])
        self.notif_thread = threading.Thread(target=self._notification_thread, name="notif_thread")

        self.set_debug_level(['CarStat'])
        super().__init__()

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
        new_generator = Generator(gen_id, self.map, period, number, source_list, target_list, self, self.lock)
        self.generators.append(new_generator)
        self.next_gen_id += 1

        self._update_comp_count()
        
    def get_generators(self):
        '''
        get a list of generators and their parameters 
        '''
        gens = [gen.describe() for gen in self.generators]
        return gens

    def del_generator(self, index):
        ''' 
        delete the generator in the given order of
        insertion (getGenerators() list order)
        '''
        del self.generators[index]

        self._update_comp_count()

    def check(self):
        with self.check_lock:
            self.finished_comp_count += 1
            if self.comp_count == self.finished_comp_count:
                self.finished_comp_count = 0
                self.send_notification()

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
            # printwc('green_bg' ,"Simulation Started !")
            self.tickperiod = tickperiod
            
            self.sim_thread.start()
            self.notif_thread.start()
        else:
            self.tick()        

    def check_sim_completed(self):
        sim_completed = True
        for gen in self.generators:
            sim_completed = sim_completed and gen.completed
        
        self.completed = sim_completed
        return sim_completed

    def send_notification(self):
        if not self.final_notif_send:
            self.notif_on.set()

    def _notification_thread(self):
        while self.notif_on.wait():
            if self.terminated:
                break
            self.stats = self.get_stats()
            self.notify(self.socket)
            self.notif_on.clear()

    def _simulation_thread(self):
        while 1:
            time.sleep(self.tickperiod * 1e-3)

            self.check_sim_completed()

            if self.terminated:
                if not self.sub_comps_terminated:
                    for gen in self.generators:
                        if not gen.completed:
                            gen.terminate()
                            gen.get_tick()
                    for _, rsegment in self.rsegments.items():
                        rsegment.complete_segment()
                        rsegment.get_tick()
                    self.sub_comps_terminated = True
                    self.manual = True
                self.send_notification()
                break

            if not self.completed:
                self.tick()
            else:
                self.reset_simulation()
                break

        printwc('red', "Simulation terminated !")
        return

    def tick(self):
        '''
        Explicit advance of simulation. tick() signal is
        generated (methods are called) for each generator and
        simulation component.
        '''
        # printwc('green_bg', "Tick #{}".format(self.clock))
        # print()
        if self.completed:
            return

        for gen in self.generators:
            gen.get_tick()

        for key, rsegment in self.rsegments.items():
            rsegment.get_tick()

        if self.manual:
            self.stats = self.get_stats()
            self.notify(self.socket)

        if not self.completed:
            for gen in self.generators:
                if gen.thread_status() is False and not gen.completed:
                    gen.start_threads()

        self.clock += 1

    def set_socket(self, socket):
        self.socket = socket

    def edge_to_rsegment(self, path):
        rsegment_path = []
        for edge in path:
            start_id = edge.start_node.node_id
            end_id = edge.end_node.node_id
            key = (start_id, end_id)
            try:
                rsegment_path.append(self.rsegments[key])
            except KeyError:
                new_rs = Rsegment(edge, self)
                self.rsegments[key] = new_rs
                rsegment_path.append(new_rs)

        # Update component count
        self._update_comp_count()

        return rsegment_path

    def _update_comp_count(self):
        self.comp_count = len(self.rsegments) + len(self.generators)

    def terminate(self):
        '''
        End the simulation.
        '''
        self.terminated = True
        if not self.manual:
            self.sim_thread.join()
            self.send_notification()
            self.notif_thread.join()
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
            if gen_thread.isAlive():
                gen_thread.join()
            if gen_clock.isAlive():
                gen_clock.join()

    def stop_rsegment_threads(self):
        for _, rsegment in self.rsegments.items():
            segment_thread = rsegment.segment_thread
            rsegment.terminate_segment()
            rsegment.get_tick()
            if segment_thread.isAlive():
                segment_thread.join()

    def reset_simulation(self):
        self.sim_on.clear()
        self.notif_on.clear()
        self.rsegments = dict()
        self.clock = 0
        self.completed = False
        self.terminated = False
        self.sub_comps_terminated = False
        self.final_notif_send = False
        self.manual = True  
        self.sim_thread = threading.Thread(target=self._simulation_thread, name="sim_thread" ,args=[])
        self.notif_thread = threading.Thread(target=self._notification_thread, name="notif_thread")
        for gen in self.generators:
            gen.reset_gen()

    def get_all_vhcls(self):
        vhcls = []
        for gen in self.generators:
            vhcls += gen.vehicles

        return vhcls

    def get_all_rsegments(self):
        return [rs for (k, rs) in self.rsegments.items()]

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level+['SimReport']

    def wait(self):
        '''
        Wait for the end of simulation. If manual tick it returns
        if simulation is over.
        '''
        if self.manual:
            return self.completed

        self.sim_thread.join()
        self.notif_thread.join()
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
        stats = {
            'CarStat': [],
            'CarEnterExist': [],
            'CarStartFinish': [],
            'EdgeStat': [],
            'SimStat': {},
            'SimReport': {},
        }
        for key, rs in self.rsegments.items():
            rs_stats = rs.get_stats()
            stats['CarStat'] += rs_stats['CarStat']
            stats['CarEnterExist'] += rs_stats['CarEnterExist']
            stats['CarStartFinish'] += rs_stats['CarStartFinish']
            stats['EdgeStat'].append(rs_stats['EdgeStat'])

        vehicles = self.get_all_vhcls()
        active_vhcls = [v for v in vehicles if not v.finish_path]
        finished_vhcls = [v for v in vehicles if v.finish_path]


        avg_speed_active = 0
        avg_speed_finished = 0

        if active_vhcls != []:
            speeds = [v.speed for v in active_vhcls]
            avg_speed_active = sum(speeds) / len(speeds)

        if finished_vhcls != []:
            speeds = [v.speed for v in finished_vhcls]
            avg_speed_finished = sum(speeds) / len(speeds)

        active_vhcls_count = len(active_vhcls)
        remaining_vhcls_count = sum([g.number-g.created_vehicle_count for g in self.generators])
        finished_vhcls_count = len(finished_vhcls)

        stats['SimStat']['active_vhcl_count'] = active_vhcls_count
        stats['SimStat']['finished_vhcl_count'] = finished_vhcls_count
        stats['SimStat']['remaining_vhcl_count'] = remaining_vhcls_count
        stats['SimStat']['avg_speed_active'] = avg_speed_active
        stats['SimStat']['avg_speed_finished'] = avg_speed_finished

        completed = active_vhcls_count == 0 and remaining_vhcls_count == 0

        if completed or self.terminated:
            vehicle_stats = [v.stats for v in vehicles]
            rsegment_stats = [rs.stats for rs in self.get_all_rsegments()]
            sim_stats = stats['SimStat']

            stats['SimReport']['vehicles'] = vehicle_stats
            stats['SimReport']['rsegments'] = rsegment_stats
            stats['SimReport']['simulation'] = sim_stats
            self.final_notif_send = True
        return stats
