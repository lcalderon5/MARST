# Lucas Calderon
# This file contains the data for the spacecraft that will be simulated.
import sys
import os
import spiceypy as spice
import numpy as np

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import namedtuple
import Config.bodies_data as bd
from Modules.helper import orbital_elements_to_cartesian

# Using named tuples to make it more numba friendly, they are immutable and faster than dictionaries

# Initial conditions for the spacecraft
# --------- INPUTS ------------

# Initial Orbit
body = 'Earth' # The body that the spacecraft is orbiting
Periapsis = 200 # h in km
Apoapsis = 4000 # h in km
Inclination = 0    # Inclination in degrees
Rigth_Ascension_node = 30 # Right Ascension of the Ascending Node in degrees
Argument_periapsis = 40 # deg
Mean_anomaly_epoch = 180 # deg (v0)
et = 0 # epoch time in seconds after J2000

#--------- END INPUTS ------------

if Apoapsis < Periapsis:
    raise ValueError("Apoapsis cannot be lower than the Periapsis")

# Calculate semi-major axis and eccentricity, ASSUMING EARTH ORBIT
body_data = getattr(bd, body)
Apoapsis = Apoapsis + body_data.radius_equator
Periapsis = Periapsis + body_data.radius_equator
a = (Apoapsis + Periapsis) / 2 # in km
e = (Apoapsis - Periapsis) / (Apoapsis + Periapsis) # unitless
mu = body_data.gravitational_parameter # This can be changed depending on the body that the spacecraft is initially orbiting 
Inclination = np.radians(Inclination)
Rigth_Ascension_node = np.radians(Rigth_Ascension_node)
Argument_periapsis = np.radians(Argument_periapsis)
Mean_anomaly_epoch = np.radians(Mean_anomaly_epoch)
elts = np.array([Periapsis, e, Inclination, Rigth_Ascension_node, Argument_periapsis, Mean_anomaly_epoch, et, mu])

# Convert these to a position and velocity vector
state = spice.conics(elts, et)

# Initial position and velocity
initial_position = state[:3] # km
initial_velocity = state[3:] # km/s

# Define named tuple for the spacecraft data
# Feel free to add more parameters to the spacecraft, such as fuel consumption, thrust, etc.
# Just make sure to name them in the namedtuple part and add them to the Spacecraft part as a value.

Spacecraft = namedtuple('MARST', ['name', 'mass0', 'C_D', 'A', 'A_intake', 'eff_in', 'initial_position', 'initial_velocity',
                                   'M_propellant', 'thrust', 'mass_flow_rate'])

spacecraft = Spacecraft(
                    name="MARST",
                    mass0=5000,  # kg
                    C_D=4,  # Drag coefficient
                    A=4,  # m^2
                    A_intake=4,  # m^2
                    eff_in=0.4,  # Efficiency of the intake
                    initial_position=initial_position,  # Initial position in km
                    initial_velocity=initial_velocity,  # Initial velocity in km/s
                    M_propellant=1000,  # kg
                    thrust=5,  # N
                    mass_flow_rate=0.01  # kg/s

)