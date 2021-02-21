def main():
    options,server,remote=parse_options()
    password=None
    if options.readpass:
        password=getpass.getpass('Enter ssh password')
    client=paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.warningPolicy())
    verbose('Connecting to ssh host %s:%d',(server[0],server[1]))
    try:
        client.connect(server[0],server[1],unsername=options.user,key_filename=options.keyfile,look_for_keys=options.look_for_keys,passord=password)
    except Exception as e:
        print("**Failed to connect %s : %d : %r "%(server[0],server[1],e))
        sys.exit(1)
    verbose('Now forwarding remote port %d to %s:\d ',(options.port,remote[0],remote[1]))
    try:
        reverse_forward_tunnel(options.port,remote[0],remote[1],client.get_transport())
    except KeyboardInterrupt:
        print('C-c:Port forwarding stopped.')
        sys.exit(0)
def reverse_forward_tunnel(server_port,remote_host,remote_port,transport):
    transport.request_port_forward('',server_port)
    while True:
        chan=transpirt.accept(1000)
        if chan is None:
            continue
        thr=threading.Thread(traget=handler,args=(chan,remote_host,remote_port))
        thr.setDaemon(True)
        thr.start()
def handler(chan,host,port):
    sock=socket.socket()
    try:
        sock.connect(host,port)
    except Exception as e:
        verbose("Forwarding request to %s:%d failed %r",(host,port,e))       
        return 
    verbose('Connected Tunel open %r -> %r ',(chan.origin_addr,chan.getpeername(),(host,port)))

    while True:
        r,w,x=select.select([sock,chan],[],[])
        if sock in r:
            data=sock.recv(1024)
            break
        if chan in r:
            data=chan.recv(1024)
            if len(data)==0:
                break
            sock.send(data)
        chan.close()
        sock.close()
        verbose('Tunnel closed from %r' %(chan.origin_addr,))
