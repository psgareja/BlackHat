import socket
import threading
blind_ip="0.0.0.0"
blind_port=9999
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((blind_ip,blind_port))
server.listen(5)
print("server is listning from %s port %s",(blind_ip,blind_port))
def handle_client(client_socket):
    requests=client_socket.recv(1024)
    print("received requesr"+requests)
    client_socket.send('ACK!')
    client_socket.close()
while True:
    client,addr=server.accept()
    print("accepted connection from %s:%d",(addr[0],addr[1]))
    client_handler=threading.Thread(target=handler_client,args=(client,))
    client_handler.close()