import random
from smart_home import SmartHomeController, EventLogger

def scenario(hour):
    """Deterministic demo: person at door at given hour."""
    return lambda: 15 if hour else 200

if __name__ == "__main__":
    logger = EventLogger("logs/demo_run.csv")

    # Scenario A: daytime visitor
    print("--- Scenario A: Daytime visitor (10:00) ---")
    a = SmartHomeController(logger, start_hour=10, door_distance_fn=lambda: 15,
                            indoor_distance_fn=lambda: 30,
                            smoke_fn=lambda: 100, temp_fn=lambda: 25.0)
    for _ in range(3): a.run_tick()

    # Scenario B: night intruder
    print("--- Scenario B: Night intruder (21:00) ---")
    b = SmartHomeController(logger, start_hour=21, door_distance_fn=lambda: 15,
                            indoor_distance_fn=lambda: 200,
                            smoke_fn=lambda: 100, temp_fn=lambda: 25.0)
    for _ in range(2): b.run_tick()

    # Scenario C: fire event
    print("--- Scenario C: Fire event ---")
    c = SmartHomeController(logger, start_hour=14,
                            smoke_fn=lambda: 850, temp_fn=lambda: 60.0)
    c.run_tick()

    print("\nLogged events saved to logs/demo_run.csv")