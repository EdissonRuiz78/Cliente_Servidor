import zmq
import sys
import os
import math

def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loadding {}".format(filename))
        files[filename] = file
    return files

def main():
    if len(sys.argv) != 3:
        print("Error!!!")
        exit()

    directory = sys.argv[2]
    port = sys.argv [1]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    files = loadFiles(sys.argv[2])

    while True:
        msg = s.recv_json()
        print("Executing request!!!")
        
        if msg["op"] == "list":
            s.send_json({"files": list(files.keys())})
            
        elif msg["op"] == "parts":
            filename = msg["file"]
            if filename in files:
                with open(directory + filename, "rb") as input:
                    data = input.read()
                    s.send_json({"parts": str(math.ceil(len(data)/(1024*1024)))})
            else:
                print("File not found!!!")
                s.send("File not found!!!")
        
        elif msg["op"] == "Parts":
            filename = msg["file"]
            Part = msg["Count"]
            if filename in files:
                with open(directory + filename, "rb") as input:
                    input.seek(1024*1024*Part)
                    data = input.read(1024*1024)
                    s.send(data)
            else:
                print("File not found!!!")
                s.send("File not found!!!")
        else:
            print("Unsupported action")

if __name__ == '__main__':
    main()
