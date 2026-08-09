import matplotlib.pyplot as plt

temperature_C = [16, 18, 20, 22, 24]
vapour_pressure_kPa = [1.817, 2.063, 2.339, 2.644, 2.984]

plt.scatter(temperature_C, vapour_pressure_kPa, s=55, label="Measurements")
plt.xlabel("Temperature (°C)")
plt.ylabel("Vapour pressure (kPa)")
plt.title("Vapour pressure of water")
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()
