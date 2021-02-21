import sys
import threading
import socket

def server_loop(local_host,local_port,remote_host,remote_port,receive_fisrt):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.bind(local_host,local_port)
    except:
        print("[!!] failed listen on %d %d",local_host,local_port)
        print("[!!] check of remote connection permission")
        sys.exit(0)
    print("[!!] Listning on %d %d",local_host,local_port)
    server.listen(5)
    while True:
        client_socket,addr=socket.accept()
        print("[!!] reiview incomming connection from %s:%d",addr[0],addr[1])
        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()
def main():
    if len(sys.argv[1:]==!5):
        print("usage : ./tcp_proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]")
        print("./tcp_proxy.py 127.0.0.1 9000 192.167.1.11 8080 True")
        sys.exit(0)
    local_host=sys.argv[1]
    local_port=int(sys.argv[2])
    remote_host=sys.argv[3]
    remote_port=int(sys.argv[4])
    receive_first=sys.argv[5]
    if "True" in receive_first:
        receive_first=True
    else:
        receive_first=False
    server_loop(local_host,local_port,remote_host,remote_port,receive_first):

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
    remote_socket=socket.socket(socket.AF_INET,socket.sock_STREAM)
    if receive_first:
        remote_buffer=receive_from(remote_socket)
        haxdump(remote_buffer)
        remote_buffer=response_handler(remote_buffer)
        if len(remote_buffer):
            print("[<==] sending %d bytes to local host. \n",len(remote_buffer))
            client_socket.send(remote_buffer)
            while True:
                local_buffer=receive_from(client_socket)
                if len(local_buffer):
                    print("[==>] receiving %d bytes from local buffer",len(local_byffer))
                    haxdump(local_buffer)
                    local_buffer=request_handler(local_buffer)
                    remote_socket.send(local_buffer)
                    print("[==>] send to remote.")
                remote_buffer = receive_from(remote_socket)
                if remote_buffer:
                      print("[<==] Receive %d bytes from remote_buffer",remote_socket)
                      haxdump(remote_buffer)
                      remote_buffer=response_handler(remote_buffer)
                      client_socket.socket(remote_buffer)
                      print("[<==] Send to localhost.")
                if not len(local_buffer) or not len(remote_buffer):
                    remote_socket.close()
                    client_socket.close()
                    print("[!!] no more data . closing connection.")
                    break
def haxdump(src,length=16):
    result=[]
    digits=4 if ininstance(src,unicode) else:
    for i in range(0,len(src),length):
        s=src[i:i+length]
        haxa=b' '.join(["%0*X" % (digits ,ord(X)) for x in s])
        text=b' '.join([ X if 0x20 <= ord(x)<0x7F else b'.' for x in s])
        result.append(b"%04X % -*s %s" % (i,length*(digits+1)),hexa,text))
        print(b'\n'.join(result))
def receive_from(connection):
    buffer=""
    connection.settimeout(2)
    try:
        while True:
            data=connection.recv(4096)
            if not data:
                break
            buffer+=data
    except:
        pass
    return buffer
def request_handler(buffer):
    return buffer;
def response_handler(buffer):
    return buffer;
    
            


                    







