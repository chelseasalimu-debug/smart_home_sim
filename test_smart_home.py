import pytest
from smart_home import SmartHomeController, EventLogger

def make_controller(**kwargs):
    logger = EventLogger()  # in-memory
    return SmartHomeController(logger, **kwargs), logger

# ---------- Security tests ----------
def test_door_opens_during_day():
    ctrl, log = make_controller(start_hour=10, door_distance_fn=lambda: 15)
    ctrl.run_tick()
    assert ctrl.door.open is True

def test_door_stays_closed_and_alarms_at_night():
    ctrl, log = make_controller(start_hour=20, door_distance_fn=lambda: 15)
    ctrl.run_tick()
    assert ctrl.door.open is False
    assert ctrl.alarm.active is True
    assert any("Night intrusion" in row[4] for row in log.events)

def test_door_closes_when_no_one_near():
    ctrl, log = make_controller(start_hour=10, door_distance_fn=lambda: 200)
    ctrl.run_tick()
    assert ctrl.door.open is False

# ---------- Lighting tests ----------
def test_light_turns_on_with_motion():
    ctrl, log = make_controller(indoor_distance_fn=lambda: 30)
    ctrl.run_tick()
    assert ctrl.light.on is True

def test_light_turns_off_after_timeout():
    ctrl, log = make_controller(indoor_distance_fn=lambda: 200)
    for _ in range(ctrl.motion_timeout):
        ctrl.run_tick()
    assert ctrl.light.on is False

# ---------- Fire tests ----------
def test_smoke_triggers_all_fire_systems():
    ctrl, log = make_controller(smoke_fn=lambda: 800, temp_fn=lambda: 25.0)
    ctrl.run_tick()
    assert ctrl.alarm.active is True
    assert ctrl.fan.on is True
    assert ctrl.sprinkler.on is True

def test_high_temperature_triggers_fire_systems():
    ctrl, log = make_controller(smoke_fn=lambda: 100, temp_fn=lambda: 55.0)
    ctrl.run_tick()
    assert ctrl.fan.on is True
    assert ctrl.sprinkler.on is True

def test_no_fire_no_activation():
    ctrl, log = make_controller(smoke_fn=lambda: 100, temp_fn=lambda: 25.0)
    ctrl.run_tick()
    assert ctrl.fan.on is False
    assert ctrl.sprinkler.on is False
    assert ctrl.alarm.active is False

# ---------- CSV logging test ----------
def test_csv_log_records_events(tmp_path):
    path = tmp_path / "events.csv"
    logger = EventLogger(str(path))
    ctrl = SmartHomeController(logger, start_hour=10, door_distance_fn=lambda: 15)
    ctrl.run_tick()
    content = path.read_text()
    assert "Door,OPEN" in content