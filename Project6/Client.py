import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
from errorclass import AuthenticationError
from Crypto.Util.number import *
import time

class Client:

    def __init__(self):
        pass


    def link_server(self, addr=('localhost', 8080)):
        clientSocket = socket.socket()
        clientSocket.connect(addr)

        publicKeyPK, pubKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(publicKeyPK).hexdigest() != pubKeySha256:
            raise AuthenticationError("密钥被篡改！")
        else:
            self.publicKey = pickle.loads(publicKeyPK)
            print("已接受公钥")

        self.year = 1978
        sendData = long_to_bytes(self.year)
        clientSocket.send(sendData)

        self.s,self.sign = pickle.loads(clientSocket.recv(1024))
        print(self.s)
        return (self.s,self.sign,self.year,self.publicKey)

class Server:
    def __init__(self, backlog=5, addr=('localhost', 8090)):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(addr)
        self.serverSocket.listen(backlog)
        
    number = 0
    def link_one_client(self,sent):
        self.s,self.sign,self.year,self.publicKey = sent
        clientSocket, addr = self.serverSocket.accept()

        print("Bob主机地址为：{}".format(addr))

        print("正在向服务器传送公钥")
        sendKey = pickle.dumps(self.publicKey)
        sendKeySha256 = hashlib.sha256(sendKey).hexdigest()
        clientSocket.send(pickle.dumps((sendKey, sendKeySha256)))

        while True:
            time.sleep(0.3)
            recvData = bytes_to_long(clientSocket.recv(1024))
            print("收到Bob发送的year：{}".format(recvData))
            d0 = recvData-self.year
            p = (self.s).encode()
            for _ in range(d0):
                p = hashlib.sha256(p).hexdigest().encode()

            sendData = pickle.dumps((p,self.sign))
            clientSocket.send(sendData)