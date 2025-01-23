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
from Modules.helper import sc_heigth, linear_interp, norm

# Rotating atmosphere model

@njit
def atmos_rot(position):

    if np.sqrt(position[0]**2 + position[1]**2) <=10:
        return np.zeros(3)

    rot_speed = 2 * np.pi / earth.day

    # Angular velocity vector 
    omega_vec = np.array([0, 0, rot_speed])

    return np.cross(omega_vec, position) # in km/s


@njit
def drag_acceleration(position:np.array, velocity:np.array, heights:np.array, air:np.array) -> np.array:
    
    # Density
    rho = linear_interp(sc_heigth(position), heights, air) # in kg/m^3, interpolated from the data in h and air

    # Substract atmos velocities
    atmos_velocity = atmos_rot(position)
    velocity_rel = velocity - atmos_velocity

    # Calculate the drag acceleration
    drag_a = -0.5 * spacecraft.C_D * spacecraft.A * rho * norm(velocity_rel) * velocity_rel / spacecraft.mass * 1000 # in km/s^2 (remember that the density is in kg/m^3, A in m^2 and velocity in km/s)

    return drag_a