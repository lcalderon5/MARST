# Lucas Calderon
# This file contains some helper functions for the project.

import sys
import os
import numpy as np
from numba import njit
import spiceypy as spice

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Config import bodies_data as bd


# ------------FUNCTION TO CALCULATE THE HEIGHT OF THE SPACECRAFT----------------
@njit
def sc_heigth(pos, body='Earth'):
    """
    This function calculates the height of the spacecraft over the body it's orbiting.
    It takes into account the oblateness of the body.

    Inputs:
        pos: The position of the spacecraft as a 3 element numpy array
        body: The celestial body that the spacecraft is orbiting, default is Earth

    Returns:
        height: The height of the spacecraft as a scalar
    """
    
    # Unpack body data
    body_data = getattr(bd, body)
    r_equator = body_data.radius_equator
    r_polar = body_data.radius_polar

    # Calculate radius, latitude and height
    theta = np.arctan(pos[2] / np.sqrt(pos[0] **2 + pos[1] **2 + 1e-10))
    r_local = r_equator - abs(theta) / (2*np.pi) * (r_equator - r_polar)
    height = np.sqrt(np.sum(pos**2)) - r_local
    return height


# ------------FUNCTIONS TO CONVERT BETWEEN COES AND STATE----------------
# Function to obtain the spacecraft's state the classical orbital elements
def coes_to_states(elts, et):

    """
    Converts orbital elements to cartesian coordinates.

    Inputs:
        mu: The gravitational parameter of the central body (km^3/s^2)
        elts: The orbital elements of the spacecraft as a 8*N element numpy array: 
            [Periapsis, e, i, raan, arg_periapsis, mean_anomaly_atepoch, et, mu] * N

    Returns:
        state: The state of the spacecraft as a 6*N element numpy array: [x, y, z, vx, vy, vz] * N
    """

    states = np.zeros((len(elts), 6))

    for i in range(len(elts)):
        state = spice.conics(elts[i], et[i])
        states[i] = state

    return states


# Function to obtain the orbital elements from the spacecraft's position and velocity
def states_to_coes(state, et, mu):

    """
    Converts cartesian coordinates to orbital elements.

    Inputs:
        state: A 2D array with the state of the spacecraft as a 6*N element numpy array over time: [x, y, z, vx, vy, vz] * N
        et: The time ephimeral time of the simulation, a list of N elements
        mu: The gravitational parameter of the central body (km^3/s^2)

    Returns:
        coes: The classical orbital elements of the spacecraft as a 11 element numpy array: 
            [peri, e, i, longitude_ascending_node, arg_periapsis, mean_anomaly_atepoch, epoch, mu, true_anomaly_atepoch, a, orbital_period] * N
    """

    coes = np.zeros((len(state), 11))

    for i in range(len(state)):
        coe = spice.oscltx(state[i], et[i], mu)
        coes[i] = coe

    return coes


#---------- NUMBA COMPATIBLE FUNCTIONS ----------
# Linear interpolation in numba
# This function finds the correspoinding value of x in the xp array and returns the interpolated value of fp
@njit
def linear_interp(x, xp, fp):
    for i in range(len(xp) - 1):
        if xp[i] <= x < xp[i + 1]:
            return fp[i] + (x - xp[i]) * (fp[i + 1] - fp[i]) / (xp[i + 1] - xp[i])
    return 0.0  # Out of range


# Function to calculate the norm of a vector
@njit
def norm(vector):
    norm = 0
    for i in vector:
        norm += i**2

    return np.sqrt(norm)


# Function to calculate the distance between two points
@njit
def distance(p1, p2):
    return norm(p1 - p2)

