---
layer: L1
purpose: "Structured SR working-notes template — copy per SR"
last_reviewed: "2026-07-08"
related_docs:
  - "../commands/avaya-sr.md"
  - "../commands/avaya-learn.md"
  - "symptom-catalog.md"
---

# SR Session Template

Copy this template at the start of every SR session. Maintain it inline as
the investigation progresses. At SR closure, feed it to `/avaya-learn` for
L3 promotion of evidence-anchored findings.

---

## SR: `<SR-number>`

- **Customer**: <name>
- **Opened**: <YYYY-MM-DD> HH:MM <timezone>
- **Reporter**: <internal engineer handle>
- **Product mix**: <e.g. AACC + POM + AEP>
- **Version pins**: <e.g. AACC 7.1.2, POM 4.0.2, AEP 8.1.2.2>
- **Severity**: <P1 / P2 / P3 / P4>

## Symptom (customer's words)

> <verbatim from customer; do not paraphrase yet>

## Symptom (structured)

- **Class**: signaling / media / control-plane / config / infra / evidence
- **Reproducibility**: always / intermittent-N% / one-off / cannot-reproduce
- **Scope**: single-user / single-site / all-sites / specific-carrier
- **First occurrence**: <date/time>
- **Trigger correlation**: <what changed recently — upgrade, config, network, load, none-known>

## Triage decision

- **Primary domain(s) loaded**: <ref file names from SKILL.md or symptom-catalog>
- **Rationale**: <why these domains, per symptom-catalog first-diagnostic-move column>
- **L-NNN prior art consulted**: <list any L-NNN entries from lessons/ that appear relevant>

## Evidence collected

Log all evidence with **timestamps** and **exact source** (host, filename, line
range where possible). This is the raw material `/avaya-learn` will extract
into L-NNN Evidence fields.

- <YYYY-MM-DD HH:MM:SS.SSS>  `<source>`  `<one-line finding>`
- <YYYY-MM-DD HH:MM:SS.SSS>  `<source>`  `<one-line finding>`

## Hypothesis chain

Number each hypothesis. When one is invalidated, keep the entry — the
rejected chain is itself learning material (`diagnostic-principles` L-002
"Discard prior hypotheses fully when contradicted"). Format:

**H1** (<date>): <hypothesis statement>
- Evidence supporting: <items from Evidence section>
- Predictions: <what would be true if H1 holds>
- Test performed: <test>
- **Result**: <SUPPORTS | INVALIDATES | INCONCLUSIVE>
- If INVALIDATES: <link to next hypothesis>; **do not partially preserve H1** below.

**H2** (<date>): <hypothesis statement after H1 invalidated>
- ...

**H3** (<date>): ...

## Vendor engagement (if applicable)

| Timestamp | Vendor | Contact / ticket | Ask | Response |
|-----------|--------|------------------|-----|----------|
| | | | | |

## Open items

| Status | Item | Owner | Due |
|--------|------|-------|-----|
| Investigating / Awaiting / Resolved | | | |

## Resolution

- **Confirmed root cause**: <one-line, evidence-anchored>
- **Root cause layer**: signaling / media / control-plane / config / infra / upstream-of-avaya
- **Fix applied**: <what was done, by whom, when>
- **SR closed**: <YYYY-MM-DD>

## KB hygiene actions at closure

Before running `/avaya-learn`, check:

- [ ] Any prior L-NNN in `lessons/` that this SR **invalidates** or **partially
  contradicts**? If yes: those L-NNN need demotion (maturity: draft) or
  rewrite (see the SR 1-23647477802 pattern in diagnostic-principles L-002).
- [ ] Any prior `references/` content this SR **contradicts**? If yes: flag
  for rewrite in the next quarterly `/avaya-gc`.
- [ ] Novel evidence-anchored findings ready for L3 capture? → run `/avaya-learn`.

## Notes for `/avaya-learn`

Any specific findings you want promoted first, or any classification
guidance (e.g. "the Evidence field for H2 rejection is the most reusable
finding — capture as type=pattern"):

- <hint 1>
- <hint 2>
