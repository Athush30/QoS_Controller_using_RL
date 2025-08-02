import time
import subprocess
import random

class RealQoSEnv:
    def __init__(self):
        self.state = self.get_network_state()

    def reset(self):
        self.state = self.get_network_state()
        return self.state

    def step(self, action):
        # Apply QoS policy (here just simulated)
        self.apply_qos(action)

        delay_before = self.state[1]
        time.sleep(1.0)  # wait to let changes take effect

        next_state = self.get_network_state()
        delay_after = next_state[1]
        packet_loss = next_state[2]

        reward = self.compute_reward(delay_before, delay_after, packet_loss)
        self.state = next_state
        done = False
        return next_state, reward, done

    def get_network_state(self):
        delay = self.ping("8.8.8.8")
        bandwidth = self.simulate_bandwidth()      # Replace with iperf if needed
        packet_loss = self.simulate_packet_loss()  # Placeholder
        return [bandwidth, delay, packet_loss]

    def ping(self, host):
        try:
            result = subprocess.run(["ping", "-n", "1", host], capture_output=True, text=True, timeout=2)
            output = result.stdout
            if "Average" in output:
                delay_line = [line for line in output.splitlines() if "Average" in line][0]
                avg_delay = int(delay_line.split("Average = ")[1].replace("ms", "").strip())
                return avg_delay / 1000.0  # convert ms to seconds
            else:
                return 1.0  # Assume 1 second if unreachable
        except Exception:
            return 1.0

    def simulate_bandwidth(self):
        # Simulate or replace with iperf3 result in Mbps
        return round(random.uniform(0.5, 10.0), 2)

    def simulate_packet_loss(self):
        # Random packet loss simulation (0.0 - 0.1)
        return round(random.uniform(0.0, 0.05), 3)

    def apply_qos(self, action):
        # Simulate or apply QoS (e.g., using tc command or router API)
        # For now, just print
        qos_level = {0: "Low Priority", 1: "Medium Priority", 2: "High Priority"}
        print(f"Applying QoS action: {qos_level.get(action, 'Unknown')}")

    def compute_reward(self, delay_before, delay_after, packet_loss):
        if delay_after < delay_before and packet_loss < 0.02:
            return +1
        elif delay_after > delay_before:
            return -1
        else:
            return 0
