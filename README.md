python server.py server_port number_of_consecutive_failed_attempts
python server.py 12000 3

python client.py server_IP server_port client_udp_server_port
python client.py 127.0.0.1 12000 6000

#COMP3331/9331 Computer Networks and Applications
#Assignment for Term 1, 2021

1. Goal and learning objectives
Zoom and Microsoft Team are widely used as a means for large groups of people to hold virtual
meetings. A good example is the on-line Zoom lectures used for this course. In this assignment, you
will have the opportunity to implement your own version of an online videoconferencing and
messaging application. Your application is based on a client server model consisting of one server
and multiple clients communicating concurrently. The text messages should be communicated using
TCP for the reason of reliability, while the video (we will use video files instead of capturing the live
video streams from cameras and microphones) should be communicated using UDP for the reason of
low latency. Your application will support a range of functions that are typically found on
videoconferencing including authentication, posting text message to all participants or one particular
participant, uploading video streams (i.e., files in this assignment). You will be designing custom
application protocols based on TCP and UDP.

##1.1 Learning Objectives
On completing this assignment, you will gain sufficient expertise in the following skills:
1. Detailed understanding of how client-server and client-client interactions work.
2. Expertise in socket programming.
3. Insights into implementing an application layer protocol.

##2. Assignment Specification
The base specification of the assignment is worth 20 marks. The specification is structured in two
parts. The first part covers the basic interactions between the clients and server and includes
functionality for clients to communicate with the server. The second part asks you implement
additional functionality whereby two clients can upload/download video files to each other directly
in a peer-to-peer fashion via UDP. This first part is self-contained (Sections 3.2 – 3.3) and is worth
Updates to the assignment, including any corrections and clarifications, will be posted on the
subject website. Please make sure that you check the subject website regularly for updates.
15 marks. Implementing video file uploading/downloading over UDP (Section 3.4) is worth 5 marks.
CSE students are expected to implement both functionalities. Non-CSE students are only required to
implement the first part (i.e. no video file uploading/downloading over UDP). The marking guidelines
are thus different for the two groups and are indicated in Section 7.
The assignment includes 2 major modules, the server program and the client program. The server
program will be run first followed by multiple instances of the client program (Each instance supports
one client). They will be run from the terminals on the same and/or different hosts.

Non-CSE Student: The rationale for this option is that students enrolled in a program that does not
include a computer science component have had very limited exposure to programming and in
particular working on complex programming assignments. A Non-CSE Student is a student who is
not enrolled in a CSE program (single or double degree). Examples would include students enrolled
exclusively in a single degree program such as Mechatronics or Aerospace or Actuarial Studies or
Law. Students enrolled in dual degree programs that include a CSE program as one of the degrees do
not qualify. Any student who meets this criterion and wishes to avail of this option MUST email
cs3331@cse.unsw.edu.au to seek approval before 5pm, 18 March (Friday, Week 5). We will
assume by default that all students are attempting the CSE version of the assignment unless they have
sought explicit permission. No exceptions.

##2.1. Assignment Specification
In this programming assignment, you will implement the client and server programs of a video
conference application, similar in many ways to the Zoom application that we use for this course.
The difference being that your application won’t capture and display live videos; instead, it will
transmit and receive video files. The text messages must communicate over TCP to the server, while
the clients communicate video files in UDP themselves. Your application will support a range of
operations including authenticating a user, post a message to the server, edit or delete messages, read
messages from server, read active users’ information, and upload video files from one user to another
user (CSE Students only). You will implement the application protocol to implement these functions.
The server will listen on a port specified as the command line argument and will wait for a client to
connect. The client program will initiate a TCP connection with the server. Upon connection
establishment, the user will initiate the authentication process. The client will interact with the user
through the command line interface. Following successful authentication, the user will initiate one of
the available commands. All commands require a simple request response interaction between the
client and server or two clients (CSE Students only). The user may execute a series of commands
(one after the other) and eventually quit. Both the client and server MUST print meaningful messages
at the command prompt that capture the specific interactions taking place. You are free to choose the
precise text that is displayed. Examples of client server interactions are given in Section 8.

