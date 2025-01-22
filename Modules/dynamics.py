# Lucas Calderon
# This file contains the physiscs for the orbital mechanics of the spacecraft.
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Modules.helper import sc_heigth
from Config import bodies_data as bd
from Modules.aero import drag_acceleration
from Modules.atmos import h, air

heights = h
rho = air

# Acceleration function
@njit
def acceleration(position:np.array, velocity:np.array, atmos:bool=True) -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    WARNING: For now it is only considering the gravitational pull of the Earth!!!!
    It takes into account the gravitational pull of the celestial bodies up to the second order.
    It also takes into account the drag of the atmosphere.

    """

    # Calculate radius, colatitude and height
    r = np.sqrt(np.sum(position**2))
    theta = np.arccos(position[2] / r)
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_r = -bd.earth.gravitational_parameter / r**2 * (1 - 1.5 * bd.earth.J2 * (bd.earth.radius_equator / r)**2 * (3 * np.sin(theta)**2 - 1))
    a_theta = -3 * bd.earth.gravitational_parameter / r**4 * bd.earth.J2 * bd.earth.radius_equator**2 * np.cos(theta) * np.sin(theta)

    # Unit vectors in spherical coordinates
    r_hat = position / r  # radial unit vector
    theta_hat = position / r * np.cos(theta) # latitudinal unit vector

    # Gravitational acceleration in Cartesian coordinates
    a_r_vec = a_r * r_hat  # Radial component
    a_theta_vec = a_theta * theta_hat  # Latitudinal component
    # No need for longitudinal component, as it is zero if only considering a second order model
    
    # Total gravitational acceleration in Cartesian coordinates
    a_total = a_r_vec + a_theta_vec # This is a three element vector, containing the x, y and z components of the acceleration

    # Acceleration due to drag
    if h < 750 and atmos is True: # Number is the atmos model height in km.
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag
    
    return a_total


@njit
def acceleration_O1(position:np.array, velocity:np.array, mu:float,  atmos:bool=True) -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    For now it is only considering the gravitational pull of the Earth!!!!
    It takes into account the gravitational pull of the celestial bodies up to the second order.
    It also takes into account the drag of the atmosphere.

    """

    # Calculate radius, colatitude and height
    r = np.sqrt(np.sum(position**2))
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_r = -mu / r**2

    # Unit vectors in spherical coordinates
    r_hat = position / r  # radial unit vectorr

    # Gravitational acceleration in Cartesian coordinates
    a_r_vec = a_r * r_hat  # Radial component

    # Acceleration due to drag
    if h < 750 and atmos is True: # Number is the atmos model height in km.
        pass
    
    return a_r_vec