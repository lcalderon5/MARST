# Lucas Calderon
# This file contains the data for the celestial bodies that will be simulated.
# The data is in the form of dictionaries.

# Earth data
earth = {
    "name": "Earth",
    "mass": 5.9722e24,  # kg
    "radius_equator": 6378.137,  # km
    "radius_polar": 6356.752,  # km
    "gravitational_parameter": 3.986004418e5,  # km^3/s^2
    "J2": 1.08262668e-3, # J2 coefficient for Earth oblateness
    "day": 86164.1,  # seconds 
    }

# Moon data
moon = {
    "name": "Moon",
    "mass": 7.342e22,  # kg
    "radius": 1737.5,  # km
    "gravitational_parameter": 4.9048695e3,  # km^3/s^2
    "day": 2360591.5,  # seconds
    }