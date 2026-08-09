import numpy as np
from scipy import stats

measurements_mg_L = np.array([5.12, 5.08, 5.15, 5.10, 5.13])
confidence_level = 0.95

n = len(measurements_mg_L)
mean = np.mean(measurements_mg_L)
sample_sd = np.std(measurements_mg_L, ddof=1)
standard_error = sample_sd / np.sqrt(n)
alpha = 1 - confidence_level
t_critical = stats.t.ppf(1 - alpha / 2, df=n - 1)
margin = t_critical * standard_error
lower_limit = mean - margin
upper_limit = mean + margin

print(f"Mean: {mean:.3f} mg/L")
print(f"Standard deviation: {sample_sd:.3f} mg/L")
print(f"Standard error: {standard_error:.3f} mg/L")
print(f"{confidence_level * 100:.0f}% CI: [{lower_limit:.3f}, {upper_limit:.3f}] mg/L")
