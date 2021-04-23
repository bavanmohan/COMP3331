#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import sys

#Server would be running on the same host as Client
server_IP = sys.argv[1]
server_port = int(sys.argv[2])
server_name = 'localhost'

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.connect((server_name, server_port))

while 1:
    c_username = input('Input username:')
    c_password = input('Input password:')
    c_auth = c_username.strip() + ' '+ c_password.strip()
    message = c_auth.encode()

    clientSocket.sendto(message.encode(),(server_name, server_port))
    #wait for the reply from the server
    data, serverAddress = clientSocket.recvfrom(2048)

    #print (receivedMessage.decode())
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

print ("CLOSED")
clientSocket.close()
# Close the socket