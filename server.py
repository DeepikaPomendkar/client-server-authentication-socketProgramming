import sys
import threading      

import actions
import database
import passwords
import config


class ClientHandler(threading.Thread):
    def __init__(self, _socket):
        threading.Thread.__init__(self)
        self.socket = _socket

    def receive(self):
        """
        receives and returns message from client and catches an error if connection breaks
        """
        input_line = None
        try:
            input_line = self.socket.recv(config.BUFFER_SIZE)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        return input_line

    def send(self, message):
        """
        sends message through socket to client
        """
        try:
            self.socket.send(message + "\n")
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def register(self):
        """
        register user function by creating user in database
        """
        print "Registering User..."

        is_taken = True
        username = None

        while is_taken:
            self.send(actions.USERNAME_ACTION)
            username = self.receive()                                   # get username
            if not database.is_username_taken(username):                # check if is free
                is_taken = False
            else:
                self.send("Username already taken, try something else")

        #username is free

        is_valid = False
        password = None

        while not is_valid:
            self.send(actions.PASSWORD_ACTION)
            password = self.receive()                                   # get password
            self.send("Repeat password \n")
            self.send(actions.PASSWORD_ACTION)
            password_repeat = self.receive()                            # get repeated password
            if password_repeat != password:                             # compare them
                self.send("Passwords are not the same, try again")      # passwords not the same
                continue                                                # prompt for passwords again
            if passwords.is_password_valid(password):                   # passwords the same -> check if pass is valid
                is_valid = True
            else:
                self.send("Password is invalid (should have more than 7 characters,"    # pass invalid
                          " at last one digit, one lowercase and one uppercase),"       # send validate pass rules
                          " try something else.")

        # password is valid

        password_hash, salt = passwords.generate_salt(password)       # create hash
        database.create_new_user(username, password_hash, salt)           # create user into database

        self.send("User successfully registered! \nNow you can log in")  # confirm successful registration

    def login(self):
        """
        login user function
        """
        print "Login...."

        self.send(actions.USERNAME_ACTION)
        username = self.receive()                                       # get username

        print username

        password_hash = None
        salt = None
        hash_and_salt = database.get_password(username)                 # get salt and hashed password from database
        if hash_and_salt:
            password_hash = hash_and_salt[0]
            salt = hash_and_salt[1]

        if not salt:                                                    # user does not exist in database
            salt = passwords.get_salt()                                 # to not reveal if username exist or not
                                                                        # behave naturally with newly generated salt
        nonce = passwords.get_salt()
        self.send(actions.NONCE_ACTION + ":" + salt + ":" + nonce)
        self.send(actions.PASSWORD_ACTION)
        password = self.receive()                                       # get password

        if password_hash is not None and passwords.check_password(password, nonce, password_hash):
            self.send("Successfully login")                             # passwords matched
            self.loggedin(username)                                       # access granted
        else:
            self.send("User or password incorrect")                     # passwords mismatch

    def change_password(self, username):
        """
        change password user function
        change password for user in database if everything succeed
        """
        print "Changing password...."

        is_valid = False
        password = None

        while not is_valid:
            self.send(actions.PASSWORD_ACTION)
            password = self.receive()                                   # get password
            self.send("Repeat password \n")
            self.send(actions.PASSWORD_ACTION)
            password_repeat = self.receive()                            # get repeated password
            if password_repeat != password:                             # compare them
                self.send("Passwords are not the same, try again")      # passwords not the same
                continue                                                # prompt for passwords again
            if passwords.is_password_valid(password):                   # passwords the same -> check if pass is valid
                is_valid = True
            else:
                self.send("Password is invalid (should have more than 7 characters,"    # pass invalid
                          " at last one digit, one lowercase and one uppercase),"       # send validate pass rules
                          " try something else.")

        # password is valid

        password_hash, salt = passwords.generate_salt(password)       # create hash
        database.change_password(username, password_hash, salt)           # change password for user into database

        self.send("Password successfully changed \nNow you can log in with a new one")  # confirm successful action

    def loggedin(self, username):
        """
        function to handle logged user
        shows menu with actions for logged users
        """

        self.send("Access granted!")

        while True:
            self.send(" \nWhat do you want to do? (ls/change_password/logout/delete_account)") # menu for logged user
            self.send(actions.TYPE_ACTION)
            current_type = self.receive()                               # get type
            if current_type is None:                                    # if
                print "Connection lost"                                 # error occurred
                return                                                  # leave function
            elif current_type == "change_password":
                self.change_password(username)
            elif current_type == "ls":                                  # ls - fake function
                self.send("root home etc lib media mnt")                # to show some directories
            elif current_type == "delete_account":                      # give possibility to resign of the account
                database.delete_user(username)                          # delete user from database
                self.send("Your account was removed form system")
                return
            elif current_type == "logout":                              # end of work
                return                                                  # leave function
            else:
                self.send("unrecognized type")

    def run(self):
        """
        main function when thread starts to manage connection with all clients
        """
        self.send("Connected to server")

        while True:
            self.send(" \nWhat do you want to do? (register/login/quit)")
            self.send(actions.TYPE_ACTION)
            current_type = self.receive()                               # get type
            if current_type is None:                                    # connection broken
                break
            elif current_type == "login":
                self.login()                                            # login action
            elif current_type == "register":
                self.register()                                         # register action
            elif current_type == "quit":
                self.send(actions.QUIT_ACTION)                          # quit action
                break
            else:
                self.send("Unrecognized type")

        # user quit from server
        print "Client disconnected"
        self.socket.close()                                             # Close the connection


