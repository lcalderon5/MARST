# Lucas Calderon
# This file contains some classes that are used in the project.

import numpy as np
from numba.experimental import jitclass

# Define spacecraft class
@jitclass
class Spacecraft:

    def __init__(self, location, Aero_param, name = ""):
        self.location = location
        self.Aero_param = Aero_param # This is a list of [m_sc, C_D, A, A_in, eff_in]
        self.name = name
    
    def radius(self):
        return self.location
    
    def r_vector(self):
        return [self.location.x, self.location.y, self.location.z]
    
    def BC(self): # Ballistic coefficient
        return self.Aero_param[1] * self.Aero_param[2] / self.Aero_param[0]