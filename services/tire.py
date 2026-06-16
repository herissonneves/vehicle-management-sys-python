from services.odometer import load_vehicle_dicts

COLD_PRESSURE = 32
HOT_PRESSURE = 34


def show_tire_pressure():
    """
    Read vehicle data from the database and display fixed pressure recommendations.
    """
    for row in load_vehicle_dicts():
        print("-" * 50)
        print(f"Vehicle: {row['brand']} {row['model']} {row['version']} ({row['plate']})")
        print(f"Recommended pressure (cold): {COLD_PRESSURE} psi")
        print(f"Recommended pressure (hot):  {HOT_PRESSURE} psi")
        print("-" * 50)


if __name__ == "__main__":
    show_tire_pressure()
