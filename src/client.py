import json
from socket import *
from threading import Thread
import time


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


if __name__ == '__main__':
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', 20445))
    c_thread = Thread(target=client_service, args=(c,))
    c_thread.start()
