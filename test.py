import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import numpy as np
import spiceypy as spice
import time
from Config import bodies_data as bd


# Load the SPICE Kernels
spice.furnsh(r"C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Data\Spice\Solar_sytem_kernel.tm")

# Do some test calculations

# Calculate the position of the Moon relative to the Earth in the J2000 ECI frame

# Set the start time of the simulation, using the time at the start of the J2000 epoch as an example
et = spice.str2et('2000-01-01T12:00:00') # Convert the time to ephemeris time

# Get the position of the Moon relative to the Earth in the J2000 ECI frame
start = time.perf_counter()
moon_state, _ = spice.spkezr('Moon', et, 'J2000', 'NONE', 'Earth')
end = time.perf_counter()
print(f'Time taken to calculate Moon position: {end - start} seconds')

# Get the moon constants
start = time.perf_counter()
moon_constants = spice.bodvrd('Moon', 'RADII', 3) # Returns r_eq, r_eq, r_polar (triaxial ellipsoid)
end = time.perf_counter()
print(f'Time taken to calculate Moon constants: {end - start} seconds')

# Extract the position and velocity vector from the state vector
moon_position = moon_state[:3]
moon_velocity = moon_state[3:]

# Test the acceleration function logic
start = time.perf_counter()
body = 'Earth'
body_data = getattr(bd, body)
mu = body_data.gravitational_parameter
J2 = body_data.J2
atmos = body_data.atmos
R_e = body_data.radius_equator
body2 = body_data.body2
mu2 = getattr(bd, body2).gravitational_parameter
pos_body2 = spice.spkezr(body2, et, 'J2000', 'NONE', body)[0][:3]
end = time.perf_counter()
print(f'Time taken to calculate acceleration logic: {end - start} seconds')

# Print the position and velocity of the Moon relative to the Earth
print(f'Moon Position (km): {moon_position}')
print(f'Moon Position from test 2 (km/s): {pos_body2}')
print(f'Moon Velocity (km/s): {moon_velocity}')
print(f'Moon Constants: {moon_constants}')
