
from socket import *
import os
from _thread import *
import sys
from datetime import datetime
import time

server_port = int(sys.argv[1])
no_attempts = int(sys.argv[2])

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', server_port))

ThreadCount = 0

"""try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))"""

print ("The server is ready to receive")

serverSocket.listen()

clients_list = []
message_list = []
#https://www.programiz.com/python-programming/datetime/current-datetime
#now=datetime.now()
#convert_now = now.strftime("%d/%m/%Y %H:%M:%S")



def write_file (clients_list):
    i = 0
    f = open('userlog.txt', 'w')
    f.close()
    f = open('userlog.txt', 'a')
    for client in clients_list:
        f.write(str(i+1)+'; '+str(client['date'])+'; '+client['username']+'; '+ client['ip'] + '; ' + client['udp'] +'\n')
        i+=1
    f.close()

def write_message(message_list):
    i = 0
    f = open('messagelog.txt', 'w')
    f.close()
    f = open('messagelog.txt', 'a')
    for message in message_list:
        f.write(str(i+1)+'; '+str(message['timestamp'])+'; '+str(message['username'])+'; '+str(message['message'])+'; '+str(message['edited'])+'\n')
        i += 1
    f.close()

def read_messages(message_list, timestamp):
    new_list = []
    #timestamp = '18/09/19 01:55:19'
    #https://www.educative.io/edpresso/how-to-convert-a-string-to-a-date-in-python
    datetimestamp = datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
    for message in message_list:
        list_timestamp = datetime.strptime(message['timestamp'], '%d/%m/%Y %H:%M:%S')
        if list_timestamp > datetimestamp:
            new_list.append(message)
    
    return new_list

def read_userlist(clients_list, username):
    new_userlist = []
    for client in clients_list:
        if client['username'] != username:
            new_userlist.append(client)
    return new_userlist

