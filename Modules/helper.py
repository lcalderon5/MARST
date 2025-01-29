# Lucas Calderon
# This file contains some helper functions for the project.

import sys
import os
import numpy as np
from numba import njit

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Config import bodies_data as bd

@njit
def sc_heigth(pos):
    """
    This function calculates the height of the spacecraft, taking into account the earth's change in radius over its latitude.

    Inputs:
        pos: The position of the spacecraft as a 3 element numpy array

    Returns:
        height: The height of the spacecraft as a scalar
    """
    
    # Calculate radius, latitude and height
    theta = np.arctan(pos[2] / np.sqrt(pos[0] **2 + pos[1] **2 + 1e-10))
    earth_radius = bd.Earth.radius_equator - abs(theta) / (2*np.pi) * (bd.Earth.radius_equator - bd.Earth.radius_polar)
    height = np.sqrt(np.sum(pos**2)) - earth_radius
    return height


# ------------Functions to be replaced by spiceypy implementations----------------
# Function to obtain the spacecraft's velocity in the inertial frame from the orbital elements
@njit
def orbital_elements_to_cartesian(mu: float, peri: float, apo: float, i: float, 
                                  raan: float, arg_periapsis: float, init_anomaly: float, t: float = 0):
    """
    Converts orbital elements to cartesian coordinates and propagates the orbit over time.

    Inputs:
        mu: The gravitational parameter of the central body (km^3/s^2)
        peri: The periapsis of the orbit (km)
        apo: The apoapsis of the orbit (km)
        i: The inclination of the orbit (degrees)
        raan: The right ascension of the ascending node (degrees)
        arg_periapsis: The argument of periapsis (degrees)
        init_anomaly: The initial true anomaly (degrees)
        t: Time since the epoch (seconds)

    Returns:
        r_inertial: The position vector in the inertial frame (km)
        v_inertial: The velocity vector in the inertial frame (km/s)
    """


    # Convert to radians
    i = np.radians(i)
    raan = np.radians(raan)
    arg_periapsis = np.radians(arg_periapsis)

    # Calculate semi-major axis and eccentricity
    a = (peri + apo) / 2  # Semi-major axis (km)
    e = (apo - peri) / (apo + peri)  # Eccentricity

    # Calculate mean motion (rad/s)
    n = np.sqrt(mu / a**3)

    # Calculate initial mean anomaly (convert initial true anomaly to mean anomaly)
    init_anomaly = np.radians(init_anomaly)
    E0 = 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(init_anomaly / 2))
    M0 = E0 - e * np.sin(E0)

    # Propagate mean anomaly to time t
    M = M0 + n * t

    # Solve Kepler's equation for eccentric anomaly
    E = M  # Initial guess
    while True:
        E_next = E + (M - (E - e * np.sin(E))) / (1 - e * np.cos(E))
        if abs(E_next - E) < 1e-8:
            break
        E = E_next


    # Calculate true anomaly (nu) from eccentric anomaly
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))

    # Calculate distance (r) at the propagated true anomaly
    p = a * (1 - e**2)  # Semi-latus rectum (km)
    r = p / (1 + e * np.cos(nu))

    # Position vector in perifocal coordinates
    r_peri = np.array([r * np.cos(nu),
                       r * np.sin(nu),
                       0.0])

    # Velocity vector in perifocal coordinates
    v_peri = np.array([-np.sqrt(mu / p) * np.sin(nu),
                       np.sqrt(mu / p) * (e + np.cos(nu)),
                       0.0])

    # Rotation matrices
    R3_raan = np.array([[np.cos(-raan), np.sin(-raan), 0.0],
                        [-np.sin(-raan), np.cos(-raan), 0.0],
                        [0.0, 0.0, 1.0]])

    R1_incl = np.array([[1.0, 0.0, 0.0],
                        [0.0, np.cos(-i), np.sin(-i)],
                        [0.0, -np.sin(-i), np.cos(-i)]])

    R3_arg_peri = np.array([[np.cos(-arg_periapsis), np.sin(-arg_periapsis), 0.0],
                            [-np.sin(-arg_periapsis), np.cos(-arg_periapsis), 0.0],
                            [0.0, 0.0, 1.0]])

    # Total rotation matrix
    R_total = R3_arg_peri @ R1_incl @ R3_raan

    # Transform to inertial frame
    r_inertial = R_total @ r_peri
    v_inertial = R_total @ v_peri

    return r_inertial, v_inertial
# Equivalent to spiceypy.conics(state, et, mu) function


# Function to obtain the orbital elements from the spacecraft's position and velocity
@njit
def cartesian_to_orbital_elements(mu, position, velocity):

    """
    Converts cartesian coordinates to orbital elements.

    Inputs:
        mu: The gravitational parameter of the central body (km^3/s^2)
        position: The position vector in the inertial frame (km)
        velocity: The velocity vector in the inertial frame (km/s)

    Returns:
        peri: The periapsis of the orbit (km)
        apo: The apoapsis of the orbit (km)
        i: The inclination of the orbit (degrees)
        raan: The right ascension of the ascending node (degrees)
        arg_periapsis: The argument of periapsis (degrees)
        true_anomaly: The true anomaly (degrees)
    """

    pass

    # return peri, apo, i, raan, arg_periapsis, true_anomaly
# Equivalent to spiceypy.oscltx(state, et, mu) function



#---------- NUMBA FUNCTIONS ----------
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

