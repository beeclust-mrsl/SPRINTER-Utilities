#! /usr/bin/env python

import socket
import time

s = socket.socket()

host = ''
port = 8080

s.bind((host, port))
print("socket binded to %s" %port)
s.listen(1)

print("Listening")

c, addr = s.accept()      
print('Got connection from', addr)

while True:

   
   string = input()
   # print(string.encode())
   c.send(string.encode())
   c.settimeout(20)
   
   while True:
      data=c.recv(20)
      # print(data)
      ack=data.decode()
      print(ack)
      data=""
      if "OK" in ack.upper():
         #print("Received :" + ack.upper())
         break

   time.sleep(1)

   # string = 'M250 S0'
   # c.send(string.encode())
   # c.settimeout(20)

   # while True:
   # 		data=c.recv(20)
   # 		print(data)
   # 		ack=data.decode()
   # 		data=""
   # 		if "OK" in ack.upper():
   # 			# print("Received :" + ack.upper())
   # 			break

   # time.sleep(1)

c.close()