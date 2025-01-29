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
from Modules.simulation_math import propagate_phase
from Modules.dynamics import acceleration
from Results.visualization import plot_orbit_plotly, plot_atmos_data
from Config.spacecraft import spacecraft
# from Modules.helper import sc_heigth


if __name__ == "__main__":

    # Load the SPICE Kernels
    spice.furnsh(r"C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Data\Spice\Solar_sytem_kernel.tm")

    # Load the spacecraft initial conditions
    et = spacecraft.et0
    t_phase = 1e7
    t_span = np.array([et, et + t_phase])
    state0 = np.concatenate((spacecraft.initial_position, spacecraft.initial_velocity, np.array([spacecraft.mass0])))

    # Run the simulation
    t_hist, pos_hist, vel_hist, mass_hist = propagate_phase(t_span, acceleration, state0)

    # print(f"Final height: {sc_heigth(pos_hist[-1])} km")
    print(np.shape(t_hist))
    print(np.shape(pos_hist))

    # Plot the results
    plot_orbit_plotly(pos_hist, res=1)

