import zmq
import sys

def main():
	if len(sys.argv) != 3:
		print("Sample call: python ServerO <address> <port>")
		exit()
	
	serverAdd = sys.argv[1]
	serverPort = sys.argv[2]
	serverAdd = serverAdd + ":" + serverPort

	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5555")

	socket.send_multipart([b"newServer", bytes(serverAdd, "ascii")])
	msg = socket.recv()
	print(msg)

	while True:
		if int(msg) == 0:
			print("Waiting.....")
			operation, *rest = socket.recv_multipart()
			if operation == b"calculate":
				nFilas2, filename, name, nFilas = rest
				
				f = open("folder/{}".format(name))
				data = f.read().strip()
				f.close()
					
				A = [[int(num) for num in line.strip().split()] for line in data.split('\n')]
				print (A)

			else:
				print("Unsupported operation")
			socket.send(b"ok")	

if __name__ == '__main__':
	main()
