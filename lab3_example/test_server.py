#coding: utf-8
from socket import *
#using the socket module

#Define connection (socket) parameters
#Address + Port no
#Server would be running on the same host as Client
# change this port number if required
serverPort = 13000 

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

connectionSocket, addr = serverSocket.accept()

while 1:
    sentence = connectionSocket.recv(1024)
#wait for data to arrive from the client

    capitalizedSentence = sentence.upper()
#change the case of the message received from client
    print("received: \t" + sentence.decode())
    connectionSocket.send(capitalizedSentence)
#and send it back to client


connectionSocket.close()
#close the connectionSocket. Note that the serverSocket is still alive waiting for new clients to connect, we are only closing the connectionSocket.
