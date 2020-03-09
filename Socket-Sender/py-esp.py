import socket
import time
s = socket.socket()
host = ''
port = 8080
s.bind((host, port))
print ("socket binded to %s" %(port)) 
s.listen(1)
print ("Listening")            
while True: 
   c, addr = s.accept()      
   print ('Got connection from', addr)
   f=open("gcode.txt", "r")
   for x in f:
      stri=x
      c.send(stri.encode())
      c.settimeout(1000)
      data=c.recv(30)
      print(data.decode()) 
   f.close()
   c.close()
