# Lucas Calderon
# This file contains the numerical methods and math to run the sim

import numpy as np
from numba import njit
from dynamics import acceleration



@njit
def run_simulation(n_max, dt, Method = "euler"):
    """
    This function runs the simulation.

    Inputs:
        dt = 1: The time step of the simulation
        n_max = 1000: The maximum number of time steps of the simulation
        Method = "euler": The method to use to run the simulation. It can be "euler" or "KR4"

    Returns:
        pos_hist: THe history of the positions of the spacecraft
        flows_hist: The history of the composition of the air captured by the spacecraft
        heat_hist: The history of the heat endured by the spacecraft
        time_hist: The history of the time elapsed in the atmosphere and in space
    
    """

    # Create lists
    pos_hist = np.zeros[(n_max, 3)] # Ordered in the following way: [x, y, z]
    vel_hist = np.zeros[(n_max, 3)] # Ordered in the following way: [v_x, v_y, v_z]
    acc_hist = np.zeros[(n_max, 3)] # Ordered in the following way: [a_x, a_y, a_z]
    flows_hist = np.zeros[(n_max, 8)] # This is the composition of the air captured by the spacecraft, ordered in the following way: [air_mass, O_num, N2_num, O2_num, He_num, Ar_num, H_num, N_num]
    heat_hist = np.array[(n_max, 1)]
    atmos_time = 0

    # Apply initial conditions
    pos_hist[0] = np.array([0, 0, 0])
    vel_hist[0] = np.array([0, 0, 0])

    # Run the simulation
    if Method == "euler":
        for i in range(1, n_max):

            acc = acceleration(pos_hist[i-1], vel_hist[i-1])
            acc_hist[i] = acc

            vel_hist[i] = vel_hist[i-1] + acc * dt
            pos_hist[i] = pos_hist[i-1] + vel_hist[i] * dt

    elif Method == "KR4":
        for i in range(1, n_max):

            k1 = acceleration(pos_hist[i-1], vel_hist[i-1])
            k2 = acceleration(pos_hist[i-1] + k1 * dt / 2, vel_hist[i-1] + k1 * dt / 2)
            k3 = acceleration(pos_hist[i-1] + k2 * dt / 2, vel_hist[i-1] + k2 * dt / 2)
            k4 = acceleration(pos_hist[i-1] + k3 * dt, vel_hist[i-1] + k3 * dt)

            acc_hist[i] = k1

            vel_hist[i] = vel_hist[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6 * dt
            pos_hist[i] = pos_hist[i-1] + vel_hist[i] * dt

    else:
        raise ValueError("Method must be 'euler' or 'KR4'")


    return pos_hist, vel_hist, acc_hist, flows_hist, heat_hist, atmos_time
