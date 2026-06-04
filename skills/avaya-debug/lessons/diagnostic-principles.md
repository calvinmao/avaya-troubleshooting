# Lessons — Diagnostic Principles

Field-captured findings that refine or extend the core diagnostic invariants in
`../references/diagnostic-principles.md`. Entries here may update known invariant
behavior, add new cross-product integration patterns, or document new case document
extraction techniques.
Mirrors `../references/diagnostic-principles.md`. See `./README.md` for the entry
template, ID convention, and promotion rule.

---

## L-001 — Verify Customer-Provided Architecture / Fault-Analysis Diagrams Against Actual Logs

- **Symptom**: Customer provides a network diagram or fault-analysis annotation that looks authoritative; investigation built on it leads to misdirected hypothesis when the specific mechanism cited doesn't match the actual call's evidence.
- **Evidence**: For SR 1-23647477802, customer NW構成簡易版 diagram annotated "183 EarlyMediaを受信⇒MPP応答後に200 OKを受信してもre-INVITEは実行されない" (after 183 Early Media + MPP response + 200 OK, re-INVITE not executed). For BC1, SM syslog reconstruction of the actual Call-ID `d6c229d2...` showed B5000→SM segment had NO 183 Early Media — direct 100 Trying → 200 OK sequence. The diagram's general fault direction (CM missing re-INVITE) was correct, but the specific trigger mechanism (183 Early Media) did not apply to the captured failing calls.
- **Root cause**: Customer's fault-analysis diagram may be informed by THEIR understanding of the system, not by the specific failing call's evidence. Useful for hypothesis-generation, dangerous as ground truth.
- **Fix / workaround**: When customer provides architecture or fault-analysis content: (1) accept their HIGH-LEVEL fault direction as a hypothesis to test, (2) verify the SPECIFIC mechanism cited (here: 183 Early Media) against actual log/pcap evidence for the failing call before adopting it, (3) if mechanism doesn't match, document the discrepancy in customer response and proceed with own evidence-anchored mechanism explanation. Never replace own observation with customer's narrative without verification.
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: pending — awaiting 2nd case to avoid single-sample bias
