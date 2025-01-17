# Lucas Calderon
# This file contains some helper functions for the project.

import numpy as np
from Config import bodies_data as bd

def sc_heigth(pos):
    """
    This function calculates the height of the spacecraft, taking into account the earth's change in radius over its latitude.

    Inputs:
        pos: The position of the spacecraft

    Returns:
        height: The height of the spacecraft
    """
    # Calculate radius and height
    theta = np.arctan(pos[2] / np.sqrt(pos[0] **2 + pos[1] **2))
    earth_radius = bd.Earth.radius_equator - abs(theta) / (2*np.pi) * (bd.Earth.radius_equator - bd.Earth.radius_polar)
    height = np.linalg.norm(pos) - earth_radius
    return height
