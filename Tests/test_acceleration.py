import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Modules.dynamics import acceleration, acceleration_sci, acceleration_sci_new
import numpy as np

# Test the acceleration function
def test_acceleration(func):

    # Test acceleration in the north pole without drag
    position = np.array([0, 0, 6371]) # in km
    velocity = np.array([0, 0, 0])
    body = 'Earth'

    state = np.concatenate((position, velocity))

    state_dot = func(0, state) * 1000 # Convert to m/s^2
    a = state_dot[3:]

    if not np.allclose(a, np.array([0, 0, -9.82]), atol=1e-2):
        print(a)
        raise ValueError("The acceleration is incorrect")
        
    # Test acceleration with drag
    position = np.array([6471, 0, 0]) # in km
    velocity = np.array([10, 0, 0]) # in km/s

    state = np.concatenate((position, velocity))

    a = func(0, state) * 1000 # Convert to m/s^2
    a = a[3:]

    if not np.allclose(a, np.array([-9.86599, 1.63698e-2, 0]), atol=1e-1):
        print(a)
        raise ValueError("The acceleration is incorrect")
    
    print("The acceleration function is correct")

if __name__ == "__main__":

    test_acceleration(acceleration_sci)
    test_acceleration(acceleration_sci_new)