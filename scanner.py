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