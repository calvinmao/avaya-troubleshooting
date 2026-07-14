# Lessons — Field-Captured Findings

This directory accumulates evidence-anchored findings from real SR cases. Each file mirrors a reference file in `../references/` and is auto-loaded alongside it when the corresponding domain activates.

## Files

| File | Mirrors |
|------|---------|
| `diagnostic-principles.md` | `../references/diagnostic-principles.md` |
| `aes-cti-jtapi.md` | `../references/aes-cti-jtapi.md` |
| `contact-center.md` | `../references/contact-center.md` |
| `recording-wfo.md` | `../references/recording-wfo.md` |
| `analytics-kubernetes.md` | `../references/analytics-kubernetes.md` |
| `security-vulnerability.md` | `../references/security-vulnerability.md` |
| `sip-voice-quality.md` | `../references/sip-voice-quality.md` |
| `certificates-login-outage.md` | `../references/certificates-login-outage.md` |
| `digital-channels.md` | `../references/digital-channels.md` |
| `ip-office.md` | `../references/ip-office.md` |
| `log-collection.md` | `../references/log-collection.md` |
| `orchestration-integration.md` | `../references/orchestration-integration.md` |
| `linux-server.md` | `../references/linux-server.md` |
| `network-infrastructure.md` | `../references/network-infrastructure.md` |
| `cloud-infrastructure.md` | `../references/cloud-infrastructure.md` |

## File-Level Frontmatter

Every lessons file (including stubs with no L-NNN yet) has a top-level YAML
frontmatter block that declares domain defaults:

```yaml
---
domain: <domain-name>          # e.g. aes-cti-jtapi
default_layer: L3              # lessons default to L3 (Vault)
default_type: experience       # lessons default to type=experience
last_reviewed: null            # or "YYYY-MM-DD" of most recent entry
---
```

## Entry Template

Each `## L-NNN` heading is preceded by its own YAML frontmatter block. Body
carries only Symptom / Evidence / Root cause / Fix — provenance and promotion
live in the frontmatter for machine parsing.

```markdown
---
id: L-<NNN>                    # must match the heading below
layer: L3                      # L1 | L2 | L3 | L4 | L5
type: experience               # fact | process | decision | experience | pattern
maturity: draft                # draft | verified | canonical
versions:                      # applicable Avaya product versions; use [TBD] if unclear
  - "AEP 8.1.x"
  - "POM 4.0.x"
provenance:
  sr: "<SR-number-as-string>"  # e.g. "1-23647477802"
  date: "YYYY-MM-DD"
promotion:
  status: pending              # pending | promoted | rejected
  target: null                 # when promoted: "references/<file>.md#<anchor>"
  date: null                   # when promoted or rejected: ISO date
  note: null                   # optional free text (e.g. "awaiting 2nd case")
owner: "@<github-handle>"
---

## L-<NNN> — <one-line symptom>

- **Symptom**: <what the customer or trace shows>
- **Evidence**: <exact trace string, file:line, config field, javadoc URL, or grep target>
- **Root cause**: <specific, evidence-anchored>
- **Fix / workaround**: <action — config change, PEA, vendor escalation, code fix>
```

- `L-NNN` is monotonic per file (`L-001`, `L-002`, …), zero-padded to 3 digits.
- The frontmatter `id:` field MUST match the `## L-NNN` heading below it.
- One entry per finding; do not bundle unrelated findings under one ID.
- Always cite the SR number and capture date in `provenance` — this is the audit trail.
- Body lines `- **Provenance**:` and `- **Promotion**:` from the old flat-markdown
  format are deprecated; that information now lives in the frontmatter.

## Maturity Ladder

| Level | Meaning | Consumer trust |
|-------|---------|----------------|
| `draft` | Single-SR finding, not yet cross-validated, may be overturned by a future SR | Use as diagnostic hint only; senior review required before applying to a customer |
| `verified` | Reproduced in ≥2 SR cases OR identifies a generalizable code path / trace string / config flag; OR promoted into `references/` | Trusted for direct application; AI-assist can surface with high confidence |
| `canonical` | Not applicable to lessons — canonicity is achieved by *promotion* into `references/<domain>.md`. Promoted lessons stay here (as `verified` with `promotion.status: promoted`) for audit trail. |

**Advancement**:
- `draft` → `verified`: satisfies the promotion rule below (or explicit
  senior sign-off after peer review of the L-NNN entry).
- `verified` → back to `draft`: a subsequent SR closure invalidates the
  finding. Set `promotion.status: rejected`, rewrite the body to reflect
  corrected understanding, cite the invalidating SR. **This is the reform's
  operational answer to KB hygiene under root-cause reversal**, as
  exemplified by SR `1-23647477802` (June 2026).

## Promotion Rule

A lesson is eligible for promotion into its matching `references/<file>.md`
(making it `maturity: verified` with `promotion.status: promoted`) when **either**:

- **(a)** it has reproduced across **≥2 SR cases** (verifiable via the
  `provenance.sr` values across multiple L-NNN entries), OR
- **(b)** it identifies a **code path, trace string, or config flag** that
  is generalizable beyond one customer environment (e.g., a CM SA flag, a
  JTAPI Javadoc clarification, an AES PostgreSQL config).

Lessons that fail both tests stay in this directory as `draft` case
anecdotes. They are still loaded with the reference and remain available
for pattern matching on future cases, but they are not promoted to
canonical guidance.

## Citation Convention

When a lesson is applied during diagnosis or cited in an SR report, always
reference it by its full ID, e.g.:

> Per L-007 in `lessons/aes-cti-jtapi.md` (SR 00876543, 2026-05-12), the
> same `connBelongToDifferentDeviceIDType` flag was observed on outbound
> park with SA9114 enabled.

This preserves provenance and lets future Claude instances verify the
claim against the source SR.

## How Lessons Get Here

Run `/avaya-learn` at the end of a session, or accept the post-report nudge
in `/avaya-report`. The command scans the conversation for evidence-anchored
findings, drafts L-NNN entries with the schema above, saves the approved
ones here, and proposes promotion of generalizable ones to the canonical
reference files.

## Quarterly Cleanup

Run `/avaya-gc` quarterly (or after every 10+ new lessons) to sweep for
pending-too-long entries, stale references, duplicates, TBD versions,
and post-promotion cleanup. See `commands/avaya-gc.md`.
