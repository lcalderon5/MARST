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
def acceleration_old(position:np.array, velocity:np.array, atmos:bool=True) -> np.array:

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
    a_total = a_r_vec + a_theta_vec # This is a three element vector, containing the x, y and z components of the acceleration, in km/s^2

    # Acceleration due to drag
    if h < 750 and atmos is True: # Number is the atmos model height in km.
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag
    
    return a_total 


@njit
def acceleration(position:np.array, velocity:np.array, body:str='Earth') -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    It can take into account the gravitational pull of the celestial bodies up to the second order.
    It can also take into account the drag of the atmosphere.

    """

    # Logic for the celestial body
    atmos = False
    if body == 'Earth':
        body_data = bd.earth
        atmos = True
    elif body == 'Moon':
        body_data = bd.moon
    else:
        raise ValueError('The body is not in the database.')

    # Calculate radius, latitude and height
    r = np.sqrt(np.sum(position**2))
    theta = np.arcsin(position[2] / r)
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_total = -body_data.gravitational_parameter / r**2

    # Acceleration due to perturbations
    if body == 'Earth':
        a_r = -1.5 * body_data.J2 * (body_data.radius_equator / r)**2 * (3 * np.sin(theta)**2 - 1)
        a_theta = -3 * body_data.gravitational_parameter / r**4 * body_data.J2 * body_data.radius_equator**2 * np.cos(theta) * np.sin(theta)
        a_total = a_total + a_r + a_theta

    # Acceleration due to drag
    if h < 745 and atmos is True:
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag
    
    # Unit vectors in spherical coordinates
    r_hat = position / r  # radial unit vectorr

    # Gravitational acceleration in Cartesian coordinates
    a_r_vec = a_total * r_hat  # Radial component


    return a_r_vec