elements = ["H", "C", "N", "O", "F", "Na", "Mg", "Cl", "Ar"]
atomic_numbers = [1, 6, 7, 8, 9, 11, 12, 17, 18]

chlorine_index = elements.index("Cl")

print("Number of elements:", len(elements))
print("Index of Cl:", chlorine_index)
print("Atomic number of Cl:", atomic_numbers[chlorine_index])
print("Last three elements:", elements[-3:])
