from scapy.all import sniff

def extract_features(pkt):
    size = len(pkt)
    proto = 0 if pkt.haslayer('TCP') else 1
    port = 0
    if pkt.haslayer('TCP') or pkt.haslayer('UDP'):
        dport = pkt.dport
        if dport <= 1023:
            port = 0
        elif dport <= 49151:
            port = 1
        else:
            port = 2
    return [size, proto, port]

def capture_packet(callback):
    sniff(prn=callback, store=0, count=1)
