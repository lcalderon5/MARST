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

# Using named tuples to make it more numba friendly, they are immutable and faster than dictionaries

# Initial conditions for the spacecraft
# --------- ORBIT INPUTS ------------

body = 'Earth' # The body that the spacecraft is orbiting
Periapsis = 400 # h in km
Apoapsis = 400 # h in km
Inclination = 45    # Inclination in degrees
Rigth_Ascension_node = 30 # Right Ascension of the Ascending Node in degrees
Argument_periapsis = 40 # deg
Mean_anomaly_epoch = 180 # deg (v0)
et = 0 # epoch time in seconds after J2000

#--------- END ORBIT INPUTS ------------

# Check that inputs make sense
if Apoapsis < Periapsis:
    raise ValueError("Apoapsis cannot be lower than the Periapsis")

if Inclination < 0 or Inclination > 180:
    raise ValueError("Inclination must be between 0 and 180 degrees")

if Rigth_Ascension_node < 0 or Rigth_Ascension_node > 360:
    raise ValueError("Right Ascension of the Ascending Node must be between 0 and 360 degrees")

if Argument_periapsis < 0 or Argument_periapsis > 360:
    raise ValueError("Argument of Periapsis must be between 0 and 360 degrees")

if Mean_anomaly_epoch < 0 or Mean_anomaly_epoch > 360:
    raise ValueError("Mean Anomaly at Epoch must be between 0 and 360 degrees")

# Process the data
body_data = getattr(bd, body)
Apoapsis = Apoapsis + body_data.radius_equator # in km
Periapsis = Periapsis + body_data.radius_equator # in km
a = (Apoapsis + Periapsis) / 2 # in km
e = (Apoapsis - Periapsis) / (Apoapsis + Periapsis) # unitless
mu = body_data.gravitational_parameter # km^3/s^2

Inclination = np.radians(Inclination) # radians
Rigth_Ascension_node = np.radians(Rigth_Ascension_node) # radians
Argument_periapsis = np.radians(Argument_periapsis) # radians
Mean_anomaly_epoch = np.radians(Mean_anomaly_epoch) # radians

elts = np.array([Periapsis, e, Inclination, Rigth_Ascension_node, Argument_periapsis, Mean_anomaly_epoch, et, mu])

# Convert these to a position and velocity vector
state = spice.conics(elts, et)

# Initial position and velocity
initial_position = state[:3] # km
initial_velocity = state[3:] # km/s

# --------- SPACECRAFT INPUTS ------------
# Define named tuple for the spacecraft data
# Feel free to add more parameters to the spacecraft, such as fuel consumption, thrust, etc.
# Just make sure to name them in the namedtuple part and add them to the Spacecraft part as a value.

Spacecraft = namedtuple('MARST', ['name', 'et0', 'mass0', 'C_D', 'A', 'A_intake', 'eff_in', 'initial_position', 'initial_velocity',
                                   'M_propellant', 'thrust', 'mass_flow_rate'])

spacecraft = Spacecraft(
                    name="MARST",
                    et0=et, # Initial epoch time in seconds after J2000
                    mass0=5000,  # kg
                    C_D=4,  # Drag coefficient
                    A=4,  # m^2
                    A_intake=4,  # m^2
                    eff_in=0.4,  # Efficiency of the intake
                    initial_position=initial_position,  # Initial position in km
                    initial_velocity=initial_velocity,  # Initial velocity in km/s
                    M_propellant=1000,  # kg
                    thrust=0,  # N
                    mass_flow_rate=0  # kg/s
)