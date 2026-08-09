amount_mg = 10.0

for half_life in range(1, 6):
    amount_mg = amount_mg / 2
    print(f"After {half_life} half-lives: {amount_mg:.3f} mg")
