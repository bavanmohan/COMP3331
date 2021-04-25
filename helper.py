from datetime import datetime
from socket import *
import sys

#       DISCLAIMER      #
# In order to convert string resembling datetime format to an object of datetime, the
# following page was used

def check_auth(credentials):
    if credentials:
        with open('credentials.txt') as fp:
            details = 1
            active = False
            while (details):
                details = fp.readline()
                if (details.strip() == credentials):
                    active = True
    else:
        active = False
    
    return active

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

def get_msg(str_list):
    str_list.remove(str_list[0])
    seperator = ' '
    msg = seperator.join(str_list)
    return msg

def find_username(user_list, address):
    for user in user_list:
        if user['address'] == address:
            return user['username']

def message_number(message_list):
    i = 1
    for message in message_list:
        i+=1
    return i