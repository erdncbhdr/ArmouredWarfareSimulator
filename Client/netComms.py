import socket
import pickle
from Errors import *

class networkComms():
    def __init__(self, ip,  port):
        self.ip = ip
        self.port = port

        try:
            self.sock = socket.create_connection((self.ip, self.port))
        except Exception as ex:
            print "Error whilst init netcomms: " + str(ex)
            raise NoConnectionException()
        self.last = 0
        self.retries = 0
        self.lastRetries = 0

    def send(self, message):
        self.toSend = pickle.dumps(message)
        try:
            self.sock.sendall(self.toSend)
            #print "SEND: " + str(message)
            self.recieved = pickle.loads(self.sock.recv(2048))
            #print "RECV: " + str(self.recieved)
            if self.last != self.recieved:
                self.last = self.recieved
            else:
                self.lastRetries += 1
                if self.lastRetries == 1000:
                    raise HostDisconnectedException()
            self.retries = 0

        except Exception as e:
            del self.sock
            self.sock = socket.create_connection((self.ip, self.port))
            self.retries += 1

            if self.retries == 5:
                raise HostDisconnectedException()

    def close(self):
        print "CLOSING CONNECTION"
        self.sock.close()
        del self.sock
