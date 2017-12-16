import json
from socket import *
from threading import Thread

class Server(Thread):
    def __init__(self, tcp_port, tcp_ip=''):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.port = tcp_port
        self.ip = tcp_ip

        self.s.bind((tcp_ip, tcp_port))
        super().__init__()

    def run(self):
        self.s.listen(1)
        try:
            while True:
                ns, peer = self.s.accept()
                t = Thread(target=self.rpc_service, args=(ns,))
                t.start()
        finally:
            self.s.close()

    def rpc_service(self, s):
        '''
        parse_service listens for remote procedure call requests and handles requests
        coming from client in the form of binary json strings.
        :param s:
        :return:
        '''

        # Receive upcoming messages length as bytes object
        req_len_bin = s.recv(10)
        peer = s.getpeername()

        # Continue to receive as long as clients leaves or sends empty bytes as length
        while req_len_bin != b'':
            # Convert bytes representation of json length to integer
            req_len = int(req_len_bin)

            # Receive rpc request as json
            req = s.recv(req_len).decode()
            req_data = json.loads(req)

            # Handle rpc request
            self.rpc_handler(req_data)

            # Wait for new rpc request
            req_len_bin = s.recv(10)

        print("{} leaves".format(peer))

    def rpc_handler(self, req_data):

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


if __name__ == '__main__':
    # Start server
    s = Server(tcp_port=20445)
    s.start()



