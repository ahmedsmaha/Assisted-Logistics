# AI-Assisted Logistics Cleanup & Reconciliation

This program cleans and normalizes logistics order data, creates an optimal delivery plan based on courier constraints, and reconciles that plan against an actual delivery log.

## Prerequisites

-   Python 3.7+
-   No external libraries are required. All necessary modules (`json`, `csv`, `re`, `datetime`, `os`) are part of the Python standard library.

## Project Structure

The project expects the following directory structure:

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   │   ├── assignment.py
│   │   └── reconciliation.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_io.py
│   └── └── helpers.py
├── input/
│   ├── orders.json
│   ├── couriers.json
│   ├── zones.csv
│   └── log.csv
├── output/
│   ├── clean_orders.json
│   ├── plan.json
│   └── reconciliation.json
├── AI_NOTES.md
├── ASSUMPTIONS.md
└── README.md
```

## How to Run

1.  **Place Input Files:** Ensure your four input data files (`orders.json`, `couriers.json`, `zones.csv`, `log.csv`) are located inside the `input/` directory.

2.  **Execute the Script:** From the src directory of the project, run the following command in your terminal:

    ```bash
    python3 -m src.main
    ```

3.  **Check the Output:** The script will process the input files and generate three JSON files (`clean_orders.json`, `plan.json`, `reconciliation.json`) in the `output/` directory. The program will print a confirmation message to the console upon successful creation of each file.
