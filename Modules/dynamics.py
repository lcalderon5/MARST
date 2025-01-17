# Lucas Calderon
# This file contains the physiscs for the orbital mechanics of the spacecraft.

import numpy as np
from numba import njit

# Acceleration function
@njit
def acceleration(position, atmos_model):

    """
    This function calculates the acceleration of the spacecraft.
    It takes into account the gravitational pull of the celestial bodies up to the second order.
    It also takes into account the drag of the atmosphere.

    """

    # Calculate radius and height

    # Acceleration due to gravity
    a_x = 0
    a_y = 0
    a_z = 0

    # Acceleration due to drag
    

    return
