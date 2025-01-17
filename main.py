# Lucas Calderon
# This is the main file for the project. It will be used to run the project.

# Importing the necessary libraries
import numpy as np


def run_simulation(Spacecraft, atmos_model, dt = 1, n_max = 1000):
    """
    This function runs the simulation.

    Inputs:
        Spacecraft: The spacecraft object that will be used in the simulation
        atmos_model: The atmospheric model that will be used in the simulation
        dt = 1: The time step of the simulation
        n_max = 1000: The maximum number of time steps of the simulation

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

    # Run the simulation


    return pos_hist, vel_hist, acc_hist, flows_hist, heat_hist, atmos_time


if __name__ == "__main__":
    # This is the main function that will be used to run the simulation
    
    pass