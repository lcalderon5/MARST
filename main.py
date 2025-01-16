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
    pos_hist = {"x":np.zeros(n_max), "y":np.zeros(n_max), "z":np.zeros(n_max), "g":np.zeros(n_max), "name":Spacecraft.name}  # G is for acceleration history but it doesn't work very well
    flows_hist = {
    "air_mass": np.zeros(n_max),
    "O_num": np.zeros(n_max),   
    "N2_num": np.zeros(n_max),
    "O2_num": np.zeros(n_max),
    "He_num": np.zeros(n_max),
    "Ar_num": np.zeros(n_max),
    "H_num": np.zeros(n_max),
    "N_num": np.zeros(n_max),
    "name": Spacecraft.name
    }
    heat_hist = {"h":np.zeros(n_max), "q":np.zeros(n_max)}
    
    time_hist = 0



    return pos_hist, flows_hist, heat_hist, time_hist


if __name__ == "__main__":
    # This is the main function that will be used to run the simulation
    
    pass