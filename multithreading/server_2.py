""" from socket import *
import threading 

# Multithreaded Python server : TCP Server Socket Thread Pool


# Multithreaded Python server : TCP Server Socket Program Stub
def processing (connectionSocket, addr):
    while 1:
        sentence = connectionSocket.recv(1024)
        #wait for data to arrive from the client

        capitalizedSentence = sentence.upper()
        #change the case of the message received from client
        print("received: \t" + sentence.decode())
        connectionSocket.send(capitalizedSentence)
        #and send it back to client

    connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
serverSocket.bind(('localhost', 12000)) 
threads = []
while True: 
    serverSocket.listen() 
    print ("The server is ready to receive\n") 
    (connectionSocket, addr) = serverSocket.accept() 
    process = processing(connectionSocket, addr)
    threading._start_new_thread(processing, (connectionSocket, addr))
    #new_thread=threading.Thread(name="RecvHandler", target=process)
    #new_thread.daemon=True
    threads.append(new_thread)
    print(threads[0])
    print('HHHHHHHHHH')
    new_thread.start() 
    """
from socket import *
import os
from _thread import *
import sys
from datetime import datetime

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
#https://www.programiz.com/python-programming/datetime/current-datetime
#now=datetime.now()
#convert_now = now.strftime("%d/%m/%Y %H:%M:%S")

def write_file (clients_list):
    i = 0
    f = open('userlog.txt', 'w')
    f.close()
    f = open('userlog.txt', 'a')
    for client in clients_list:
        f.write(str(i+1)+' '+str(client['date'])+' '+client['username']+' \n')
        i+=1
    f.close()

def threaded_client(connectionSocket, address, no_attempts):
    
    active = False
    chance = no_attempts
    global clients_list
    
    while True:
        data = connectionSocket.recv(2048)
        auth_details = data.decode()
        #print(data.decode(), "\t", address[0])

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
                #print (auth_details + " matches")
                auth = "success"
                hostname = gethostname()
                ip_addr = gethostbyname(hostname)
                auth_details = auth_details.split()
                username = auth_details[1]
                print("> " + username + " login")
                #print("YYYYYYYYYYYYYYY\n" + username + ip_addr)
                now=datetime.now()
                clients_list.append ({
                    'date': now.strftime("%d/%m/%Y %H:%M:%S"),
                    'username' : username,
                    'ip': ip_addr,
                    'udp':'na',
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
            message = data.decode()
            if (message == 'OUT'):
                print(data.decode(), address[1])
                for client in clients_list:
                    if client['address'] == address:
                        username = client['username']
                        clients_list.remove(client)
                        write_file(clients_list)
                        message = '> Bye ' + username
                        connectionSocket.sendall(message.encode())
                        print("> " + username + " logout")
                                        




    print("CLOSING\n")
    connectionSocket.close()




#MAIN
while True:
    Client, address = serverSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, address, no_attempts))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
serverSocket.close()