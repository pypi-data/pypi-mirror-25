import matplotlib.pyplot as plt
import numpy as np
plt.ion()
plt.scatter(*np.random.randn(2, 1000), c=np.random.randn(1000))
plt.show()