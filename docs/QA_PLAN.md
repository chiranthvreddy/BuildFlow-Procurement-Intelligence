# Quality assurance and user acceptance testing

## Automated coverage
Run `pytest -q`. Tests check aggregate order values, overdue flags, on-time rates, supplier handling without delivered orders, duplicate IDs and incomplete delivered records.

## Manual UAT checklist — pending browser verification
- [ ] Launch the app using `streamlit run app/main.py`.
- [ ] Confirm overview shows six metrics and two charts.
- [ ] Select one site; verify table and totals update.
- [ ] Deselect all materials; verify zero-count state displays without exception.
- [ ] Use all three filters in combination.
- [ ] Verify late or overdue rows are flagged correctly.
- [ ] Export filtered orders and inspect CSV row count.
- [ ] Check a supplier with no delivered orders shows N/A.
- [ ] Upload an invalid CSV and verify friendly error.
- [ ] Test mobile browser layout and keyboard navigation.

## Known limitations
This is a static demo with synthetic orders and a fixed demonstration as-of date. The dashboard does not create or update orders, use real ERP feeds, maintain audit trails, or send supplier notifications. Automated test success does not imply usability or production readiness.

## Defect template
Title; environment; reproduction steps; expected outcome; actual outcome; severity; screenshot; owner; fix verification.
