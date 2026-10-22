# BuildFlow — Product Requirements Document (PRD)
**Version:** 1.0 | **Stage:** Independent portfolio prototype | **Primary user:** Construction procurement coordinator

## Problem statement
Procurement teams often track purchase orders, suppliers and delivery commitments across fragmented tools. Finding overdue orders and comparing supplier delivery reliability may require manual reconciliation. This is a product hypothesis, not a validated customer finding.

## Opportunity and user jobs
- As a procurement coordinator, I want to filter orders by site, material and status so I can quickly identify commitments requiring follow-up.
- As a site manager, I want to see delivery exceptions before they disrupt material planning.
- As a category buyer, I want to compare supplier performance and spend so I can assess options beyond quoted unit price.

## Goals
1. Enable users to identify overdue open orders within two minutes in a moderated usability test.
2. Display procurement spend, open orders, exception count and completed-delivery on-time rate.
3. Export a filtered follow-up list.
4. Support supplier-level comparison of historical delivery performance.

## MVP scope
**Included:** Read-only dashboard; site/material/status filtering; supplier scorecard; overdue/late flags; CSV export; input validation; synthetic demonstration data.
**Excluded:** Authentication, purchase-order creation, transactions, supplier messaging, live delivery tracking, predictive AI, ERP integrations.

## Functional requirements
| ID | Requirement | Acceptance criteria |
|---|---|---|
| F1 | Read orders CSV | Valid CSV loads; missing mandatory fields show useful validation error |
| F2 | Filter order list | Changing site/material/status updates both rows and aggregate KPIs |
| F3 | Show operational KPIs | Order count, spend, open orders, exception count, on-time rate and lead time are recalculated |
| F4 | Flag exceptions | Open order past promised date is overdue; completed order after promised date is late |
| F5 | Compare suppliers | Spend and completed-delivery on-time rates appear by supplier; suppliers with no completed orders display N/A |
| F6 | Export | Download contains currently filtered orders |

## Nonfunctional expectations
- Input data must be clearly labeled as synthetic.
- Invalid and duplicate order IDs must be rejected.
- Dates must be parsed and checked for consistency.
- Metrics must avoid dividing by zero and differentiate completed orders from open orders.
- Responsiveness and accessibility require browser-level testing before any production claims.

## Edge cases
No rows after filtering; no deliveries for a supplier; malformed dates; duplicated IDs; zero/negative quantity; missing delivery timestamp on a delivered order.

## Risks and open questions
Are promised dates trustworthy? Do partial deliveries exist? What constitutes a critical order? Is the cost of a late shipment dependent on site schedule? These need stakeholder discovery before deployment.

## Release gate
Automated tests pass, manual UAT checklist executed, usability feedback collected, and data definitions reviewed with domain stakeholders.
