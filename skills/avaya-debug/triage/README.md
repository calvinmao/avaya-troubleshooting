---
layer: L1
purpose: "Session-level triage — symptom-to-domain routing and SR session template"
last_reviewed: "2026-07-08"
---

# Triage — L1 (Session Layer)

The **L1 Triage layer** is the first-touch surface when a new SR arrives.
Its job is to route a raw customer symptom to the right L4 reference
domain(s) and to structure the working notes engineers take while the SR
is open.

## How L1 fits in the 5×5×3 architecture

| Layer | Role | Lives in |
|-------|------|----------|
| **L1 Triage** (this dir) | Session-level: symptom routing, working notes, hypothesis chain | `skills/avaya-debug/triage/` |
| L2 Process | Reusable playbooks, log-collection commands, escalation scripts | `commands/`, `skills/avaya-debug/references/log-collection.md` |
| L3 Vault | Evidence-anchored L-NNN lessons from closed SRs | `skills/avaya-debug/lessons/` |
| L4 Standard | Canonical domain references and diagnostic invariants | `skills/avaya-debug/references/` |
| L5 Strategy | Long-lived design decisions and cross-product architecture | `CLAUDE.md`, `AGENTS.md`, `docs/reform/` |

L1 is deliberately **the shortest-lived, most-mutable layer**. A triage
note has a lifetime of one SR. When the SR closes, evidence-anchored
findings graduate to L3 (via `/avaya-learn`); the triage notes themselves
are ephemeral by design.

## Files in this directory

| File | Purpose |
|------|---------|
| `README.md` | This file — L1 concept and how to use it |
| `symptom-catalog.md` | Finer-grained symptom → domain mapping than SKILL.md. Use when the SKILL.md single-line trigger keywords don't disambiguate. |
| `session-template.md` | Structured SR working-notes template. Copy per SR; feed to `/avaya-learn` at closure. |

## Relationship to SKILL.md

`SKILL.md` contains a **coarse-grained trigger table** — keyword ↔ reference
file. It runs automatically on every session for progressive loading.

`symptom-catalog.md` is a **finer-grained fallback** for ambiguous or
multi-symptom cases. Use it when:

- The customer's symptom string doesn't clearly match one SKILL.md row.
- Multiple domains are plausible and you need to disambiguate before
  loading a reference.
- You want to see historical patterns (which SRs had similar symptoms)
  before choosing an investigation direction.

## Relationship to `/avaya-sr` and `/avaya-learn`

- `/avaya-sr <SR-number> <symptom>` starts a session and typically opens a
  filled-in copy of `session-template.md` in the working notes.
- During the session, the engineer maintains that template inline.
- At closure, `/avaya-learn` reads the session (including the template) to
  extract evidence-anchored findings for L3 promotion.

## Why L1 exists as a named layer

Before this reform, session-level artifacts (working notes, hypothesis
chains, rejected assumptions) were scattered across engineer emails, chat
messages, and one-off Confluence pages. The 5×5×3 methodology names L1
explicitly so these artifacts have a **known place to live and a known
lifecycle** — even if that lifecycle is "one SR, then either graduate to
L3 or discard."

The SR 1-23647477802 case (June 2026) demonstrated the cost of not
having L1 formalized: three days were spent reconstructing the working
hypothesis chain during KB hygiene because the H1/H2/H3 progression had
lived only in email threads. With `session-template.md`, that progression
is captured natively.
