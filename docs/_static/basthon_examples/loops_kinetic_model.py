k = 0.15             # rate constant in s^-1
A = 1.00             # initial concentration of A in mol/L
B = 0.00             # initial concentration of B in mol/L
dt = 0.10            # time step in s
end_time = 10        # final time in s

number_of_steps = int(end_time / dt)

for step in range(number_of_steps):
    change = k * A * dt
    A = A - change
    B = B + change

print(f"After {end_time} s, [A] = {A:.3f} mol/L.")
print(f"After {end_time} s, [B] = {B:.3f} mol/L.")
print(f"Total concentration: {A + B:.3f} mol/L.")
