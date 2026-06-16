# Vehicle Management System

Vehicle Management System is a personal desktop application for tracking vehicle fuel logs, fuel consumption, tire
pressure recommendations, and odometer correction caused by tire-size changes.

The application is built with Python, PySide6, PostgreSQL, and SQLAlchemy.

## Features

- Register refueling records with odometer, fuel type, value, price per liter, and liters.
- Calculate average fuel consumption from refueling history.
- Compare original and current tire sizes to estimate odometer difference.
- Show fixed cold/hot tire pressure recommendations.
- Display refueling records in a desktop table view.

## Requirements

- Python 3.14
- `pip`
- PostgreSQL
- macOS, Linux, or Windows with a supported Qt/PySide6 runtime

## Setup

Create a virtual environment before installing dependencies.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Windows Command Prompt

```bash
py -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

## Database

The application uses PostgreSQL through SQLAlchemy. By default, it connects to:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/vehicle_management
```

Override this by setting `DATABASE_URL`. The configured PostgreSQL user must be able to create databases if the target
database does not exist yet.

### Configure The Database URL

macOS/Linux:

```bash
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/vehicle_management"
```

Windows PowerShell:

```bash
$env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/vehicle_management"
```

On startup, the application checks whether the configured database exists. It creates the database only when it is
missing, then creates any missing tables automatically.

## Running The App

Activate the virtual environment first, then run the application from the project root.

### macOS/Linux

```bash
source .venv/bin/activate
python main.py
```

### Windows PowerShell

```bash
.\.venv\Scripts\Activate.ps1
python main.py
```

### Windows Command Prompt

```bash
.\.venv\Scripts\activate.bat
python main.py
```

In PyCharm, configure a Python run configuration that executes:

```text
main.py
```

with the working directory set to the project root.

## Initial Data

The application needs at least one vehicle row to calculate odometer correction and tire pressure recommendations.
Insert a vehicle using your PostgreSQL client:

```sql
INSERT INTO vehicles (
    brand, model, version, plate, year,
    original_width, original_aspect, original_rim,
    current_width, current_aspect, current_rim,
    fuel_tank_capacity
) VALUES (
    'Toyota', 'Corolla', 'GLI Flex', 'ABC1D23', 2019,
    195, 65, 15,
    205, 60, 16,
    60
);
```

Refueling records can be added through the application UI.

## Legacy CSV Examples

The repository still includes example CSV files under `data/` as reference material for the original file-based format:

- `data/vehicle.example.csv`
- `data/refuels.example.csv`

### Vehicle CSV

Legacy vehicle format:

```csv
brand,model,version,plate,year,original_width,original_aspect,original_rim,current_width,current_aspect,current_rim,fuel_tank_capacity
Toyota,Corolla,GLI Flex,ABC1D23,2019,195,65,15,205,60,16,60
```

### Refuels CSV

Legacy refueling format:

```csv
date,odometer,fuel_type,total_value,price_per_liter,liters
2025-04-16,12345,gasoline,250.00,5.25,47.62
```

## Development

Run syntax checks:

macOS/Linux:

```bash
source .venv/bin/activate
python -m py_compile main.py gui/main_window.py gui/dialogs/*.py services/*.py models/*.py tests/*.py
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
python -m py_compile main.py gui/main_window.py gui/dialogs/*.py services/*.py models/*.py tests/*.py
```

Run tests:

macOS/Linux:

```bash
source .venv/bin/activate
python -m pytest
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Some existing tests may need updates as the service API evolves.

## Project Structure

```text
assets/     Icons and static assets
data/       Legacy CSV example files
gui/        PySide6 windows and dialogs
models/     Dataclasses used by services
services/   Database, fueling, odometer, and tire logic
tests/      Automated tests
main.py     Application entry point
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
