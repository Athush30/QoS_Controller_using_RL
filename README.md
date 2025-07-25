# 🧠 QoS Controller with Reinforcement Learning 🚀

This project implements a **Reinforcement Learning (RL)**-based **Quality of Service (QoS)** controller for network traffic management. It uses a **Deep Q-Network (DQN)** to classify network packets and dynamically assign QoS priorities to optimize bandwidth allocation. The system is trained in a simulated environment and deployed to process real network packets in real-time, applying bandwidth limits using Linux `tc` (traffic control) commands.

---

## 📌 Overview

The QoS Controller uses a **DQN-based RL agent** to classify network packets based on features such as packet size, protocol (TCP/UDP), and port category. The agent assigns one of three QoS priorities: 🟥 **High**, 🟨 **Medium**, and 🟦 **Low**. These priorities correspond to bandwidth limits enforced via `tc`.

🧪 Trained in simulation ➡️ 🚦 Deployed on real packets ➡️ 📉 Applies bandwidth control dynamically.

---

## ✨ Features

✅ Simulated environment for training RL agent  
✅ Real-time packet processing using Scapy  
✅ Dynamic QoS assignment with `tc` command  
✅ Online learning during live deployment  
✅ Modular and easy-to-understand code structure

---

## 🛠️ Requirements

**Python:** 3.8+  
**Dependencies:**

- `numpy`
- `torch`
- `scapy`

**System:**

- Linux OS with `tc` (traffic control)
- Network interface: `eth0` (configurable)

**Hardware:** Standard machine with network access

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/qos-rl-controller.git
cd qos-rl-controller

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install tc (if not already installed)
sudo apt-get install iproute2

# 4. (Optional) Setup a virtual environment
python -m venv venv
source venv/bin/activate
```

---

## 📁 Project Structure

```
qos-rl-controller/
├── env.py              # Simulated environment for training
├── utils.py            # Helper functions for simulation & rewards
├── agent.py            # DQN-based RL agent implementation
├── main.py             # Training script
├── qos_controller.py   # QoS logic with tc commands
├── packet_sniffer.py   # Packet capture & feature extraction
├── deploy.py           # Real-time deployment using trained model
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Usage

### 📊 Training the Model

```bash
python main.py
```

- Trains the RL agent over 1000 episodes
- Model saved as `model.pt`
- Progress printed every 100 episodes

### 🔧 Deploying the QoS Controller

```bash
sudo python deploy.py
```

⚠️ `sudo` is required for packet sniffing and applying `tc` rules.

- Captures real-time packets
- Classifies using the RL model
- Applies bandwidth control
- Logs QoS actions and rewards

---

## ⚙️ How It Works

### 🏋️‍♂️ Training Phase

- `env.py`: Simulates packets with features (size, protocol, port)
- `agent.py`: Deep Q-Network selects QoS action
- Rewards favor efficient classification (e.g., UDP + small size = high priority)
- Model saved as `model.pt`

### 🛰️ Deployment Phase

- `packet_sniffer.py`: Extracts live packet features
- `agent.py`: Loads model, selects QoS level
- `qos_controller.py`: Applies bandwidth via `tc`
- Logs actions and supports basic online learning

---

## 🔮 Potential Improvements

- Add real-time performance metrics (latency, congestion)
- Expand feature set (IP addresses, packet frequency)
- Implement DQN target network for stability
- Support multiple interfaces and finer QoS levels
- Better error handling and metrics visualization

---

## 📝 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

🌐 **Happy networking with ML!**
