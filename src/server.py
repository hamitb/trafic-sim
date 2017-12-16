import json
from socket import *
from threading import Thread


def rpc_service(s):
    '''
    parse_service listens for remote procedure call requests and handles requests
    coming from client in the form of binary json strings.
    :param s:
    :return:
    '''

    # Receive upcoming messages length as bytes object
    req_len_bin = s.recv(10)
    peer= s.getpeername()

    # Continue to receive as long as clients leaves or sends empty bytes as length
    while req_len_bin != b'':
        # Convert bytes representation of json length to integer
        req_len = int(req_len_bin)

        # Receive rpc request as json
        req = s.recv(req_len).decode()
        req_data = json.loads(req)

        # Handle rpc request
        rpc_handler(req_data)

        # Wait for new rpc request
        req_len_bin = s.recv(10)

    print("{} leaves".format(peer))


def rpc_handler(req_data):

    '''
    Given rpc request data coming from client, rpc_handler executes the given method with
    given parameters.
    :param req_data:
    :return:
    '''
    obj_id = req_data['obj_id']
    method = req_data['method']
    args = req_data['args']
    kwargs = req_data['kwargs']

    print("Server executes: {}.{} with args:{} and kwargs:{}".format(obj_id, method, args, kwargs))


def server(port):
    s=socket(AF_INET,SOCK_STREAM)
    s.bind(( '' , port))
    s.listen(1)
    try:
        while True: 
            ns,peer=s.accept()
            t=Thread(target=rpc_service,args=(ns,))
            t.start()
    finally:
        s.close()


if __name__ == '__main__':
    # Start server
    server=Thread(target=server,args=(20445,))
    server.start()



