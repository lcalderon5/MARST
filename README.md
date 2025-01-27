# MARST
Program to help in the design of a Multi-mission, Atmospheric Refueling Space Tug.

# Conventions for coordinates
The coordinates used during calculation are cartesian coordinates, according to the J2000 ECI coordinate system

Reference Frame:
    Origin: The center of the Earth.
    Primary Axis: The x-axis points toward the vernal equinox as it appeared on January 1, 2000, 12:00 TT (Terrestrial Time).
    Plane: The x-y plane lies in the Earth's equatorial plane as of the J2000 epoch.
    z-Axis: Points along the Earth's rotational axis (northward), perpendicular to the x-y plane.

Inertial Frame:
    The J2000 ECI frame is considered inertial, meaning it does not rotate with the Earth. It’s fixed relative to distant stars, making it ideal for orbital dynamics.
    
Fixed Epoch:
    The reference is tied to a specific epoch (J2000.0), so it accounts for the Earth's orientation and precession at that time. Over time, Earth's axis precesses and nutates, but J2000 remains fixed.

Often coordinates for position, velocity or acceleration are sotred in numpy arrays in the order [x, y, z]

# About numba
I'm still learning how to properly use it, but so far some recomendations are:  
Rules to ensure numba works as good as possible
    Avoid dictionaries, you can use named tuples instead
    Avoid lists with different types inside
    Use nonpython mode as much as possible
    basically use simple arithmetic and life wil be fast and good


# About the simulation function: run_simualation()
This function basically runs the math of the simulation and integrates the spacecrafts motions, it then outputs arrays with data from the dyamics and even the atmosphere. The plan is to make the simulation be able to run with some different numerical integration methods such as euler, runge-kutta 4, verlet and in the future runge - kutta 4-5. It is built such that everything is stored in numpy arrays for numba compatiblitiy. It is best to keep it as lightweight as possible to make it more efficient and avoid upsettin numba

For now it only needs the acceleration function, which should also take into account drag.

# Notes for Lucas
Check out pygmo
Check out pykep