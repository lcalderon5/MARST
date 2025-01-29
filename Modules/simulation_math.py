# Lucas Calderon
# This file contains the numerical methods and math to run the sim
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import scipy.integrate as spi
from numba import njit
from Modules.dynamics import acceleration
from Config.spacecraft import spacecraft
from Modules.helper import sc_heigth, orbital_elements_to_cartesian


# Orbit propagator using scipy ODE solver: solve_ivp with RK45
def propagate_phase(t_span:np.ndarray, acc_func:callable, state0:np.ndarray):

    """
    This function propagates an orbit.

    Inputs:
        t_span: The time span of the simulation, a 2 member numpy array with the initial and final time, in et seconds
        acc_func: The acceleration function to use
        state0: The initial state of the spacecraft, a 7 member numpy array with the initial position, velocity and mass of the spacecraft
    Returns:
        pos_hist: THe history of the positions of the spacecraft
        vel_hist: The history of the velocities of the spacecraft
        mass_hist: The history of the mass of the spacecraft
        t_hist: The history of the time of the simulation

    """
    # Print that the propagation is starting
    print("Propagating orbit")

    # Define event functions
    # Collision event
    def collision_event(t, state):
        R = 6371  # Earth's radius in meters
        tolerance = 69  # Allow a buffer for a realistic height boundary
        r = np.linalg.norm(state[:3])
        return r - (R + tolerance)

    collision_event.terminal = True
    collision_event.direction = 0

    # SOI event (Work in progress, for the future)
    def SOI_event(t, state):
        pass

    # Define the events
    events = [collision_event]

    # Solve ODE: dv/dt = a, dx/dt = v
    sol = spi.solve_ivp(acc_func, t_span, state0, method='LSODA', rtol=1e-9, atol=1e-9, events=events)

    # Extract the results
    t_hist = sol.t
    pos_hist = sol.y[:3]
    vel_hist = sol.y[3:6]
    mass_hist = sol.y[6]

    # Print end
    print("Propagation finished")
    
    return t_hist.T, pos_hist.T, vel_hist.T, mass_hist.T


# Numba compatible propagation function (OLD, NOT SUPPORTED ANYMORE)
@njit
def run_simulation(n_max: int, dt:float, Method:str = "RK4"):
    """
    This function runs the simulation.

    Inputs:
        dt = 1: The time step of the simulation
        n_max = 1000: The maximum number of time steps of the simulation
        Method = "RK4": The method to use to run the simulation. Currently only RK4 is supported, but more methods can be added in the future.
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

    elif Method == "RK4":
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
            
            if sc_heigth(pos_hist[i]) < 745:
                atmos_time += dt
                # Calculate the composition of the air captured by the spacecraft
                flows_hist[i] = [0, 0, 0, 0, 0, 0, 0, 0] # This is a placeholder for now
                
                # Check for crash
                if sc_heigth(pos_hist[i]) < 69: # Check for unrealistic values
                    print("The spacecraft has crashed")

                    # Trim the ourput arrays
                    pos_hist = pos_hist[:i]
                    vel_hist = vel_hist[:i]
                    acc_hist = acc_hist[:i]
                    flows_hist = flows_hist[:i]

                    break

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


