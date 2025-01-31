# Lucas Calderon
# This file contains the data for the celestial bodies that will be simulated.
# The data is taken mostly from the NASA fact sheets for the Earth and the Moon.

from collections import namedtuple
import spicepy as spice

# Using named tuples to make it more numba friendly, they are immutable and faster than dictionaries

# Define named tuples for Earth and Moon data
Earth = namedtuple('Earth', ['name', 'mass', 'radius_mean', 'radius_equator', 'radius_polar', 'gravitational_parameter', 'J2',
                            'atmos', 'day', 'SOI', 'body2'])
Moon = namedtuple('Moon', ['name', 'mass', 'radius_mean', 'radius_equator', 'radius_polar', 'gravitational_parameter', 'J2',
                            'atmos', 'day', 'SOI', 'body2'])

# Earth data
Earth = Earth(
    name="Earth",
    mass=5.9722e24,  # kg
    radius_mean=6371,  # km
    radius_equator=6378.137,  # km
    radius_polar=6356.752,  # km
    gravitational_parameter=3.986004418e5,  # km^3/s^2
    J2=1.08262668e-3,  # J2 coefficient for Earth oblateness
    atmos=True, # The Earth has an atmosphere
    day=86164.1,  # seconds
    SOI=0.929e6, # km, Sphere of Influence
    body2='Moon', # The main perturbing body for the earth, the moon
)

# Moon data
Moon = Moon(
    name="Moon",
    mass=7.342e22,  # kg
    radius_mean=1737.4,  # km
    radius_equator=1738.1,  # km
    radius_polar=1736.0,  # km
    gravitational_parameter=4.9048695e3,  # km^3/s^2
    J2=2.033e-4,  # J2 coefficient for Moon oblateness
    atmos=False, # The Moon doesn't have an atmosphere
    day=2360591.5,  # seconds
    SOI=0.0643e6, # km
    body2='Earth', # The main perturbing body for the moon, the earth
)
