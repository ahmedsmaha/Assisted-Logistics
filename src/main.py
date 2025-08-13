"""Main script for processing orders, couriers, and log entries.
It reads input data from JSON and CSV files, processes it to clean orders,
plans assignments for couriers, reconciles the planned assignments with actual deliveries,
and writes the output data to JSON files.
It handles file existence checks and ensures data is correctly formatted."""
import os
from src.processing.data_processing import clean_orders
from src.processing.assignment import plan_assignments
from src.processing.reconciliation import reconcile
from src.utils.file_io import read_orders, read_couriers, read_log, write_json

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def ensure_directory_exists(path):
    """Ensure that the specified directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    """Main function to process orders, couriers, and log entries."""
    # Ensure directories exist
    ensure_directory_exists(INPUT_DIR)
    ensure_directory_exists(OUTPUT_DIR)

    # Define input paths
    orders_path = f'{INPUT_DIR}/orders.json'
    couriers_path = f'{INPUT_DIR}/couriers.json'
    zones_path = f'{INPUT_DIR}/zones.csv'
    log_path = f'{INPUT_DIR}/log.csv'

    # Load input data
    orders = read_orders(orders_path)
    couriers = read_couriers(couriers_path)
    log_entries = read_log(log_path)

    # Process data
    cleaned_orders = clean_orders(orders, zones_path)
    plan = plan_assignments(cleaned_orders, couriers)
    reconciliation = reconcile(cleaned_orders, plan, log_entries, couriers)

    # Define output paths
    clean_orders_path = f'{OUTPUT_DIR}/clean_orders.json'
    plan_path = f'{OUTPUT_DIR}/plan.json'
    reconciliation_path = f'{OUTPUT_DIR}/reconciliation.json'

    # Write outputs
    write_json(clean_orders_path, cleaned_orders)
    write_json(plan_path, plan)
    write_json(reconciliation_path, reconciliation)

    print(f"Success! Outputs written to {OUTPUT_DIR}/ directory")


if __name__ == '__main__':
    main()
