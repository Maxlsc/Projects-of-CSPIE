import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
from errorclass import AuthenticationError
from Crypto.Util.number import *
import time

class Client2:

    def __init__(self):
        pass


    def link_server(self, addr=('localhost', 8090)):
        clientSocket = socket.socket()
        clientSocket.connect(addr)

       
        publicKeyPK, pubKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(publicKeyPK).hexdigest() != pubKeySha256:
            raise AuthenticationError("密钥被篡改！")
        else:
            self.publicKey = pickle.loads(publicKeyPK)
            print("已接受公钥")

        self.year = 2000
        sendData = long_to_bytes(self.year)
        clientSocket.send(sendData)

        self.p,self.sign = pickle.loads(clientSocket.recv(1024))
        c = (self.p)
        for _ in range(2100-self.year):
            c = hashlib.sha256(c).hexdigest().encode()
        rsa.verify(c,self.sign,self.publicKey)
        print("验证成功。")
