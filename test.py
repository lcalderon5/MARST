import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import numpy as np
import spiceypy as spice
import time


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

# Extract the position and velocity vector from the state vector
moon_position = moon_state[:3]
moon_velocity = moon_state[3:]

# Print the position and velocity of the Moon relative to the Earth
print(f'Moon Position (km): {moon_position}')
print(f'Moon Velocity (km/s): {moon_velocity}')
