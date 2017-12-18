import json
from socket import *
from threading import Thread
from printwc import printwc
import time
def client_receive(s):
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
        printwc('yellow', "Received: {}\n".format(req_data))

        # Wait for new rpc request
        req_len_bin = s.recv(10)

def client_service(s):
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
            'method': 'start_simulation',
            'args': [500],
            'kwargs': {}
        },
    ]

    for mes in messages:
        print('Sent!')
        mes_json = json.dumps(mes)
        mes_length = len(mes_json)
        s.send('{:10d}'.format(mes_length).encode())
        s.send(mes_json.encode())
        time.sleep(1)

    time.sleep(15)


if __name__ == '__main__':
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', 20445))
    c_thread = Thread(target=client_service, args=(c,))
    r_thread = Thread(target=client_receive, args=(c,))
    c_thread.start()
    r_thread.start()
