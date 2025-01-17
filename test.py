# This file will simulate a ball bouncing

# Import
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the simulation parameters
n_max = 1000
dt = 0.01

# Define the initial conditions
initial_position = np.array([0, 10]) # m
initial_velocity = np.array([10, 5])

# Define the acceleration function
acc = np.array([0, -9.81]) # m/s^2

# Create lists
pos_hist = np.zeros((n_max, 2)) # Ordered in the following way: [x, y]
vel_hist = np.zeros((n_max, 2)) # Ordered in the following way: [v_x, v_y]

# Apply initial conditions
pos_hist[0] = initial_position
vel_hist[0] = initial_velocity

# Run the simulation
for i in range(n_max - 1):
    vel_hist[i+1] = vel_hist[i] + acc * dt
    pos_hist[i+1] = pos_hist[i] + vel_hist[i] * dt

    # Add bounce check
    if pos_hist[i+1][1] < 0:
        pos_hist[i+1][1] = 0
        vel_hist[i+1][1] = -vel_hist[i+1][1] * 0.9

# Animate the ball bouncing

# Extract the x and y positions
x_positions = pos_hist[:, 0]
y_positions = pos_hist[:, 1]

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(min(x_positions) - 1, max(y_positions) + 1)
ax.set_ylim(min(y_positions) - 1, max(y_positions) + 1)

# Initialize a point (ball) to be plotted
ball, = ax.plot([], [], 'bo', markersize=10)

# Function to initialize the animation
def init():
    ball.set_data([], [])
    return ball,

# Function to update the ball's position for each frame
def update(frame):
    ball.set_data(x_positions[frame], y_positions[frame])
    return ball,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x_positions), init_func=init, blit=True, interval=1)

plt.show()

