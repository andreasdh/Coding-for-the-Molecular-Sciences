import numpy as np
from scipy import stats

method_A_mg_L = np.array([5.10, 10.20, 7.50, 12.30, 3.90, 8.80, 15.10, 6.40])
method_B_mg_L = np.array([5.22, 10.28, 7.65, 12.40, 3.99, 8.93, 15.21, 6.47])

differences = method_B_mg_L - method_A_mg_L
test = stats.ttest_rel(method_B_mg_L, method_A_mg_L)

print("Difference for each sample pair:")
print(differences)
print(f"Mean difference: {differences.mean():.3f} mg/L")
print(f"p-value: {test.pvalue:.5f}")
