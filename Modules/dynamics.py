# Lucas Calderon
# This file contains the physiscs for the orbital mechanics of the spacecraft.

import numpy as np
from numba import njit
from helper import sc_heigth
from Config import bodies_data as bd

# Acceleration function
@njit
def acceleration(position, atmos=True):

    """
    This function calculates the acceleration of the spacecraft.
    It takes into account the gravitational pull of the celestial bodies up to the second order.
    It also takes into account the drag of the atmosphere.

    """

    # Calculate radius, colatitude, longitude and height
    r = np.linalg.norm(position)
    theta = np.arccos(position[2] / r)
    phi = np.arctan(position[1] / position[0])
    h = sc_heigth(position)

    # Acceleration due to gravity
    a_r = -bd.earth.gravitational_parameter / r**2 * (1 - 1.5 * bd.earth.J2 * (bd.earth.radius_equator / r)**2 * (3 * np.cos(theta)**2 - 1))
    a_theta = -3 * bd.earth.gravitational_parameter / r**4 * bd.earth.J2 * bd.earth.radius_equator**2 * np.cos(theta) * np.sin(theta)

    # Unit vectors in spherical coordinates
    r_hat = position / r  # radial unit vector
    theta_hat = np.array([x / r * np.cos(theta) for x in position])

    # Gravitational acceleration in Cartesian coordinates
    a_r_vec = a_r * r_hat  # Radial component
    a_theta_vec = a_theta * theta_hat  # Latitudinal component
    # No need for longitudinal component, as it is zero if only considering a second order model
    
    # Total gravitational acceleration in Cartesian coordinates
    a_total = a_r_vec + a_theta_vec # This is a three element vector, containing the x, y and z components of the acceleration

    # Acceleration due to drag
    if h < 750 and atmos is True: # Number is the atmos model height in km.
        pass
    

    return a_total



