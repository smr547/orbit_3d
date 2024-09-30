# binary_star_system.py
import os
import time
from solar_system_3d import SolarSystem, Sun, Planet

frame_rate = 15
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


def dump_results():
    while True:
        solar_system.read_positions_from_pipe(r)

def display_results():
    while True:

        start_time = time.time()  # 
        solar_system.read_positions_from_pipe(r)
        solar_system.draw_all()
        solar_system.draw_all_bodies()
        
        # throttle this loop to the frame rate
        display_time = time.time() - start_time 
        sleep_time = frame_interval - display_time 
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            actual_frame_rate = frame_rate
            if sleep_time != 0:
                actual_frame_rate = 1/display_time
            print("WARNING: frame rate ", int(actual_frame_rate), " try for ", frame_rate)



def compute_results():
    
    while True:
        # start_time = time.time()  # 
        solar_system.calculate_all_body_interactions()
        solar_system.move_all()
        solar_system.write_positions_to_pipe(w)

        # throttle this loop to the frame rate

        # sleep_time = frame_interval - (time.time() - start_time) 
        # if sleep_time > 0:
        #    time.sleep(sleep_time)

        


# solar system and display properties have been intialised...
# now we can fork -- child will do the computation and parent will do the display


r, w = os.pipe() 
pid = os.fork() 
if pid:  # parent does the displaying 
   os.close(w) 
   r = os.fdopen(r) 
   print ("Parent is displaying results pid ", os.getpid()) 
   print ("Child is computing results for ", len(solar_system.bodies), " bodies. pid: ", pid) 
   display_results()
   #dump_results()

else:  # child does the computation 
   os.close(r) 
   w = os.fdopen (w, 'w') 
   compute_results()
