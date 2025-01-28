from Modules.dynamics import acceleration, acceleration_new
import numpy as np

# Test the acceleration function
def test_acceleration(func):

    # Test acceleration in the north pole without drag
    position = np.array([0, 0, 6371]) # in km
    velocity = np.array([0, 0, 0])
    body = 'Earth'

    a = func(position, velocity, body) * 1000 # Convert to m/s^2

    if not np.allclose(a, np.array([0, 0, -9.82]), atol=1e-2):
        raise ValueError("The acceleration is incorrect")\
        
    # Test acceleration with drag
    position = np.array([6471, 0, 0]) # in km
    velocity = np.array([10, 0, 0]) # in km/s

    a = func(position, velocity, body) * 1000 # Convert to m/s^2

    if not np.allclose(a, np.array([-9.86599, 1.63698e-2, 0]), atol=1e-1):
        raise ValueError("The acceleration is incorrect")
    
    print("The acceleration function is correct")
