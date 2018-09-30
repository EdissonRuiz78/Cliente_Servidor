import zmq
import sys
import os
import json

def main():
    if len(sys.argv) != 2:
        print("Sample call python <serverM.py> <filename>")
        exit()
    context = zmq.Context()
    servers = context.socket(zmq.REP)
    servers.bind("tcp://*:5555")
    print("Started Master server")
    
    poller = zmq.Poller()
    poller.register(servers, zmq.POLLIN)
    
    path = "folder/"
    if not os.path.exists(path):
        os.makedirs(path)

    filename = sys.argv[1]
    servAddresses = []

    

    f = open("folder/{}".format(filename))
    data = f.read().strip()
    f.close()
     
    A = [[int(num) for num in line.strip().split()] for line in data.split('\n')]
    print (A)
    
    while True:
        socks = dict(poller.poll())
        if servers in socks:
            print("New server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                servers.send(b"ok")
            
if __name__ == '__main__':
    main()
