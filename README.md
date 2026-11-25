# 🏠 Intelligent Home Security and Fire Detection System

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Arduino](https://img.shields.io/badge/Arduino-C++-teal.svg)
![Status](https://img.shields.io/badge/Tests-9%20Passed-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Project:** Intelligent Home Security and Fire Detection System  
**Author:** [Chelsea Salimu]  
**Course:** [Research Methods and Statistics]

## 📖 1. Introduction
With the advancement of technology, modern homes are becoming smarter by integrating automated systems that improve security, safety, and convenience. This project aims to design and develop a smart home model that uses sensors to monitor movement and detect fire hazards, while automatically responding to different situations.

This repository contains:
1.  **A Python-based simulation with a Graphical User Interface (GUI)** used to validate the system logic.
2.  **Arduino C++ source code** ready for deployment on physical hardware.
3.  **Automated tests and CSV logging** to provide reproducible evidence of the system's functionality.

## 🎯 2. Project Objectives
- To design a smart home model with motion detection.
- To develop a time-based automated door system.
- To implement an indoor automation system (lighting).
- To design a fire detection system using smoke and temperature sensors.
- To create an automated response system (alarm, ventilation, and sprinkler).

## ⚙️ 3. System Architecture & Methodology
The system is divided into three distinct subsystems:

### 🚪 3.1 Security System (Door Control)
- An ultrasonic sensor outside detects movement near the door.
- The system checks the time using a Real-Time Clock (RTC) logic.
- **During the day:** The door opens automatically via a servo motor.
- **At night (after 7 PM):** The door remains closed, and an alarm is triggered.

### 💡 3.2 Indoor Automation (Lighting)
- An ultrasonic/PIR sensor inside detects indoor movement.
- **Motion detected:** Lights turn ON automatically.
- **No motion detected:** Lights turn OFF after a predefined timeout to save energy.

### 🔥 3.3 Fire Detection and Response
- An MQ-2 smoke sensor and LM35 temperature sensor continuously monitor the environment.
- **When fire is detected:** 
  - A buzzer alarm is activated.
  - An exhaust fan turns ON to remove smoke.
  - A sprinkler water pump is activated to extinguish the fire.

---

## 💻 4. Software Simulation (Python GUI)

To safely test the logic without risking hardware damage, a Python simulation with a Tkinter GUI was developed.

### Prerequisites
- Python 3.x installed on your system.

### Installation & Execution
1. **Clone the repository:**
   ```bash
   git clone https://github.com/chelseasalimu-debug/smart_home_sim.git
   cd smart_home_sim
   Create and activate a virtual environment:
2. **Create and activate a virtual environment:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

3. **Install required packages:**
```bash
pip install pytest

4. **Run the GUI Dashboard:**
```bash
python gui_app.py
A visual dashboard will open. You can click buttons to simulate a person at the door, toggle day/night, or trigger a fire to see the automated responses in real-time.
