import numpy as np
import matplotlib.pyplot as plt

k = 0.03
A0 = 1.0
dt = 1.0
t_end = 150

time = np.arange(0, t_end + dt, dt)
A = np.zeros(len(time))
A[0] = A0

for n in range(len(time) - 1):
    # Complete the Euler update:
    # A[n + 1] = ...
    A[n + 1] = A[n]

analytical = A0*np.exp(-k*time)

plt.plot(time, A, "o-", label="Euler")
plt.plot(time, analytical, label="Analytical")
plt.xlabel("Time (s)")
plt.ylabel("[A] (mol/L)")
plt.legend()
plt.show()
