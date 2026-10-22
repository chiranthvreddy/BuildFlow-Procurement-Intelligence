# QA and UAT plan

## Automated tests
Run `python -m pytest -q` or inspect the GitHub Actions workflow. Tests cover basic KPIs, separate active overdue and historical late metrics, supplier reliability with missing observations, duplicate IDs, invalid lifecycle dates, anomaly calculations, quote comparison, empty selections and generated dataset validity.

## Manual UAT (not yet completed)
- [ ] App loads with 300 synthetic orders.
- [ ] Command centre updates when filters change.
- [ ] Overdue queue excludes delivered orders.
- [ ] New order creation updates session data.
- [ ] Order status updates validate dates and refresh tables.
- [ ] Follow-up notes remain in the current session.
- [ ] Supplier comparison explains estimates and sample sizes.
- [ ] Price threshold changes anomaly counts.
- [ ] CSV export matches current filters.
- [ ] CSV upload rejects malformed records gracefully.
- [ ] Keyboard navigation, mobile layout and color contrast checked.

## Limitations
No persistent backend, authentication, real procurement integrations, real user research or production rollout. Browser-level testing and usability research must be completed before claiming a validated release.
