def dilution(initial_concentration, initial_volume, final_volume):
    final_concentration = initial_concentration * initial_volume / final_volume
    dilution_factor = final_volume / initial_volume
    amount = initial_concentration * initial_volume / 1000  # volumes in mL
    return final_concentration, dilution_factor, amount

c2, factor, n = dilution(0.50, 10.0, 100.0)

print(f"Final concentration: {c2:.3f} mol/L")
print(f"Dilution factor: {factor:.0f}")
print(f"Amount of substance: {n:.4f} mol")
