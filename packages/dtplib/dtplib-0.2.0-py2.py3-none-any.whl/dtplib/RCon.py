"""Remote Console network server classes.

Example:
    >>> from dtplib.RCon import Server, Client
    >>> server = Server(lambda cmd: cmd.swapcase())
    >>> server.addUser("myusername", "password123")
    >>> server.start()
    >>> addr = server.getAddr()
    >>> client = Client()
    >>> client.login(addr, "myusername", "password123")
    >>> print client.send("Hello World!")
    hELLO wORLD!
    >>> print client.send("Foo Bar")
    fOO bAR
    >>> client.logout()
    >>> server.stop()
"""

import socket
import threading
try:
    import cPickle as pickle
except:
    import pickle
from .Encrypt import encrypt, decrypt, random
from .UserDB import UserDB

buffersize = 4096
sockFamily = socket.AF_INET
sockType = socket.SOCK_STREAM

class RConError(Exception):
    pass

class Client:
    """Connect to a server with a valid username and password. Send
    commands and receive responses.

    Any Python object can be passed through the send method, as it
    supports serialization.
    """
    def __init__(self):
        self.host = None
        self.port = None
        self.running = False
        self.sock = None
        self.key = None
        self.IV = None

    def login(self, addr, username, password):
        """Log in to a server."""
        (host, port) = addr
        if self.running:
            raise RConError("already connected to server")
        self.sock = socket.socket(sockFamily, sockType)
        self.sock.connect((host, port))
        keyIV = self.sock.recv(32)
        self.key = keyIV[:16]
        self.IV = keyIV[16:]
        self.running = True
        if not self.send((username, password)):
            self.running = False
            self.sock.close()
            self.sock = None
            self.key = None
            self.IV = None
            raise RConError("login failed")
        self.host = host
        self.port = port

    def logout(self):
        """Log out of the server."""
        self.running = False
        self.sock.close()
        self.sock = None
        self.key = None
        self.IV = None

    def getAddr(self):
        """Get the address of the client in the format (host, port)."""
        return self.sock.getsockname()

    def getServerAddr(self):
        """Get the address of the server in the format (host, port)."""
        return self.sock.getpeername()

    def send(self, command):
        """Send commands to the server and receive responses."""
        if not self.running:
            raise RConError("not connected to a server")
        command = pickle.dumps(command)
        command = encrypt(command, self.key, self.IV)
        if len(command) % buffersize == 0:
            command += " "
        self.sock.send(command)
        result = ""
        while len(result) % buffersize == 0:
            chunk = self.sock.recv(buffersize)
            if chunk == "":
                self.disconnect()
                raise RConError("socket connection broken")
            result += chunk
        result = result[:int(len(result) / 16) * 16]
        result = decrypt(result, self.key, self.IV)
        result = pickle.loads(result)
        return result

class Server:
    """Continuously serve clients with valid login information.

    'handler' is a function which takes the command argument. If
    something is returned, it will be sent to the client.
    Leave port = 0 for an arbitrary, unused port.
    'dbFileName' is the file in which the user database is stored.
    'dbHashFunction' can be any typical hash algorithm: md5, sha1,
    sha256, etc. The default algorithm is md5.
    """
    def __init__(self, handler, port = 0, dbFileName = "users.db", dbHashFunction = "md5"):
        self.handler = handler
        self.host = socket.gethostname()
        self.port = port
        self.running = False
        self.serveThread = None
        self.sock = None
        self.clients = []
        self.users = UserDB(dbFileName, dbHashFunction)

    def start(self):
        """Start the server."""
        if self.running:
            raise RequestHandlerError("server already running")
        self.sock = socket.socket(sockFamily, sockType)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True
        self.serveThread = threading.Thread(target = self.serve)
        self.serveThread.daemon = True
        self.serveThread.start()

    def stop(self):
        """Stop the server."""
        self.running = False
        for client in self.clients:
            client[0].close()
        self.clients = []
        killsock = socket.socket(sockFamily, sockType)
        killsock.connect(self.getAddr())
        killsock.close()
        self.sock.close()
        self.sock = None

    def serve(self):
        while True:
            conn, addr = self.sock.accept()
            if not self.running:
                break
            key = random()
            IV = random()
            conn.send(key + IV)
            login = ""
            try:
                while len(login) % buffersize == 0:
                    chunk = conn.recv(buffersize)
                    if chunk == "":
                        conn.close()
                        raise RConError
                    login += chunk
            except RConError:
                continue
            login = login[:int(len(login) / 16) * 16]
            login = decrypt(login, key, IV)
            login = pickle.loads(login)
            isValid = self.users.validLogin(*login)
            valid = pickle.dumps(isValid)
            valid = encrypt(valid, key, IV)
            if len(valid) % buffersize == 0:
                valid += " "
            conn.send(valid)
            if isValid:
                self.clients.append((conn, addr, key, IV))
                t = threading.Thread(target = self.handle, args = (conn, addr, key, IV))
                t.daemon = True
                t.start()
            else:
                conn.close()

    def handle(self, conn, addr, key, IV):
        while True:
            command = ""
            while len(command) % buffersize == 0:
                chunk = conn.recv(buffersize)
                if chunk == "":
                    self.remove(conn)
                    return
                command += chunk
            command = command[:int(len(command) / 16) * 16]
            command = decrypt(command, key, IV)
            command = pickle.loads(command)
            result = self.handler(command)
            result = pickle.dumps(result)
            result = encrypt(result, key, IV)
            if len(result) % buffersize == 0:
                result += " "
            conn.send(result)

    def remove(self, conn):
        """Remove a client."""
        conn.close()
        for i in range(len(self.clients)):
            if conn is self.clients[i][0]:
                del self.clients[i]

    def getAddr(self):
        """Get the address of the server in the format (host, port)."""
        return self.sock.getsockname()

    def addUser(self, username, password, info = None):
        """Create a new user with specified username, password, and
        info (optional).
        """
        self.users.new(username, password, info)

    def delUser(self, username):
        """Delete a user from the database."""
        self.users.remove(username)

    def getUserInfo(self, username):
        """Get the info of a user. If no info exists, a NoneType is
        returned.
        """
        return self.users.getInfo(username)

    def setUserInfo(self, info):
        """Set the info of a user."""
        self.users.setInfo(info)

    def delDB(self):
        """Delete the database."""
        self.users.delete()
        self.users = None

if __name__ == "__main__":
    pass
