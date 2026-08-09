total_volume = 24       # mL
volume_per_tube = 5     # mL

full_tubes = total_volume // volume_per_tube
remaining_volume = total_volume % volume_per_tube

print("Number of full test tubes:", full_tubes)
print("Remaining solution:", remaining_volume, "mL")
