# Lucas Calderon
# This file contains the physiscs for the orbital mechanics of the spacecraft.
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Modules.helper import sc_heigth, norm
from Config import bodies_data as bd
from Modules.aero import drag_acceleration
from Modules.atmos import h, air

heights = h
rho = air

# Acceleration function

@njit()
def acceleration(position:np.array, velocity:np.array, body:str='Earth') -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    It can take into account the gravitational pull of the celestial bodies up to the second order.
    It can also take into account the drag of the atmosphere.

    """

    # Logic for the celestial body
    atmos = False
    if body == 'Earth':
        mu = bd.earth.gravitational_parameter
        J2 = bd.earth.J2
        R_e = bd.earth.radius_equator
        atmos = True
    elif body == 'Moon':
        mu = bd.moon.gravitational_parameter
    else:
        raise ValueError('The body is not in the database.')

    # Calculate radius, colatitude and height
    r = norm(position)
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_total = - mu / r**3 * position

    # Acceleration due to perturbations
    if body == 'Earth':
        a_total += -3 * mu * J2 * R_e**2 / r**5 * np.array([position[0] * (5 * position[2]**2 / r**2 - 1), position[1] * (5 * position[2]**2 / r**2 - 1), position[2] * (5 * position[2]**2 / r**2 - 3)])

    # Acceleration due to drag
    if h < 745 and atmos is True:
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag 

    return a_total


# New acceleration function
@njit()
def acceleration_new(position:np.array, velocity:np.array, 
                 mu:float, J2:float, R_e:float, atmos:bool,
                 mu2:float=0) -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    It can take into account the gravitational pull of the celestial bodies up to the second order.
    It can also take into account the drag of the atmosphere.

    """

    # Calculate radius, colatitude and height
    r = np.sqrt(np.sum(position**2))
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_total = - mu / r**3 * position

    # Acceleration due to second order perturbations
    if J2 > 1e-10:
        a_total += -3 * mu * J2 * R_e**2 / r**5 * np.array([position[0] * (5 * position[2]**2 / r**2 - 1), position[1] * (5 * position[2]**2 / r**2 - 1), position[2] * (5 * position[2]**2 / r**2 - 3)])

    # Acceleration due to third body perturbations
    if mu2 > 1e-10:
        position2 = np.array([0, 0, 0]) # Placeholder for now
        r2 = np.sqrt(np.sum(position2**2))
        a_total += - mu2 / r2**3 * position

    # Acceleration due to drag
    if h < 745 and atmos is True:
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag 

    return a_total



# Test the function
if __name__ == "__main__":
    position = np.array([6471, 0, 0])
    velocity = np.array([10, 0, 0])
    print(acceleration(position, velocity)) # Expected: [-0.00981, 0, 0] for Earth