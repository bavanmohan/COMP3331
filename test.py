    #Authentication
# match = False

# message = 'Hans Jedi*knight'
# with open('credentials.txt') as fp:
#     details = 1
#     while (details):
#         details = fp.readline()
#         print(details)
#         if (details.strip() == message):
#             break
from datetime import datetime 
import time
import sys

try:
    no_attempts = int(sys.argv[1])
except:
    print("Invalid number of allowed failed consecutive attempt: " + sys.argv[2] + \
        " - The valid value of argument number is an integer between 1 and 5")
    exit()

if not isinstance(no_attempts, int) or not no_attempts > 0 or not no_attempts < 6:
    print('k')



print('HHHH')

global clients_list
clients_list = []
def add (username, ip_addr):
    global clients_list
    now=datetime.now()
    clients_list.append ({
        'date': now.strftime("%d/%m/%Y %H:%M:%S"),
        'username' : username,
        'ip': ip_addr,
        'udp':'na',
    })

def write_file (clients_list):
    i = 0
    f = open('userlog.txt', 'w')
    f.close()
    f = open('userlog.txt', 'a')
    for client in clients_list:
        f.write(str(i)+' '+str(client['date'])+' '+client['username']+' \n')
        i+=1
    f.close()

