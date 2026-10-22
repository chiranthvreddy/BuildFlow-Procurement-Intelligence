# BuildFlow — Construction Procurement Intelligence

**Independent Product Management case study and working Streamlit prototype** for B2B construction-material procurement. This project is not affiliated with ArisInfra or any real construction supplier.

## Problem
Construction procurement teams need to compare suppliers, monitor orders, identify delayed deliveries, and make better purchasing decisions. Fragmented spreadsheets and status updates make this difficult.

## Product concept
BuildFlow combines an interactive procurement dashboard, supplier/order insights, and configurable at-risk delivery flags. All example data are **synthetic**; metrics are demonstrations, not real business outcomes.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app/main.py
```

## Repository guide
- `app/main.py` — interactive Streamlit dashboard
- `app/core.py` — reusable KPI and risk calculations
- `app/generate_data.py` — reproducible synthetic-data generator
- `data/sample_orders.csv` — example procurement orders
- `tests/test_core.py` — automated tests
- `docs/PRD.md` — product requirements and acceptance criteria
- `docs/DISCOVERY.md` — user and problem discovery assumptions
- `docs/METRICS.md` — product metrics specification
- `docs/ROADMAP.md` — MVP roadmap and prioritization
- `docs/QA_PLAN.md` — QA/UAT checklist
- `docs/CASE_STUDY.md` — portfolio case study

## Scope and limitations
A demonstration prototype, not a production application. There is no authentication, supplier integration, live logistics tracking, or validated customer research. Any usability testing and estimated impact must be performed before claiming measurable outcomes. Do not present synthetic results as observed customer results.

## Portfolio positioning
Product thinking (PRD, user stories, metric definition, prioritization), analytics (Python, pandas, Streamlit), and engineering collaboration (tests, acceptance criteria, QA).