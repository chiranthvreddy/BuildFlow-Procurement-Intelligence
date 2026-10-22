# BuildFlow — Product Requirements Document
**Version 2.0 · Independent portfolio prototype · October 2026**

## Problem hypothesis
Construction procurement coordinators working across multiple sites may struggle to monitor purchase orders, spot overdue commitments and compare suppliers when information is fragmented. This hypothesis requires actual user validation.

## Primary personas
- Procurement coordinator: needs an exception-first view and a way to follow up on orders.
- Site manager: needs material-delivery visibility.
- Category buyer: needs indicative supplier cost and reliability comparisons.

## Jobs to be done
1. When reviewing the morning backlog, identify overdue orders and their suppliers.
2. When requesting materials, estimate supplier cost and consider delivery reliability.
3. When a supplier confirms dispatch, update an order status and record a follow-up note.
4. When a price looks unusual, understand why it was flagged and whether the difference is legitimate.

## MVP functional requirements
| ID | Feature | Acceptance criteria |
|---|---|---|
| F1 | Command centre | Display spend, open, overdue, historically late and completed on-time metrics |
| F2 | Filters | Site, material and status filters update dashboard and order register |
| F3 | Order creation | Valid supplier, material, quantity, price and promised date create a unique session order |
| F4 | Status management | Status updates reject delivery dates before order creation; notes remain in session |
| F5 | Supplier comparison | Show historical median price × requested quantity and completed-delivery rate |
| F6 | Price intelligence | Flag orders whose unit price differs from material median beyond adjustable threshold |
| F7 | Export/import | Export filtered orders; validate uploaded CSV schema and dates |
| F8 | Research instrumentation | Log demo interactions locally without pretending they are real telemetry |

## Product constraints and tradeoffs
The prototype uses Streamlit session state instead of a database for speed and clarity; data will not persist across sessions. Median prices are not live supplier quotes. The anomaly rule is not a trained model. Open overdue and historically late completed orders must be reported separately.

## Out of scope
Authentication, persistent multi-user workflows, real-time supplier integration, payments, partial deliveries, ERP integration, real predictive AI, mobile-native app.

## Nonfunctional expectations
Readable data definitions, deterministic demo data, automated KPI tests, clear error messages and accessible responsive UI (manual verification pending).

## Release criteria
CI tests passing, browser UAT completed, three representative user sessions conducted, observed findings documented, and demo URL verified.
