# Sample code for Multi-Threaded Server
#Python 3
# Usage: python3 UDPserver3.py
#coding: utf-8
from socket import *
import threading
from _thread import *
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


def recv_handler(connectionSocket, address):
    global t_lock
    global ser
    print('Server is ready for service')
    while(1):
        with t_lock:
            sentence = connectionSocket.recv(1024)
            #wait for data to arrive from the client

            capitalizedSentence = sentence.upper()
            #change the case of the message received from client
            print("received: \t" + sentence.decode())
            
            #with t_lock:
            #send message to the client
            connectionSocket.send(capitalizedSentence)
            #notify the thread waiting
            t_lock.notify()
    connectionSocket.close()

def process_handler():
    while (1):
        connectionSocket, addr = serverSocket.accept()
        recv_thread=threading.Thread(name='please', target=recv_handler(connectionSocket, addr))
        recv_thread.daemon=True
        recv_thread.start()

#we will use two sockets, one for sending and one for receiving
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen()

#process = recv_handler(connectionSocket, addr)

recv_thread=threading.Thread(name='please', target=process_handler)
recv_thread.daemon=True
recv_thread.start()

#send_thread=threading.Thread(name="SendHandler",target=send_handler)
#send_thread.daemon=True
#send_thread.start()

#this is the main thread
while True:
    time.sleep(0.1)
