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

#Configure config.txt using simple dialog
def setup_conf():
    
    ip_list = []
    port_list = []
    t = simpledialog.askstring("Config helper", "Set scan time spacing [s]:")
    r = simpledialog.askstring("Config helper", "Set nubmer of first and last port to scan [separate by space]:")
    if t == None:
        return 0
    i = int(simpledialog.askstring("Config helper", "How many hosts do you want to scan:"))
    for x in range(i):
        ip_list.append(simpledialog.askstring("Config helper", f'Enter ip address of the host nr {x+1}:'))
        port_list.append(simpledialog.askstring("Config helper", f'Enter the port numbers that should remain open [separated by space button]:'))
    
    
    with open(config, 'w') as file:
        file.write('#This is configuration file, use the following structure:\n#[scan interval in seconds]\n#port-range [first port number] [last port number]\n')
        file.write('#Host[id] [ip address] [ports allowed]  e.g.\n#\n#90\n#port-range 1 1024\n#Host0 192.168.1.1 22 443\n#\n')
        file.write(f'{t}\n')
        file.write(f'port-range {r}\n')
        for x in range(i):
            file.write(f'Host{x} {ip_list[x]} {''.join(map(str, port_list[x]))}\n')
    file.close
    
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

def menu():
    
    global root
    root = tk.Tk()
    root.title("ACTIVE OPEN PORT SCANNER")

    label1 = tk.Label(root, text="PATRYK KOCIOL'S PORT SCANNER", font=("Arial", 16))
    label1.pack(pady=10)
    label2 = tk.Label(root, text="Make sure you are connected and have the right to scan the specified hosts", font=("Arial", 12))
    label2.pack(pady=5)
    label3 = tk.Label(root, text="Configuration can be also done inside config.txt file", font=("Arial", 12))
    label3.pack(pady=5)

    button1 = tk.Button(root, text="Setup configuration", command=setup_conf)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="Start scanning", command=scan)
    button2.pack(pady=10)

    root.mainloop()

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
        
    root.after(1000*int(scan_interval), scan)
    
if __name__ == "__main__":
    menu()

# Made by Patryk Kocioł @PatPalCoder