def threaded_client(connectionSocket, address, no_attempts):
    
    
    active = False
    chance = no_attempts
    global clients_list
    global message_list
    
    while True:
        if active == False:
            data = connectionSocket.recv(2048)
            auth_details = data.decode()
            auth_details = auth_details.split()
            credentials = auth_details[0] + ' ' + auth_details[1]
            with open('credentials.txt') as fp:
                details = 1
                while (details):
                    details = fp.readline()
                    if (details.strip() == credentials):
                        active = True
                        break

            if (credentials.strip()==""):
                active = False

            if active == True: 
                #print (auth_details + " matches")
                auth = "success"
                hostname = gethostname()
                ip_addr = gethostbyname(hostname)
                username = auth_details[1]
                upd_port = auth_details[2]
                print("> " + username + " login")
                #print("YYYYYYYYYYYYYYY\n" + username + ip_addr)
                now=datetime.now()
                clients_list.append ({
                    'date': now.strftime("%d/%m/%Y %H:%M:%S"),
                    'username' : username,
                    'ip': ip_addr,
                    'udp':upd_port,
                    'address':address
                })
                write_file(clients_list)

            else:
                #print (auth_details + " does not match")
                chance -= 1
                if (chance == 0):
                    chance = no_attempts
                    auth = "timeout " + str(no_attempts)
                    #connectionSocket.send(message.encode())
                    # THIS MAY NOT RETURN TO TOP OF PROPER LOOP
                    # continue
                else:
                    auth = "fail" + ' ' + str(chance)
            connectionSocket.sendall(auth.encode())
        
        #Logged in users
        if (active ==True):
            #message = "> Enter one of the following commands (MSG, DLT, EDT, RDM, ATU, OUT, UPD):"
            #connectionSocket.sendall(message.encode())
            data = connectionSocket.recv(2048)
            #time.sleep(0.1)
            message = data.decode()

            if message:
                command = message.split()
                #print(message, command[0])
            else:
                break
            
            if (command[0] == 'OUT'):
                print(data.decode(), address[1])
                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                        clients_list.remove(client)
                        write_file(clients_list)
                        message = '> Bye ' + username
                        connectionSocket.sendall(message.encode())
                        print("> " + username + " logout")
            elif (command[0] == 'MSG'):
                command.remove(command[0])
                seperator = ' '
                msg = seperator.join(command)
                
                now=datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                i = 1
                for message in message_list:
                    i+=1
                message_list.append({
                    'number': i,
                    'timestamp': timestamp,
                    'username': username,
                    'message':msg,
                    'edited': 'no',
                })
                write_message(message_list)
                client_msg ='  > Message #'+ str(i) +' posted at '+ str(now.strftime("%d/%m/%Y %H:%M:%S"))
                connectionSocket.send(client_msg.encode())
                server_msg = '  > ' + username + ' posted MSG #' + str(i) + ' "' + msg +'" at' + ' ' + str(timestamp) + '.'
                print(server_msg)

            elif (command[0] == 'DLT'):
                delete = False
                #print(command[1],'\t',command[2])
                msg_number = command[1]
                timestamp = command[2] + ' ' + command[3]
                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                #print('K', msg_number, timestamp, username)
                i = 0
                for message in message_list:
                    i +=1
                    message['number'] == i
                    #print('L', message['number'], message['timestamp'], message['username'])
                    if (username == message['username']) and \
                        int(msg_number) == message['number'] and\
                        timestamp == message['timestamp']:
                        delete = True
                        server_msg = '> ' + username + ' deleted MSG #' + msg_number + ' "' + message['message'] + '" at ' + timestamp + '.' 
                        print(server_msg)
                        #SEND TO CLIENT
                        client_msg = "  > Message #" + str(msg_number)+ ' deleted at ' + timestamp + '.'
                        print(client_msg)
                        message_list.remove(message)
                        write_message(message_list)

                if delete == False:
                    #SEND TO CLIENT
                    print('  > Please select a message created by you:\n')
                    
            elif (command[0] == 'EDT'):
                #print('HH', command)
                edited = False
                msg_number = command[1]
                timestamp = command[2] +' '+ command[3]
                command.remove(command[0])
                command.remove(command[0])
                command.remove(command[0])
                command.remove(command[0])
                seperator = ' '
                msg = seperator.join(command)
                #print ('time', timestamp)
                #print ('msg', msg)
                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                now=datetime.now()
                for message in message_list:
                    if (username == message['username']) and \
                        int(msg_number) == message['number']and\
                        timestamp == message['timestamp']:
                            edited = True
                            #print(message)
                            message['message'] = msg
                            message['timestamp'] = now.strftime("%d/%m/%Y %H:%M:%S")
                            message['edited'] = 'yes'
                            write_message(message_list)
                            #print(message)
                            server_msg = '> ' +username + ' edited MSG #' + str(msg_number) + ' "' + msg + '" at ' + timestamp + '.'
                            print(server_msg)
                            # SEND TO CLIENT
                            client_msg = '> Message #' + str(msg_number) + ' edited at ' + timestamp + '.'
                            #print(client_msg)
                            connectionSocket.send(client_msg.encode())

                
                if edited == False:
                    #SEND TO CLIENT
                    print('> Please select a message created by you:\n')
            
            elif(command[0] == 'RDM'):
                #print('HHHHHHHHH')
                timestamp = command[1] + ' ' + command[2]
                print(timestamp)
                read_list = read_messages(message_list, timestamp)
                server_msg = '> ' + username + ' issued RDM command.\n> Return messages:'
                print(server_msg)
                client_msg = ''
                for msg in read_list:
                    #print (msg)
                    if msg['edited'] == 'yes':
                        server_msg = '#' + str(msg['number']) + ' ' + msg['username'] + ', ' + msg['message'] + ', edited at ' + str(timestamp) + '.'
                        print(server_msg)
                        #SEND TO CLIENT
                        msg = '\n  > #' + str(msg['number']) + ', ' + msg['username']+ ': ' + msg['message'] + ', edited at ' + str(timestamp) + '.'
                        client_msg = client_msg + ' ' + msg
                    elif msg['edited'] == 'no':
                        server_msg = '#' + str(msg['number']) + ' ' + msg['username'] + ', ' + msg['message'] + ', posted at ' + str(timestamp) + '.'
                        print(server_msg)
                        #SEND TO CLIENT
                        msg = '\n  > #' + str(msg['number']) + ', ' + msg['username'] + ': ' + msg['message'] + ', posted at ' + str(timestamp) + '.'
                        client_msg = client_msg + ' ' + msg
                #print(client_msg)
                connectionSocket.send(client_msg.encode())
                

            elif (command[0] == 'ATU'):
                activeuser_list = read_userlist(clients_list, username)
                #print(activeuser_list)
                server_msg = '> ' + username + ' issued ATU command. \n> Return active user list:\n'
                print (server_msg)
                if (activeuser_list) == []:
                    server_msg = '> No other active user'
                    print(server_msg)
                    client_msg = '  > No other active user'
                    connectionSocket.send(client_msg.encode())
                else:
                    client_msg =  ''
                    for user in activeuser_list:
                        i = 1
                        server_msg = user['username'] + ', '+ user['ip'] + ', '+ user['udp'] + ', active since ' + str(user['date']) + '.'
                        print(server_msg)
                        msg = '\n  >' + user['username'] + '; '+ user['ip'] + '; '+ user['udp'] + '; active since ' + str(user['date']) + '.'                    
                        client_msg = client_msg + ' ' + msg
                        i =+ 1
                    connectionSocket.send(client_msg.encode())


    connectionSocket.close()

#MAIN
while True:
    Client, address = serverSocket.accept()
    #print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, address, no_attempts))
    ThreadCount += 1
    #print('Thread Number: ' + str(ThreadCount))
serverSocket.close()