##2.2 Authentication
When a client requests for a connection to the server, e.g., for attending a video conference, the server
should prompt the user to input the username and password and authenticate the user. The valid
username and password combinations will be stored in a file called credentials.txt which will be in
the same directory as the server program. An example credentials.txt file is provided on the
assignment page. Username and passwords are case-sensitive. We may use a different file for testing
so DO NOT hardcode this information in your program. You may assume that each username and
password will be on a separate line and that there will be one white space between the two. If the
credentials are correct, the client is considered to be logged in and a welcome message is displayed.
You should make sure that write permissions are enabled for the credentials.txt file (type “chmod +w
credentials.txt” at a terminal in the current working directory of the server).
On entering invalid credentials, the user is prompted to retry. After a number of consecutive failed
attempts, the user is blocked for a duration of 10 seconds (number is an integer command line
argument supplied to the server and the valid value of number should be between 1 and 5) and cannot
login during this 10 second duration (even from another IP address). If an invalid number value (e.g.,
a floating-point value, 0 or 6) is supplied to the server, the server prints out a message such as “Invalid
number of allowed failed consecutive attempt: number. The valid value of argument number is an
integer between 1 and 5”.
For non-CSE Students: After a user logs in successfully, the server should record a timestamp of
the user logging in event and the username in the active user log file (userlog.txt, you should make
sure that write permissions are enabled for userlog.txt). Active users are numbered starting at 1:
Active user sequence number; timestamp; username
1; 19 Feb 2021 21:30:04; yoda
For CSE Students: After a user logs in successfully, the client should next send the UDP port number
that it is listening to the server. The server should record a timestamp of the user logging in event, the
username, the IP address (how?) and port number that the client listens to in the active user log file
(userlog.txt):
Active user sequence number; timestamp; username; client IP address;
client UDP server port number
1; 19 Feb 2021 21:30:04; yoda; 129.64.1.11; 6666
For simplicity, a user will log in once in any given time, e.g., multiple logins concurrently are not
allowed, and we won’t test this case.

