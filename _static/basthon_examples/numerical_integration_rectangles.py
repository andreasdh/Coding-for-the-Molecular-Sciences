def left_rectangle(f, a, b, n):
    h = (b - a) / n
    area = 0.0
    x = a

    for k in range(n):
        area = area + f(x) * h
        x = x + h

    return area

def right_rectangle(f, a, b, n):
    # Complete this function
    pass

def midpoint_rectangle(f, a, b, n):
    # Complete this function
    pass

def f(x):
    return x**3

a = 0
b = 5

for n in [10, 100, 1000]:
    print("n =", n, "left =", left_rectangle(f, a, b, n))
    # Uncomment when the other methods are complete:
    # print("right =", right_rectangle(f, a, b, n))
    # print("midpoint =", midpoint_rectangle(f, a, b, n))
