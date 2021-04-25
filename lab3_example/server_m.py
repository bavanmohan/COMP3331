# Sample code for Multi-Threaded Server
#Python 3
# Usage: python3 UDPserver3.py
#coding: utf-8
from socket import *
import threading
import time
import datetime as dt

#Server will run on this port
serverPort = 12000
t_lock=threading.Condition()
#will store clients info in this list
clients=[]
# would communicate with clients after every second
UPDATE_INTERVAL= 1
timeout=False


def recv_handler(serverSocket):
    print('Server is ready for service')
    while(1):
        
        message = serverSocket.recv(2048)
        #received data from the client, now we know who we are talking with
        message = message.decode()
        #get lock as we might me accessing some shared data structures
        with t_lock:
            serverMessage = message.isupper()
            #send message to the client
            serverSocket.send(serverMessage.encode())
            #notify the thread waiting
            t_lock.notify()

#we will use two sockets, one for sending and one for receiving

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen()
print("listening for connections")

while True:
    client, address = serverSocket.accept()
    print ("connected on ", client, address)
    recv_thread=threading.Thread(name="RecvHandler", target=recv_handler(serverSocket))
    recv_thread.daemon=True
    recv_thread.start()
