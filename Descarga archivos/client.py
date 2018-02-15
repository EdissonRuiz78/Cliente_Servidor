import zmq
import sys
import os
import math
import time

def main():
    if len(sys.argv) != 3:
        print("Error!!!")
        exit()

    ip = sys.argv[1] #Server's ip
    port = sys.argv[2] #Server's port

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(ip, port))

    print("Connecting to server {} at {}".format(ip, port))
    def menu():
        print("\n1 - List music available on server")
        print("2 - You can see the weight of a file in megabytes")
        print("3 - Download a file divide in parts of 1Mb")
        print("4 - Exit\n")
    
    while True:
        menu()
        operation = input("Choose a option:")
        
        if operation == "1":
            s.send_json({"op":"list"})
            files = s.recv_json()
            print("\n", files)
        
        elif operation == "2":
            name = input("File to see: ")
            s.send_json({"op": "parts", "file": name})
            file = s.recv_json()
            print("\nThis file contains: " + file["parts"] + " megabytes")
    
        elif operation == "3":
            name = input("File to download: ")
            s.send_json({"op": "parts", "file": name})
            Part = s.recv_json()
            count = 0;
            Part = int(Part["parts"])
            start=time.time()
            print("TIME START")
            while count < Part:
                s.send_json({"op": "Parts", "file": name, "Count": count})
                file = s.recv()
                with open("{}".format(name), "ab+") as output:
                    print("Incoming part: {}".format(count))
                    output.write(file)
                count = count + 1
            end= time.time() 
            print("\nTIME ", str(math.ceil(end-start)), " SECONDS")
        elif operation == "4":
            exit()
        else:
            print("Error!!! unsupported operation")

if __name__ == '__main__':
    main()
