import numpy as np
from numba import njit
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
M = 5.972e24     # Mass of Earth, kg
R = 6.371e6      # Radius of Earth, m

@njit
def compute_acceleration(position):
    """Compute gravitational acceleration at a given position."""
    r = np.linalg.norm(position)
    if r == 0:
        return np.array([0.0, 0.0])
    return -G * M / r**3 * position

@njit
def run_simulation(initial_position, initial_velocity, dt, steps):
    """Simulate the orbit using the Euler method."""
    position = np.zeros((steps, 2))
    velocity = np.zeros((steps, 2))
    position[0] = initial_position
    velocity[0] = initial_velocity

    for i in range(1, steps):
        acceleration = compute_acceleration(position[i-1])
        velocity[i] = velocity[i-1] + acceleration * dt
        position[i] = position[i-1] + velocity[i-1] * dt

    return position

# Initial conditions
initial_position = np.array([R + 500e3, 0.0])  # 500 km above Earth's surface
initial_velocity = np.array([0.0, 7.8e3])      # Approx orbital velocity, m/s
dt = 1.0                                       # Time step, seconds
steps = 10000                                  # Number of steps

# Run the simulation
positions = run_simulation(initial_position, initial_velocity, dt, steps)

# Plot the orbit
plt.figure(figsize=(8, 8))
plt.plot(positions[:, 0], positions[:, 1], label="Orbit")
plt.scatter(0, 0, color='red', label="Earth", s=100)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Orbit Simulation")
plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.legend()
plt.grid()
plt.show()
