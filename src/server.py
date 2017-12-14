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

    ############### Map Methods ###############

    if json_data['method'] == "createMap":

    if json_data['method'] == "addNode":
    
    if json_data['method'] == "deleteNode":

    if json_data['method'] == "addRoad":

    if json_data['method'] == "deleteRoad":

    if json_data['method'] == "saveMap":

    if json_data['method'] == "deleteMap":

    if json_data['method'] == "loadMap":
    
    if json_data['method'] == "getShortestPath":

    ############### Simulation Methods ###########
    
    if json_data['method'] == "createSimulation":
    
    if json_data['method'] == "setMap":
    
    if json_data['method'] == "addGenerator":

    if json_data['method'] == "delGenerator":

    if json_data['method'] == "startSimulation":
    
    if json_data['method'] == "tickSimulation":

    if json_data['method'] == "waitSimulation":

    if json_data['method'] == "terminateSimulation":

    if json_data['method'] == "getSimulationStats":

    if json_data['method'] == "SimulationDebugLevel":