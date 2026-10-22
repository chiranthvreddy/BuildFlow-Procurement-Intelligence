# BuildFlow — Construction Procurement Intelligence

**Product Management case study + interactive B2B procurement workspace**

An independent, fictional prototype exploring how construction procurement teams could create purchase orders, monitor deliveries, compare suppliers and investigate pricing anomalies. All names, order records and prices are synthetic.

## Why this product?
Procurement coordinators working across multiple construction sites may struggle to track supplier commitments and identify overdue materials across fragmented systems. BuildFlow explores an exception-first workflow, with a product specification, prioritization decisions and testable metrics. The problem hypotheses have **not yet been validated by interviews**.

## Features
- **Command centre:** spend, order volume, active overdue orders, historical late deliveries, on-time performance and material breakdowns
- **Order operations:** create purchase orders, update statuses, add follow-up notes, export filtered records
- **Supplier comparison:** estimated cost from historical median prices alongside completed-delivery reliability
- **Price intelligence:** adjustable, explainable material-median deviation alerts
- **Product insights:** documented hypotheses and local demo interaction events
- **300 deterministic synthetic orders** generated at app startup; optional CSV import
- **Automated Python tests** and GitHub Actions CI

> Updates are held in Streamlit session state and are **not persisted**. This is a prototype, not a production procurement system.

## Quick start
```bash
git clone https://github.com/chiranthvreddy/BuildFlow-Procurement-Intelligence.git
cd BuildFlow-Procurement-Intelligence
python -m pip install -r requirements.txt
streamlit run app/main.py
```
Open the local address Streamlit prints (typically http://localhost:8501).

## Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/ and sign in with GitHub.
2. Select this repository, branch `main`, and entrypoint `app/main.py`.
3. Deploy and add the generated public URL to the repository About section.

A public deployment URL is **not yet verified**.

## Product documents
| Artifact | Purpose |
|---|---|
| [PRD](docs/PRD.md) | User stories, MVP scope and acceptance criteria |
| [Discovery](docs/DISCOVERY.md) | Proto-personas and research interview guide |
| [Metrics](docs/METRICS.md) | KPI definitions and experiment design |
| [Roadmap](docs/ROADMAP.md) | RICE prioritization and product trade-offs |
| [QA plan](docs/QA_PLAN.md) | Manual UAT and release checks |
| [Case study](docs/CASE_STUDY.md) | Problem, decisions, implementation and limitations |
| [Architecture](docs/ARCHITECTURE.md) | System diagram and data flow |
| [Demo script](docs/DEMO_SCRIPT.md) | Two-minute guided walkthrough |
| [Interview guide](docs/INTERVIEW_GUIDE.md) | Product interview questions and defensible answers |

## Tests
```bash
python -m pytest -q
```

## Important limitations
No authenticated accounts, real suppliers, actual customer research, payment processing, real ERP integration or persistent backend. Price alerts are deterministic statistical rules, **not machine learning**. Synthetic dashboard outcomes are not evidence of real-world impact. Manual usability testing and accessibility testing remain pending.
