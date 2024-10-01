# solar_system_3d.py

import os
import time
import itertools
import math
import matplotlib.pyplot as plt

from vectors import Vector

class SolarSystem:
    def __init__(self, size, projection_2d=False, frame_rate=15):
        self.size = size
        self.projection_2d = projection_2d
        self.frame_rate = frame_rate
        self.bodies = []

        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(self.size / 50, self.size / 50),
        )
        if self.projection_2d:
            self.ax.view_init(10, 0)
        else:
            self.ax.view_init(0, 0)
        self.fig.tight_layout()

    def add_body(self, body):
        body.no = len(self.bodies)
        self.bodies.append(body)

    def move_all(self):
        for body in self.bodies:
            body.move()

    def draw_all_bodies(self):
        self.bodies.sort(key=lambda item: item.position[0])
        for body in self.bodies:
            #body.move()
            body.draw()
        self.bodies.sort(key=lambda item: item.no)

    def read_positions_from_pipe(self, aPipe):
        active_bodies = set() 
        while True:
            rec = aPipe.readline().strip()
            if len(rec) == 0:
                break
            fields = rec.split(',')
            bodyNo = int(fields[0])
            active_bodies.add(bodyNo)
            self.bodies[bodyNo].position = (float(fields[1]), float(fields[2]), float(fields[3]))

        # check if any bodies have been deleted by the computation engine and remove from display

        if (len(active_bodies) == len(self.bodies)):
            return  # nothing has been delete by the computation engine
        for i in range(len(self.bodies)-1, 0, -1):
            if self.bodies[i].no not in active_bodies:
                self.bodies.pop(i)

    def write_positions_to_pipe(self, aPipe):
        for body in self.bodies:
            body.write_position_to_pipe(aPipe)
        aPipe.write("\n")  # blank line indicates end of this frame of data
        aPipe.flush()

    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        if self.projection_2d:
            self.ax.xaxis.set_ticklabels([])
            self.ax.yaxis.set_ticklabels([])
            self.ax.zaxis.set_ticklabels([])
        else:
            self.ax.axis(False)
        plt.pause(0.001)
        self.ax.clear()

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)

    def display_results(self, r):
        while True:

            start_time = time.time()  # 
            self.read_positions_from_pipe(r)
            self.draw_all()
            self.draw_all_bodies()
        
            # throttle this loop to the frame rate
            display_time = time.time() - start_time 
            sleep_time = (1 / self.frame_rate) - display_time 
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                actual_frame_rate = self.frame_rate
                if sleep_time != 0:
                    actual_frame_rate = 1/display_time
                print("WARNING: frame rate ", int(actual_frame_rate), " try for ", self.frame_rate)

    def compute_results(self, w):
        while True:
            self.calculate_all_body_interactions()
            self.move_all()
            self.write_positions_to_pipe(w)

    def run(self):
        r, w = os.pipe() 
        pid = os.fork() 
        if pid:  # parent does the displaying 
            os.close(w) 
            r = os.fdopen(r) 
            print ("Parent is displaying results pid ", os.getpid()) 
            print ("Child is computing results for ", len(self.bodies), " bodies. pid: ", pid) 
            self.display_results(r)
            #dump_results()

        else:  # child does the computation 
            os.close(r) 
            w = os.fdopen (w, 'w') 
            self.compute_results(w)

class SolarSystemBody:
    min_display_size = 10
    display_log_base = 1.3

    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0, 0),
        velocity=(0, 0, 0)):

        self.no = 0
        self.solar_system = solar_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(*velocity)
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        self.colour = "black"

        self.solar_system.add_body(self)

    def move(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2],
        )

    def write_position_to_pipe(self, aPipe):
        rec = '{n:d},{x:f},{y:f},{z:f}\n'.format(n=self.no, x=self.position[0], y=self.position[1], z=self.position[2])
        aPipe.write(rec)

    def draw(self):
        self.solar_system.ax.plot(
            *self.position,
            marker="o",
            markersize=self.display_size + self.position[0] / 30,
            color=self.colour
        )
        if self.solar_system.projection_2d:
            self.solar_system.ax.plot(
                self.position[0],
                self.position[1],
                -self.solar_system.size / 2,
                marker="o",
                markersize=self.display_size / 2,
                color=(.5, .5, .5),
            )

    def accelerate_due_to_gravity(self, other):
        # print("computing for ",self," and ", other)
        distance = Vector(*other.position) - Vector(*self.position)
        distance_mag = distance.get_magnitude()

        force_mag = self.mass * other.mass / (distance_mag ** 2)
        force = distance.normalize() * force_mag

        reverse = 1
        for body in self, other:
            acceleration = force / body.mass
            body.velocity += acceleration * reverse
            reverse = -1

class Sun(SolarSystemBody):
    def __init__(
        self,
        solar_system,
        mass=10_000,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
    ):
        super(Sun, self).__init__(solar_system, mass, position, velocity)
        self.colour = "yellow"

class Planet(SolarSystemBody):
    colours = itertools.cycle([(1, 0, 0), (0, 1, 0), (0, 0, 1)])

    def __init__(
        self,
        solar_system,
        mass=10,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
    ):
        super(Planet, self).__init__(solar_system, mass, position, velocity)
        self.colour = next(Planet.colours)
