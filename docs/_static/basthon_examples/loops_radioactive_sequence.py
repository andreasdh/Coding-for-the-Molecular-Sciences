amount = 4.0  # kg

for number_of_half_lives in range(11):
    print(f"n = {number_of_half_lives}: {amount:.6f} kg")
    amount = amount / 2
