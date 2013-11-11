import socket
import pickle
import errno

class networkComms():
    def __init__(self,  ip , newport_gwent):
        self.ip = ip
        self.port = newport_gwent
        self.sock = socket.create_connection((self.ip,  self.port))
    def send(self, message):
        self.toSend = pickle.dumps(message)
        try:
            self.sock.sendall(self.toSend)
            self.recieved = pickle.loads(self.sock.recv(2048))
        except Exception:
            del self.sock
            self.sock = socket.create_connection((self.ip,  self.port))
    def close(self):
        self.sock.close()
