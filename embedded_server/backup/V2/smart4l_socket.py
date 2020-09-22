# -*- coding: utf-8 -*-

from utils import Message, Status, ServiceObjectInterface
import socket


class Smart4lServer(ServiceObjectInterface):
    def __init__(self, do_func):
        self.doFunc = do_func
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = Status.START.value
        self.s.bind((socket.gethostname(), 7545))
        self.s.listen(5)

    def do(self):
        while self.status == Status.START.value:
            # accept connections from outside
            (client, address) = self.s.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            response = client.recv(255)
            if not response == "":
                print(response)
        client.close()

    def receive_message(self):
        self.doFunc()

    def stop(self):
        self.status = Status.STOP.value
        self.s.close()


class Smart4lClient:
    def __init__(self,):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), 7545))

    def send_message(self, uid, value):
        self.s.send(bytes(f"{uid}: {value}", "utf-8"))


"""
# Client.py
import socket
s=socker.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(socker.gethostname(),8080)
msg = s.recv(1024)
print(msg.decode('utf-8'))

# while True:
#    msg = s.recv(8)
#    print(msg.decode('utf-8'))

# fullMessage = ""
# while True:
#   msg = s.recv(8)
#   if len(msg)<=0:
#        break
#    fullMessage+=msg.decode('utf-8')    
# print(fullMessage)

"""
