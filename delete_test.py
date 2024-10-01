# simple_solar_system.py

from solar_system_3d import SolarSystem, Sun, Planet

solar_system = SolarSystem(400, projection_2d=True)

sun = Sun(solar_system)

planets = (
    Planet(
        solar_system,
        position=(350, 0, 0),
        velocity=(-1, 0, 0),
    ),
)

solar_system.run()
