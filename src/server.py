import json
from socket import *
from printwc import printwc
from threading import Thread
from controller import Controller

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

        # Controller(Map + Simulation) of this connection
        c = Controller()
        c_methods = c.methods

        # Receive the upcoming message's length as bytes object
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
            m_name = req_data['method']
            args = req_data['args']
            kwargs = req_data['kwargs']

            printwc('yellow', "{} calls: {} with args:{} and kwargs:{}\n".format(peer, m_name, args, kwargs))

            # Call requested method
            f = c_methods[m_name]
            f(*args, **kwargs)

            # Wait for new rpc request
            req_len_bin = s.recv(10)

        printwc('blue', "{} leaves\n".format(peer))


if __name__ == '__main__':
    # Start server
    s = Server(tcp_port=20445)
    s.start()



