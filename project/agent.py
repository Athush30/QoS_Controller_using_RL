import torch
import torch.nn as nn
import torch.optim as optim
import random

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.model(x)

class RLAgent:
    def __init__(self, state_size, action_size, lr=0.001, gamma=0.95, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995

        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        with torch.no_grad():
            state = torch.FloatTensor(state)
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train_step(self, state, action, reward, next_state):
        state = torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state)
        target = self.model(state)
        with torch.no_grad():
            q_next = self.model(next_state)
        target[action] = reward + self.gamma * torch.max(q_next)
        predicted = self.model(state)

        loss = self.loss_fn(predicted, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
