import threading
import paramiko
import subprocess
def ssh_command(ip,user,passwd,command):
    client=paramiko.SSHClient()
    client.set_missing_host_keys_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=passwd)
    ssh_session=client.get_transport().open_session()
    if ssh_session.active:
        print(ssh_session.recv(1024))
    return 
    