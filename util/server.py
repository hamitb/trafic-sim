import json
from socket import *
from .printwc import printwc
from threading import Thread
from .controller import Controller

pairs = dict()
def set_controller(key, c):
    pairs[key] = {
        'c': c,
    }

def is_sim_active_for(key):
    return not (get_controller(key).sim.manual)

def get_controller(key):
    return pairs[key]['c']

def get_map_state_for(session_id):
    return get_controller(session_id).get_map_state()

def session_exist_with(key):
    return key in pairs

def rpc_call(req_string, session_id):
    printwc("green", "RPC Call from: {}".format(session_id))
    get_controller(session_id).execute_rpc(req_string)

def rpc_service(session_id, quick_start=False):
    '''
    parse_service listens for remote procedure call requests and handles requests
    coming from client in the form of binary json strings.
    :param s:
    :return:
    '''
    
    if not session_exist_with(session_id):
        # Controller(Map + Simulation) of this connection
        c = Controller(session_id=session_id)
        c.register_cb(notify_client)

        print("Add contoller to dict with session-id: {}".format(session_id))
        set_controller(session_id, c)

        if quick_start:
            print("Quick starting: setting maps and nodes")
            c.quick_start()
    

def register_socket(session_id, reply_channel):
    pairs[session_id]['s'] = reply_channel

def get_socket(session_id):
    return pairs[session_id]['s']

def notify_client(subj):
    data = subj.stats
    mes = {}
    debug_level = subj.debug_level

    try:
        reply_channel = get_socket(subj.session_id)
    except:
        reply_channel = None

    send_dl = []
    for dl in debug_level:
        current_dl = data[dl]
        if len(current_dl) != 0:
            mes[dl] = current_dl
            send_dl.append(dl)

    mes['clock'] = subj.clock

    if len(mes) != 0:
        mes_json = json.dumps(mes, indent=4)

        if reply_channel:
            reply_channel.send({
                "text": mes_json
            })
        else:
            printwc('red', "Error no socket found, no data send")

        printwc('green', 'Tick #{}, send stats: {}\n'.format(subj.clock, send_dl))



