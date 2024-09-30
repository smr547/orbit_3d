# binary_star_system.py

import time
from solar_system_3d import SolarSystem, Sun, Planet

frame_rate = 20
frame_interval = 1 / frame_rate
report_rate_frames = frame_rate

solar_system = SolarSystem(800, projection_2d=True)

suns = (
    Sun(solar_system, position=(40, 40, 40), velocity=(6, 0, 6)),
    Sun(solar_system, position=(-40, -40, 40), velocity=(-6, 0, -6)),
)

planets = (
    Planet(
        solar_system,
        10,
        position=(100, 100, 0),
        velocity=(0, 5.5, 5.5),
    ),
    Planet(
        solar_system,
        20,
        position=(0, 0, 0),
        velocity=(-11, 11, 0),
    ),
)

spawn_time = time.time()
frames_since_last_report = 0
total_sleep_time = 0
sleeps = 0

while True:
    frame_start_time = time.time()

    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
    solar_system.draw_all()

    loop_time = time.time() - frame_start_time
    if loop_time < frame_interval:
        sleep_time = frame_interval - loop_time
        time.sleep(sleep_time)
        total_sleep_time += sleep_time
        sleeps += 1

    frames_since_last_report += 1
    if frames_since_last_report >= report_rate_frames:
        idle_percent = total_sleep_time * 100 / (frame_interval * report_rate_frames)
        print(int(idle_percent), " %idle CPU", end="\r")
        frames_since_last_report = 0
        total_sleep_time = 0
        sleeps = 0
