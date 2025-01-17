# Lucas Calderon
# This file contains the data for the spacecraft that will be simulated.

import numpy as np
from collections import namedtuple
from bodies_data import Earth
from Modules.helper import orbital_elements_to_cartesian

# Using named tuples to make it more numba friendly, they are immutable and faster than dictionaries

# Initial conditions for the spacecraft
# --------- INPUTS ------------

# Initial Orbit
Periapsis = 100 # h in km
Apoapsis = 5000 # h in km
Inclination = 10    # Inclination in degrees
Rigth_Ascension_node = 30 # Right Ascension of the Ascending Node in degrees
Argument_periapsis = 40 # deg
Initial_anomaly = 180 # deg

# Calculate semi-major axis and eccentricity
Apoapsis = Apoapsis + Earth.radius_equator
Periapsis = Periapsis + Earth.radius_equator
a = (Apoapsis + Periapsis) / 2 # in km
e = (Apoapsis - Periapsis) / (Apoapsis + Periapsis) # unitless

# Convert these to a position and velocity vector
mu = Earth.gravitational_parameter # This can be changed depending on the body that the spacecraft is initially orbiting
initial_position, initial_velocity = orbital_elements_to_cartesian(mu, Periapsis, Apoapsis, Inclination, Rigth_Ascension_node, Argument_periapsis, Initial_anomaly)



# Define named tuple for the spacecraft data
# Feel free to add more parameters to the spacecraft, such as fuel consumption, thrust, etc.
# Just make sure to name them in the namedtuple part and add them to the Spacecraft part as a value.

Spacecraft = namedtuple('MARST', ['name', 'mass', 'C_D', 'A', 'A_intake', 'eff_in', 'initial_position', 'initial_velocity'])

Spacecraft = Spacecraft(
                    name="MARST",
                    mass=5000,  # kg
                    C_D=4,  # Drag coefficient
                    A=4,  # m^2
                    A_intake=4,  # m^2
                    eff_in=0.4,  # Efficiency of the intake
                    initial_position=initial_position,  # Initial position in km
                    initial_velocity=initial_velocity  # Initial velocity in km/s
)