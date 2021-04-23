#coding: utf-8
from socket import *
from threading import *
import sys
#using the socket module

#Define connection (socket) parameters
#Address + Port no
#Server would be running on the same host as Client
# change this port number if required
server_port = int(sys.argv[1])
no_attempts = int(sys.argv[2])

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', server_port))

serverSocket.listen(1)

print ("The server is ready to receive")

connectionSocket, addr = serverSocket.accept()

active = False
chance = no_attempts
#chance = 1
while 1:

    reply = connectionSocket.recv(1024)
    
    auth_details = reply.decode()

    #Authentication
    if active == False:
        with open('credentials.txt') as fp:
            details = 1
            while (details):
                details = fp.readline()
                if (details.strip() == auth_details):
                    active = True
                    break

        if (auth_details.strip()==""):
            active = False

        if active == True: 
            print (auth_details + " matches")
            auth = "success"
        else:
            print (auth_details + " does not match")
            chance -= 1
            if (chance == 0):
                chance = no_attempts
                auth = "timeout " + str(no_attempts)
                #connectionSocket.send(message.encode())
                # THIS MAY NOT RETURN TO TOP OF PROPER LOOP
                # continue
            else:
                auth = str(chance)
        connectionSocket.send(auth.encode())


connectionSocket.close()