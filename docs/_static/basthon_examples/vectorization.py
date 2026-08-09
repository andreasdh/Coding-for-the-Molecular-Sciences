import numpy as np
import time

size = 200000
array1 = np.linspace(1, 10, size)
array2 = np.linspace(10, 1, size)

start = time.perf_counter()
loop_result = np.zeros(size)
for i in range(size):
    loop_result[i] = array1[i] * array2[i]
loop_time = time.perf_counter() - start

start = time.perf_counter()
vectorized_result = array1 * array2
vectorized_time = time.perf_counter() - start

print(f"Loop time: {loop_time:.6f} s")
print(f"Vectorised time: {vectorized_time:.6f} s")
print("Results agree:", np.allclose(loop_result, vectorized_result))
