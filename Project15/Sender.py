from Crypto.Util.number import *
from gmssl.sm2 import CryptSM2
from hashlib import sha256
from random import randint
import socket
import pickle
import random

def getRandom(randomlength=16):
    upperLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerLetter = "abcdefghigklmnopqrstuvwxyz"
    digits="0123456789"
    wpecialCharacters = "!@#$%&_-.+="
    str_list =[random.choice(upperLetter+lowerLetter+digits+wpecialCharacters) for _ in range(randomlength)]
    random_str =''.join(str_list)
    return random_str

def verify(e,r,s,G,P,n):
    sm2_t = CryptSM2("0","0")
    t = (r + s) % n
    Q = sm2_t._convert_jacb_to_nor(sm2_t._add_point(sm2_t._kg(s,G),sm2_t._kg(t,P)))
    x1 = int(Q[0:64], 16)
    y1 = int(Q[64:len(Q)], 16)
    R = (e + x1) % n
    assert R == r


class sender:

    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    g = '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7''bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0'

    def __init__(self, addr=('localhost', 8080)):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(addr)
        self.serverSocket.listen()

    def link_one_client(self):
        serverSocket, addr = self.serverSocket.accept()
        print("Receiver主机地址为：{}".format(addr))

        sm2_t = CryptSM2("0","0")
        d1 = randint(1,self.n-1)
        P1 = sm2_t._kg(inverse(d1,self.n),self.g)
        serverSocket.send(pickle.dumps(P1))

        P = pickle.loads(serverSocket.recv(1024))
        Z = getRandom()
        M = 'This is a text.'
        e = int(sha256((Z+M).encode()).hexdigest(), 16)
        k1 = randint(1, self.n-1)
        Q1 = sm2_t._kg(k1, self.g)
        serverSocket.send(pickle.dumps((e,Q1)))

        r,s2,s3 = pickle.loads(serverSocket.recv(1024))
        s = ((d1*k1)*s2 + d1 * s3 - r) % self.n
        verify(e,r,s,self.g,P,self.n)
        if s!=0 or s!=self.n-r:
            sigma = (r,s)
            return sigma
        else:
            return None

tmp = sender()
print(tmp.link_one_client())