# Vehicle Management System

Vehicle Management System is a personal desktop application for tracking vehicle fuel logs, fuel consumption, tire
pressure recommendations, and odometer correction caused by tire-size changes.

The application is built with Python and PySide6, and stores its data in local CSV files.

## Features

- Register refueling records with odometer, fuel type, value, price per liter, and liters.
- Calculate average fuel consumption from refueling history.
- Compare original and current tire sizes to estimate odometer difference.
- Show fixed cold/hot tire pressure recommendations.
- Display refueling records in a desktop table view.

## Requirements

- Python 3.14
- `pip`
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

## Data Files

The application expects local CSV files under `data/`:

- `data/vehicle.csv`
- `data/refuels.csv`

These files are ignored by Git because they contain local/personal data. Example files are provided:

- `data/vehicle.example.csv`
- `data/refuels.example.csv`

Create your local files from the examples:

```bash
cp data/vehicle.example.csv data/vehicle.csv
cp data/refuels.example.csv data/refuels.csv
```

### Vehicle CSV

`vehicle.csv` stores vehicle and tire configuration:

```csv
brand,model,version,plate,year,original_width,original_aspect,original_rim,current_width,current_aspect,current_rim,fuel_tank_capacity
Toyota,Corolla,GLI Flex,ABC1D23,2019,195,65,15,205,60,16,60
```

### Refuels CSV

`refuels.csv` stores fueling records:

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
data/       Local CSV data and example CSV files
gui/        PySide6 windows and dialogs
models/     Dataclasses used by services
services/   Fueling, odometer, and tire logic
tests/      Automated tests
main.py     Application entry point
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
