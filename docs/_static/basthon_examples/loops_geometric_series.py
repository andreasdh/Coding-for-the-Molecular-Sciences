number_of_terms = 100
total = 0

for n in range(number_of_terms):
    term = (2 / 3)**n
    total = total + term

print("Partial sum:", total)
