# Metric definitions and experiment design

## Candidate north-star outcome
**Critical-material on-time fulfillment rate**, defined as critical orders delivered by promised date divided by all critical orders delivered. The current dataset has no validated criticality flag, so the prototype reports overall completed-delivery on-time rate instead.

## Operational metrics
- **Total orders:** count of filtered purchase orders.
- **Procurement value:** sum(quantity × unit price), ₹.
- **Open orders:** status other than Delivered.
- **Overdue open orders:** open orders with promised date before the analysis date.
- **Late completed orders:** delivered after promised date.
- **Exception count:** overdue open plus late completed. This mixes active exceptions and historical failures; in production the two should have separate tiles.
- **On-time delivery rate:** delivered on or before promised date / delivered orders, excluding open orders.
- **Average completed lead time:** mean days between created and delivered dates for delivered orders.
- **Supplier reliability:** on-time delivered / all delivered for that supplier, N/A if none.

## Data requirements
Stable order IDs, normalized statuses, created/promised/actual delivery timestamps, supplier identifiers, units, prices and site mapping. For meaningful procurement risk scoring, add material criticality, expected consumption date, partial deliveries and lead time variability.

## Instrumentation proposal (future)
Events: dashboard_opened, filter_applied, late_order_opened, supplier_compared, export_clicked. Do not interpret sample-data values as usage telemetry.

## Experiment: exception-first dashboard
**Hypothesis:** Showing exceptions before the full table lowers the time to identify urgent follow-ups.
**Design:** Compare baseline order-list view with exception-first variant among representative users; counterbalance task order.
**Primary metric:** Median time to correctly identify critical overdue orders.
**Guardrails:** False-positive decisions, task errors, satisfaction and accessibility issues.
**Decision rule:** Define improvement threshold and sample size before testing; no results are claimed.
