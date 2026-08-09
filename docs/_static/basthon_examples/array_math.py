import numpy as np

v = np.array([1.0, 4.0, 5.0])
w = np.array([2.0, -1.0, 3.0])

print("v + w =", v + w)
print("v - w =", v - w)
print("2v =", 2 * v)
print("Element-wise product =", v * w)
print("Dot product =", np.dot(v, w))
print("Length of v =", np.linalg.norm(v))
