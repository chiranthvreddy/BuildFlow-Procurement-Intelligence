from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import enrich_orders, metrics, supplier_scorecard

st.set_page_config(page_title="BuildFlow | Procurement Intelligence", page_icon="🏗️", layout="wide")
st.markdown("""<style>.block-container{padding-top:1.7rem}.hero{padding:1.5rem 1.8rem;background:linear-gradient(115deg,#12243c,#244a65);color:white;border-radius:16px;margin-bottom:1rem}.hero h1{color:white;margin:0;font-size:2.2rem}.hero p{color:#d5e7f4;margin:.4rem 0 0}.stMetric{background:#f3f6fa;padding:14px;border-radius:12px}</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>BuildFlow</h1><p>Construction procurement intelligence · Interactive product case study</p></div>', unsafe_allow_html=True)
st.caption("Portfolio demonstration • Synthetic, illustrative data • Not affiliated with ArisInfra")
base = Path(__file__).resolve().parents[1]
@st.cache_data
def load_data():
    return pd.read_csv(base / "data" / "sample_orders.csv")

uploaded = st.sidebar.file_uploader("Optional: upload compatible orders CSV", type="csv")
try:
    raw = pd.read_csv(uploaded) if uploaded else load_data()
    orders = enrich_orders(raw, as_of="2026-10-22" if not uploaded else None)
except (ValueError, KeyError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load orders: {exc}")
    st.stop()

st.sidebar.header("Filters")
sites = sorted(orders.site.dropna().unique()) if "site" in orders else []
selected_sites = st.sidebar.multiselect("Construction sites", sites, default=sites)
selected_materials = st.sidebar.multiselect("Materials", sorted(orders.material.unique()), default=sorted(orders.material.unique()))
selected_statuses = st.sidebar.multiselect("Order status", sorted(orders.status.unique()), default=sorted(orders.status.unique()))
if sites:
    orders = orders[orders.site.isin(selected_sites)]
orders = orders[orders.material.isin(selected_materials) & orders.status.isin(selected_statuses)]

summary = metrics(orders)
tabs = st.tabs(["Overview", "Order operations", "Supplier intelligence", "Product insights"])
with tabs[0]:
    a,b,c,d = st.columns(4)
    a.metric("Orders", f"{summary['total_orders']:,}")
    b.metric("Procurement value", f"₹{summary['procurement_value']/100000:,.1f}L")
    c.metric("Open orders", summary['open_orders'])
    d.metric("Late / at-risk", summary['at_risk_orders'])
    e,f = st.columns(2)
    e.metric("On-time delivery (completed)", f"{summary['on_time_rate']:.1%}" if summary['on_time_rate'] is not None else "N/A")
    f.metric("Avg. completed lead time", f"{summary['average_lead_days']:.1f} days" if summary['average_lead_days'] is not None else "N/A")
    left,right = st.columns(2)
    with left:
        by_material = orders.groupby("material",as_index=False).order_value.sum()
        st.plotly_chart(px.bar(by_material,x="material",y="order_value",title="Spend by material",labels={"order_value":"Spend (₹)","material":"Material"}),use_container_width=True)
    with right:
        by_status = orders.status.value_counts().rename_axis("status").reset_index(name="count")
        st.plotly_chart(px.pie(by_status,names="status",values="count",hole=.55,title="Order status mix"),use_container_width=True)
with tabs[1]:
    st.subheader("Procurement order tracker")
    show = orders.sort_values("created_date",ascending=False).copy()
    show["risk_flag"] = show.is_late.map({True:"⚠️ Late / at-risk",False:"On track"})
    st.dataframe(show[["order_id","site","supplier","material","quantity","order_value","status","promised_date","delivered_date","risk_flag"]] if "site" in show else show,hide_index=True,use_container_width=True)
    st.download_button("Export filtered orders",orders.to_csv(index=False),"buildflow_orders.csv","text/csv")
with tabs[2]:
    st.subheader("Supplier scorecard")
    score = supplier_scorecard(orders)
    st.dataframe(score.style.format({"spend":"₹{:,.0f}","on_time_rate":"{:.1%}","average_lead_days":"{:.1f}"},na_rep="N/A"),hide_index=True,use_container_width=True)
    st.caption("On-time rate is calculated only on delivered orders; missing values indicate no completed deliveries.")
with tabs[3]:
    st.subheader("Product hypotheses to validate")
    st.markdown("**Hypothesis 1 — Delivery visibility:** Surfacing late-order alerts could reduce time spent manually following up with suppliers.")
    st.markdown("**Hypothesis 2 — Supplier selection:** Showing historical delivery reliability alongside price could improve purchasing decisions.")
    st.markdown("**Hypothesis 3 — Operational triage:** An exception-first dashboard could shorten the time to identify at-risk orders.")
    st.info("These are proposed hypotheses, not experimentally validated outcomes. See docs for the PRD, metrics and test plan.")
