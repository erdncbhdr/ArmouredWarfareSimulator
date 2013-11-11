import socket
import pickle
class networkComms():
    def __init__(self, ip,  port):
        self.ip = ip
        self.port = port

    def send(self, message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,  int(self.port)))
        self.toSend = pickle.dumps(message)
        self.sock.sendall(self.toSend)
        self.recieved = pickle.loads(self.sock.recv(1024))
        self.sock.close()
