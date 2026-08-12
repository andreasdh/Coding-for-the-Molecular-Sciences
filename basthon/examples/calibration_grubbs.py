import numpy as np
from scipy import stats

measurements_mg_L = np.array([10.02, 10.05, 9.98, 10.01, 10.42])
alpha = 0.05

n = len(measurements_mg_L)
mean = np.mean(measurements_mg_L)
sample_sd = np.std(measurements_mg_L, ddof=1)
deviations = np.abs(measurements_mg_L - mean)
suspect_index = np.argmax(deviations)
G_calculated = deviations[suspect_index] / sample_sd
t_critical = stats.t.ppf(1 - alpha / (2 * n), df=n - 2)
G_critical = (n - 1) / np.sqrt(n) * np.sqrt(t_critical**2 / (n - 2 + t_critical**2))

print(f"Suspected measurement: {measurements_mg_L[suspect_index]:.2f} mg/L")
print(f"Calculated G: {G_calculated:.3f}")
print(f"Critical G: {G_critical:.3f}")
print("The measurement is flagged by the test." if G_calculated > G_critical else "The measurement is not flagged by the test.")
