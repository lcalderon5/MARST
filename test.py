import numpy as np
import matplotlib.pyplot as plt
from orbitpy import Orbit
from orbitpy.core import OrbitPlotter

# Example initial conditions for the orbit (semi-major axis, eccentricity, inclination, etc.)
orbit = Orbit(a=7000, e=0.1, i=30, omega=0, w=0, f=0)  # Simple example

# Propagate the orbit
orbit.plot_orbit()  # Plot the orbit

plt.show()
