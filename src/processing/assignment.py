"""Data Processing Module
This module handles the cleaning and normalization of order data, ensuring unique order IDs,
consistent formatting, and handling of duplicates. It also includes functions to normalize
zones and prepare orders for assignment to couriers."""


def plan_assignments(orders, couriers):
    """Plan assignments of orders to couriers based on zones, payment types, and product types."""
    orders_sorted = sorted(orders, key=lambda o: (o['deadline'], o['orderId']))
    courier_loads = {c['courierId']: 0.0 for c in couriers}
    assignments = []
    unassigned = []

    for order in orders_sorted:
        eligible = []
        for courier in couriers:
            cid = courier['courierId']
            covered = (order['city'] in courier['zonesCovered'] or
                       order['zoneHint'] in courier['zonesCovered'])
            if not covered:
                continue
            if order['paymentType'] == 'COD' and not courier['acceptsCOD']:
                continue
            if order['productType'] in courier['exclusions']:
                continue
            if courier_loads[cid] + order['weight'] > courier['dailyCapacity']:
                continue
            eligible.append(courier)

        if not eligible:
            unassigned.append({
                'orderId': order['orderId'],
                'reason': 'no_supported_courier_or_capacity'
            })
            continue

        best_courier = min(
            eligible,
            key=lambda c: (
                c['priority'],
                courier_loads[c['courierId']],
                c['courierId']
            )
        )
        cid = best_courier['courierId']
        assignments.append({
            'orderId': order['orderId'],
            'courierId': cid
        })
        courier_loads[cid] += order['weight']

    capacity_usage = [
        {'courierId': cid, 'totalWeight': load}
        for cid, load in courier_loads.items()
    ]

    return {
        'assignments': sorted(assignments, key=lambda x: x['orderId']),
        'unassigned': sorted(unassigned, key=lambda x: x['orderId']),
        'capacityUsage': sorted(capacity_usage, key=lambda x: x['courierId'])
    }
