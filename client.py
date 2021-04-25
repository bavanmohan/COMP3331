from socket import *
from threading import *
import sys
import time

#       DISCLAIMER      # 
# I referenced the TCPClient.py program provided underneath the COMP3331 LAB03 resources. https://webcms3.cse.unsw.edu.au/COMP3331/21T1/resources/58257
# The above program was used as a basic skeleton for this file.

# This serves as the primary client-side function. It's purpose is to interact with clients 
# through the command line interface and then relaying the relevant command/data to the 
# server through simple request/response interactions.
def processes(client_port):
    logged_on = False
    # This while loop will continue until the user logs out, it is split into 2 if statements:
    # If the user is logged on or if the user is yet to log on
    while 1:
        # If the user is not yet logged on, they must undergo the authenticatio process in this if statement
        if (logged_on ==False):
            c_username = input('\n> Username:')
            c_password = input('\n> Password:')
            # The username and password are converted into a string to be split again once they reach the server
            # I included client_port in this message as it was the easiest method to inform the server of the clients port
            c_auth = c_username.strip() + ' '+ c_password.strip() + ' ' + str(client_port)
            
            # The send and recv functions below demonstrate the request/response interactions between client and server
            clientSocket.send(c_auth.encode())
            data = clientSocket.recv(1024)
            
            # For this authentication section, the server will reply with whether success if the user was authenticated
            # or timeout + number of failed attempts if the user is blocked
            # and fail + number of  attempts remaining before the user is blocked
            msg = data.decode()
            reply = msg.split()
            # This first if statement is where the blocking feature occurs, after the server informs the client that they have
            # reached the threshold of incorrect inputs, time.sleep(10) is used to pause the execution of this block for 10 seconds
            if (reply[0] == 'timeout'):
                print("> You have incorrectly entered details {} times, you must now wait for 10 seconds to resume".format(reply[1]))
                time.sleep(10)
                print("\n> You may now resume")
            # In the event that a login fails, the server will send an additionaly string in the reply column relaying how many
            # attempts the user has remaining
            elif (reply[0]=='fail'):
                print("\n> Invalid Details. Please try again: " + reply[1] + " attempt(s) left")
            else:
                logged_on = True
                print ("\n> Welcome to TOOM!")

        #if the user is logged in, this series of if statements will determine the command entered as well as any additional data
        if (logged_on == True):
            command = input("\n> Enter one of the following commands (MSG, DLT, EDT, RDM, ATU, OUT, UPD):\n")
            if not command:
                continue
            commands = command.split()
            #The logout function below is different to the other functions of this series as it exits the program to then 
            # disconnect from the server
            if (commands[0] == 'OUT'):
                clientSocket.sendall(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())
                exit()
            elif (commands[0] == 'MSG'):
                clientSocket.send(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())             
            elif (commands[0] == 'DLT'):
                clientSocket.send(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())
            elif (commands[0] == 'EDT'):
                clientSocket.send(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())
            elif (commands[0] == 'RDM'):
                clientSocket.send(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())
            elif (commands[0] == 'ATU'):
                clientSocket.send(command.encode())
                data = clientSocket.recv(1024)
                print(data.decode())
            elif (command == 'UPD'): 
                clientSocket.send(command.encode())
            else:
                print ('> Error, Invalid command!')



server_IP = sys.argv[1]
server_port = int(sys.argv[2])
client_port = int(sys.argv[3])
server_name = 'localhost'


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_name, server_port))

# This line below calls the main function on this page above
processes(client_port)

clientSocket.close()