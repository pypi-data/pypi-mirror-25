"""Single-request network server classes.

Example:
    >>> from dtplib.RequestHandler import RequestHandler, getResponse
    >>> server = RequestHandler(lambda request: request.swapcase())
    >>> server.start()
    >>> addr = server.getAddr()
    >>> getResponse("Hello", addr)
    'hELLO'
    >>> getResponse("World!", addr)
    'wORLD!'
    >>> server.stop()
"""

import socket
import threading
from .Encrypt import encrypt, decrypt, random

buffersize = 4096
nullstr = " "
sockFamily = socket.AF_INET
sockType = socket.SOCK_STREAM

class RequestHandlerError(Exception):
    pass

def getResponse(request, addr):
    """Send a request to a server and receive a response."""
    (host, port) = addr
    s = socket.socket(sockFamily, sockType)
    s.connect((host, port))
    keyIV = s.recv(32)
    key = keyIV[:16]
    IV = keyIV[16:]
    request = encrypt(request, key, IV)
    s.send(str(len(request)))
    s.recv(len(nullstr))
    s.send(str(request))
    response = ""
    length = s.recv(buffersize)
    if length == "":
        s.close()
        raise RequestHandlerError("socket connection broken")
    length = int(length)
    s.send(nullstr)
    while len(response) < length:
        chunk = s.recv(buffersize)
        if chunk == "":
            s.close()
            raise RequestHandlerError("socket connection broken")
        response += chunk
    s.close()
    response = decrypt(response, key, IV)
    return response

class RequestHandler:
    """Receive requests from clients and send responses back.

    'handler' is a function which takes the request argument and
    returns the response.
    Leave port = 0 for an arbitrary, unused port.
    Server.host can be changed to '', 'localhost', etc. before the
    start method is called.
    """
    def __init__(self, handler, port = 0):
        self.handler = handler
        self.host = socket.gethostname()
        self.port = port
        self.running = False
        self.serveThread = None
        self.sock = None
        self.clients = []

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
            self.clients.append((conn, addr, key, IV))
            t = threading.Thread(target = self.handle, args = (conn, addr, key, IV))
            t.daemon = True
            t.start()

    def handle(self, conn, addr, key, IV):
        request = ""
        length = conn.recv(buffersize)
        if length == "":
            self.remove(conn)
            return
        length = int(length)
        conn.send(nullstr)
        while len(request) < length:
            chunk = conn.recv(buffersize)
            if chunk == "":
                self.remove(conn)
                return
            request += chunk
        request = decrypt(request, key, IV)
        result = self.handler(request)
        result = encrypt(result, key, IV)
        conn.send(str(len(result)))
        conn.recv(len(nullstr))
        conn.send(str(result))
        self.remove(conn)

    def remove(self, conn):
        """Remove a client."""
        conn.close()
        for i in range(len(self.clients)):
            if conn is self.clients[i][0]:
                del self.clients[i]

    def getAddr(self):
        """Get the address of the server in the format (host, port)."""
        return self.sock.getsockname()

if __name__ == "__main__":
    pass
