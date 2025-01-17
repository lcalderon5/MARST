# Lucas Calderon
# This is the main file for the project. It will be used to run the project.
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import thingies
from Modules.simulation_math import run_simulation
from Results.visualization import plot_orbit_plotly, plot_atmos_data


if __name__ == "__main__":

    # Define the simulation parameters
    n_max = 1000000
    dt = 0.1

    # Run the simulation
    pos_hist, vel_hist, acc_hist, flows_hist, atmos_time = run_simulation(n_max, dt, Method = "RK4")
    print("Simulation finished")

    # Plot the results
    plot_orbit_plotly(pos_hist, res=0.1)

