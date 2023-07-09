from Crypto.Util.number import *
from gmssl.sm2 import CryptSM2
from random import randint
import socket
import pickle

class Receiver:

    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    g = '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7''bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0'

    def __init__(self):
        pass

    def link_server(self, addr=('localhost', 8080)):
        clientSocket = socket.socket()
        clientSocket.connect(addr)
        print("Sender主机地址为：{}".format(addr))

        sm2_t = CryptSM2("0","0")
        P1 = pickle.loads(clientSocket.recv(1024))
        d2 = randint(1,self.n-1)
        P_t = sm2_t._kg(inverse(d2,self.n),P1)
        G_i = sm2_t._kg(self.n-1,self.g)
        P = sm2_t._convert_jacb_to_nor(sm2_t._add_point(P_t,G_i))
        clientSocket.send(pickle.dumps(P))

        e,Q1 = pickle.loads(clientSocket.recv(1024))
        k2 = randint(1, self.n-1)
        Q2 = sm2_t._kg(k2, self.g)
        k3 = randint(1, self.n-1)
        Q3 = sm2_t._convert_jacb_to_nor(sm2_t._add_point(sm2_t._kg(k3, Q1), Q2))
        x1 = int(Q3[0:64], 16)
        y1 = int(Q3[64:len(Q3)], 16)
        r = (x1 + e) % self.n
        s2 = (d2 * k3) % self.n
        s3 = (d2*(r + k2)) % self.n
        clientSocket.send(pickle.dumps((r,s2,s3)))


tmp = Receiver()
tmp.link_server()