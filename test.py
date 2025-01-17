import numpy as np
import matplotlib.pyplot as plt

# Define constants
mass = 1.0  # kg
initial_position = np.array([0.0, 0.0])  # meters
initial_velocity = np.array([1.0, 0.0])  # m/s (initial velocity in x direction)

# Define the acceleration as a function of time or position
def acceleration(t, position, velocity):
    # Example: constant acceleration in the x direction
    return np.array([0.0, -9.81])  # m/s^2 (gravity in the negative y direction)

# Define the system of equations
def system(t, state):
    position = state[:2]
    velocity = state[2:]
    acc = acceleration(t, position, velocity)
    return np.concatenate([velocity, acc])

# Runge-Kutta 4th order method
def runge_kutta_4(f, t0, tf, h, initial_state):
    t = np.arange(t0, tf, h)
    num_steps = len(t)
    state = np.zeros((num_steps, len(initial_state)))

    state[0] = initial_state
    for i in range(1, num_steps):
        t_current = t[i-1]
        state_current = state[i-1]

        k1 = h * f(t_current, state_current)
        k2 = h * f(t_current + 0.5 * h, state_current + 0.5 * k1)
        k3 = h * f(t_current + 0.5 * h, state_current + 0.5 * k2)
        k4 = h * f(t_current + h, state_current + k3)

        state[i] = state_current + (k1 + 2*k2 + 2*k3 + k4) / 6

    return t, state

# Define initial state
initial_state = np.concatenate([initial_position, initial_velocity])

# Time parameters
t0 = 0.0  # Start time
tf = 10.0  # End time
h = 0.01  # Time step size

# Solve using Runge-Kutta method
t, state = runge_kutta_4(system, t0, tf, h, initial_state)

# Extract position and velocity from the state array
positions = state[:, :2]  # Position is the first two components
velocities = state[:, 2:]  # Velocity is the last two components

# Plot results
plt.figure(figsize=(12, 6))

# Position plot
plt.subplot(1, 2, 1)
plt.plot(t, positions[:, 0], label="X Position")
plt.plot(t, positions[:, 1], label="Y Position")
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Position vs Time')
plt.legend()

# Velocity plot
plt.subplot(1, 2, 2)
plt.plot(t, velocities[:, 0], label="X Velocity")
plt.plot(t, velocities[:, 1], label="Y Velocity")
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Time')
plt.legend()

plt.tight_layout()
plt.show()
