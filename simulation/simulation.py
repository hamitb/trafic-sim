import threading
import time
class Simulation(object):
    def __init__(self):
        '''
        Creates an empty simulation
        '''
        self.map = None
        self.sim_on = threading.Event()
        self.sim_thread = None
    def set_map(self, map_object):
        '''
        set Map object as the map for the simulation
        '''
        self.map = map_object
    def add_generator(self, sourcelist, targetlist, period, number):
        ''' 
        Add a traffic generator. Generator generates a vehicle
        once in the given period. After generating number
        vehicles it stops generating
        '''
    def get_generators(self):
        '''
        get a list of generators and their parameters 
        '''
    def del_generator(self, num):
        ''' 
        delete the generator in the given order of
        insertion (getGenerators() list order)
        '''
    def start_simulation(self, tickperiod = 0):
        '''
        Start the simulation with each tick of clock lasts
        tickperiod milliseconds. A thread sends tick() signal to
        all generators and edges to advance simulation once in
        tickperiod milliseconds. If tickperiod is 0, tick() is
        explicit. The program/user calls Simulation.tick()
        that advances simulation clock explicitly.
        '''
        self.sim_on.set()
        print("Simulation Started !")
        self.sim_thread = threading.Thread(target=self.simulation_thread, args=[tickperiod])
        self.sim_thread.start()
        print("Threads are started")

    def simulation_thread(self, tickperiod):
        while self.sim_on.wait(tickperiod*1e-3 + 0.5):
            time.sleep(tickperiod * 1e-3)
            print("Tick!")
            self.tick() 
        print("Termination")
    def tick(self):
        '''
        Explicit advance of simulation. tick() signal is
        generated (methods are called) for each generator and
        simulation component.
        '''
        print("Generators informed values updated")
            
    def terminate(self):
        '''
        End the simulation.
        '''
        self.sim_on.clear()
        self.sim_thread.join()
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

s = Simulation()
s.start_simulation(2000)

print("Something else happens here")

time.sleep(5)
s.terminate()
# def tick(event):
#     """
#     wait for two seconds, then make 'event' fire
#     """
#     print("tick signal send, waiting 2 seconds!")
#     time.sleep(2)
#     event.set()

# def progress(event):
#     while event.wait(timeout=None):
#         print("Tick!!")
#         event.clear()

# stop_event = threading.Event()
# t1 = threading.Thread(target=tick, args=[stop_event])
# t2 = threading.Thread(target=progress, args=[stop_event])

# while True:
#     t1.start()
#     t1.join()
#     t2.start()
#     t2.join()