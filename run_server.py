import socket
from OpenSSL import SSL

import database as database
import addresses
from server import ClientHandler

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   
# creating a socket with parameters AF_INET - address family of the inet, SOCK_STREAM - indicating the socket is TCP not UDP

s.bind((addresses.IP, addresses.PORT))                                        
# bind the scoket to the port

s.listen(5)                                                             
# wait and listen for client connection
database.create_table()                                                 
# create table for storing username and hashed password

while True:
    client_socket, address = s.accept()      # Establish connection with client
    clientThread = ClientHandler(client_socket)     # create a thread for each client so that requests can be handled simultaneously
    clientThread.start()     # run thread
