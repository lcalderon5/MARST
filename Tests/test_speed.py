import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import numpy as np
# from Modules.dynamics import acceleration, acceleration_new

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Time taken to run {func.__name__}: {end - start} seconds")
    return wrapper


if __name__ == "__main__":
    
    start = time.time()
    # Test the acceleration function
    # acceleration(np.array([0, 0, 6471]), np.array([0, 0, 0]), 'Earth')

    # end = time.time()
    # print(f"Time taken to run acceleration: {end - start} seconds")