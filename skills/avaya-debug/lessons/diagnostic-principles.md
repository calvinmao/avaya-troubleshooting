---
domain: diagnostic-principles
default_layer: L3
default_type: experience
last_reviewed: "2026-06-17"
---

# Lessons — Diagnostic Principles

Field-captured findings that refine or extend the core diagnostic invariants in
`../references/diagnostic-principles.md`. Entries here may update known invariant
behavior, add new cross-product integration patterns, or document new case document
extraction techniques.
Mirrors `../references/diagnostic-principles.md`. See `./README.md` for the entry
template, ID convention, and promotion rule.

---
id: L-001
layer: L3
type: pattern
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-04"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting 2nd case to avoid single-sample bias; lesson validated at SR closure on 2026-06-17 (customer diagram narrative was directionally wrong, real root cause was upstream of all customer-managed components)"
owner: "@hmao911"
---

## L-001 — Verify Customer-Provided Architecture / Fault-Analysis Diagrams Against Actual Logs

- **Symptom**: Customer provides a network diagram or fault-analysis annotation that looks authoritative; investigation built on it leads to misdirected hypothesis when the specific mechanism cited doesn't match the actual call's evidence.
- **Evidence**: For SR 1-23647477802, customer NW構成簡易版 diagram annotated "183 EarlyMediaを受信⇒MPP応答後に200 OKを受信してもre-INVITEは実行されない" (after 183 Early Media + MPP response + 200 OK, re-INVITE not executed). For BC1, SM syslog reconstruction of the actual Call-ID `d6c229d2...` showed B5000→SM segment had NO 183 Early Media — direct 100 Trying → 200 OK sequence. Both the specific trigger mechanism cited (183 Early Media) AND the general fault direction (CM missing re-INVITE) were subsequently disproven by RTP-level analysis and three-vendor escalation, which localized the real root cause to a malfunction inside the SIP-SP's internal network infrastructure — completely outside the customer-managed signaling layer.
- **Root cause**: Customer's fault-analysis diagram may be informed by THEIR understanding of the system, not by the specific failing call's evidence. Useful for hypothesis-generation, dangerous as ground truth.
- **Fix / workaround**: When customer provides architecture or fault-analysis content: (1) accept their HIGH-LEVEL fault direction as a hypothesis to test, (2) verify the SPECIFIC mechanism cited (here: 183 Early Media) against actual log/pcap evidence for the failing call before adopting it, (3) if mechanism doesn't match, document the discrepancy in customer response and proceed with own evidence-anchored mechanism explanation. Never replace own observation with customer's narrative without verification.

---
id: L-002
layer: L3
type: pattern
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-17"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting 2nd case"
owner: "@hmao911"
---

## L-002 — Discard Prior Hypotheses Fully When New Evidence Contradicts Them — Do Not Partially Preserve

- **Symptom**: A long-running investigation evolves through multiple working hypotheses. Risk: when new evidence partially contradicts an earlier hypothesis, the temptation is to "patch" the old hypothesis rather than abandon it. Result: investigation drifts, conclusions remain anchored to an incorrect framing, and the team loses time rebuilding from a wrong foundation.
- **Evidence**: SR `1-23647477802` cycled through three working hypotheses over 17 days: (H1, 2026-06-04) CM B2BUA Replaces propagation defect, inferred from CSeq:2 INVITE absence; (H2, 2026-06-09) Third-party SBC RTP relay failure, after RTP-level pcap analysis showed B5000→CM RTP = 0; (H3, 2026-06-17) Malfunction in NTT Docomo internal network infrastructure, confirmed by customer after SBC vendor + SIP-SP both cleared. Each transition required fully discarding the prior hypothesis. H1's CSeq observation was technically accurate but inferentially wrong — preserving it as "partially correct" would have anchored H2 incorrectly on CM B2BUA contribution; preserving H2 as "B5000 still partly at fault" would have prevented escalation to NTT Docomo internal.
- **Root cause of the discipline failure mode**: Sunk-cost reasoning. Engineers and customers both resist fully discarding a hypothesis that consumed analytical effort. The hypothesis acquires unwarranted credibility from the work done on it, not from evidential support.
- **Fix / workaround**: When new evidence directly contradicts a prior hypothesis, **fully discard the hypothesis** — do not preserve fragments of it. Document the transition explicitly in the investigation report (cite the contradicting evidence) so the audit trail shows why the old hypothesis was rejected. Resist phrases like "still contributes" or "may be a co-factor" unless there is independent evidence for the residual claim. Treat each new evidence-driven transition as a fresh start, not as an incremental update.
