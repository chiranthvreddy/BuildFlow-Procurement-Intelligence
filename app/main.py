from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0,str(Path(__file__).resolve().parent))
from core import enrich_orders,metrics,supplier_scorecard,price_anomalies,quote_comparison
from generate_data import generate_orders,MATERIALS,SUPPLIERS,SITES

st.set_page_config(page_title="BuildFlow | Procurement Workspace",page_icon="🏗️",layout="wide")
st.markdown("""<style>.block-container{padding-top:1.5rem;max-width:1450px}.hero{background:linear-gradient(120deg,#11233d,#1b6472);border-radius:18px;padding:25px 30px;color:white;margin-bottom:14px}.hero h1{color:white;margin:0;font-size:2.35rem}.hero p{color:#dceef4;margin:8px 0 0}.stMetric{background:#f1f5f9;padding:14px;border-radius:12px}</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>BuildFlow</h1><p>Procurement command centre · Purchase orders, supplier intelligence and delivery exceptions</p></div>',unsafe_allow_html=True)
st.caption("Independent portfolio prototype · All supplier names, orders and prices are synthetic · Personal passion project · Fictional suppliers and sample orders")
AS_OF = pd.Timestamp("2026-10-22")
if "orders" not in st.session_state:
    st.session_state.orders = generate_orders(300,seed=42)
if "notes" not in st.session_state:
    st.session_state.notes = {}
if "events" not in st.session_state:
    st.session_state.events = []

def log_event(event):
    st.session_state.events.append({"event":event,"timestamp":pd.Timestamp.now().isoformat()})

with st.sidebar:
    st.header("Workspace")
    st.info("Demo snapshot: 22 Oct 2026")
    uploaded = st.file_uploader("Import compatible purchase orders CSV",type="csv")
    if uploaded is not None:
        if st.button("Replace demo data with uploaded CSV"):
            try:
                incoming = pd.read_csv(uploaded)
                enrich_orders(incoming,as_of=AS_OF)
                st.session_state.orders = incoming
                log_event("csv_imported")
                st.success("Imported")
            except (ValueError,KeyError,pd.errors.ParserError) as exc:
                st.error(str(exc))
    if st.button("Reset to 300 synthetic orders"):
        st.session_state.orders = generate_orders(300,seed=42)
        st.session_state.notes = {}
        log_event("demo_reset")
        st.rerun()

try:
    full = enrich_orders(st.session_state.orders,as_of=AS_OF)
except (ValueError,KeyError,TypeError) as exc:
    st.error(f"Invalid data: {exc}")
    st.stop()
with st.sidebar:
    sites = sorted(full.site.dropna().unique()) if "site" in full else []
    site_choice = st.multiselect("Site",sites,default=sites)
    material_choice = st.multiselect("Material",sorted(full.material.unique()),default=sorted(full.material.unique()))
    status_choice = st.multiselect("Status",sorted(full.status.unique()),default=sorted(full.status.unique()))
filtered = full.copy()
if sites:
    filtered = filtered[filtered.site.isin(site_choice)]
filtered = filtered[filtered.material.isin(material_choice)&filtered.status.isin(status_choice)]
m = metrics(filtered)
tabs = st.tabs(["Command centre","Purchase orders","Supplier comparison","Price intelligence","Product insights"])
with tabs[0]:
    a,b,c,d,e = st.columns(5)
    a.metric("Orders",m["total_orders"])
    b.metric("Procurement value",f"₹{m['procurement_value']/100000:,.1f}L")
    c.metric("Open orders",m["open_orders"])
    d.metric("Overdue open",m["overdue_open"])
    e.metric("Historically late",m["late_delivered"])
    a,b = st.columns(2)
    a.metric("Completed on-time rate",f"{m['on_time_rate']:.1%}" if m["on_time_rate"] is not None else "N/A")
    b.metric("Avg completed lead time",f"{m['average_lead_days']:.1f} days" if m["average_lead_days"] is not None else "N/A")
    left,right = st.columns(2)
    with left:
        spend = filtered.groupby("material",as_index=False).order_value.sum()
        st.plotly_chart(px.bar(spend,x="material",y="order_value",title="Procurement spend by material",labels={"order_value":"Spend (₹)"}),use_container_width=True)
    with right:
        status_counts = filtered.status.value_counts().rename_axis("status").reset_index(name="orders")
        st.plotly_chart(px.pie(status_counts,names="status",values="orders",hole=.55,title="Order lifecycle distribution"),use_container_width=True)
    st.subheader("Exception queue")
    exceptions = filtered[filtered.overdue_open].sort_values("days_overdue",ascending=False)
    st.dataframe(exceptions[["order_id","supplier","material","site","promised_date","days_overdue","status"]] if "site" in exceptions else exceptions,hide_index=True,use_container_width=True)
    st.caption("Exception queue contains only outstanding overdue orders. Completed late orders are reported separately.")
with tabs[1]:
    st.subheader("Create a purchase order")
    with st.form("new_po",clear_on_submit=True):
        x,y,z = st.columns(3)
        supplier = x.selectbox("Supplier",SUPPLIERS)
        material = y.selectbox("Material",sorted(MATERIALS))
        site = z.selectbox("Site",SITES)
        x,y,z = st.columns(3)
        quantity = x.number_input("Quantity",min_value=1,value=100,step=1)
        unit_price = y.number_input("Unit price (₹)",min_value=0.01,value=100.0,step=1.0)
        promised = z.date_input("Promised delivery",value=(AS_OF+pd.Timedelta(days=7)).date(),min_value=AS_OF.date())
        submitted = st.form_submit_button("Create purchase order",type="primary")
    if submitted:
        ids = pd.to_numeric(st.session_state.orders.order_id.astype(str).str.extract(r"PO-(\d+)")[0],errors="coerce").dropna()
        next_id = int(ids.max())+1 if len(ids) else 10001
        row = {"order_id":f"PO-{next_id}","supplier":supplier,"material":material,"site":site,"quantity":quantity,"unit_price":unit_price,"created_date":AS_OF.date().isoformat(),"promised_date":promised.isoformat(),"delivered_date":"","status":"Placed"}
        st.session_state.orders = pd.concat([st.session_state.orders,pd.DataFrame([row])],ignore_index=True)
        log_event("order_created")
        st.success(f"Created {row['order_id']} in this demo session")
    st.subheader("Manage an order")
    open_ids = full.loc[full.status.ne("Delivered"),"order_id"].tolist()
    if open_ids:
        selected = st.selectbox("Select open order",open_ids)
        current = full.loc[full.order_id.eq(selected)].iloc[0]
        st.caption(f"Current status: {current.status} · Supplier: {current.supplier} · Material: {current.material}")
        next_status = st.selectbox("Update status",["Placed","Confirmed","In Transit","Delivered"],index=["Placed","Confirmed","In Transit","Delivered"].index(current.status))
        delivery_date = st.date_input("Actual delivery date (only if Delivered)",value=AS_OF.date())
        note = st.text_area("Follow-up / resolution note",value=st.session_state.notes.get(selected,""),max_chars=500)
        if st.button("Save order update"):
            if next_status=="Delivered" and pd.Timestamp(delivery_date)<current.created_date:
                st.error("Delivery date cannot precede creation")
            else:
                mask=st.session_state.orders.order_id.eq(selected)
                st.session_state.orders.loc[mask,"status"]=next_status
                st.session_state.orders.loc[mask,"delivered_date"]=delivery_date.isoformat() if next_status=="Delivered" else ""
                st.session_state.notes[selected]=note
                log_event("order_updated")
                st.success("Saved in this browser session")
                st.rerun()
    st.subheader("Order register")
    display = filtered.copy()
    display["exception"] = display.overdue_open.map({True:"Overdue — follow up",False:""}) 
    st.dataframe(display.sort_values("created_date",ascending=False),hide_index=True,use_container_width=True)
    st.download_button("Download filtered orders",filtered.to_csv(index=False),"buildflow_orders.csv","text/csv",on_click=lambda:log_event("orders_exported"))
with tabs[2]:
    st.subheader("Indicative supplier quote comparison")
    st.caption("Estimates use median historical synthetic unit prices, not live supplier quotations or contractual offers.")
    x,y = st.columns(2)
    chosen_material = x.selectbox("Compare suppliers for",sorted(full.material.unique()))
    requested_qty = y.number_input("Required quantity",min_value=1,value=100,step=1)
    quotes = quote_comparison(full,chosen_material,requested_qty)
    st.dataframe(quotes.style.format({"indicative_unit_price":"₹{:,.2f}","estimated_total":"₹{:,.0f}","completed_on_time_rate":"{:.1%}"},na_rep="N/A"),hide_index=True,use_container_width=True)
    st.subheader("Historical supplier performance")
    score = supplier_scorecard(filtered)
    st.dataframe(score.style.format({"spend":"₹{:,.0f}","on_time_rate":"{:.1%}","average_lead_days":"{:.1f}"},na_rep="N/A"),hide_index=True,use_container_width=True)
    st.caption("On-time rate is measured only across completed orders; small samples can be misleading.")
with tabs[3]:
    st.subheader("Explainable price anomaly detection")
    threshold = st.slider("Flag deviation from material median (%)",10,60,20,5)
    enriched = price_anomalies(filtered,threshold/100)
    anomalies = enriched[enriched.price_anomaly].sort_values("price_deviation_pct",key=abs,ascending=False)
    st.metric("Flagged order prices",len(anomalies))
    st.dataframe(anomalies[["order_id","material","supplier","unit_price","reference_price","price_deviation_pct"]].style.format({"unit_price":"₹{:,.2f}","reference_price":"₹{:,.2f}","price_deviation_pct":"{:+.1%}"}),hide_index=True,use_container_width=True)
    st.info("This is a transparent median-based rule, not a trained AI model. Different grades, regions, order sizes and delivery terms can legitimately explain price differences.")
with tabs[4]:
    st.subheader("Product hypotheses and instrumentation")
    st.markdown("**Hypothesis A:** An exception-first queue reduces time to find overdue orders.\n\n**Hypothesis B:** Supplier reliability next to estimated cost improves purchasing trade-off decisions.\n\n**Hypothesis C:** Price flags help buyers investigate unusual quotes.")
    st.write("Demo interactions this session:",len(st.session_state.events))
    st.dataframe(pd.DataFrame(st.session_state.events),hide_index=True,use_container_width=True)
    st.caption("Session events are local demo interactions, not customer usage analytics. See docs for PRD, experiment design and UAT.")
