# import socket programming library 
import socket 

# import thread module 
from _thread import *
import threading 

print_lock = threading.Lock() 

# thread function 
def threaded(c): 
	while True:
		f=open("gcode.txt", "r")
		c.send("M20".encode())
		data=c.recv()
		if not data :
			print_lock.release()
			break
		if (data.decode())=="OK\n":
			for x in f:
				c.send(x.encode())
			f.close()
			break
		#print_lock.release()
		#break	
	c.close() 


def Main(): 
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 8080
	s = socket.socket() 
	s.bind((host, port)) 
	print("socket binded to port", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("socket is listening") 

	# a forever loop until client wants to exit 
	while True: 

		# establish connection with client 
		c, addr = s.accept() 

		# lock acquired by client 
		print_lock.acquire() 
		print('Connected to :', addr[0], ':', addr[1]) 

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,)) 
	s.close() 


if __name__ == '__main__': 
	Main() 
