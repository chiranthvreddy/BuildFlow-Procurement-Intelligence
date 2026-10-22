from __future__ import annotations
import pandas as pd

REQUIRED = {"order_id","supplier","material","quantity","unit_price","promised_date","delivered_date","status","created_date"}
STATUSES = {"Placed","Confirmed","In Transit","Delivered"}

def validate_orders(df):
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    if df.order_id.isna().any() or df.order_id.duplicated().any():
        raise ValueError("Order IDs must be present and unique")
    if not df.status.isin(STATUSES).all():
        raise ValueError("Unknown order status")
    for field in ("quantity","unit_price"):
        if pd.to_numeric(df[field], errors="coerce").isna().any():
            raise ValueError(f"{field} must be numeric")
    if (pd.to_numeric(df.quantity) <= 0).any() or (pd.to_numeric(df.unit_price) < 0).any():
        raise ValueError("Quantity must be positive; price cannot be negative")

def enrich_orders(df, as_of=None):
    validate_orders(df)
    out = df.copy()
    out["quantity"] = pd.to_numeric(out.quantity)
    out["unit_price"] = pd.to_numeric(out.unit_price)
    for field in ("created_date","promised_date","delivered_date"):
        out[field] = pd.to_datetime(out[field], errors="coerce")
    if out[["created_date","promised_date"]].isna().any().any():
        raise ValueError("Created/promised dates must be valid")
    if (out.promised_date < out.created_date).any():
        raise ValueError("Promised date cannot precede order creation")
    completed = out.status.eq("Delivered")
    if (completed & out.delivered_date.isna()).any() or ((~completed) & out.delivered_date.notna()).any():
        raise ValueError("Delivery dates must match Delivered status")
    if (completed & (out.delivered_date < out.created_date)).any():
        raise ValueError("Delivered date cannot precede creation")
    today = pd.Timestamp(as_of).normalize() if as_of is not None else pd.Timestamp.today().normalize()
    out["order_value"] = out.quantity * out.unit_price
    out["overdue_open"] = ~completed & out.promised_date.lt(today)
    out["late_delivered"] = completed & out.delivered_date.gt(out.promised_date)
    out["is_late"] = out.overdue_open | out.late_delivered
    out["on_time_delivery"] = completed & out.delivered_date.le(out.promised_date)
    out["lead_time_days"] = (out.delivered_date - out.created_date).dt.days
    out["days_overdue"] = (today - out.promised_date).dt.days.clip(lower=0).where(~completed,0)
    return out

def metrics(df):
    delivered = df[df.status.eq("Delivered")]
    return {
        "total_orders":len(df),
        "procurement_value":float(df.order_value.sum()),
        "open_orders":int(df.status.ne("Delivered").sum()),
        "overdue_open":int(df.overdue_open.sum()),
        "late_delivered":int(df.late_delivered.sum()),
        "at_risk_orders":int(df.is_late.sum()),
        "on_time_rate":float(delivered.on_time_delivery.mean()) if len(delivered) else None,
        "average_lead_days":float(delivered.lead_time_days.mean()) if len(delivered) else None
    }

def supplier_scorecard(df):
    base = df.groupby("supplier",as_index=False).agg(orders=("order_id","count"),spend=("order_value","sum"))
    delivered = df[df.status.eq("Delivered")]
    perf = delivered.groupby("supplier",as_index=False).agg(completed=("order_id","count"),on_time_rate=("on_time_delivery","mean"),average_lead_days=("lead_time_days","mean"))
    return base.merge(perf,on="supplier",how="left").sort_values("spend",ascending=False)

def price_anomalies(df, threshold=0.20):
    out = df.copy()
    reference = out.groupby("material")["unit_price"].transform("median")
    out["reference_price"] = reference
    out["price_deviation_pct"] = (out.unit_price / reference - 1).where(reference.gt(0))
    out["price_anomaly"] = out.price_deviation_pct.abs().gt(threshold).fillna(False)
    return out

def quote_comparison(df, material, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    subset = df[df.material.eq(material)]
    if subset.empty:
        return pd.DataFrame(columns=["supplier","indicative_unit_price","estimated_total","completed_on_time_rate","observations"])
    quotes = subset.groupby("supplier",as_index=False).agg(indicative_unit_price=("unit_price","median"),observations=("order_id","count"))
    perf = supplier_scorecard(subset)[["supplier","on_time_rate"]].rename(columns={"on_time_rate":"completed_on_time_rate"})
    quotes = quotes.merge(perf,on="supplier",how="left")
    quotes["estimated_total"] = quotes.indicative_unit_price * quantity
    return quotes.sort_values("estimated_total")
