import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import spiceypy as spice
import time
import pymsis as msis
import datetime 

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Config import bodies_data as bd

# Load the SPICE Kernels
spice.furnsh(r"C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Data\Spice\Solar_sytem_kernel.tm")

# Get todays date
et = spice.str2et('2022-01-01T00:00:00')
date = datetime.datetime(2013, 3, 31, 12)

# Latitudes, longitudes and altitudes
lats = np.linspace(-90, 90, 100)
lons = np.linspace(-180, 180, 100)
alts = np.linspace(0, 1000, 100)

start = time.perf_counter()
output = msis.calculate(date, lons, lats, alts)
end = time.perf_counter()
print(f"Time elapsed: {end-start} seconds")
