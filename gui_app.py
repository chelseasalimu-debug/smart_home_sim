import tkinter as tk
from tkinter import messagebox
import time
from smart_home import SmartHomeController, EventLogger

class SmartHomeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Security & Fire System")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")

        # Initialize the core logic
        self.logger = EventLogger()
        
        # We will use variables to control the sensors manually via the GUI
        self.door_dist = tk.IntVar(value=200)
        self.indoor_dist = tk.IntVar(value=200)
        self.smoke_val = tk.IntVar(value=100)
        self.temp_val = tk.DoubleVar(value=25.0)
        self.current_hour = tk.IntVar(value=10) # Start at 10 AM

        # Create the Controller using these dynamic variables
        self.ctrl = SmartHomeController(
            self.logger,
            door_distance_fn=lambda: self.door_dist.get(),
            indoor_distance_fn=lambda: self.indoor_dist.get(),
            smoke_fn=lambda: self.smoke_val.get(),
            temp_fn=lambda: self.temp_val.get(),
            start_hour=self.current_hour.get()
        )

        self.setup_ui()
        self.update_loop()

    def setup_ui(self):
        # --- Title ---
        title = tk.Label(self.root, text="🏠 Smart Home Dashboard", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=10)

        # --- Time Control ---
        time_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        time_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(time_frame, text="Simulated Time:", fg="white", bg="#34495e", font=("Arial", 12)).pack(side="left", padx=10)
        self.time_label = tk.Label(time_frame, text="10:00 (Day)", fg="#f1c40f", bg="#34495e", font=("Arial", 12, "bold"))
        self.time_label.pack(side="left")
        tk.Button(time_frame, text="Toggle Day/Night", command=self.toggle_time, bg="#3498db", fg="white").pack(side="right", padx=10)

        # --- Sensors & Actuators Display ---
        display_frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Security Section
        sec_frame = tk.LabelFrame(display_frame, text="Security & Lighting", bg="#ecf0f1", font=("Arial", 12, "bold"))
        sec_frame.pack(fill="x", pady=10)
        
        self.door_status = tk.Label(sec_frame, text="Door: CLOSED", fg="red", bg="#ecf0f1", font=("Arial", 12))
        self.door_status.pack(anchor="w", padx=10, pady=2)
        self.light_status = tk.Label(sec_frame, text="Light: OFF", fg="gray", bg="#ecf0f1", font=("Arial", 12))
        self.light_status.pack(anchor="w", padx=10, pady=2)

        # Fire Section
        fire_frame = tk.LabelFrame(display_frame, text="Fire Detection", bg="#ecf0f1", font=("Arial", 12, "bold"))
        fire_frame.pack(fill="x", pady=10)
        
        self.alarm_status = tk.Label(fire_frame, text="Alarm: OFF", fg="gray", bg="#ecf0f1", font=("Arial", 12))
        self.alarm_status.pack(anchor="w", padx=10, pady=2)
        self.fan_status = tk.Label(fire_frame, text="Exhaust Fan: OFF", fg="gray", bg="#ecf0f1", font=("Arial", 12))
        self.fan_status.pack(anchor="w", padx=10, pady=2)
        self.sprinkler_status = tk.Label(fire_frame, text="Sprinkler: OFF", fg="gray", bg="#ecf0f1", font=("Arial", 12))
        self.sprinkler_status.pack(anchor="w", padx=10, pady=2)

        # --- Controls ---
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(control_frame, text="👤 Person at Door", command=self.person_at_door, bg="#e67e22", fg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="🚶 Person Indoors", command=self.person_indoors, bg="#2ecc71", fg="white", width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="🔥 Trigger Fire", command=self.trigger_fire, bg="#e74c3c", fg="white", width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="🔄 Reset Sensors", command=self.reset_sensors, bg="#95a5a6", fg="white", width=15).grid(row=1, column=1, padx=5, pady=5)

    def toggle_time(self):
        if self.current_hour.get() == 10:
            self.current_hour.set(21)
            self.ctrl.clock.hour = 21
            self.time_label.config(text="21:00 (Night)", fg="#9b59b6")
        else:
            self.current_hour.set(10)
            self.ctrl.clock.hour = 10
            self.time_label.config(text="10:00 (Day)", fg="#f1c40f")

    def person_at_door(self):
        self.door_dist.set(15)
        self.root.after(3000, lambda: self.door_dist.set(200)) # Reset after 3 seconds

    def person_indoors(self):
        self.indoor_dist.set(30)
        self.root.after(5000, lambda: self.indoor_dist.set(200)) # Reset after 5 seconds

    def trigger_fire(self):
        self.smoke_val.set(850)
        self.temp_val.set(65.0)

    def reset_sensors(self):
        self.door_dist.set(200)
        self.indoor_dist.set(200)
        self.smoke_val.set(100)
        self.temp_val.set(25.0)
        self.ctrl.alarm.silence()

    def update_loop(self):
        # 1. Run the logic tick (without advancing the clock automatically so we control it)
        self.ctrl.run_tick()

        # 2. Update GUI Colors/Text based on actuator states
        # Door
        if self.ctrl.door.open:
            self.door_status.config(text="Door: OPEN", fg="#27ae60")
        else:
            self.door_status.config(text="Door: CLOSED", fg="#c0392b")

        # Light
        if self.ctrl.light.on:
            self.light_status.config(text="Light: ON", fg="#27ae60")
        else:
            self.light_status.config(text="Light: OFF", fg="gray")

        # Fire Systems
        if self.ctrl.alarm.active:
            self.alarm_status.config(text="Alarm: ACTIVE! 🚨", fg="#c0392b")
        else:
            self.alarm_status.config(text="Alarm: OFF", fg="gray")

        if self.ctrl.fan.on:
            self.fan_status.config(text="Exhaust Fan: ON", fg="#27ae60")
        else:
            self.fan_status.config(text="Exhaust Fan: OFF", fg="gray")

        if self.ctrl.sprinkler.on:
            self.sprinkler_status.config(text="Sprinkler: ON 💦", fg="#2980b9")
        else:
            self.sprinkler_status.config(text="Sprinkler: OFF", fg="gray")

        # 3. Loop every 500ms
        self.root.after(500, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeGUI(root)
    root.mainloop()