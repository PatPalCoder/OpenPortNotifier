import socket
import os
import platform
from plyer import notification
import tkinter as tk
from tkinter import simpledialog

cd = os.path.dirname(__file__)
config= os.path.join(cd, "config.txt")
log = os.path.join(cd, "log.txt")
icon = os.path.join(cd, "icon.ico") if platform.system() == 'Windows' else None

host_ip = []
ports_opened = []
scan_interval = 90 

#Notifying unauthorized open ports using system notifications & log.txt file
def warning(ports,host):
    
    with open(log, 'a') as file:
        file.write(f'{host} {', '.join(map(str, ports))}\n')
    file.close
    
    notification.notify(
        title='Security Warning',
        message=f'Ports opened without permission \n{', '.join(map(str, ports))} @ {host}',
        app_icon=icon ,  
        timeout=10, 
    )
    
def read_conf():
    
    temp = []
    with open(config, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n','')
            if line.startswith("#") or not line:
                continue
            elif line[0].isdigit():
                temp = line.split(' ')
                scan_interval = temp[0]
                temp = []
            elif line.startswith('port-range'):
                temp = line.split(' ')
                p_range_first = temp[1]
                p_range_last = temp[2]
                temp = []
            elif line.startswith('Host'):
                temp = line.split(' ')
                host_ip.append(temp[1])
                del temp[0:2]
                ports_opened.append(temp)
                temp = []
            else:
                continue
    file.close 
    return scan_interval, p_range_first, p_range_last, host_ip, ports_opened

#Perform sock.connect to see if host respond at given port
def scan():
    
    scan_interval, p_range_first, p_range_last, host_ip, ports_opened = read_conf()
    sock = socket.socket()
    
    for ip in host_ip:
        temp = []
        for p in range(int(p_range_first),int(p_range_last)):
            try:
                
                sock.connect((ip,p))
                sock.close
                temp.append(p)
            except:
                pass
        for el in ports_opened[host_ip.index(ip)]:
            if el in temp:
                temp.remove(el)
        if temp:
            warning(temp,ip)
        temp = []