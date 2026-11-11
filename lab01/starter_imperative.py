from typing import Any

TAX_RATE = 0.2

BASE_RATE_PER_KG = 12.0
RATE_PER_KM = 2.5
SURCHARGE_MAP = {"standard": 1.0, "express": 1.35, "same_day": 1.75}
MIN_ACCEPTABLE_WEIGHT = 0.1
MAX_ACCEPTABLE_WEIGHT = 50.0


def process_orders(
    orders: list[Any], min_total: float, discount: float
) -> dict[str, Any]:
    valid: list[dict[str, Any]] = []
    total_revenue = 0.0

    for o in orders:
        if not o["paid"]:
            continue
        print("Processing order:", o["id"])

        order_total = 0.0
        for it in o["items"]:
            order_total += it["price"] * it["qty"]
        if order_total < min_total:
            continue

        order_total = order_total * (1 - discount)
        order_total = order_total * (1 + TAX_RATE)

        o["total"] = order_total
        valid.append(o)
        total_revenue += order_total

    return {"count": len(valid), "revenue": total_revenue, "orders": valid}


def process_parcels(parcels: list[Any], min_distance: float) -> dict[str, Any]:
    valid: list[dict[str, Any]] = []
    total_cost = 0.0

    for p in parcels:
        if not p["paid"]:
            continue
        print("Processing parcel:", p["id"])

        weight = p["weight"]
        dist = p["distance"]
        if dist < min_distance:
            continue
        if weight < MIN_ACCEPTABLE_WEIGHT or weight > MAX_ACCEPTABLE_WEIGHT:
            continue

        surcharge = SURCHARGE_MAP.get(p["delivery_type"], 1.0)
        base_tariff = (weight * BASE_RATE_PER_KG) + (dist * RATE_PER_KM)
        cost = base_tariff * surcharge

        p["cost"] = round(cost, 2)
        valid.append(p)
        total_cost += cost

    return {"count": len(valid), "total_cost": round(total_cost, 2), "parcels": valid}
