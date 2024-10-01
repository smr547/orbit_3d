# simple_solar_system.py

from solar_system_3d import SolarSystem, Sun, Planet

solar_system = SolarSystem(400, projection_2d=True)

sun = Sun(solar_system)

planets = (
    Planet(
        solar_system,
        position=(150, 50, 0),
        velocity=(0, 5, 5),
    ),
    Planet(
        solar_system,
        mass=20,
        position=(100, -50, 150),
        velocity=(5, 0, 0)
    )
)

solar_system.run()
