import subprocess

def apply_qos(priority):
    iface = "wlp0s20f3"
    parent_class = "1:"
    base_cmd = ["tc", "class", "replace", "dev", iface, "parent", parent_class]

    # Setup root qdisc and base classes once (if not already present)
    subprocess.run(f"tc qdisc del dev {iface} root".split(), stderr=subprocess.DEVNULL)
    subprocess.run(f"tc qdisc add dev {iface} root handle 1: htb default 12".split())
    subprocess.run(f"tc class add dev {iface} parent 1: classid 1:1 htb rate 10mbit".split(), stderr=subprocess.DEVNULL)
    subprocess.run(f"tc class add dev {iface} parent 1: classid 1:2 htb rate 5mbit".split(), stderr=subprocess.DEVNULL)
    subprocess.run(f"tc class add dev {iface} parent 1: classid 1:3 htb rate 1mbit".split(), stderr=subprocess.DEVNULL)

    if priority == 0:
        cmd = base_cmd + ["classid", "1:1", "htb", "rate", "10mbit"]
    elif priority == 1:
        cmd = base_cmd + ["classid", "1:2", "htb", "rate", "5mbit"]
    elif priority == 2:
        cmd = base_cmd + ["classid", "1:3", "htb", "rate", "1mbit"]
    else:
        print("Invalid priority")
        return

    subprocess.run(cmd)
    print(f"[✓] Applied QoS for priority {priority}")
