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

# Numba compatible function
def atmos_data(filename=r'C:\Users\lucas\Desktop\Code Adventures\MARST\MARST\Modules\01-01-2025 N43.3W3 NRLMSIS-00.txt'):

    # Load data with numpy
    data = np.genfromtxt(filename, delimiter=None, names=True, dtype=None)
    print(data.dtype.names)

    # Extract colums as np arrays, and convert units
    h = np.array(data['Heit(km)'], dtype=np.float64)
    O = np.array(data['Oden(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    N2 = np.array(data['N2den(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    O2 = np.array(data['O2den(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    air = np.array(data['air(gm/cm3)'], dtype=np.float64) * 1000 # in Kg/m3
    T = np.array(data['T(K)'], dtype=np.float64)
    He = np.array(data['Heden(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    Ar = np.array(data['Arden(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    H = np.array(data['Hden(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3
    N = np.array(data['Nden(cm-3)'], dtype=np.float64) * 1e6 # in molecules/m3

    return h, O, N2, O2, air, T, He, Ar, H, N

# Load data
h, O, N2, O2, air, T, He, Ar, H, N = atmos_data()
