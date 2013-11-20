import socket
import pickle

class networkComms():
    def __init__(self, ip,  port):
        self.ip = ip
        self.port = port
        self.sock = socket.create_connection((self.ip, self.port))

    def send(self, messaege):
        #print "SEND: "+str(messaege)
        self.toSend = pickle.dumps(messaege)
        try:
            self.sock.sendall(self.toSend)
            #print "SENT"
            self.recieved = pickle.loads(self.sock.recv(2048))
            #print "RECV: "+str(self.recieved)
        except Exception as e:
            print "ERROR: "+str(e)
            del self.sock
            self.sock = socket.create_connection((self.ip, self.port))

    def close(self):
        print "CLOSING CONNECTION"
        self.sock.close()
