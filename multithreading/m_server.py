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


def recv_handler():
    global t_lock
    global clientSocket
    global serverSocket
    print('Server is ready for service')
    while(1):
        message, clientAddress = serverSocket.recvfrom(2048)
        #received data from the client, now we know who we are talking with
        message = message.decode()
        print ("received message: " + message)
        sentence = message.upper()
        #get lock as we might me accessing some shared data structures
        print (clientAddress)
        with t_lock:
            #send message to the client
            serverSocket.sendto(sentence.encode(), clientAddress)
            #notify the thread waiting
            t_lock.notify()


def send_handler():
    global t_lock
    global clientSocket
    global serverSocket
    global timeout
    #go through the list of the subscribed clients and send them the current time after every 1 second
    while(1):
        #get lock
        with t_lock:
            # clientSocket.sendto(message.encode(), ADDRESS)
            #notify other thread
            t_lock.notify()
        #sleep for UPDATE_INTERVAL
        time.sleep(UPDATE_INTERVAL)

#we will use two sockets, one for sending and one for receiving
clientSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
serverSocket.bind(('localhost', serverPort))

recv_thread=threading.Thread(name="RecvHandler", target=recv_handler)
recv_thread.daemon=True
recv_thread.start()

#send_thread=threading.Thread(name="SendHandler",target=send_handler)
#send_thread.daemon=True
#send_thread.start()
#this is the main thread
while True:
    time.sleep(0.1)
