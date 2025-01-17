# Lucas Calderon
# This file contains the numerical methods and math to run the sim
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from numba import njit
from Modules.dynamics import acceleration
from Config.spacecraft import spacecraft


@njit
def run_simulation(n_max: int, dt:float, Method = "euler"):
    """
    This function runs the simulation.

    Inputs:
        dt = 1: The time step of the simulation
        n_max = 1000: The maximum number of time steps of the simulation
        Method = "euler": The method to use to run the simulation. It can be "euler", "KR4"  and "Verlet" for now and in the future maybe "RK45" if I get carried away

    Returns:
        pos_hist: THe history of the positions of the spacecraft
        vel_hist: The history of the velocities of the spacecraft
        acc_hist: The history of the accelerations of the spacecraft
        flows_hist: The history of the composition of the air captured by the spacecraft
        atmos_time: The time that the spacecraft has been in the atmosphere
    
    """

    # Create lists
    pos_hist = np.zeros((n_max, 3)) # Ordered in the following way: [x, y, z]
    vel_hist = np.zeros((n_max, 3)) # Ordered in the following way: [v_x, v_y, v_z]
    acc_hist = np.zeros((n_max, 3)) # Ordered in the following way: [a_x, a_y, a_z]
    flows_hist = np.zeros((n_max, 8)) # This is the composition of the air captured by the spacecraft, ordered in the following way: [air_mass, O_num, N2_num, O2_num, He_num, Ar_num, H_num, N_num]
    atmos_time = 0

    # Apply initial conditions
    pos_hist[0] = spacecraft.initial_position
    vel_hist[0] = spacecraft.initial_velocity

    # Run the simulation
    if Method == "euler": # Simple euler implementation
        for i in range(1, n_max):

            acc = acceleration(pos_hist[i-1], vel_hist[i-1])
            acc_hist[i] = acc

            vel_hist[i] = vel_hist[i-1] + acc * dt
            pos_hist[i] = pos_hist[i-1] + vel_hist[i] * dt

    elif Method == "KR4":
        for i in range(1, n_max):
            # RK4 for velocity
            k1_v = acceleration(pos_hist[i-1], vel_hist[i-1])
            k2_v = acceleration(pos_hist[i-1] + vel_hist[i-1] * dt / 2, vel_hist[i-1] + k1_v * dt / 2)
            k3_v = acceleration(pos_hist[i-1] + vel_hist[i-1] * dt / 2, vel_hist[i-1] + k2_v * dt / 2)
            k4_v = acceleration(pos_hist[i-1] + vel_hist[i-1] * dt, vel_hist[i-1] + k3_v * dt)

            acc_hist[i] = k1_v
            vel_hist[i] = vel_hist[i-1] + (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6 * dt

            # RK4 for position
            k1_r = vel_hist[i-1]
            k2_r = vel_hist[i-1] + k1_v * dt / 2
            k3_r = vel_hist[i-1] + k2_v * dt / 2
            k4_r = vel_hist[i-1] + k3_v * dt

            pos_hist[i] = pos_hist[i-1] + (k1_r + 2*k2_r + 2*k3_r + k4_r) / 6 * dt

    elif Method == "Verlet":
        # Initial updates
        a0 = acceleration(pos_hist[0], vel_hist[0])
        pos_hist[1] = pos_hist[0] + vel_hist[0] * dt + 0.5 * a0 * dt**2
        a1 = acceleration(pos_hist[1], vel_hist[0])
        vel_hist[1] = vel_hist[0] + 0.5 * (a0 + a1) * dt
        
        for i in range(1, n_max - 1):
            # Verlet for position
            pos_hist[i + 1] = pos_hist[i] + vel_hist[i] * dt + 0.5 * a1 * dt**2
            
            # Update acceleration at new position
            a2 = acceleration(pos_hist[i + 1], vel_hist[i])
            
            # Verlet for velocity
            vel_hist[i + 1] = vel_hist[i] + 0.5 * (a1 + a2) * dt
            
            # Update previous acceleration for the next step
            a1 = a2

    else:
        raise ValueError("Method must be a valid entry")


    return pos_hist, vel_hist, acc_hist, flows_hist, atmos_time


