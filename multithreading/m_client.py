#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import sys

#Server would be running on the same host as Client
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_DGRAM)
while 1:
    message = input("Please type sentence\n")

    clientSocket.sendto(message.encode(),(serverName, serverPort))
    #wait for the reply from the server
    receivedMessage, serverAddress = clientSocket.recvfrom(2048)

    #print (receivedMessage.decode())
    print(receivedMessage.decode())

clientSocket.close()
# Close the socket