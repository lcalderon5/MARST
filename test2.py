import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
mu = 398600.4418  # Gravitational parameter for Earth (km^3/s^2)
Re = 6378.137     # Earth's equatorial radius (km)
J2 = 1.08263e-3   # J2 coefficient of Earth's gravitational field

# Orbital parameters (example)
a = 10000          # Semi-major axis (km)
e = 0.001          # Eccentricity
i = np.radians(98) # Inclination (radians)
omega = np.radians(100)  # Argument of perigee (radians)
raan = 0           # Right ascension of ascending node (radians)
M0 = 0             # Mean anomaly at t=0 (radians)

# Initial orbital state (elements to state vector conversion)
def orbital_elements_to_state(a, e, i, omega, raan, M0):
    # Initial conditions (state vector in 6D [x, y, z, vx, vy, vz])
    p = a * (1 - e**2)  # semi-latus rectum
    r = p / (1 + e * np.cos(M0))  # Initial distance from the center
    theta = M0
    x = r * (np.cos(raan) * np.cos(omega + theta) - np.sin(raan) * np.sin(omega + theta) * np.cos(i))
    y = r * (np.sin(raan) * np.cos(omega + theta) + np.cos(raan) * np.sin(omega + theta) * np.cos(i))
    z = r * (np.sin(i) * np.sin(omega + theta))
    r_vec = np.array([x, y, z])

    # Velocity (using orbital mechanics relations)
    # Derivative of position to get velocity components
    vx = np.sqrt(mu / a) * (-np.sin(M0))
    vy = np.sqrt(mu / a) * (np.sqrt(1 - e**2) * np.cos(M0))
    vz = 0
    v_vec = np.array([vx, vy, vz])
    
    return np.concatenate([r_vec, v_vec])

# J2 Perturbation equations
def j2_perturbation(t, state):
    x, y, z, vx, vy, vz = state
    r = np.sqrt(x**2 + y**2 + z**2)
    R = np.array([x, y, z])
    V = np.array([vx, vy, vz])
    
    # Calculate the J2 perturbation force
    r_dot = np.dot(R, V)
    coeff = (3/2) * J2 * (mu / r**4) * Re**2

    # Perturbation on the orbital elements (argument of perigee and inclination)
    ax = -coeff * (x/r) * (5*(z**2)/r**2 - 1)
    ay = -coeff * (y/r) * (5*(z**2)/r**2 - 1)
    az = -coeff * (z/r) * (5*(z**2)/r**2 - 3)
    
    # Return derivatives of the state (6D vector)
    return [vx, vy, vz, ax, ay, az]

# Initial state vector (in 6D)
initial_state = orbital_elements_to_state(a, e, i, omega, raan, M0)

# Time span and integration
t_span = (0, 86400 * 365)  # One year (seconds)
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Evaluation time steps

# Solve the equations of motion with the J2 perturbation
sol = solve_ivp(j2_perturbation, t_span, initial_state, t_eval=t_eval)

# Extract the position and velocity components
x_vals, y_vals, z_vals = sol.y[0], sol.y[1], sol.y[2]

# Plot the orbit (3D plot)
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_vals, y_vals, z_vals, label="Orbit with J2 Precession", color="blue")
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.legend()
plt.title("Orbital Precession due to J2 Perturbation")
plt.show()

# Plot the inclination and argument of perigee evolution
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_eval / (86400), np.degrees(np.arcsin(z_vals / np.sqrt(x_vals**2 + y_vals**2 + z_vals**2))), label="Inclination (deg)")
plt.xlabel("Time (days)")
plt.ylabel("Inclination (degrees)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_eval / (86400), np.degrees(np.arctan2(y_vals, x_vals)), label="Argument of Perigee (deg)")
plt.xlabel("Time (days)")
plt.ylabel("Argument of Perigee (degrees)")
plt.legend()

plt.tight_layout()
plt.show()
