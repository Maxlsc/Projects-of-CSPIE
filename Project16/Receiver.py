from Crypto.Util.number import *
from gmssl.sm2 import CryptSM2
from random import randint
import socket
import pickle

class Receiver:

    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

    def __init__(self):
        self.d2 = 0x383c53f785cd1e45da3c07f8473527581a2ee50a5974943691868e73694a4f61

    def link_server(self, addr=('localhost', 8080)):
        clientSocket = socket.socket()
        clientSocket.connect(addr)
        print("Sender主机地址为：{}".format(addr))
       
        T1 = pickle.loads(clientSocket.recv(1024))

        sm2_t = CryptSM2("0","0")
        t2 = inverse(self.d2,self.n)
        T2 = sm2_t._kg(t2,T1)
        
        clientSocket.send(pickle.dumps(T2))


tmp = Receiver()
tmp.link_server()