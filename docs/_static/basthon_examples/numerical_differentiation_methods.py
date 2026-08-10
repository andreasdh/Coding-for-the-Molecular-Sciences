import numpy as np

def forward_difference(f, x, h):
    return (f(x + h) - f(x)) / h

def backward_difference(f, x, h):
    # Complete this function
    pass

def central_difference(f, x, h):
    # Complete this function
    pass

def f(x):
    return np.sin(x)

x = 1.0
exact = np.cos(x)

for h in [1e-1, 1e-2, 1e-3, 1e-4]:
    forward = forward_difference(f, x, h)
    # Uncomment when you have completed the functions:
    # backward = backward_difference(f, x, h)
    # central = central_difference(f, x, h)
    # print(h, forward, backward, central, exact)
    print("h =", h, "forward =", forward, "exact =", exact)
