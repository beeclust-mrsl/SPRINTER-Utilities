import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 8080

s.bind((host, port))
print ("socket binded to %s" %(port)) 
s.listen(1)

print ("Listening")

c, addr = s.accept()      
print ('Got connection from', addr)  

while True: 

   f=open("gcode.txt", "r")

   for x in f:
      print(x)
      c.send(x.encode())
      c.settimeout(200)

      while True:
         data=c.recv(16)
         ack=data.decode()

         if 'OK' in ack.upper():
            print ("Received :"+ack)
            break

   f.close()

c.close()