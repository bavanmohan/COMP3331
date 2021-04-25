
from socket import *
from _thread import *
from helper import *
import os
import sys
from datetime import datetime
import time

#       DISCLAIMER      #
# Some files were referenced/used to produce this code:
# I referenced the TCPServer.py program provided underneath the COMP3331 LAB03 resources. https://webcms3.cse.unsw.edu.au/COMP3331/21T1/resources/58254
# The above program was used as a basic skeleton for this file.
#
# In order to get current timestamps and convert them to the relevant format, 
# e.g. now=datetime.now() --> now.strftime("%d/%m/%Y %H:%M:%S") I used the following link:
# https://www.programiz.com/python-programming/datetime/current-datetime
# This was used multiple times throughout the code 
#
# In order to implement multithreading, the following webpage was used 
# https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
# Specifically for the application of the start_new_thread function on line 244

# Once a thread has been created for each client, they are redirected here. This function will 
# receive a message indicating which command the user has requested and will follow through to 
# deliver output to the client's interface
def threaded_client(connectionSocket, address, no_attempts):
    
    active = False
    chance = no_attempts
    global clients_list
    global message_list
    
    #Below is an endless loop housing where the client will be redirected. At first the client
    # will have status active = False, indicating they are not yet logged in
    while True:
        if active == False:
            # The section of code under this if statement will only be activated when the user 
            # is not logged in, therefore will be used to check authentication
            data = connectionSocket.recv(2048)
            auth_details = data.decode()
            # The data received from the client will be in the format 'username password udp_port'
            if auth_details:
                auth_details = auth_details.split()
                credentials = auth_details[0] + ' ' + auth_details[1]
            
            #After the username and password have been concatenated to resemble the format seen in 
            # credentials.txt, the function below will check to see if a match is found in the text file
            # True is returned for yes, False is returned for no match, or empty credentials 
            active = check_auth(credentials)

            #The if statement below is activated following the succesful sign in of a client
            if active == True: 
                auth = "success"

                # As opposed to using localhost, the two lines below where used to determine the
                # IP address of the client
                hostname = gethostname()
                ip_addr = gethostbyname(hostname)

                username = auth_details[1]
                upd_port = auth_details[2]
                # A message is printed to the server's terminal once a user logs in
                print("> " + username + " login")

                now=datetime.now()

                # Following a succesful login, the user's details must be appended to client_list
                # client list is a global list of dictionaries. To update the userlog, the client_list is copied into the userlog.txt file every time a 
                # change has been made to the data structure. The user_number is not kept in this data structure
                # as it is never called upon. It is instead inserted as the data structure is copied to the txt file
                # see function write_file in helper.py 
                clients_list.append ({
                    'date': now.strftime("%d/%m/%Y %H:%M:%S"),
                    'username' : username,
                    'ip': ip_addr,
                    'udp':upd_port,
                    'address':address
                })
                write_file(clients_list)

            # This if statement is called when a user fails to input the correct details. chance represents
            # the number of attempts left before the user is shut from the system. For every failed attempt,
            # chance is decreased by 1 until it equals 0 resulting in blocking
            else:
                chance -= 1
                if (chance == 0):
                    chance = no_attempts
                    auth = "timeout " + str(no_attempts)
                else:
                    auth = "fail" + ' ' + str(chance)

            connectionSocket.sendall(auth.encode())
        
        #The below if statement is called when a user has successfully logged in
        # It functions by receiving data from the client in order to execute the relevant command
        if (active ==True):
            data = connectionSocket.recv(2048)
            message = data.decode()

            #Once data has been received it is split into a list of strings with the first element
            # responsible for calling the command and the rest providing information to be used in the 
            # execution of the command
            if message:
                command = message.split()
            else:
                break
            # The if statement below is responsible for logging out the user.
            if (command[0] == 'OUT'):
                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                        # The client is then removed from clients_list, and the userlog.txt is updated
                        clients_list.remove(client)
                        write_file(clients_list)
                         #Data is also sent back to where
                        # the OUT command was request, and will deliver a goodbye message. 
                        # Upon reception the client will disconnect
                        message = '> Bye ' + username
                        connectionSocket.sendall(message.encode())
                        print("> " + username + " logout")
            # The elif statement below is responsible for posting a message.
            elif (command[0] == 'MSG'):
                # The function below is written in the helper.py file. command (a list of strings)
                # is formatted into a string by joining each element with a space
                msg = get_msg(command)
                
                now=datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
                # The function below can be found in helper.py. It iterates through the clients_list
                # until a match is found, and returns the username of the corresponding client 
                username = find_username(clients_list, address)
                # The function below can be found in helper.py. It uses message_list to return the number value 
                # of the latest message + 1
                msg_counter = message_number(message_list)
                # Similar to clients_list, once a message has been appended to the data structure, the 
                # message log is updated through write_message. The write message function can be found 
                # in helper.py
                message_list.append({
                    'number': msg_counter,
                    'timestamp': timestamp,
                    'username': username,
                    'message':msg,
                    'edited': 'no',
                })
                write_message(message_list)

                #Finally a message is created for both the client and server. The client's is sent and the server's is printed
                client_msg ='  > Message #'+ str(msg_counter) +' posted at '+ str(now.strftime("%d/%m/%Y %H:%M:%S"))
                server_msg = '\n> ' + username + ' posted MSG #' + str(msg_counter) + ' "' + msg +'" at' + ' ' + str(timestamp) + '.'
                connectionSocket.send(client_msg.encode())
                print(server_msg)

            elif (command[0] == 'DLT'):
                delete = False
                msg_number = command[1]
                timestamp = command[2] + ' ' + command[3]
                username = find_username(clients_list, address)
                i = 0
                for message in message_list:
                    # The if statement below searches through message_list until a match is found for username, number and timestamp
                    if (username == message['username']) and \
                        int(msg_number) == message['number'] and\
                        timestamp == message['timestamp']:
                        #If a match has been found, delete is set to True, messages are created and delivered and the
                        #data structure and message;og.txt file is updated
                        delete = True

                        client_msg = "  > Message #" + str(msg_number)+ ' deleted at ' + timestamp + '.'
                        server_msg = '\n> ' + username + ' deleted MSG #' + msg_number + ' "' + message['message'] + '" at ' + timestamp + '.' 
                        connectionSocket.send(client_msg.encode())
                        print(server_msg)                     
                        
                        message_list.remove(message)
                        write_message(message_list)
                # The if statement below is activated if a message has not been deleted. This is due to no matches being found
                # and a response is sent to the client's terminal asking to change their input
                if delete == False:
                    client_msg = '> Please select a message created by you:'
                    connectionSocket.send(client_msg.encode())
            # This elif statement below is responsible for editing an existing comment. 
            elif (command[0] == 'EDT'):
                edited = False
                msg_number = command[1]
                timestamp = command[2] +' '+ command[3]
                # The first 4 elements of the command list are removed to leave behind just the indexes
                # containing strings for the message. This list of strings is then joined together to
                # create one message
                for i in range(4):
                    command.remove(command[0])

                seperator = ' '
                msg = seperator.join(command)

                username = find_username(clients_list, address)
                now=datetime.now()
                # After details have been gathered, similar to DLT, the message_list is iterated through until
                # a match is found
                for message in message_list:
                    if (username == message['username']) and \
                        int(msg_number) == message['number']and\
                        timestamp == message['timestamp']:
                            edited = True
                            # Once a match is found, the message, timestamp and edit status is then updated
                            message['message'] = msg
                            message['timestamp'] = now.strftime("%d/%m/%Y %H:%M:%S")
                            message['edited'] = 'yes'
                            write_message(message_list)

                            client_msg = '> Message #' + str(msg_number) + ' edited at ' + timestamp + '.'
                            server_msg = '\n> ' +username + ' edited MSG #' + str(msg_number) + ' "' + msg + '" at ' + timestamp + '.'
                            connectionSocket.send(client_msg.encode())
                            print(server_msg)
                # The if statement below is activated if a match was not found after iterating through the data structure
                # As a response the server will send a message to the client asking to attempt again
                if edited == False:
                    client_msg = '> Please select a message created by you:'
                    connectionSocket.send(client_msg.encode())
            # The elif statement below is used to relay a list of messages.
            elif(command[0] == 'RDM'):
                # The timestamp is concatenated and then fed to read_messages function which converts the string
                # to an object of datetime, then returns a list of messages, which were posted at a later time. 
                # read_messages can be found in the helper.py file
                timestamp = command[1] + ' ' + command[2]
                read_list = read_messages(message_list, timestamp)

                server_msg = '\n> ' + username + ' issued RDM command.\n> Return messages:'
                print(server_msg)
                # As seen below, client_msg is intialised as an empty string. The for loop below is used to iterate through the read_list and collate all
                # responses to send to the client. For each iteration, the client message is appended to itself + msg in order to allow for one large message
                # sent to the client as opposed to several smaller ones. The server_msg is handled differently, instead it prints to the server's terminal 
                # after each iteration
                client_msg = ''
                for msg in read_list:
                    # The if and elif statements below are used to differentiate between edited and non-edit messages as they both result in different messages
                    if msg['edited'] == 'yes':
                        server_msg = '#' + str(msg['number']) + ' ' + msg['username'] + ', ' + msg['message'] + ', edited at ' + str(msg['timestamp']) + '.'
                        msg = '\n  > #' + str(msg['number']) + ', ' + msg['username']+ ': ' + msg['message'] + ', edited at ' + str(msg['timestamp']) + '.'
                        print(server_msg)
                        client_msg = client_msg + ' ' + msg
                    elif msg['edited'] == 'no':
                        server_msg = '#' + str(msg['number']) + ' ' + msg['username'] + ', ' + msg['message'] + ', posted at ' + str(msg['timestamp']) + '.'
                        msg = '\n  > #' + str(msg['number']) + ', ' + msg['username'] + ': ' + msg['message'] + ', posted at ' + str(msg['timestamp']) + '.'
                        print(server_msg)
                        client_msg = client_msg + ' ' + msg

                connectionSocket.send(client_msg.encode())
            # The elif statement below is responsible for the returning a list of all active users. 
            elif (command[0] == 'ATU'):
                # read_userlist below is used to iterate through clients_list and return all clients who do not have the same username
                # as the current client. read_userlist can be found in the helper.py file
                activeuser_list = read_userlist(clients_list, username)

                server_msg = '\n> ' + username + ' issued ATU command. \n> Return active user list:'
                print (server_msg)
                # If read_userlist returns an empty list, then there are no other active users
                if (activeuser_list) == []:
                    server_msg = '\n> No other active user'
                    print(server_msg)
                    client_msg = '  > No other active user'
                    connectionSocket.send(client_msg.encode())
                # The else statement below will operate similar to the statement seen above in RDM. It will iterate through the returned list
                # and collate all responses in order to send to the client.
                else:
                    client_msg =  ''
                    for user in activeuser_list:
                        # 
                        #
                        #
                        i = 1 # IS THE COUNTER NECESSARY????????????????????
                        server_msg = user['username'] + ', '+ user['ip'] + ', '+ user['udp'] + ', active since ' + str(user['date']) + '.'
                        msg = '\n  >' + user['username'] + '; '+ user['ip'] + '; '+ user['udp'] + '; active since ' + str(user['date']) + '.'                    
                        print(server_msg)
                        client_msg = client_msg + ' ' + msg
                        i =+ 1
                    connectionSocket.send(client_msg.encode())


    connectionSocket.close()

server_port = int(sys.argv[1])
# If the number of attempts allowed is provided in an invalid format, the following is raised
# and the program will close
try:
    no_attempts = int(sys.argv[2])
except:
    print("Invalid number of allowed failed consecutive attempt: " + sys.argv[2] + \
        " - The valid value of argument number is an integer between 1 and 5")
    exit()

if not isinstance(no_attempts, int) or not no_attempts > 0 or not no_attempts < 6:
    print("Invalid number of allowed failed consecutive attempt: " + sys.argv[2] + \
        " - The valid value of argument number is an integer between 1 and 5")
    exit()


clients_list = []
message_list = []

#MAIN
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', server_port))

print ("The server is ready to receive")

serverSocket.listen()

while True:
    Client, address = serverSocket.accept()
    start_new_thread(threaded_client, (Client, address, no_attempts))

serverSocket.close()