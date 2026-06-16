"""
This module provides functions to calculate tire diameters and their effects on odometer readings.

The module contains utilities to:
- Calculate the total diameter of a tire based on its specifications
- Determine how different tire sizes affect odometer readings
- Calculate actual distances traveled when using non-standard tire sizes
"""
from models.odomoter_difference_result import OdometerDifferenceResult
from models.tire import Tire
from services.database import VehicleEntry, session_scope


def calculate_total_diameter(tire: Tire) -> float:
    """
    Calculate the total diameter of a tire in millimeters.

    Args:
        tire (Tire): A Tire object containing width, aspect ratio and rim measurements

    Returns:
        float: The total diameter of the tire in millimeters
    """
    sidewall_height = tire.width * (tire.aspect_ratio / 100)
    rim_in_mm = tire.rim * 25.4
    return 2 * sidewall_height + rim_in_mm


def calculate_odometer_difference(original: Tire, replacement: Tire) -> OdometerDifferenceResult:
    """
    Compare original and replacement tire diameters to determine odometer discrepancy.

    Args:
        original (Tire): The original tire.
        replacement (Tire): The replacement tire.

    Returns:
        OdometerDifferenceResult: Object with detailed comparison results.
    """
    original_diameter = calculate_total_diameter(original)
    replacement_diameter = calculate_total_diameter(replacement)

    difference_percentage = ((replacement_diameter - original_diameter) / original_diameter) * 100
    direction = 'underreports' if difference_percentage > 0 else 'overreports'
    real_distance_per_100km = 100 + difference_percentage

    return OdometerDifferenceResult(
        original_diameter=round(original_diameter, 2),
        replacement_diameter=round(replacement_diameter, 2),
        difference_percentage=round(abs(difference_percentage), 2),
        direction=direction,
        real_distance_per_100km=round(real_distance_per_100km, 2)
    )


def load_vehicles() -> list[VehicleEntry]:
    """
    Load vehicle data from the database.
    """
    with session_scope() as session:
        return session.query(VehicleEntry).order_by(VehicleEntry.id.asc()).all()


def load_vehicle_dicts() -> list[dict]:
    """
    Load vehicle data from the database using the dictionary shape expected by existing UI code.
    """
    vehicles = []
    for vehicle in load_vehicles():
        vehicles.append({
            "brand": vehicle.brand,
            "model": vehicle.model,
            "version": vehicle.version,
            "plate": vehicle.plate,
            "year": str(vehicle.year),
            "original_width": str(vehicle.original_width),
            "original_aspect": str(vehicle.original_aspect),
            "original_rim": str(vehicle.original_rim),
            "current_width": str(vehicle.current_width),
            "current_aspect": str(vehicle.current_aspect),
            "current_rim": str(vehicle.current_rim),
            "fuel_tank_capacity": str(vehicle.fuel_tank_capacity or ""),
        })
    return vehicles


def load_tires() -> list[tuple[str, Tire, Tire]]:
    """
    Load tire data from the database and create Tire objects for each vehicle.

    Returns:
        list of tuple: Each tuple contains a label and two Tire objects (original and current).
    """
    vehicles = []
    for vehicle in load_vehicles():
        label = f"{vehicle.brand} {vehicle.model} {vehicle.plate} ({vehicle.year})"
        original = Tire(
            width=vehicle.original_width,
            aspect_ratio=vehicle.original_aspect,
            rim=vehicle.original_rim,
        )
        current = Tire(
            width=vehicle.current_width,
            aspect_ratio=vehicle.current_aspect,
            rim=vehicle.current_rim,
        )
        vehicles.append((label, original, current))
    return vehicles


def show_odometer_differences_from_file():
    """
    Print the odometer difference results for each vehicle listed in the database.
    """
    vehicles = load_tires()

    for label, original, current in vehicles:
        result = calculate_odometer_difference(original, current)

        print(f"\nVehicle: {label}")
        print(f"Odometer {result.direction} by {result.difference_percentage:.2f}%")
        print(f"When odometer shows 100km, real distance is: {result.real_distance_per_100km:.2f} km")
