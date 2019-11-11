import socket

import addresses
from client import Client

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# creating a socket with parameters AF_INET - address family of the inet, SOCK_STREAM - indicating the socket is TCP not UDP

s.connect((addresses.IP, addresses.PORT))                           
# connect to server

client = Client(s)                                            
# create a new client object
client.handle_connection()                                    
# handle connection with server
