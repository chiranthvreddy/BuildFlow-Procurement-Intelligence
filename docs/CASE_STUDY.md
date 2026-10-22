# BuildFlow — Product Management Case Study

## Overview
BuildFlow is an independent construction procurement prototype designed to explore a B2B workflow: create a purchase order, monitor commitments, follow up on overdue orders, compare indicative supplier costs and investigate price outliers.

## Problem and discovery
The assumed user is a procurement coordinator managing several construction sites. Pain points are hypotheses derived from the workflow, **not findings from completed interviews**. A discovery guide is provided in DISCOVERY.md.

## Product strategy
An exception-first dashboard was chosen before complex forecasting because the most immediate proposed job is finding orders that need action. Order creation, status updates, supplier comparison and transparent price flags form the prototype workflow.

## Key tradeoffs
- Transparent median-based price anomaly flags over opaque AI claims.
- Historical median unit price over simulated live supplier quotes.
- Session-state prototype over backend deployment.
- Separate overdue-open and late-delivered metrics so action queues don't include historical failures.

## Implementation
Python, pandas, Streamlit, Plotly; deterministic synthetic data generator; unit tests and GitHub Actions workflow. Interactive features include order creation, status changes, local follow-up notes, supplier comparisons and exports.

## Measurement plan
Potential outcome: time to correctly identify critical overdue orders. Supporting metrics: completed on-time rate, overdue open count, supplier delivery reliability and workflow completion. An A/B or usability study is proposed but **not conducted**.

## Evidence status
No real customer interviews, measured time savings, production deployment or experimental lift are claimed. Manual UAT and deployment verification are outstanding.

## Interview discussion
Explain why procurement visibility matters, why the MVP scope is limited, how median-based price alerts work, what data is needed for supplier scoring, and how real user feedback would change the roadmap.
