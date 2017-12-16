import json
from socket import *
from threading import Thread
import time


def client_service(s):
    mes = {
        'obj_id': 'map', 'method': 'add_node',
        'args': [5, 4],
        'kwargs': {'node_id': 10}
    }
    mes_json = json.dumps(mes)
    mes_length = len(mes_json)
    s.send('{:10d}'.format(mes_length).encode())
    s.send(mes_json.encode())

    time.sleep(3)

if __name__ == '__main__':
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', 20445))
    c_thread = Thread(target=client_service, args=(c,))
    c_thread.start()
