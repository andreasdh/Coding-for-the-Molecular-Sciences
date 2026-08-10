import numpy as np
import matplotlib.pyplot as plt

k = 0.15
A0 = 1.0
dt = 0.5
t_end = 20

t = np.arange(0, t_end + dt, dt)
A = np.zeros(len(t))
A[0] = A0

for n in range(len(t) - 1):
    # Complete the Euler update:
    # A[n + 1] = ...
    A[n + 1] = A[n]

analytical = A0*np.exp(-k*t)

plt.plot(t, A, "o-", label="Euler")
plt.plot(t, analytical, label="Analytical")
plt.xlabel("Time")
plt.ylabel("[A] (mol/L)")
plt.legend()
plt.show()
