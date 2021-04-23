#coding: utf-8
from socket import *
from threading import *
import sys
import time

#Define connection (socket) parameters
#Address + Port no
#Server would be running on the same host as Client
server_IP = sys.argv[1]
server_port = int(sys.argv[2])
server_name = 'localhost'


clientSocket = socket(AF_INET, SOCK_STREAM)
#This line creates the client’s socket. The first parameter indicates the address family; in particular,AF_INET indicates that the underlying network is using IPv4. The second parameter indicates that the socket is of type SOCK_STREAM,which means it is a TCP socket (rather than a UDP socket, where we use SOCK_DGRAM). 

clientSocket.connect((server_name, server_port))
#Before the client can send data to the server (or vice versa) using a TCP socket, a TCP connection must first be established between the client and server. The above line initiates the TCP connection between the client and server. The parameter of the connect( ) method is the address of the server side of the connection. After this line of code is executed, the three-way handshake is performed and a TCP connection is established between the client and server.
client_on = True
#while (client_on == True):
while 1:

    c_username = input('Input username:')
    c_password = input('Input password:')
    c_auth = c_username.strip() + ' '+ c_password.strip()
    message = c_auth.encode()
    #raw_input() is a built-in function in Python. When this command is executed, the user at the client is prompted with the words “Input lowercase sentence:” The user then uses the keyboard to input a line, which is put into the variable sentence. Now that we have a socket and a message, we will want to send the message through the socket to the destination host.

    clientSocket.send(message)
    #As the connection has already been established, the client program simply drops the bytes in the string sentence into the TCP connection. Note the difference between UDP sendto() and TCP send() calls. In TCP we do not need to attach the destination address to the packet, as was the case with UDP sockets.

    data = clientSocket.recv(1024)
    #We wait to receive the reply from the server, store it in modifiedSentence

    msg = data.decode()
    reply = msg.split()

    if (reply[0] == 'timeout'):
        print("You have incorrectly entered details {} times, you must now wait for 10 seconds to resume".format(reply[1]))
        time.sleep(10)
        print("You may now resume")

    elif (reply[0] == 'success'):
        client_on = False
    else:
        attempts = int(reply[0])
        print("Details invalid, you have " + reply[0] + " more tries")
#print what we have received

print("CLOSED")
clientSocket.close()
#and close the socket