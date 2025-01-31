import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import spiceypy as spice
import time
import pymsis as msis
import nrlmsise00 as nrl
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
lats = 50 # np.linspace(-90, 90, 100)
lons = 50 # np.linspace(-180, 180, 100)
alts = 400 # np.linspace(0, 1000, 100)

start = time.perf_counter()
output = msis.calculate(date, lons, lats, alts, f107s=150, f107as=150, aps=4)
end = time.perf_counter()
print(f"Time elapsed: {end-start} seconds")
print(output)

switches = [1 for _ in range(24)]
start = time.perf_counter()
output = nrl.msise_model(date, alts, lats, lons, f107a=150, f107=150, ap=4, flags=switches)
end = time.perf_counter()
print(f"Time elapsed: {end-start} seconds")
print(output)
