from __future__ import annotations
import pandas as pd

REQUIRED = {"order_id", "supplier", "material", "quantity", "unit_price", "promised_date", "delivered_date", "status", "created_date"}

def validate_orders(df: pd.DataFrame) -> None:
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if df.order_id.duplicated().any():
        raise ValueError("Order IDs must be unique")
    if (df.quantity <= 0).any() or (df.unit_price < 0).any():
        raise ValueError("Quantities must be positive and prices cannot be negative")

def enrich_orders(df: pd.DataFrame, as_of=None) -> pd.DataFrame:
    validate_orders(df)
    out = df.copy()
    for col in ["promised_date", "delivered_date", "created_date"]:
        out[col] = pd.to_datetime(out[col], errors="coerce")
    if out[["promised_date", "created_date"]].isna().any().any():
        raise ValueError("Promised and created dates must be valid")
    if ((out.delivered_date.notna()) & (out.status != "Delivered")).any():
        raise ValueError("Only delivered orders can have delivered dates")
    if ((out.status == "Delivered") & (out.delivered_date.isna())).any():
        raise ValueError("Delivered orders require delivered dates")
    today = pd.Timestamp(as_of).normalize() if as_of is not None else pd.Timestamp.today().normalize()
    out["order_value"] = out.quantity * out.unit_price
    out["is_late"] = ((out.status == "Delivered") & (out.delivered_date > out.promised_date)) | ((out.status != "Delivered") & (out.promised_date < today))
    out["on_time_delivery"] = (out.status == "Delivered") & (out.delivered_date <= out.promised_date)
    out["lead_time_days"] = (out.delivered_date - out.created_date).dt.days
    return out

def metrics(df: pd.DataFrame) -> dict:
    delivered = df[df.status == "Delivered"]
    return {
        "total_orders": len(df),
        "procurement_value": float(df.order_value.sum()),
        "open_orders": int((df.status != "Delivered").sum()),
        "at_risk_orders": int(df.is_late.sum()),
        "on_time_rate": float(delivered.on_time_delivery.mean()) if len(delivered) else None,
        "average_lead_days": float(delivered.lead_time_days.mean()) if len(delivered) else None,
    }

def supplier_scorecard(df: pd.DataFrame) -> pd.DataFrame:
    delivered = df[df.status == "Delivered"]
    base = df.groupby("supplier", as_index=False).agg(orders=("order_id", "count"), spend=("order_value", "sum"))
    rate = delivered.groupby("supplier", as_index=False).agg(on_time_rate=("on_time_delivery", "mean"), average_lead_days=("lead_time_days", "mean"))
    return base.merge(rate, on="supplier", how="left").sort_values("spend", ascending=False)
