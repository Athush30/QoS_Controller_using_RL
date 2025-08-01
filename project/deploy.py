from agent import RLAgent
from packet_sniffer import capture_packet, extract_features
from qos_controller import apply_qos
import torch

# Initialize agent and load trained model
agent = RLAgent(state_size=3, action_size=3)
agent.model.load_state_dict(torch.load("model.pt"))
agent.model.eval()

def compute_reward(features, action):
    # Simple example: smaller packet size = higher reward
    # You can replace this logic with real-time latency, congestion, etc.
    pkt_size = features[1]  # Assuming feature[1] = packet length
    reward = 1000 / (pkt_size + 1)
    return reward

def handle(pkt):
    # 1. Extract features
    state = extract_features(pkt)

    # 2. Agent selects action
    action = agent.act(state)

    # 3. Apply QoS action
    apply_qos(action)

    # 4. Calculate reward (can be improved)
    reward = compute_reward(state, action)

    # 5. Train agent online
    next_state = state  # or update if available
    agent.train_step(state, action, reward, next_state)

    # 6. Log
    print(f"Packet classified. QoS level: {action}, Reward: {reward:.2f}")

if __name__ == "__main__":
    while True:
        capture_packet(handle)
