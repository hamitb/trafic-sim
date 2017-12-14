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

def parse_jsonobj(data):
    json_data=data.decode()

    if json_data['objid'] == "Map":
        if json_data['method'] == "constructor":
        
        if json_data['method'] == "addNode":
            
        if json_data['method'] == "deleteNode":

        if json_data['method'] == "addRoad":

        if json_data['method'] == "deleteRoad":

        if json_data['method'] == "getShortestPath":
        
        if json_data['method'] == "saveMap":

        if json_data['method'] == "deleteMap":

        if json_data['method'] == "loadMap":
 
    if json_data['objid'] == "Simulation":
        
        if json_data['method'] == "constructor":
        
        if json_data['method'] == "setMap":
            
        if json_data['method'] == "addGenerator":

        if json_data['method'] == "getGenerators":

        if json_data['method'] == "delGenerator":

        if json_data['method'] == "startSimulation":
        
        if json_data['method'] == "tick":

        if json_data['method'] == "terminate":

        if json_data['method'] == "wait":

        if json_data['method'] == "getStats":

    
    if json_data['objid'] == "RSegment":

        if json_data['method'] == "constructor":
        
        if json_data['method'] == "insertVehicle":
            
        if json_data['method'] == "getInfo":

        if json_data['method'] == "getNVehicles":

        if json_data['method'] == "getCapacity":

        if json_data['method'] == "full":
        
        if json_data['method'] == "getStats":
