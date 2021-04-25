#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import sys

#Server would be running on the same host as Client
serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while 1:
    message = input("Please type sentence\n")

    clientSocket.send(message.encode())
    #wait for the reply from the server
    receivedMessage = clientSocket.recvfrom(2048)

    #print (receivedMessage.decode())
    print(receivedMessage.decode())

clientSocket.close()
# Close the socket