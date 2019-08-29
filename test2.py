import numpy as np

x = 3
y = -4.0
a = 0
a = np.arctan2([y],[x])[0] * 180/np.pi
a = 360 + a if a < 0 else a
print(a)