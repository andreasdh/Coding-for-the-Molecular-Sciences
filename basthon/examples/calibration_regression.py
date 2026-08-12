import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

concentration_uM = np.array([0, 0, 2, 2, 2, 4, 4, 4, 6, 6, 6, 8, 8, 8, 10, 10, 10])
absorbance = np.array([0.010, 0.011, 0.171, 0.169, 0.172, 0.329, 0.331, 0.328, 0.489, 0.491, 0.487, 0.648, 0.652, 0.650, 0.807, 0.812, 0.809])
unknown_absorbance = np.mean([0.603, 0.606, 0.604])

result = stats.linregress(concentration_uM, absorbance)
slope = result.slope
intercept = result.intercept
r_squared = result.rvalue**2
unknown_concentration = (unknown_absorbance - intercept) / slope

x_model = np.linspace(concentration_uM.min(), concentration_uM.max(), 100)
y_model = slope * x_model + intercept

plt.scatter(concentration_uM, absorbance, label="Measurements")
plt.plot(x_model, y_model, label="Linear model")
plt.xlabel("Concentration (µmol/L)")
plt.ylabel("Absorbance")
plt.legend()
plt.tight_layout()
plt.show()

print(f"Slope: {slope:.5f} L/µmol")
print(f"Intercept: {intercept:.5f}")
print(f"R²: {r_squared:.6f}")
print(f"Unknown concentration: {unknown_concentration:.2f} µmol/L")
