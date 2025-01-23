# Lucas Calderon
# This is the main file for the project. It will be used to run the project.
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import thingies
from Modules.simulation_math import run_simulation
from Results.visualization import plot_orbit_plotly, plot_atmos_data
# from Modules.helper import sc_heigth


if __name__ == "__main__":

    # Define the simulation parameters
    n_max = 10000000
    dt = 1

    # Run the simulation
    print("Running simulation")
    pos_hist, vel_hist, acc_hist, flows_hist, atmos_time = run_simulation(n_max, dt, Method = "RK4")
    print("Simulation finished")
    print(f"Time in atmosphere: {atmos_time} s")
    # print(f"Final height: {sc_heigth(pos_hist[-1])} km")

    # Plot the results
    plot_orbit_plotly(pos_hist, res=0.1)

