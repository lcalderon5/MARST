from Modules.atmos import h, air
from Modules.helper import linear_interp
import numpy as np
import matplotlib.pyplot as plt

plt.plot(h, air)
plt.yscale('log')
plt.title('Density vs Height')
plt.grid()
plt.show()

# Now with interpolation
heights = np.linspace(0, 740, 1000)
rho = np.zeros(1000)

for i in range(1000):
    rho[i] = linear_interp(heights[i], h, air)

plt.plot(heights, rho)
plt.yscale('log')
plt.title('Density vs Height')
plt.grid()
plt.show()