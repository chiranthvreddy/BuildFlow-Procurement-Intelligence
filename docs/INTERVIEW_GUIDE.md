# Product interview guide — BuildFlow

## 45-second pitch
BuildFlow is an independent B2B construction procurement prototype. I explored a procurement coordinator's workflow from order creation to delivery exception management. The app supports purchase-order tracking, supplier comparison and explainable price alerts, and the product case study includes a PRD, metrics, RICE prioritization and test plans. It uses synthetic data; I have not claimed measured customer impact.

## Product questions and defensible answers

**Why this problem?** Construction purchasing can span several materials, suppliers and sites. A single view of open orders and overdue commitments is a plausible first problem to validate with users.

**Why build visibility first?** It can be implemented without requiring live ERP integration or speculative AI. It gives users a way to identify exceptions before building more sophisticated automation.

**How did you prioritize?** I documented a RICE comparison with illustrative assumptions. The scores are a decision-making exercise, not validated reach estimates.

**What is the North Star?** Eventually critical-material on-time fulfilment. The prototype currently measures completed on-time delivery, open overdue orders and historical late deliveries separately.

**Why compare median prices?** Historical median prices are a simple reference. They are not contractual quotes; real purchasing needs material grade, location, delivery terms and order size.

**What is the AI feature?** There is no trained AI model. Price flags are explainable threshold-based statistical rules; a future ML model would need validated data.

**How would you validate it?** Observe real procurement users performing exception triage, record task completion and errors, interview users about existing workflows, and refine the product.

**What would you build next?** Persistent storage, permissions, audit trails, supplier/ERP integration, partial delivery support and criticality-aware prioritization.

## Claims to avoid
Do not claim live supplier integrations, real customer interviews, A/B test results, production deployment, cost savings or machine-learning predictions.
