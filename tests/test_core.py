import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
import pandas as pd
import pytest
from core import enrich_orders, metrics, supplier_scorecard

def sample():
    return pd.DataFrame([
        {"order_id":"A","supplier":"S1","material":"Steel","quantity":2,"unit_price":10,"created_date":"2026-01-01","promised_date":"2026-01-05","delivered_date":"2026-01-04","status":"Delivered"},
        {"order_id":"B","supplier":"S2","material":"Cement","quantity":3,"unit_price":20,"created_date":"2026-01-02","promised_date":"2026-01-06","delivered_date":"","status":"In Transit"},
    ])

def test_metrics():
    df = enrich_orders(sample(),as_of="2026-01-10")
    m = metrics(df)
    assert m["procurement_value"] == 80
    assert m["at_risk_orders"] == 1
    assert m["on_time_rate"] == 1
    assert m["open_orders"] == 1

def test_supplier_scorecard():
    score = supplier_scorecard(enrich_orders(sample(),as_of="2026-01-10"))
    assert len(score) == 2
    assert pd.isna(score.loc[score.supplier == "S2", "on_time_rate"].iloc[0])

def test_duplicate_ids_rejected():
    df = sample()
    df.loc[1,"order_id"] = "A"
    with pytest.raises(ValueError):
        enrich_orders(df)

def test_delivered_requires_date():
    df = sample()
    df.loc[0,"delivered_date"] = ""
    with pytest.raises(ValueError):
        enrich_orders(df)
