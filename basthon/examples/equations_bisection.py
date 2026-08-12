import numpy as np

C = 0.010
Ka = 1.75e-5
Kw = 1.0e-14

def charge_balance(h):
    A_minus = C * Ka / (h + Ka)
    OH = Kw / h
    return h - A_minus - OH

def bisection(f, a, b, tol=1e-10, max_iterations=100):
    # Complete the method:
    # 1. Check that f(a) and f(b) have opposite signs.
    # 2. Calculate the midpoint.
    # 3. Keep the half-interval that contains a sign change.
    # 4. Stop when |f(m)| is smaller than tol.
    pass

# When your function is complete, uncomment:
# h_root, iterations = bisection(charge_balance, 1e-7, 1e-2)
# print(f"[H3O+] = {h_root:.6e} mol/L")
# print(f"pH = {-np.log10(h_root):.3f}")
# print("Iterations:", iterations)
