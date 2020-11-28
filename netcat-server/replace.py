import sys
import os
import socket
import getopt
import threading
import subprocess


listen=False
command=False
upload=False
execute=""
target=""
upload_destination=""
port=0


def usage():
    print("PPPPPPPPPPPPPPPPPP")
    print("PPPPPPPPPPPPPPPPPP")          
    print("PPPP          PPPP")
    print("PPPP          PPPP")
    print("PPPPPPPPPPPPPPPPPP")
    print("PPPPPPPPPPPPPPPPPP")
    print("PPPP")
    print("PPPP")
    print("PPPP")
    print("PPPP")
    print("PPPP")
    print('--------------------------------------')
    print("own light net tools")
    print(" ")
    print("Usage: replace.py -t target_host -p port")
    print("-l --listen                      -l listen on [host]:[port] for incoming connection")
    print("-e --execute=file_to_run - execute file upon recieving connection")
    print("-c --command initilize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file or write to destination")
    print()
    print()
    print("Example")
    print("...................................................................")
    print("replace.py -t 192.165.3.2 -p 90 -l -c")
    print("replace.py -t 192.165.3.2 -p 90 -l -c -u=:\\target.exe")
    print("replace.py -t 192.165.3.2 -p 90 -l -c -e=\"cat etc/passwd\"")
    print("echo 'ABCD' | ./replace.py -t 192.165.3.2 -p 90 -l -c")
    sys.exit(0)

def main():
    global listen
    global command
    
    global execute
    global target
    global upload_destination
    global port
    
    if not len(sys.argv[1:]):
        usage()
    try: 
        opt,args=getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ('-h','--help'):
            usage()
        elif o in ('-l','--listen'):
            listen=True
        elif o in ('-e','--execute'):
            execute=a
        elif o in ('-c','--commandshell'):
            command=True
        elif o in ('-u','--upload'):
           upload_destination=a


        elif o in ('-t','--target'):
            target=a
        elif o in ('-p','--port'):
            port=int(a)
        else:
            assert False,"Unhandle Option"
    if not listen and len(target) and port>0:
        buffer=sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()
main()        
def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        while True:
            recv_len=1
            response=""
            while recv_len:
                data=client.recv(4096)
                recv_len=len(data)
                response+=data

                if recv_len<4096:
                    break
            buffer=input("")
            buffer+="\n"
            client.send(buffer)

    except:
        print("[*] Exeption Existing")
        client.close()
def server_loop():
    global target
    if not len(target):
        target="0.0.0.0"
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    while True:
        client_socket,addr=server.accept()
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thared.start()
def run_command(command):
    command=command.rstrip()
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="Failed to execute command.\n\r"
    return output

def client_handler(client_socket):
    global upload
    global command
    global execute
    if len(upload_destination):
        file_buffer=""
        while True:
            data=client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
        try:
            file_descriptor=open(upload_descriptor,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send("Failed to save file %s\r\n"%upload_destination)

    if len(execute):
        output=run_command(execute)
        client_socket.send(output) 
    if command:
        while True:
            client_socket.send("<BHP:#>")
            #(enter key)
            cmd_buffer=" " 
            while "\n"  not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
            response=run_command(cmd_buffer)
            client_socket.send(response)



                

