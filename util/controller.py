from .simulation import *
from .map import Map
from .printwc import printwc
import json

class Controller(object):
    def __init__(self, socket):
        self.map = Map()
        self.sim = Simulation()
        self.sim.set_map(self.map)
        self.sim.set_socket(socket)
        self.socket = socket
        self.methods = {
            # Add map methods
            'add_node': self.map.add_node,
            'delete_node': self.map.delete_node,
            'add_road': self.map.add_road,
            'delete_road': self.map.delete_road,
            'save_map': self.map.save_map,
            'load_map': self.map.load_map,
            #Add simulation methods
            'add_generator': self.sim.add_generator,
            'get_generators': self.sim.get_generators,
            'del_generators': self.sim.del_generator,
            'start_simulation': self.sim.start_simulation,
            'tick': self.sim.tick,
            'wait': self.sim.wait,
            'get_stats': self.sim.get_stats,
            'set_debug_level': self.sim.set_debug_level,
        }

    def register_cb(self, f):
        self.sim.register(f)

    def execute_rpc(self, req):
        mes = json.loads(req)

        m_name = mes['method']
        args = mes['args']
        kwargs = mes['kwargs']

        printwc('yellow', "{} called: {} with args:{} and kwargs:{}\n".format(self.socket.name, m_name, args, kwargs))

        # Call requested method
        f = self.methods[m_name]
        f(*args, **kwargs)

    def quick_start(self):
        messages = [
            {
                'method': 'load_map',
                'args': ["RemoteMap"],
                'kwargs': {}
            },
            {
                'method': 'add_generator',
                'args': [list(range(1,6)), list(range(1,6)), 2, 10],
                'kwargs': {}
            },
            {
                'method': 'add_generator',
                'args': [list(range(1,6)), list(range(1,6)), 3, 5],
                'kwargs': {}
            },
            {
                'method': 'set_debug_level',
                'args': [['CarStat']],
                'kwargs': {}
            },
        ]

        for mes in messages:
            m_name = mes['method']
            args = mes['args']
            kwargs = mes['kwargs']

            printwc('yellow', "{} called: {} with args:{} and kwargs:{}\n".format(self.socket.name, m_name, args, kwargs))

            # Call requested method
            f = self.methods[m_name]
            f(*args, **kwargs)
