import matplotlib.pyplot as plt

time_s = [0, 10, 20, 30, 40, 50, 60]
absorbance = [0.812, 0.673, 0.552, 0.458, 0.378, 0.313, 0.260]

plt.plot(time_s, absorbance, marker="o")
plt.xlabel("Time (s)")
plt.ylabel("Absorbance")
plt.title("Absorbance during a reaction")
plt.tight_layout()
plt.show()
