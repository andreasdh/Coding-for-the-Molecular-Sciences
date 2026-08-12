concentration = 0.80       # mol/L
limit = 0.05               # mol/L
number_of_dilutions = 0

while concentration >= limit:
    print(f"After {number_of_dilutions} dilutions: {concentration:.3f} mol/L")
    concentration = concentration / 2
    number_of_dilutions = number_of_dilutions + 1

print(f"The concentration is now {concentration:.3f} mol/L.")
