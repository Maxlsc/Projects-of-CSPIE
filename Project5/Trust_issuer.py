import threading

from Server import Server

print("欢迎使用服务端程序！")

server = Server()
server.link_one_client()