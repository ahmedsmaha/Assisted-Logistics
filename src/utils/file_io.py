"""File I/O Utilities Module
This module provides functions to load zones mapping, read orders and couriers,
read log entries, and write output data to JSON files.
It handles file existence checks and ensures data is correctly formatted."""
import json
import csv
import os
from src.utils.helpers import parse_datetime, normalize_order_id


def load_zones_mapping(filename):
    """Load zones mapping from a CSV file."""
    if not os.path.exists(filename):
        return {}
    mapping = {}
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_key = row['raw'].strip().lower()
            mapping[raw_key] = row['canonical']
    return mapping


def read_orders(filename):
    """Read orders from a JSON file."""
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', encoding='utf-8') as f:
        return json.load(f)


def read_couriers(filename):
    """Read couriers from a JSON file."""
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', encoding='utf-8') as f:
        return json.load(f)


def read_log(filename):
    """Read log entries from a CSV file."""
    if not os.path.exists(filename):
        return []
    entries = []
    with open(filename, mode='r', encoding='utf-8') as f:
        # Handle log files with and without headers
        sample = f.read(1024)
        f.seek(0)

        has_header = csv.Sniffer().has_header(sample)
        reader = csv.reader(f)

        if has_header:
            next(reader)  # Skip header row

        for row in reader:
            try:
                if len(row) < 3:
                    continue

                entry = {
                    'orderId': normalize_order_id(row[0]),
                    'courierId': row[1].strip().upper(),
                    'deliveredAt': parse_datetime(row[2])
                }
                entries.append(entry)
            except (IndexError, ValueError):
                continue
    return entries


def write_json(filename, data):
    """Write data to a JSON file."""
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
