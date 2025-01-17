# Lucas Calderon
# This file contains the functions to calculate aerodynamic drag and mass flows.

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from Config.spacecraft import spacecraft
from Config.bodies_data import earth
from Modules.helper import sc_heigth

# Rotating atmosphere model
# Because im a bit dumb, for now I'm just going to assume it has the earths rotational velocity in the beggining 
# and that it tapers off to 0 at 750 km in an exponential fashion (Made this shit up)
# No vertical atmospheric movement, no crosswind, no coriolis shit. Maybe in the future.

def atmos_rot(position):

    if np.sqrt(position[0]**2 + position[1]**2) <=10:
        return np.zeros(1, 3)

    # Constants
    atmos_velocity = np.zeros(1, 3)
    r_mag = position / np.sqrt(np.sum(position**2))

    # Speed Calculations
    Earth_radius = earth.radius_equator
    Earth_rot_speed = Earth_radius * 2 * np.pi / earth.day # Km/s
    # Exponential decay based on scale height
    scale_height = 745  # km
    atmos_speed = Earth_rot_speed * np.exp(-(r_mag - Earth_radius) / scale_height)


    # Vector shenaningans
    k = - np.array([0, 0, 1])
    v_perp = np.cross(k, position)
    unit_vector = v_perp / np.linalg.norm(v_perp)

    # Vectorial velocity
    velocity = atmos_speed * unit_vector
    atmos_velocity[0] = velocity[0]
    atmos_velocity[1] = velocity[1]
    atmos_velocity[2] = 0

    return atmos_velocity # Given in km/s