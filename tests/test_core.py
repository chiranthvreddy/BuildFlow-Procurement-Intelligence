import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"app"))
import pandas as pd
import pytest
from core import enrich_orders,metrics,supplier_scorecard,price_anomalies,quote_comparison
from generate_data import generate_orders

def sample():
    return pd.DataFrame([
        {"order_id":"A","supplier":"S1","material":"Steel","quantity":2,"unit_price":10,"created_date":"2026-01-01","promised_date":"2026-01-05","delivered_date":"2026-01-04","status":"Delivered"},
        {"order_id":"B","supplier":"S2","material":"Steel","quantity":3,"unit_price":20,"created_date":"2026-01-02","promised_date":"2026-01-06","delivered_date":"","status":"In Transit"},
    ])

def test_metrics():
    m=metrics(enrich_orders(sample(),as_of="2026-01-10"))
    assert m["procurement_value"]==80
    assert m["overdue_open"]==1
    assert m["late_delivered"]==0
    assert m["on_time_rate"]==1

def test_supplier_without_deliveries():
    score=supplier_scorecard(enrich_orders(sample(),as_of="2026-01-10"))
    assert pd.isna(score.loc[score.supplier=="S2","on_time_rate"].iloc[0])

def test_duplicate_ids():
    df=sample();df.loc[1,"order_id"]="A"
    with pytest.raises(ValueError):enrich_orders(df)

def test_missing_delivery_date():
    df=sample();df.loc[0,"delivered_date"]=""
    with pytest.raises(ValueError):enrich_orders(df)

def test_impossible_delivery():
    df=sample();df.loc[0,"delivered_date"]="2025-12-30"
    with pytest.raises(ValueError):enrich_orders(df)

def test_late_completed_separate_from_open():
    df=sample();df.loc[0,"delivered_date"]="2026-01-07"
    m=metrics(enrich_orders(df,as_of="2026-01-10"))
    assert m["late_delivered"]==1 and m["overdue_open"]==1

def test_price_anomaly():
    df=enrich_orders(sample(),as_of="2026-01-10")
    out=price_anomalies(df,threshold=.2)
    assert out.price_anomaly.sum()==2

def test_quote_comparison():
    df=enrich_orders(sample(),as_of="2026-01-10")
    q=quote_comparison(df,"Steel",10)
    assert len(q)==2 and q.iloc[0].estimated_total==100

def test_empty_filters():
    df=enrich_orders(sample(),as_of="2026-01-10").iloc[0:0]
    assert metrics(df)["on_time_rate"] is None
    assert supplier_scorecard(df).empty

def test_generator_validity():
    df=generate_orders(300)
    assert len(df)==300
    enrich_orders(df,as_of="2026-10-22")
