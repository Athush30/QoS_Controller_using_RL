from agent import RLAgent
from packet_sniffer import capture_packet, extract_features
from qos_controller import apply_qos
from scapy.all import IP
import torch
import socket
from functools import lru_cache

# === Load Trained RL Agent ===
agent = RLAgent(state_size=3, action_size=3)
agent.model.load_state_dict(torch.load("/home/thusa/Downloads/rl/dqn_model.pt"))
agent.model.eval()

# === Known Services Mapping ===
KNOWN_SERVICES = {
    "1e100.net": "Google",
    "google": "Google",
    "youtube": "YouTube",
    "fbcdn.net": "Facebook CDN",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "twitter": "Twitter",
    "whatsapp": "WhatsApp",
    "netflix": "Netflix",
    "cloudflare": "Cloudflare",
    "amazonaws": "Amazon AWS",
    "amazon": "Amazon",
    "microsoft": "Microsoft",
    "office365": "Microsoft Office",
    "zoom": "Zoom",
    "discord": "Discord"
}

# === Cached DNS Lookup ===
@lru_cache(maxsize=1000)
def identify_service(dst_ip):
    try:
        hostname = socket.gethostbyaddr(dst_ip)[0].lower()
        for keyword, label in KNOWN_SERVICES.items():
            if keyword in hostname:
                return label
        return hostname.split('.')[0].capitalize()
    except:
        return "Unknown"

# === Compute Reward Based on Feature Heuristics ===
def compute_reward(features, action):
    pkt_size = features[1]  # Assuming feature[1] = packet length
    reward = 1000 / (pkt_size + 1)
    return reward

# === Main Packet Handler ===
def handle(pkt):
    if IP in pkt:
        dst_ip = pkt[IP].dst
        service = identify_service(dst_ip)
        print(f"[🌐] Packet to: {dst_ip} → Service: {service}")

        # Extract features and act
        state = extract_features(pkt)
        action = agent.act(state)
        apply_qos(action)

        # Reward and online learning
        reward = compute_reward(state, action)
        agent.train_step(state, action, reward, state)

        print(f"[📊] QoS level: {action}, Reward: {reward:.2f}")

# === Start Capturing Packets ===
if __name__ == "__main__":
    print("📡 Listening for packets...")
    while True:
        capture_packet(handle)
