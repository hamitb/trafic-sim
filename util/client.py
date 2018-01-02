import json
from socket import *
from threading import Thread
from .printwc import printwc
import time

def client_receive_service(s, color='yellow'):
    # Receive the upcoming message's length as bytes object
    peer = s.getpeername()

    req_len_bin = s.recv(10)
    # Continue to receive as long as clients leaves or sends empty bytes as length
    while req_len_bin != b'':
        # Convert bytes representation of json length to integer
        req_len = int(req_len_bin)

        # Receive rpc request as json
        req = s.recv(req_len).decode()
        req_data = json.loads(req)

        # Handle rpc request
        printwc(color, "Message from {}: {}\n".format(peer, json.dumps(req_data, indent=4)))

        # Wait for new rpc request
        req_len_bin = s.recv(10)

def client_send_service(s, debug_level=['CarStat']):
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
            'args': [debug_level],
            'kwargs': {}
        },
        {
            'method': 'start_simulation',
            'args': [500],
            'kwargs': {}
        },

    ]

    for mes in messages:
        printwc('blue', '{}: Send method: {} with args:{} and kwargs:{}'.
              format(s.getsockname(), mes['method'], mes['args'], mes['kwargs']))
        mes_json = json.dumps(mes)
        mes_length = len(mes_json)
        s.send('{:10d}'.format(mes_length).encode())
        s.send(mes_json.encode())
        time.sleep(1)

    time.sleep(15)


if __name__ == '__main__':
    client_count = 3
    colors = ['yellow', 'blue', 'red']
    debug_levels = [['CarStat'], ['CarStat', 'EdgeStat'], ['CarEnterExist']]

    clients = [socket(AF_INET, SOCK_STREAM) for i in range(client_count)]
    for c in clients: c.connect(('127.0.0.1', 20445))

    send_threads = [Thread(target=client_send_service, args=(clients[i],debug_levels[i])) for i in range(len(clients))]
    receive_threads = [Thread(target=client_receive_service, args=(clients[i],colors[i])) for i in range(len(clients))]

    for t in send_threads: t.start()
    for t in receive_threads: t.start()
