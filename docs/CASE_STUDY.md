# BuildFlow — Product Management Portfolio Case Study

## Thirty-second pitch
BuildFlow is an independent B2B construction procurement prototype exploring how procurement teams could monitor supplier commitments and identify exceptions faster. I defined a hypothesized user problem, prioritized an MVP, documented functional requirements and metrics, and built a dashboard with testable logic using synthetic order records.

## Context
Construction procurement workflows can involve several sites, suppliers and materials. A coordinator may need to identify late deliveries and compare supplier performance before follow-up. These are plausible workflow challenges, not established findings from interviews.

## Product decision
Prioritize a read-only visibility layer before procurement transactions or generative AI features. The rationale: teams need consistent data and clear exception definitions before relying on advanced automation.

## Shipped demonstration features
- Interactive overview of volume, spend, delivery exceptions and average completed lead time.
- Filtering by site, material and order status.
- Inspectable order table with exception status and CSV export.
- Supplier scorecard with spend, completed on-time rate and lead time.
- Automated validation of order schema, dates and duplicates.

## PM deliverables
PRD with user stories and acceptance criteria; discovery plan; RICE scoring; roadmap; metric definitions; proposed experiment; UAT checklist.

## Technical implementation
Python, pandas, Streamlit and Plotly. Deterministic synthetic-data generator; isolated calculation functions; pytest unit tests.

## Evaluation and limitations
Automated tests validate calculation logic. No actual customers, interviews, A/B test, production rollout, cost savings or measured improvements are claimed. Manual interface UAT remains to be completed.

## Suggested interview narrative
1. Describe the user and the hypothesized problem.
2. Explain why exception visibility won over AI forecasting in the MVP.
3. Walk through a filter → exception → supplier comparison → export user journey.
4. Explain denominators and edge cases behind supplier reliability.
5. Discuss what discovery evidence and telemetry would be required before launch.
6. Describe future opportunities and tradeoffs without overclaiming outcomes.
