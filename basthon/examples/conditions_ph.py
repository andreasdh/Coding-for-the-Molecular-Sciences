pH = float(input("Enter the pH value: "))

if pH < 7:
    print("The solution is acidic.")
elif pH > 7:
    print("The solution is basic.")
else:
    print("The solution is neutral.")
