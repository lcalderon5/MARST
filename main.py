# Lucas Calderon
# This is the main file for the project. It will be used to run the project.

# Import thingies
from Modules.simulation_math import run_simulation


if __name__ == "__main__":

    # Define the simulation parameters
    n_max = 10000
    dt = 1

    # Run the simulation
    pos_hist, vel_hist, acc_hist, flows_hist, atmos_time = run_simulation(n_max, dt, Method = "KR4")

    # Plot the results


