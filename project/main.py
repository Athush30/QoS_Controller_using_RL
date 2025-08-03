from agent import RLAgent
from env import QoSEnv
import torch

EPISODES = 1000

def train():
    env = QoSEnv()
    agent = RLAgent(state_size=3, action_size=3)
    for ep in range(EPISODES):
        state = env.reset()
        for _ in range(10):
            action = agent.act(state)
            next_state, reward, _ = env.step(action)
            agent.train_step(state, action, reward, next_state)
            state = next_state
        if ep % 100 == 0:
            print(f"Episode {ep} complete")
    torch.save(agent.model.state_dict(), "/home/thusa/Downloads/rl/dqn_model.pt")

if __name__ == "__main__":
    train()
