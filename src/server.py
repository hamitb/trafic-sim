import time
import random
import json


def echoservice(sock):
    length=int(s.recv())
    request=sock.recv(length)
    while request and request!= '':
        '''parse received json data
        request= request.rstrip()
        sock.send(request)
        request=sock.recv(1000)'''
        
    print (sock.getpeername() ," closing")

def server(port):
    s=socket(AF_INET,SOCK_STREAM)
    s.bind( ( '' , port ) )
    s.listen(1)
    try:
        while True: 
            ns,peer=s.accept()
            t=Thread(target=echoservice,args=(ns,))
            t.start()
    finally:
        s.close()

server=Thread(target=server,args=(20445,))
server.start()

