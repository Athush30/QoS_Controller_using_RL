import subprocess
import time
import json
import os
import random

class RealQoSEnv:
    def __init__(self, iface='eth0', iperf_server='iperf.he.net'):
        self.iface = iface
        self.iperf_server = iperf_server

        # List of (IP/domain, traffic type)
        self.targets = [
            ("8.8.8.8", "dns"),              # Google DNS
            ("1.1.1.1", "dns"),              # Cloudflare DNS
            ("208.67.222.222", "dns"),       # OpenDNS
            ("192.168.1.1", "lan"),          # Local Router
            ("192.168.1.50", "iot"),         # Local IoT device
            ("www.youtube.com", "video"),    # Streaming
            ("www.netflix.com", "video"),    # Streaming
            ("www.facebook.com", "social"),  # Social media
            ("twitter.com", "social"),       # Social media
            ("www.github.com", "dev"),       # Developer platform
            ("stackoverflow.com", "dev"),    # Developer Q&A
            ("172.217.168.206", "web"),      # Google.com IP
            ("13.107.21.200", "web"),        # Microsoft.com IP
        ]

        self.current_target = random.choice(self.targets)
        self.state = self.get_network_state()

    def reset(self):
        self.current_target = random.choice(self.targets)  # Pick new target every episode
        self.state = self.get_network_state()
        print(f"[Episode] Target = {self.current_target[0]} ({self.current_target[1]})")
        return self.state

    def step(self, action):
        self.apply_qos(action)
        delay_before = self.state[1]
        time.sleep(2)  # wait for QoS to take effect

        next_state = self.get_network_state()
        delay_after = next_state[1]
        packet_loss = next_state[2]

        reward = self.compute_reward(delay_before, delay_after, packet_loss)
        self.state = next_state
        done = False
        return next_state, reward, done

    def get_network_state(self):
        ip, traffic_type = self.current_target
        delay, loss = self.measure_ping(ip)
        bandwidth = self.measure_bandwidth()
        # You could one-hot encode traffic_type here if desired
        return [bandwidth, delay, loss]

    def measure_ping(self, host):
        try:
            # Send 10 pings, get statistics
            result = subprocess.run(["ping", "-c", "10", host], capture_output=True, text=True, timeout=15)
            output = result.stdout

            # Extract avg delay (ms)
            avg_line = [line for line in output.splitlines() if "rtt min/avg/max" in line]
            if avg_line:
                avg_delay_ms = float(avg_line[0].split("/")[4])
                avg_delay = avg_delay_ms / 1000.0  # convert ms to seconds
            else:
                avg_delay = 1.0

            # Extract packet loss percentage
            loss_line = [line for line in output.splitlines() if "packet loss" in line]
            if loss_line:
                loss_percent = float(loss_line[0].split('%')[0].split()[-1]) / 100.0
            else:
                loss_percent = 1.0

            return avg_delay, loss_percent
        except Exception as e:
            print(f"[Ping Error] {e}")
            return 1.0, 1.0

    def measure_bandwidth(self):
        try:
            # Run iperf3 test for 5 seconds
            result = subprocess.run(
                ["iperf3", "-c", self.iperf_server, "-J", "-t", "5"],
                capture_output=True, text=True, timeout=15
            )
            data = json.loads(result.stdout)
            bps = data['end']['sum_received']['bits_per_second']
            mbps = round(bps / 1_000_000, 2)
            return mbps
        except Exception as e:
            print(f"[iPerf3 Error] {e}")
            return 0.0

    def apply_qos(self, action):
        # Remove existing rules to avoid conflicts
        os.system(f"sudo tc qdisc del dev {self.iface} root 2>/dev/null")

        # Map actions to bandwidth limits
        if action == 0:
            rate = "1mbit"
        elif action == 1:
            rate = "5mbit"
        elif action == 2:
            rate = "10mbit"
        else:
            rate = "5mbit"  # default fallback

        print(f"[QoS] Setting bandwidth limit: {rate}")
        os.system(f"sudo tc qdisc add dev {self.iface} root tbf rate {rate} burst 32kbit latency 400ms")

    def compute_reward(self, delay_before, delay_after, loss):
        if delay_after < delay_before and loss < 0.02:
            return 1
        elif delay_after > delay_before or loss > 0.05:
            return -1
        else:
            return 0
