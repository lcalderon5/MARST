# Lucas Calderon
# This file contains the data for the spacecraft that will be simulated.

import numpy as np
from collections import namedtuple

# Using named tuples to make it more numba friendly, they are immutable and faster than dictionaries

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
                    initial_position=np.array([6500, 0, 0]),  # Initial position in km
                    initial_velocity=np.array([0, 0, 0])  # Initial velocity in km/s
)