##2.3. Text message operation
Following successful login, the client displays a message to the user informing them of all available
commands and prompting to select one command. The following commands are available: MSG:
Post Message, DLT: Delete Message, EDT: Edit Message, RDM: Read Message, ATU: Display
active users, OUT: Log out and UPD: Upload file (for CSE Students only). All available commands
should be shown to the user in the first instance after successful login. Subsequent prompts for actions
should include this same message.
If an invalid command is selected, an error message should be shown to the user and they should be
prompted to select one of the available actions.
In the following, the implementation of each command is explained in detail. The expected usage of
each command (i.e., syntax) is included. Note that, all commands should be upper-case (RDM,
MSG, etc.). All arguments (if any) are separated by a single white space and will be one word long
(except messages which can contain white spaces and timestamps that have a fixed format of dd Mmm
yyyy hh:mm:ss such as 23 Feb 2021 16:01:20). You may assume that the message text
may contain uppercase characters (A-Z), lowercase characters (a-z) and digits (0-9) and the
following limited set of special characters (!@#$%.?,).
If the user does not follow the expected usage of any of the operations listed below, i.e., missing (e.g.,
not specifying the body of a message when posting the message) or incorrect number of arguments
(e.g., inclusion of additional or fewer arguments than required), an error message should be shown to 
the user and they should be prompted to select one of the available commands. Section 8 illustrates
sample interactions between the client and server.
There are 6 commands for Non-CSE Students and 7 commands for CSE Students respectively,
which users can execute. The execution of each individual command is described below.

###MSG: Post Message
MSG message
The message body should be included as the argument. Note that, the message may contain white
spaces (e.g., “hello how are you”). The client should send the command (MSG), the message and the
username to the server. In our tests, we will only use short messages (a few words long). The server
should append the message, the username, and a timestamp at the end of the message log file (file
(messagelog.txt, you should make sure that write permissions are enabled for messagelog.txt) in the
format, along with the number of the messages (messages are numbered starting at 1):
Messagenumber; timestamp; username; message; edited
1; 19 Feb 2021 21:39:04; yoda; do or do not, there is no try; no
After the message is successfully received at a server, a confirmation message with message number
and timestamp should be sent from the server to the client and displayed to the user. If there is no
argument after the MSG command. The client should display an error message before prompting the
user to select one of the available commands.
###DLT: Delete Message
DLT messagenumber timestamp
The message number to be deleted and the message’s timestamp should be included as arguments. A
message can only be deleted by the user who originally posted that message. The client sends the
command (DLT), the message number, its timestamp and the username to the server. The server
should check if the message number is valid, if the timestamp is correct, and finally if this user had
originally posted this message. In the event that any of these checks are unsuccessful, an appropriate
error message should be sent to the client and displayed at the prompt to the user. If all checks pass,
then the server should delete the message, which entails deleting the line containing this message in
the message log file (all subsequent messages in the file should be moved up by one line and their
message numbers should be updated appropriately) and a confirmation should be sent to the client
and displayed at the prompt to the user. The client should next prompt the user to select one of the
available commands.
###EDT: Edit Message
EDT messagenumber timestamp message
The message number to be edited, the message’s timestamp and the new message should be included
as arguments. A message can only be edited by the user who originally posted that message. The
client should send the command (EDT), the message number, the original message’s timestamp, the
new message and the username to the server. The server should check if the corresponding message
number is valid, if the message’s timestamp is correct, and finally if the username had posted this
message. In the event that any of these checks are unsuccessful, an appropriate error message should 
be sent to the client and displayed at the prompt to the user. If all checks pass, then the server should
replace the original message with the new message, update the timestamp, and marked the message
as edited in the message log file (the rest of the details associated with this message, i.e., message
number and username should remain unchanged).
Messagenumber; timestamp; username; message; edited
1; 19 Feb 2021 21:39:10; yoda; do or do not; yes
A confirmation should be sent to the client and displayed at the prompt to the user. The client should
next prompt the user to select one of the commands.
###RDM: Read Messages
RDM timestamp
The timestamp, after which the messages to be read, should be included as an argument. The client
should send the command (RDM) and a timestamp to the server. The server should check if there are
any new messages (i.e., the timestamps of the messages that are larger/later than the timestamp
specified in the RDM message) in the message log file. If so, the server should send these new
messages to the client. The client should display all received messages at the terminal to the user. If
there is no new message exist, a notification message of “no new message” should be sent to the
client and displayed at the prompt to the user. The client should next prompt the user to select one of
the available commands.
###ATU: Download Active Users
ATU
There should be no arguments for this command. The server should check if there are any other active
users apart from the client that sends the ATU command. If so, the server should send the usernames,
timestamp since the users are active, (and their IP addresses and Port Numbers, CSE Students only)
in active user log file to the client (the server should exclude the information of the client, who sends
ATU command to the server.). The client should display all the information of all received users at
the terminal to the user. If there is no other active user exist, a notification message of “no other active
user” should be sent to the client and displayed at the prompt to the user. The client should next
prompt the user to select one of the available commands.
###OUT: Log out
OUT
There should be no arguments for this command. The client should close the TCP connection, (UDP
client server, CSE Students only) and exit with a goodbye message displayed at the terminal to the
user. The server should update its state information about currently logged on users and the active
user log file. Namely, based on the message (with the username information) from the client, the
server should delete user, which entails deleting the line containing this user in the active user log file
(all subsequent users in the file should be moved up by one line and their active user sequence
numbers should be updated appropriately) and a confirmation should be sent to the client and
displayed at the prompt to the user. Note that any messages uploaded by the user must not be deleted.
For simplicity, we won’t test the cases that a user forgets to log out or log out is unsuccessful. 
##3.4 Peer to Peer Communication (Video file upload, CSE Students only)
The P2P part of the assignment enables one client upload video files to another client using UDP.
Each client is in one of two states, Presenter or Audience. The Presenter client sends video files the
Audience client. Here, the presenter client is the UDP client, while the Audience client is the UDP
server. After receiving the video files, the Audience client saves the files and the username of
Presenter. Note that a client can behave in either Presenter or Audience state.
To implement this functionality your client should support the following command.
###UPD: Upload file
UPD username filename
The Audience user and the name of the file should be included as arguments. You may assume that
the file included in the argument will be available in the current working directory of the client with
the correct access permissions set (read). You should not assume that the file will be in a particular
format, i.e., just assume that it is a binary file. The Presenter client (e.g., Yoda) should check if the
Audience user (indicated by the username argument, e.g., Obi-wan) is active (e.g., by issuing
command ATU). If Obi-wan is not active, the Presenter client should display an appropriate error
message (e.g., Obi-wan is offline) at the prompt to Yoda. If Obi-wan is active, Yoda should obtain the
Obi-wan’s address and UDP server port number (e.g., by issuing command ATU) before transferring
the contents of the file to Obi-wan via UDP. Here, Yoda is the UDP client and Obi-Wan is the UDP
server. The file should be stored in the current working directory of Obi-wan with the file name
presenterusername_filename (DO NOT add an extension to the name. If the filename has an extension
mp4, e.g., test.mp4 should be stored as yoda_test.mp4 in our example). File names are case sensitive
and one word long. After the file transmission, the terminal of Yoda should next prompt the user to
select one of the available commands. The terminal of Obi-wan should display an appropriate
message, e.g., a file (test.mp4) has been received from Yoda, before prompting the user to select one
of the available commands.
TESTING NOTES: 1) When you are testing your assignment, you may run the server and multiple
clients on the same machine on separate terminals. In this case, use 127.0.0.1 (local host) as the
destination (e.g., Obi-wan’s in our example above) IP address. 2) For simplicity, we will run different
clients at different directories, and won’t test the scenario that a file is received when a user is
typing/issuing a command.
##3.5 File Names & Execution
The main code for the server and client should be contained in the following files: server.c, or
Server.java or server.py, and client.c or Client.java or client.py. You are free
to create additional files such as header files or other class files and name them as you wish.
The server should accept the following two arguments:
• server_port: this is the port number which the server will use to communicate with the
clients. Recall that a TCP socket is NOT uniquely identified by the server port number. So it
is possible for multiple TCP connections to use the same server-side port number.
• number_of_consecutive_failed_attempts: this is the number of consecutive
unsuccessful authentication attempts before a user should be blocked for 10 seconds. It should
be an integer between 1 and 5.
The server should be executed before any of the clients. It should be initiated as follows:
If you use Java:
java Server server_port number_of_consecutive_failed_attempts
If you use C:
./server server_port number_of_consecutive_failed_attempts
If you use Python:
python server.py server_port number_of_consecutive_failed_attempts
The client should accept the following three arguments:
• server_IP: this is the IP address of the machine on which the server is running.
• server_port: this is the port number being used by the server. This argument should be the
same as the first argument of the server.
• client_udp_port: this is the port number which the client will listen to/wait for the UDP
traffic from the other clients.
Note that, you do not have to specify the TCP port to be used by the client. You should allow the OS
to pick a random available port. Similarly, you should allow the OS to pick a random available UDP
source port for the UDP client. Each client should be initiated in a separate terminal as follows:
For non-CSE Students:
If you use Java:
java Client server_IP server_port
If you use C:
./client server_IP server_port
If you use Python:
python client.py server_IP server_port
For CSE Students:
If you use Java:
java Client server_IP server_port client_udp_server_port
If you use C:
./client server_IP server_port client_udp_server_port
If you use Python:
python client.py server_IP server_port client_udp_server_port
Note: 1) The additional argument of client_udp_server_port for CSE Students for the P2P UDP
communication described in Section 3.4. In UDP P2P communication, one client program (i.e.,
Audience) acts as UDP server and the other client program (i.e., Presenter) acts as UDP client. 2)
When you are testing your assignment, you can run the server and multiple clients on the same 
8
machine on separate terminals. In this case, use 127.0.0.1 (local host) as the server IP address.
##3.6 Program Design Considerations
###Client Design
The client program should be fairly straightforward. The client needs to interact with the user through
the command line interface and print meaningful messages. Section 8 provides some examples. You
do not have the use the exact same text as shown in the samples. Upon initiation, the client should
establish a TCP connection with the server and execute the user authentication process. Following
authentication, the user should be prompted to enter one of the available commands. Almost all
commands require simple request/response interactions between the client with the server. Note that,
the client does not need to maintain any state about the videoconferencing.
For CSE Students, the client program also involves P2P communication using UDP. Similar to
above, the user should be prompted to enter the available P2P communication command: UPD. This
function should be implemented using a new thread since the user may want to interact with the client
program when the file is uploading. The thread will end when the upload finishes. Similarly, the
client UDP server should be implemented with another thread. However, this thread should be run
until the client logs off since it is a UDP server thread. You should be particularly careful about how
multiple threads will interact with the various data structures. Code snippets for multi-threading in
all supported languages are available on the course webpage.
###Server Design
When the server starts up, the videoconference is empty – i.e., there exist no users. The server should
wait for a client to connect, perform authentication and service each command issued by the client
sequentially. Note that, you will need to define a number of data structures for managing the current
state of the videoconference (e.g., active users and posts) and the server must be able to interact with
multiple clients simultaneously. A robust way to achieve this to use multithreading. In this approach,
you will need a main thread to listen for new connections. This can be done using the socket accept
function within a while loop. This main thread is your main program. For each connected client, you
will need to create a new thread. When interacting with one particular client, the server should receive
a request for a particular operation, take necessary action and respond accordingly to the client and
wait for the next request. You may assume that each interaction with a client is atomic. Consider that
client A initiates an interaction (i.e., a command) with the server. While the server is processing this
interaction, it cannot be interrupted by a command from another client B. Client B’s command will
be acted upon after the command from client A is processed. Once a client exits, the corresponding
thread should also be terminated. You should be particularly careful about how multiple threads will
interact with the various data structures. Code snippets for multi-threading in all supported languages
are available on the course webpage. 
