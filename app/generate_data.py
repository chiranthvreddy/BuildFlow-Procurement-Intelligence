from pathlib import Path
import random
from datetime import date, timedelta
import pandas as pd

MATERIALS = {"Cement (bags)": (310, 410), "TMT Steel (kg)": (52, 72), "Sand (tonnes)": (1100, 1900), "Aggregate (tonnes)": (900, 1500), "Bricks (units)": (7, 12)}
SUPPLIERS = ["Apex Materials", "MetroBuild Traders", "SolidStone Supply", "Prime Cement Co", "Nandi Infrastructure", "Eastline Aggregates"]
SITES = ["Whitefield Tower", "HSR Commercial", "Sarjapur Residences", "Electronic City Campus"]

def generate_orders(n=240, seed=42, as_of=date(2026, 10, 22)):
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        material = rng.choice(list(MATERIALS))
        low, high = MATERIALS[material]
        created = as_of - timedelta(days=rng.randint(0, 115))
        promised = created + timedelta(days=rng.randint(4, 18))
        days_since = (as_of - promised).days
        status = "Delivered" if days_since >= 0 and rng.random() < 0.78 else rng.choice(["Placed", "Confirmed", "In Transit"])
        delivered = promised + timedelta(days=rng.randint(-3, 8)) if status == "Delivered" else None
        if delivered and delivered > as_of:
            status, delivered = "In Transit", None
        rows.append({"order_id": f"PO-{10001+i}", "supplier": rng.choice(SUPPLIERS), "material": material, "quantity": rng.randint(20, 450), "unit_price": round(rng.uniform(low, high), 2), "promised_date": promised.isoformat(), "delivered_date": delivered.isoformat() if delivered else "", "status": status, "created_date": created.isoformat(), "site": rng.choice(SITES)})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "data" / "sample_orders.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    generate_orders().to_csv(path, index=False)
    print(path)
