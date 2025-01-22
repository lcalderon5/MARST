# Lucas Calderon
# This file contains the functions to calculate aerodynamic drag and mass flows.

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Config.spacecraft import spacecraft
from Config.bodies_data import earth
from Modules.helper import sc_heigth, linear_interp

# Rotating atmosphere model
# Because im a bit dumb, for now I'm just going to assume it has the earths rotational velocity in the beggining 
# and that it tapers off to 0 at 750 km in an exponential fashion (Made this shit up)
# No vertical atmospheric movement, no crosswind, no coriolis shit. Maybe in the future.44

@njit
def atmos_rot(position):

    if np.sqrt(position[0]**2 + position[1]**2) <=10:
        return np.zeros(3)

    # Constants
    atmos_velocity = np.zeros(3)
    r_mag = position / np.sqrt(np.sum(position**2))

    # Speed Calculations
    theta = np.arctan(position[2] / np.sqrt(position[0] **2 + position[1] **2))
    earth_radius_true = earth.radius_equator - abs(theta) / (2*np.pi) * (earth.radius_equator - earth.radius_polar)
    rot_speed = earth_radius_true * 2 * np.pi / earth.day * np.cos(theta) # Km/s

    # Exponential decay based on scale height
    scale_height = 745  # km
    atmos_speed = rot_speed * np.exp(-(r_mag - earth_radius_true) / scale_height)

    # Vector shenaningans
    k = - np.array([0, 0, 1])
    v_perp = np.cross(k, position)
    unit_vector = v_perp / np.sqrt(np.sum(v_perp**2))

    # Vectorial velocity
    velocity = atmos_speed * unit_vector
    atmos_velocity[0] = velocity[0]
    atmos_velocity[1] = velocity[1]
    atmos_velocity[2] = 0

    return atmos_velocity # Given in km/s


@njit
def calculate_density(h, altitudes, densities):
    return linear_interp(h, altitudes, densities)


@njit
def drag_acceleration(position:np.array, velocity:np.array, heights:np.array, air:np.array) -> np.array:
    
    # Density
    rho = calculate_density(sc_heigth(position), heights, air)

    # Substract atmos velocities
    atmos_velocity = atmos_rot(position)
    velocity_rel = velocity - atmos_velocity

    # Calculate the drag acceleration
    drag_a = -0.5 * spacecraft.C_D * spacecraft.A * rho * np.sqrt(np.sum(velocity_rel**2)) * velocity_rel / spacecraft.mass # in km/s^2

    return drag_a