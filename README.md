
# 🧠 Real-Time QoS Controller with Reinforcement Learning 🚀

This project implements a **Reinforcement Learning (RL)**-based **Quality of Service (QoS)** controller that dynamically manages bandwidth allocation on a Linux network interface. It uses a **Deep Q-Network (DQN)** agent to analyze **live network performance** (delay, loss, bandwidth) and apply **traffic shaping rules** using Linux `tc`.

---

## 📌 Overview

The QoS controller interacts with a real-time environment where it:

🔎 **Measures**:
- Ping delay and packet loss to various IPs (Google, Cloudflare, local devices, etc.)
- Available bandwidth using `iperf3`

🧠 **Learns**:
- How to adjust traffic shaping rules (high/med/low bandwidth) using DQN
- Improves behavior based on rewards calculated from delay and loss

⚙️ **Controls**:
- Network interface shaping using Linux `tc`
- Adapts bandwidth limits dynamically during deployment

---

## ✨ Features

✅ Real-time environment using ping + iperf3  
✅ Deep Q-Network (DQN) RL agent  
✅ Reward feedback from network performance (delay, loss, bandwidth)  
✅ Dynamic QoS enforcement using Linux `tc`  
✅ Modular and clean code structure  
✅ Extendable to handle packet-level decisions, traffic types, or advanced QoS

---

## 🛠️ Requirements

**Python:** 3.8+  
**Dependencies:**
- `numpy`
- `torch`
- `subprocess` (standard)
- `json` (standard)
- `iperf3` installed on system

**System:**
- Linux OS with `tc` (`sudo apt install iproute2`)
- Network interface (e.g., `eth0`, configurable)

**Optional:**
- iPerf3 server (default: `iperf.he.net`, or your own)

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/rl-qos-controller.git
cd rl-qos-controller

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install tc if not available
sudo apt-get install iproute2

# 4. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate
```

---

## 📁 Project Structure

```
project/
├── env.py              # Simulated environment for training
├── utils.py            # Helper functions for simulation & rewards
├── agent.py            # DQN-based RL agent implementation
├── main.py             # Training script
├── qos_controller.py   # QoS logic with tc commands
├── packet_sniffer.py   # Packet capture & feature extraction
└── deploy.py           # Real-time deployment using trained model 
```

---

## 🚀 Usage

### 📊 Train the RL Agent
```bash
python main.py
```
- Trains over 1000 episodes
- Uses live network metrics as environment
- Adjusts `tc` QoS settings per action
- Model saved as `model.pt`

### 🧠 Example Reward Logic

- **+1** if delay improves and loss < 2%  
- **0** if delay stable and loss reasonable  
- **-1** if delay worsens or high packet loss

---

## 🔧 Customization

- **Change interface:** in `env.py`, e.g., `iface='wlan0'`
- **Add targets:** edit `self.targets` in `RealQoSEnv`
- **Change reward rules:** edit `compute_reward()`
- **Log training:** add `CSV` or `JSON` logger in `main.py`

---

## 🔮 Potential Improvements

- Add jitter, RTT variance, or real packet features (via Scapy)
- Deploy agent on live routers or IoT gateways
- One-hot encode traffic types as part of RL state
- Train using simulator (Mininet) and then apply to real-time
- Add GUI or monitoring dashboard

---

## ⚙️ Example Target Set

- `8.8.8.8` – Google DNS  
- `1.1.1.1` – Cloudflare  
- `192.168.1.1` – Local Router  
- `www.youtube.com` – Streaming traffic  
- `192.168.1.50` – IoT Device  

---

## 📝 License

This project is licensed under the **MIT License**. See the LICENSE file for details.

---

## 🌐 Happy networking🚦📡
