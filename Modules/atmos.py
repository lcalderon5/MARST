# 30/11/2024
# This is an atmospheric model based on NASA's NRLMSIS-00 pyublic model
# By default this models the atmosphere the day 01/01/2024 at N43.3, W3 (Somewhere around Bilbao)
# , but a different file can be given to model a different atmoshpere

import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

def atmos_splines(filename: str=r'Modules\01-01-2025 N43.3W3 NRLMSIS-00.txt') -> dict:
    """
    Load atmospheric data from a file and create interpolation splines.
    
    Args:
        filename (str): Path to the atmospheric data file.
    
    Returns:
        dict: A dictionary of splines for different atmospheric parameters.
    """
    # Load file
    data = pd.read_csv(filename, sep='\s+')

    # Get lists
    h = np.array(data['Heit(km)'].tolist())
    splines = {
        'O': interp1d(h, np.array(data['Oden(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'N2': interp1d(h, np.array(data['N2den(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'O2': interp1d(h, np.array(data['O2den(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'air': interp1d(h, np.array(data['air(gm/cm3)'].tolist()), kind='linear'),  # g/cm3
        'T': interp1d(h, np.array(data['T(K)'].tolist()), kind='linear'),  # K
        'He': interp1d(h, np.array(data['Heden(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'Ar': interp1d(h, np.array(data['Arden(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'H': interp1d(h, np.array(data['Hden(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
        'N': interp1d(h, np.array(data['Nden(cm-3)'].tolist()), kind='linear'),  # molecules/ cm3
    }
    
    return splines


# Return numpy arrays instead of pandas series
def atmos_data(filename=r'C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Modules\01-01-2025 N43.3W3 NRLMSIS-00.txt'):
    # Use pandas to read the space-separated file
    df = pd.read_csv(filename, sep='\s+')

    # Extract columns and convert units
    h = df['Heit(km)'].to_numpy()
    O = df['Oden(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    N2 = df['N2den(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    O2 = df['O2den(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    air = df['air(gm/cm3)'].to_numpy() * 1000  # in Kg/m3
    T = df['T(K)'].to_numpy()
    He = df['Heden(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    Ar = df['Arden(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    H = df['Hden(cm-3)'].to_numpy() * 1e6  # in molecules/m3
    N = df['Nden(cm-3)'].to_numpy() * 1e6  # in molecules/m3

    return h, O, N2, O2, air, T, He, Ar, H, N


# Load data
h, O, N2, O2, air, T, He, Ar, H, N = atmos_data()

# Plot data
import matplotlib.pyplot as plt

# Plot data
plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(h, O, label='O')
plt.plot(h, N2, label='N2')
plt.plot(h, O2, label='O2')
plt.plot(h, He, label='He')
plt.plot(h, Ar, label='Ar')
plt.plot(h, H, label='H')
plt.plot(h, N, label='N')
plt.axhline(0, color='black', lw=0.5)
plt.yscale('log')
plt.xlabel('Height (km)')
plt.ylabel('Density (molecules/m3)')
plt.legend()
plt.title('Density of Different Gases vs Height')

plt.subplot(2, 1, 2)
plt.plot(h, air, label='Air Density')
plt.axhline(0, color='black', lw=0.5)
plt.yscale('log')
plt.xlabel('Height (km)')
plt.ylabel('Air Density (Kg/m3)')
plt.legend()
plt.title('Air Density vs Height')


plt.tight_layout()
plt.show()