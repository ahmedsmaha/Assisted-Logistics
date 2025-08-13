""""Reconciliation Module
This module compares planned assignments with actual deliveries,
detects discrepancies, and categorizes results into missing, unexpected, duplicate,
late, misassigned, and overloaded couriers."""
from collections import defaultdict


def build_lookups(clean_orders, plan, couriers):
    """Build lookup dictionaries for orders, assignments, and courier capacities."""
    orders_dict = {o['orderId']: o for o in clean_orders}
    planned_assignments = {a['orderId']: a['courierId']
                           for a in plan['assignments']}
    courier_capacities = {c['courierId']: c['dailyCapacity'] for c in couriers}
    return orders_dict, planned_assignments, courier_capacities


def process_log_entries(log_entries):
    """Group log entries by order ID."""
    log_by_order = defaultdict(list)
    for entry in log_entries:
        log_by_order[entry['orderId']].append(entry)
    return log_by_order


def update_results(order_id, entries, context):
    """
    Update result categories and courier weights for a given order.

    Args:
        order_id (str): The order ID.
        entries (list): Log entries for the order.
        context (dict): Contains orders_dict, planned_assignments, result,
                        courier_weights, processed_orders.
    """
    if len(entries) > 1:
        context['result']['duplicate'].append(order_id)

    first_entry = entries[0]
    courier_id = first_entry['courierId']
    delivered_at = first_entry['deliveredAt']

    context['processed_orders'].add(order_id)

    if order_id not in context['orders_dict']:
        context['result']['unexpected'].append(order_id)
        return

    order = context['orders_dict'][order_id]
    if delivered_at > order['deadline']:
        context['result']['late'].append(order_id)

    planned_courier = context['planned_assignments'].get(order_id)
    if planned_courier and planned_courier != courier_id:
        context['result']['misassigned'].append(order_id)

    context['courier_weights'][courier_id] += order['weight']


def check_overloaded_couriers(courier_weights, courier_capacities, result):
    """Check for overloaded couriers."""
    for courier_id, total_weight in courier_weights.items():
        capacity = courier_capacities.get(courier_id, float('inf'))
        if total_weight > capacity:
            result['overloadedCouriers'].append(courier_id)


def process_entry(entry, context):
    """Process a single log entry for reconciliation."""
    order_id = entry['orderId']
    courier_id = entry['courierId']
    context['order_scans'][order_id].append(entry)

    if order_id in context['processed_orders']:
        return

    context['processed_orders'].add(order_id)

    if order_id not in context['orders_dict']:
        return

    order = context['orders_dict'][order_id]
    context['courier_weights'][courier_id] += order['weight']

    if entry['deliveredAt'] > order['deadline']:
        context['result']['late'].append(order_id)

    planned_courier = context['planned_assignments'].get(order_id)
    if planned_courier and planned_courier.upper() != courier_id:
        context['result']['misassigned'].append(order_id)


def finalize_results(context):
    """Finalize duplicate, unexpected, missing, and overloaded courier results."""
    for order_id, scans in context['order_scans'].items():
        if len(scans) > 1:
            context['result']['duplicate'].append(order_id)
        if order_id not in context['orders_dict']:
            context['result']['unexpected'].append(order_id)

    all_planned_orders = set(context['planned_assignments'].keys())
    context['result']['missing'] = sorted(
        all_planned_orders - set(context['order_scans'].keys()))

    for courier_id, total_weight in context['courier_weights'].items():
        capacity = context['courier_capacities'].get(courier_id, float('inf'))
        if total_weight > capacity:
            context['result']['overloadedCouriers'].append(courier_id)

    for key in context['result']:
        context['result'][key] = sorted(context['result'][key])


def reconcile(clean_orders, plan, log_entries, couriers):
    """Compare planned assignments with actual deliveries."""
    orders_dict = {o['orderId']: o for o in clean_orders}
    planned_assignments = {a['orderId']: a['courierId']
                           for a in plan['assignments']}
    courier_capacities = {c['courierId']: c['dailyCapacity'] for c in couriers}

    result = {
        'missing': [],
        'unexpected': [],
        'duplicate': [],
        'late': [],
        'misassigned': [],
        'overloadedCouriers': []
    }

    context = {
        'orders_dict': orders_dict,
        'planned_assignments': planned_assignments,
        'courier_capacities': courier_capacities,
        'result': result,
        'processed_orders': set(),
        'courier_weights': defaultdict(float),
        'order_scans': defaultdict(list)
    }

    for entry in log_entries:
        process_entry(entry, context)

    finalize_results(context)

    return context['result']
