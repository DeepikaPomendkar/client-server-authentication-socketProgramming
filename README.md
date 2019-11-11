# DCCN-MINI PROJECT client-server-authentication-socketProgramming


* The code is written in python 2.7
* In this project an authentication of the client can be done using Socket programming.

* Socket is used for creating a connection between the client and server.
* Sqlite3 is used as a backend database.
* SHA256 is used for hashing in this program.


* In config.py file:
  * Store the IP address of the server in the IP variable and the port number on which the server is to be kept running.
  
* Server side:
  * Start the server by running "python run_server.py" in the terminal.
  * When the server starts a socket is made the socket continuously listens for a IPV4 connection over a TCP protocol .
  * If there is a congestion then at a time the server can put 8 client connection requests in the queue (You can change this number).
  * When a client sends a request the connection is made with the client and a thread is created for each client connected to the server.
  * When the client registers a Salt value is generated and the password entered by the client is hashed and stored in the database as follows:
    * hashedPassword =(username, hash( salt + password), salt)
    
  * When the client wants to log In a challenge is sent to the client. This challenge is verified on the server side and only then the client is authenticated.
  * A nonce is generated and sent to the client. (nonce: One time used salt)
  * The response sent by the client is checked as follows:
    * if (hash( nonce + hashedPassword)) == response sent by client
      - Client is authenticated.
  
  
* Client side:
  * Start the client by running "python run_client.py" in the terminal.
  * While registering the client enters the username and password which is stored by the server in the database.
  * When the client want to log In it has to accept the challenge sent by the server.
  * The server sends the salt corresponding to the username entered by the user which was previously stored in the database when the user had registered.
  * The password entered by the user is hashed as follows on the client side:
    * hash( nonce + hash (salt +password))
    * This is sent to the server as response.
    * If the responce sent by the client is same as that computed by the server then the client is authenticated.
    
    
    

* Shematic view of the client-server-authentication model 
<img src="https://user-images.githubusercontent.com/45281119/68567149-5368f800-047e-11ea-81e8-7fa4b6793ffa.jpeg" width="500px">
  


