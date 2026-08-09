import numpy as np

data = np.array([
    [0.0, 1.0, 2.0, 3.0],
    [2.0, 9.1, 2.2, 4.0],
    [3.5, 9.1, 6.7, 5.5],
    [1.1, 0.2, 8.9, 7.8],
])

print("Complete array:\n", data)
print("Row 1:", data[1, :])
print("Column 0:", data[:, 0])
print("Element 6.7:", data[2, 2])
