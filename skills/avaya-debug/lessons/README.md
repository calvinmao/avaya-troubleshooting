# Lessons — Field-Captured Findings

This directory accumulates evidence-anchored findings from real SR cases. Each file mirrors a reference file in `../references/` and is auto-loaded alongside it when the corresponding domain activates.

## Files

| File | Mirrors |
|------|---------|
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

## Entry Template

```markdown
## L-<NNN> — <one-line symptom>

- **Symptom**: <what the customer or trace shows>
- **Evidence**: <exact trace string, file:line, config field, javadoc URL, or grep target>
- **Root cause**: <specific, evidence-anchored>
- **Fix / workaround**: <action — config change, PEA, vendor escalation, code fix>
- **Provenance**: SR <number> | <YYYY-MM-DD>
- **Promotion**: <pending | promoted to references/<file>.md#<anchor> on YYYY-MM-DD | rejected — <reason>>
```

- `L-NNN` is monotonic per file (`L-001`, `L-002`, …), zero-padded to 3 digits.
- One entry per finding; do not bundle unrelated findings under one ID.
- Always cite the SR number and capture date in `Provenance` — this is the audit trail.

## Promotion Rule

A lesson is eligible for promotion into its matching `references/<file>.md` when **either**:

- **(a)** it has reproduced across **≥2 SR cases** (verifiable via the `Provenance` lines), OR
- **(b)** it identifies a **code path, trace string, or config flag** that is generalizable beyond one customer environment (e.g., a CM SA flag, a JTAPI Javadoc clarification, an AES PostgreSQL config).

Lessons that fail both tests stay in this directory as case anecdotes. They are still loaded with the reference and remain available for pattern matching on future cases, but they are not promoted to canonical guidance.

## Citation Convention

When a lesson is applied during diagnosis or cited in an SR report, always reference it by its full ID, e.g.:

> Per L-007 in `lessons/aes-cti-jtapi.md` (SR 00876543, 2026-05-12), the same `connBelongToDifferentDeviceIDType` flag was observed on outbound park with SA9114 enabled.

This preserves provenance and lets future Claude instances verify the claim against the source SR.

## How Lessons Get Here

Run `/avaya-learn` at the end of a session, or accept the post-report nudge in `/avaya-report`. The command scans the conversation for evidence-anchored findings, drafts L-NNN entries, saves the approved ones here, and proposes promotion of generalizable ones to the canonical reference files.
