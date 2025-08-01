import random

def simulate_packet():
    return [random.uniform(64, 1500), random.choice([0, 1]), random.choice([0, 1, 2])]

def compute_reward(state, action):
    packet_size, protocol, port_cat = state
    if protocol == 1 and packet_size < 300 and port_cat == 0:
        return 1 if action == 0 else -1
    elif packet_size > 1000:
        return 1 if action == 2 else -1
    return 0.5 if action == 1 else -0.5
