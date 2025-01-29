# Lucas Calderon
# This file contains the physiscs for the orbital mechanics of the spacecraft.
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Modules.helper import sc_heigth, norm, orbital_elements_to_cartesian
from Config import bodies_data as bd
from Config.spacecraft import spacecraft
from Modules.aero import drag_acceleration
from Modules.atmos import h, air

heights = h
rho = air


# Acceleratin function for scipy integration
def acceleration(t:float, state:np.ndarray) -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    It can take into account the gravitational pull of the celestial bodies up to the second order.
    It can also take into account the drag of the atmosphere.

    Inputs:
        t: The time of the simulation
        state: The state of the spacecraft as a 6 element numpy array: [x, y, z, vx, vy, vz]

    Returns:
        state_dot: The derivative of the state as a 6 element numpy array: [vx, vy, vz, ax, ay, az]

    """
    # Obtain constants ( TO BE EXPANDED )
    mu = bd.earth.gravitational_parameter
    J2 = bd.earth.J2
    R_e = bd.earth.radius_equator
    atmos = bd.earth.atmos

    # Unpack the state vector
    position = state[:3]
    velocity = state[3:]

    # Calculate radius, colatitude and height
    r = np.linalg.norm(position)
    # r2 = np.sqrt(np.sum(position2**2))
    h = sc_heigth(position)

    # Acceleration due to gravity of the first body
    a_total = - mu / r**3 * position

    # Acceleration due to second order perturbations
    a_total += -1.5 * mu * J2 * R_e**2 / r**5 * np.array([
        position[0] * (5 * position[2]**2 / r**2 - 1),
        position[1] * (5 * position[2]**2 / r**2 - 1),
        position[2] * (5 * position[2]**2 / r**2 - 3)])

    # Acceleration due to gravity of the second body
    # a_total += - mu2 / r2**3 * position2

    # Acceleration due to drag
    if h < 745 and atmos is True:
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag 

    # Acceleration due to thrust, assumed to be perfectly aligned with the velocity vector
    # a_total += a_T

    # Create state_dot vector
    state_dot = np.concatenate((velocity, a_total))

    return state_dot


# Generalized function with more perturbations
def acceleration_new(t:float, state:np.ndarray, body='earth') -> np.array:

    """
    This function calculates the acceleration of the spacecraft.
    It can take into account the gravitational pull of the celestial bodies up to the second order.
    It can also take into account the drag of the atmosphere.

    Inputs:
        t: The time of the simulation
        state: The state of the spacecraft as a 7 element numpy array: [x, y, z, vx, vy, vz, m]

    Returns:
        state_dot: The derivative of the state as a 7 element numpy array: [vx, vy, vz, ax, ay, az, m_dot]

    """

    # Obtain constants ( CONSIDER BRINGING OUT OF THE FUNCTION )

    # From the body data
    body_data = getattr(bd, body)
    mu = body_data.gravitational_parameter
    J2 = body_data.J2
    atmos = body_data.atmos
    R_e = body_data.radius_equator
    body2 = body_data.body2
    mu2 = getattr(bd, body2).gravitational_parameter
    pos_body2 = np.array([0, 0, 0]) # PLACEHOLDER

    # From the spacecraft data
    a_T = spacecraft.thrust
    if spacecraft.thrust is not None:
        m_dot = spacecraft.mass_flow_rate
    else:
        m_dot = 0

    #--------------------------------

    # Unpack the state vector
    position = state[:3]
    velocity = state[3:]

    # Calculate radius, position2 and height
    r = np.linalg.norm(position) 
    h = sc_heigth(position)
    position2 = position - pos_body2
    r2 = np.linalg.norm(position2)

    # Acceleration due to gravity of the first body
    a_total = - mu / r**3 * position

    # Acceleration due to second order perturbations
    a_total += -3 * mu * J2 * R_e**2 / r**5 * np.array([
        position[0] * (5 * position[2]**2 / r**2 - 1), 
        position[1] * (5 * position[2]**2 / r**2 - 1), 
        position[2] * (5 * position[2]**2 / r**2 - 3)
    ])

    # Acceleration due to gravity of the second body
    a_total += - mu2 / r2**3 * position2

    # Acceleration due to drag
    if h < 745 and atmos is True:
        a_drag = drag_acceleration(position, velocity, heights, rho)
        a_total += a_drag 

    # Acceleration due to thrust, assumed to be perfectly aligned with the velocity vector
    a_total += a_T

    # Create state_dot vector
    state_dot = np.concatenate((velocity, a_total, -m_dot))

    return state_dot


# Numba version of the acceleration function
@njit()
def acceleration_numba(position:np.array, velocity:np.array, body:str='Earth') -> np.array:

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
        a_total += -1.5 * mu * J2 * R_e**2 / r**5 * np.array([position[0] * (5 * position[2]**2 / r**2 - 1), position[1] * (5 * position[2]**2 / r**2 - 1), position[2] * (5 * position[2]**2 / r**2 - 3)])

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
