# Lucas Calderon
# This is the main file for the project. It will be used to run the project.

# Import 3rd party Libraries
import sys
import os
import spiceypy as spice 
import numpy as np

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import own Libraries
from Modules.simulation_math import run_simulation, propagate_phase
from Modules.dynamics import acceleration, acceleration_new
from Results.visualization import plot_orbit_plotly, plot_atmos_data
from Config.spacecraft import initial_position, initial_velocity
# from Modules.helper import sc_heigth


if __name__ == "__main__":

    # Load the SPICE Kernels
    spice.furnsh(r"C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Data\Spice\Solar_sytem_kernel.tm")

    # Load the spacecraft initial conditions
    t_span = [0, 1e6]
    state0 = np.concatenate((initial_position, initial_velocity))

    # Run the simulation
    print("Running simulation")
    t_hist, pos_hist, vel_hist = propagate_phase(t_span, acceleration, state0)
    print("Simulation finished")

    # print(f"Time in atmosphere: {atmos_time} s")
    # print(f"Final height: {sc_heigth(pos_hist[-1])} km")
    print(np.shape(t_hist))
    print(np.shape(pos_hist))

    # Plot the results
    plot_orbit_plotly(pos_hist, res=1)

