import csv
import os
from datetime import datetime

class EventLogger:
    def __init__(self, path=None):
        self.path = path
        self.events = []
        if path and not os.path.exists(path):
            with open(path, "w", newline="") as f:
                csv.writer(f).writerow(["tick", "hour", "component", "action", "detail"])

    def log(self, tick, hour, component, action, detail=""):
        row = [tick, f"{hour:02d}:00", component, action, detail]
        self.events.append(row)
        if self.path:
            with open(self.path, "a", newline="") as f:
                csv.writer(f).writerow(row)

# ---------- Actuators ----------
class Door:
    def __init__(self, logger, tick_ref):
        self.open = False; self.logger = logger; self.tick_ref = tick_ref
    def open_door(self):
        if not self.open:
            self.open = True
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Door", "OPEN", "")
    def close_door(self):
        if self.open:
            self.open = False
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Door", "CLOSE", "")

class Light:
    def __init__(self, logger, tick_ref):
        self.on = False; self.logger = logger; self.tick_ref = tick_ref
    def turn_on(self):
        if not self.on:
            self.on = True
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Light", "ON", "")
    def turn_off(self):
        if self.on:
            self.on = False
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Light", "OFF", "")

class Alarm:
    def __init__(self, logger, tick_ref):
        self.active = False; self.logger = logger; self.tick_ref = tick_ref
    def sound(self, reason):
        if not self.active:
            self.active = True
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Alarm", "SOUND", reason)
    def silence(self):
        if self.active:
            self.active = False
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Alarm", "SILENCE", "")

class Fan:
    def __init__(self, logger, tick_ref):
        self.on = False; self.logger = logger; self.tick_ref = tick_ref
    def start(self):
        if not self.on:
            self.on = True
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Fan", "ON", "")
    def stop(self):
        if self.on:
            self.on = False
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Fan", "OFF", "")

class Sprinkler:
    def __init__(self, logger, tick_ref):
        self.on = False; self.logger = logger; self.tick_ref = tick_ref
    def activate(self):
        if not self.on:
            self.on = True
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Sprinkler", "ON", "")
    def deactivate(self):
        if self.on:
            self.on = False
            self.logger.log(self.tick_ref[0], self.tick_ref[1], "Sprinkler", "OFF", "")

# ---------- Sensors ----------
class Clock:
    def __init__(self, start_hour=10): self.hour = start_hour
    def tick(self): self.hour = (self.hour + 1) % 24
    def is_night(self): return self.hour >= 19 or self.hour < 6

class UltrasonicSensor:
    def __init__(self, distance_fn=None):
        self.distance_fn = distance_fn or (lambda: 200)
    def read(self): return self.distance_fn()

class FireSensor:
    def __init__(self, smoke_fn=None, temp_fn=None):
        self.smoke_fn = smoke_fn or (lambda: 100)
        self.temp_fn = temp_fn or (lambda: 25.0)
    def read(self): return self.smoke_fn(), self.temp_fn()

# ---------- Controller ----------
class SmartHomeController:
    def __init__(self, logger, door_distance_fn=None, indoor_distance_fn=None,
                 smoke_fn=None, temp_fn=None, start_hour=10):
        self.logger = logger
        self.tick_ref = [0, start_hour]  # [tick_count, hour]
        self.clock = Clock(start_hour)
        self.door_sensor = UltrasonicSensor(door_distance_fn)
        self.indoor_sensor = UltrasonicSensor(indoor_distance_fn)
        self.fire_sensor = FireSensor(smoke_fn, temp_fn)
        self.door = Door(logger, self.tick_ref)
        self.light = Light(logger, self.tick_ref)
        self.alarm = Alarm(logger, self.tick_ref)
        self.fan = Fan(logger, self.tick_ref)
        self.sprinkler = Sprinkler(logger, self.tick_ref)
        self.smoke_threshold = 600
        self.temp_threshold = 45.0
        self.motion_timeout = 3
        self.no_motion_counter = 0

    def security_logic(self):
        if self.door_sensor.read() < 20:
            if self.clock.is_night():
                self.alarm.sound("Night intrusion at door")
                self.door.close_door()
            else:
                self.door.open_door()
        else:
            self.door.close_door()

    def lighting_logic(self):
        if self.indoor_sensor.read() < 50:
            self.light.turn_on()
            self.no_motion_counter = 0
        else:
            self.no_motion_counter += 1
            if self.no_motion_counter >= self.motion_timeout:
                self.light.turn_off()

    def fire_logic(self):
        smoke, temp = self.fire_sensor.read()
        if smoke > self.smoke_threshold or temp > self.temp_threshold:
            self.alarm.sound("Fire detected")
            self.fan.start()
            self.sprinkler.activate()
        else:
            self.fan.stop()
            self.sprinkler.deactivate()

    def run_tick(self):
        self.tick_ref[0] += 1
        self.tick_ref[1] = self.clock.hour
        self.security_logic()
        self.lighting_logic()
        self.fire_logic()
        # Night alarm only silences when day returns
        if not self.clock.is_night() and "Night intrusion" in str(self.logger.events[-3:]):
            self.alarm.silence()
        self.clock.tick()