import numpy as np
from utils import simulate_packet, compute_reward

class QoSEnv:
    def __init__(self):
        self.state = simulate_packet()

    def reset(self):
        self.state = simulate_packet()
        return self.state

    def step(self, action):
        next_state = simulate_packet()
        reward = compute_reward(self.state, action)
        done = False
        self.state = next_state
        return next_state, reward, done
