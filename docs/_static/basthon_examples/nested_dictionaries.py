elements = {
    "H": {
        "name": "hydrogen",
        "atomic_number": 1,
        "atomic_mass": 1.008,
        "melting_point_C": -259.16,
    },
    "V": {
        "name": "vanadium",
        "atomic_number": 23,
        "atomic_mass": 50.942,
        "melting_point_C": 1910,
    },
}

for symbol, properties in elements.items():
    print(symbol)
    for property_name, value in properties.items():
        print(f"  {property_name}: {value}")

print("Atomic mass of V:", elements["V"]["atomic_mass"])
