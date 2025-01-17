# Lucas Calderon
# This file contains some helper functions for the project.

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Config import bodies_data as bd

@njit
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


# Function to set intial conditions
@njit
def orbital_elements_to_cartesian(mu, peri, apo, i, raan, arg_periapsis, init_anomaly):

    """
    This function converts orbital elements to cartesian coordinates.

    Inputs:
        mu: The gravitational parameter of the central body
        peri: The periapsis of the orbit
        apo: The apoapsis of the orbit
        i: The inclination of the orbit
        raan: The right ascension of the ascending node
        arg_periapsis: The argument of periapsis
        init_anomaly: The initial true anomaly

    Returns:
        r_inertial: The position vector in the inertial frame
        v_inertial: The velocity vector in the inertial frame

    """

    # Convert some stuff to radians
    i = np.radians(i)
    raan = np.radians(raan)
    arg_periapsis = np.radians(arg_periapsis)
    init_anomaly = np.radians(init_anomaly)

    # Calculate semi-major axis and eccentricity
    a = (peri + apo) / 2  # km
    e = (apo - peri) / (apo + peri)  # unitless

    # Calculate position and velocity in the perifocal frame
    p = a * (1 - e**2)  # Semi-latus rectum, km
    r = p / (1 + e * np.cos(init_anomaly))  # Radius, km

    # Position vector in perifocal coordinates
    r_peri = np.array([
        r * np.cos(init_anomaly),
        r * np.sin(init_anomaly),
        0
    ])

    # Velocity vector in perifocal coordinates
    v_peri = np.array([
        -np.sqrt(mu / p) * np.sin(init_anomaly),
        np.sqrt(mu / p) * (e + np.cos(init_anomaly)),
        0
    ])

    # Rotation matrices
    R3_raan = np.array([
        [np.cos(-raan), np.sin(-raan), 0],
        [-np.sin(-raan), np.cos(-raan), 0],
        [0, 0, 1]
    ])

    R1_incl = np.array([
        [1, 0, 0],
        [0, np.cos(-i), np.sin(-i)],
        [0, -np.sin(-i), np.cos(-i)]
    ])

    R3_arg_peri = np.array([
        [np.cos(-arg_periapsis), np.sin(-arg_periapsis), 0],
        [-np.sin(-arg_periapsis), np.cos(-arg_periapsis), 0],
        [0, 0, 1]
    ])

    # Correct combined rotation matrix
    R_total = R3_arg_peri @ R1_incl @ R3_raan

    # Transform to inertial frame
    r_inertial = R_total @ r_peri
    v_inertial = R_total @ v_peri

    return r_inertial, v_inertial
