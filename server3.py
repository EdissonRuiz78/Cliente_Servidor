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
	m = socket.recv()
	print(m)


	#while True:
	#	msg = socket.recv_multipart()
	#	print(msg)

if __name__ == '__main__':
	main()
