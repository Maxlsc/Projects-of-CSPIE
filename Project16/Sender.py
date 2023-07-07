from Crypto.Util.number import *
from gmssl.sm2 import CryptSM2
from gmssl import sm3
from random import randint
import socket
import pickle

c = b'\xb4\x932\xcd\xa4\x84\xc4V\xd1l\r\xe1\xbe\xbbN\xf4\x13\xdd\x7f9\x8c\xdeR:\xc9\xd34\x15\xe90\x1c7\xeb\x90ZJ\x8f\x07\xa2\x7f`2T,\x94\xb4\x0b\xf1\xa5r)\xe8\xa6|\xd9\r\xadD\xa9\x9f\xdf\xdd\xd99|mI\x98\xa9\x92\xe13e\x93\x99\xb6\xc8I\xbcA\x92\xebYx\x19/CrP!\xf7}$\xbc\x162\xc25\x11\xea\x13\xf0\x87\xe2\xc7\xf2{\x14\x87r6'
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF

class sender:

    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

    def __init__(self, addr=('localhost', 8080)):
        self.d1 = 0x94b8a9d27b8821945c0ff89bef829a357dec0b70de8377cec7c70bd294887cb4 
        self.d2 = 0x383c53f785cd1e45da3c07f8473527581a2ee50a5974943691868e73694a4f61
        self.serverSocket = socket.socket()
        self.serverSocket.bind(addr)
        self.serverSocket.listen()

    def link_one_client(self):
        clientSocket, addr = self.serverSocket.accept()
        print("Receiver主机地址为：{}".format(addr))

        sm2_t = CryptSM2("0","0")
        data = c.hex()
        len_2 = 2 * 64
        C1 = data[0:len_2]
        C2 = data[len_2:-64]
        C3 = data[-64:]
        if int(C1,16) == 0:
            return 0
        t1 = inverse(self.d1,self.n)
        T1 = sm2_t._kg(t1,C1)
        clientSocket.send(pickle.dumps(T1))

        T2 = pickle.loads(clientSocket.recv(1024))
        # t2 = inverse(self.d2,self.n)
        # T2 = sm2_t._kg(t2,T1)
        C1_i = sm2_t._kg(self.n-1,C1)
        kP = sm2_t._convert_jacb_to_nor(sm2_t._add_point(T2,C1_i))
        x = kP[0:64]
        y = kP[64:len_2]
        t = sm3.sm3_kdf(kP.encode('utf8'), len(C2)/2)
        form = '%%0%dx' % len(C2)
        M = form % (int(C2, 16) ^ int(t, 16))
        if C3 == sm3.sm3_hash([i for i in bytes.fromhex('%s%s%s' % (x, M, y))]):
            return bytes.fromhex(M)
        else:
            return None

tmp = sender()
print(tmp.link_one_client())