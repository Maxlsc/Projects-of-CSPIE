import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
from errorclass import AuthenticationError
import time
import random
from Crypto.Util.number import *

class Server:


    def __init__(self, backlog=5, addr=('localhost', 8080)):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(addr)
        self.serverSocket.listen(backlog)

        self.seed = random.randint(2^128,2^129)
        self.s = hashlib.sha256(long_to_bytes(self.seed)).hexdigest()

        self.asyKey = rsa.newkeys(2048)
        self.publicKey = self.asyKey[0]
        self.privateKey = self.asyKey[1]
        
    def link_one_client(self):
        clientSocket, addr = self.serverSocket.accept()

        print("Alice主机地址为：{}".format(addr))

        print("正在向服务器传送公钥")
        sendKey = pickle.dumps(self.publicKey)
        sendKeySha256 = hashlib.sha256(sendKey).hexdigest()
        clientSocket.send(pickle.dumps((sendKey, sendKeySha256)))

        while True:
            time.sleep(0.3)
            recvData = bytes_to_long(clientSocket.recv(1024))
            print("收到Alice发送的year：{}".format(recvData))

            c = (self.s).encode()
            for _ in range(2100-recvData):
                c = hashlib.sha256(c).hexdigest().encode()
            sign = rsa.sign(c,self.privateKey,'SHA-256')
            sendData = pickle.dumps((self.s,sign))
            print(self.s)
            clientSocket.send(sendData)
