import matplotlib.pyplot as plt
import numpy as np

# Create points ranging from latitude 90 to -90

r = 6471000
theta = np.linspace(-np.pi/2, np.pi/2, 1000)

x = r * np.cos(theta)
z = r * np.sin(theta)
y = np.zeros_like(x)
position = np.array([x, y, z])

mu = 3.986004418e14
J2 = 1.082626925638815e-3
R_e = 6371000

a_total = -1.5 * mu * J2 * R_e**2 / r**5 * np.array([
        position[0] * (5 * position[2]**2 / r**2 - 1),
        position[1] * (5 * position[2]**2 / r**2 - 1),
        position[2] * (5 * position[2]**2 / r**2 - 3)])


a_mag = np.linalg.norm(a_total, axis=0)
theta = np.degrees(theta)
a_r = a_total * position / np.linalg.norm(position, axis=0)

a_r_mag = np.linalg.norm(a_r, axis=0)

plt.plot(theta, a_r[0], label="a_x")
plt.plot(theta, a_r[1], label="a_y")
plt.plot(theta, a_r[2], label="a_z")

plt.plot(theta, a_mag, label="a_mag")

plt.plot(theta, a_r_mag, label="a_r")

plt.legend()

plt.show()
