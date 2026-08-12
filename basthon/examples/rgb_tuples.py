import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Create four RGB tuples here. Components should be integers from 0 to 255.
red = (255, 0, 0)
green = (0, 180, 0)
blue = (0, 0, 255)
purple = (150, 0, 180)

colours = [red, green, blue, purple]

fig, ax = plt.subplots()
for i, rgb in enumerate(colours):
    colour = tuple(component / 255 for component in rgb)
    ax.add_patch(Circle((i + 1, 1), 0.35, color=colour))

ax.set_xlim(0.4, 4.6)
ax.set_ylim(0.4, 1.6)
ax.set_aspect("equal")
ax.axis("off")
plt.show()
