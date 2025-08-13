"""Data Processing Module
This module handles the cleaning and normalization of order data, ensuring unique order IDs,
consistent formatting, and handling of duplicates. It also includes functions to normalize
zones and prepare orders for assignment to couriers."""
from src.utils.helpers import (
    normalize_order_id,
    normalize_text,
    parse_datetime,
    calculate_similarity,
)
from src.utils.file_io import load_zones_mapping


def handle_duplicate(existing, cleaned):
    """Update existing order with info from a duplicate cleaned order."""
    addr1 = normalize_text(existing['address'])
    addr2 = normalize_text(cleaned['address'])
    similarity = calculate_similarity(addr1, addr2)

    if similarity < 0.8:
        if 'warnings' not in existing:
            existing['warnings'] = []
        existing['warnings'].append(
            f"Address conflict: '{existing['address']}' vs '{cleaned['address']}'"
        )

    for field in ['city', 'zoneHint']:
        if not existing[field] and cleaned[field]:
            existing[field] = cleaned[field]

    if cleaned['deadline'] < existing['deadline']:
        existing['deadline'] = cleaned['deadline']


def clean_orders(orders, zones_file):
    """Clean and normalize order data, ensuring unique order IDs and consistent formatting."""
    zones_mapping = load_zones_mapping(zones_file)
    orders_by_id = {}
    cleaned_orders = []

    def normalize_zone(zone_str):
        key = zone_str.strip().lower()
        return zones_mapping.get(key, zone_str.strip())

    for order in orders:
        norm_id = normalize_order_id(order['orderId'])
        norm_city = normalize_zone(order.get('city', ''))
        norm_zone = normalize_zone(order.get('zoneHint', ''))

        cleaned = {
            'orderId': norm_id,
            'city': norm_city,
            'zoneHint': norm_zone,
            'address': order.get('address', '').strip(),
            'paymentType': 'COD' if 'cod' in order['paymentType'].lower() else 'Prepaid',
            'productType': order['productType'].strip().lower(),
            'weight': float(order['weight']),
            'deadline': parse_datetime(order['deadline'])
        }

        if norm_id in orders_by_id:
            handle_duplicate(orders_by_id[norm_id], cleaned)
        else:
            orders_by_id[norm_id] = cleaned
            cleaned_orders.append(cleaned)

    return cleaned_orders
