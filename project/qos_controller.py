import os

def apply_qos(priority):
    if priority == 0:
        os.system("tc class change dev eth0 parent 1: classid 1:1 htb rate 10mbit")
    elif priority == 1:
        os.system("tc class change dev eth0 parent 1: classid 1:2 htb rate 5mbit")
    elif priority == 2:
        os.system("tc class change dev eth0 parent 1: classid 1:3 htb rate 1mbit")
