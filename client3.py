import zmq
import sys
import os
import shutil
import json

def main():
    if len(sys.argv) != 3:
        print("Sample call python <serverM.py> <filename> <servers>")
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
    nSO = int(sys.argv[2])
    servAddresses = []

    f = open("folder/{}".format(filename))
    data = f.read().strip()
    f.close()
     
    A = [[int(num) for num in line.strip().split()] for line in data.split('\n')]
    print (A)

    for i in range(int(nSO)):
        socks = dict(poller.poll())
        if servers in socks:
            print("New server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                data = nSO - i
                servers.send(bytes(str(data), "ascii"))

    if len(A) % 2 == 0:
        nFilas = len(A)/int(nSO)
        print(nFilas)
    else:
        nFilas = len(A)/int(nSO)
        eFilas = len(A)%int(nSO)
        print(eFilas)
    
    name = "ansMat.dat"
    
    if os.path.exists("folder/{}".format(filename)):
        with open("folder/{}".format(filename), "rb") as forigen:
            with open("folder/{}".format(name), "wb") as fdestino:
                shutil.copyfileobj(forigen, fdestino)
                print("matriz copiada")
    
    sockets = []
    for ad in servAddresses:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ ad.decode("ascii"))
        sockets.append(s)
    
    for ad in range(len(sockets)):
        s = sockets[ad]
        s.send(b"0")
        
    for i in range(len(A)):
        for j in range(len(servAddresses)):
            s = sockets[j % len(sockets)]
            s.send_multipart([b"calculate", bytes(str(nFilas*j), "ascii"), bytes(str(filename), "ascii"), bytes(str(name), "ascii"), bytes(str(nFilas), "ascii")])
            s.recv()
    
if __name__ == '__main__':
    main()
