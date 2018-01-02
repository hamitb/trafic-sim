import json
from socket import *
from .printwc import printwc
from threading import Thread
from .controller import Controller

pairs = dict()

def rpc_call(req_string, reply_channel):
    print("calling execute method")
    pairs[reply_channel.name].execute_rpc(req_string)

def rpc_service(reply_channel, quick_start=False):
    '''
    parse_service listens for remote procedure call requests and handles requests
    coming from client in the form of binary json strings.
    :param s:
    :return:
    '''

    # Controller(Map + Simulation) of this connection
    c = Controller(reply_channel)
    c_methods = c.methods
    c.register_cb(notify_client)

    print("Add reply channel to dict")
    pairs[reply_channel.name] = c

    if quick_start:
        c.quick_start()
    # while req_len_bin != b'':
    #     # Convert bytes representation of json length to integer
    #     req_len = int(req_len_bin)
    #
    #     # Receive rpc request as json
    #     req = s.recv(req_len).decode()
    #     req_data = json.loads(req)
    #
    #     # Handle rpc request
    #     m_name = req_data['method']
    #     args = req_data['args']
    #     kwargs = req_data['kwargs']
    #
    #     printwc('yellow', "{} calls: {} with args:{} and kwargs:{}\n".format(peer, m_name, args, kwargs))
    #
    #     # Call requested method
    #     f = c_methods[m_name]
    #     f(*args, **kwargs)
    #
    #     # Wait for new rpc request
    #     req_len_bin = s.recv(10)

def notify_client(reply_channel, subj):
    data = subj.stats
    mes = dict()
    debug_level = subj.debug_level

    send_dl = []
    for dl in debug_level:
        current_dl = data[dl]
        if len(current_dl) != 0:
            mes[dl] = current_dl
            send_dl.append(dl)

    if len(mes) != 0:
        mes_json = json.dumps(mes)
        reply_channel.send({
            "text": mes_json
        })
        printwc('green', 'Tick #{}, send stats: {}\n'.format(subj.clock, send_dl))



