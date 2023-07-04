from Client import Client,Server

print("Alice登入。")
client = Client()
server = Server()
sent = client.link_server()
server.link_one_client(sent)