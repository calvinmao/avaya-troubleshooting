---
description: Quarterly knowledge-base cleanup for avaya-debug — scans lessons and references for pending promotions, stale docs, duplicates, TBD versions, and post-promotion cleanup opportunities. Presents findings as a review queue for the KB owner.
argument-hint: "[optional: --dry-run | --domain=<name>]"
---

Run the quarterly (or post-10-new-lessons) cleanup for the avaya-debug knowledge base. Execute the seven steps below in order. This command is **read-and-propose only** — it does NOT modify files without explicit user approval per proposal.

If `$ARGUMENTS` contains `--dry-run`, only report findings without asking for approvals.
If `$ARGUMENTS` contains `--domain=<name>`, restrict the sweep to that one domain (`lessons/<name>.md` and `references/<name>.md`).

## Step 1 — Scan for pending-too-long lessons (promotion candidates)

Read every `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/lessons/*.md` and parse each per-entry YAML frontmatter block. For entries where `promotion.status: pending`:

- Group by `provenance.sr` — if the same underlying finding appears in **≥2 distinct SRs**, that satisfies rule (a) of the promotion rule.
- Cross-reference the body: if it identifies a specific code path / trace string / config flag, that satisfies rule (b).
- Present the qualifying candidates as a promotion queue:

```
Promotion candidates (N lessons meet the ≥2-SR or generalizable-finding rule):
[1] lessons/aes-cti-jtapi.md L-005 — <symptom> — Rule (b): identifies TSCall.java:784 code path
[2] lessons/sip-voice-quality.md L-003 — <symptom> — Rule (a): matches L-014 in same file (2 SRs)
    Suggested: also see lessons/sip-voice-quality.md L-003 promotion.note "strong candidate ..."
```

For each, offer: `promote / defer / reject-with-reason`. On approval, update the frontmatter fields per the /avaya-learn Step 5 procedure and edit the target `references/<domain>.md`.

## Step 2 — Scan for stale references (last_reviewed > 6 months)

Read every `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/references/*.md` frontmatter. Compute the difference between today and each `last_reviewed:` value. Flag any reference where `today - last_reviewed > 180 days`.

Present as a review queue:

```
Stale references (N files reviewed >6 months ago):
[1] references/analytics-kubernetes.md — last_reviewed 2026-06-03 (over threshold by X days)
    staleness_risks: K8s API deprecations, MicroStrategy version...
[2] ...
```

For each, offer: `mark reviewed today (bump last_reviewed)` / `defer` / `queue for content review`. Marking reviewed only bumps the date if the user confirms no content changes are needed.

## Step 3 — Scan for duplicate or near-duplicate invariants across references

Grep across all `references/*.md` for near-identical invariant sentences. Use a light similarity heuristic (shared 5+ word n-grams). Present suspected duplicates:

```
Potential duplicates:
[1] references/aes-cti-jtapi.md line 120: "Always cast event to LucentV5CallInfo and call getUCID()"
    references/diagnostic-principles.md line 30: "Always extract via cast event to LucentV5CallInfo → call getUCID()"
    Suggested action: keep diagnostic-principles.md (canonical single source), remove from aes-cti-jtapi.md, add "See diagnostic-principles.md invariant #3" pointer.
```

For each, offer: `merge into <canonical>` / `keep both with cross-reference` / `not a duplicate`. On approval, apply the merge.

## Step 4 — Clean up already-promoted lessons

For every lesson with `promotion.status: promoted`, verify:

- The `promotion.target` file exists and contains the promoted content (grep for a signature line from the lesson body inside the target reference).
- If confirmed present in `references/`, the lesson entry has served its capture purpose. Present option:

```
Post-promotion cleanup candidates:
[1] lessons/log-collection.md L-001 — promoted to references/log-collection.md#mpp-sipccxml-log-invariants-for-pom-predictive-investigations on 2026-06-04
    Verified present in target. Action: keep body-collapsed audit stub (retain L-NNN heading + frontmatter for provenance; replace body with pointer to promoted section).
```

Offer per lesson: `collapse to audit stub` / `keep full` / `remove entirely (rare — loses provenance)`. Default is `collapse` for lessons where the promoted reference is stable.

**Never remove the frontmatter or heading** — the L-NNN ID is a durable citation anchor.

## Step 5 — Update evals with any new SKILL.md triggers

Diff `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/SKILL.md` trigger-keyword table against the terms exercised by `${CLAUDE_PLUGIN_ROOT}/evals/activation.md` cases. Report keywords added since last GC that are not exercised by any A-NNN case:

```
Untested SKILL.md triggers (N new since last GC):
[1] SKILL.md contact-center row added "Edify" trigger — no A-NNN case tests it
    Suggested: add A-072 "Edify service divergence on LDAP sync" → contact-center.md + linux-server.md
```

For each, offer: `draft new eval case` / `defer` / `not needed`. On approval, propose the case for `evals/activation.md`.

## Step 6 — Refresh staleness_risks per reference

For each reference, re-examine the `staleness_risks:` list against the body content. Flag risks that are:
- **Stale (already realized)**: e.g. "AES version-specific X" but body has been updated to cover multiple versions → risk can be removed.
- **Missing (newly emerged)**: e.g. body mentions a vendor-specific behavior with no matching risk entry → suggest addition.

Present as a change queue per reference.

## Step 7 — Sweep TBD versions on L-NNN entries

For every `lessons/*.md` per-entry frontmatter where `versions: [TBD]`:

- Re-read the entry body for version cues (product names + numbers).
- If a cue is present, propose a concrete backfill (e.g. `versions: ["AEP 8.1.x"]`).
- If truly version-agnostic, offer to change to `versions: [any]` (a distinct sentinel from `[TBD]` meaning "explicitly version-agnostic, not merely unknown").

```
TBD-version backfill candidates:
[1] lessons/sip-voice-quality.md L-001 (OPTIONS keep-alive):
    Evidence cites "Session Manager per RFC 3261" and "CM SIP Trunks" without version.
    Suggestion: versions: [any]  (SIP RFC-level behavior, not Avaya-version-specific)
[2] lessons/log-collection.md L-001 (MPP log rotation):
    Evidence cites "MPP PVCLIPOMPP2A21H" (host, not version).
    Suggestion: versions: ["AEP 8.x", "POM 4.x"]  (POM Predictive campaign context implies this range)
```

For each, offer: `apply suggestion` / `set to different value` / `defer (keep TBD)`.

## Output

At the end, print a summary:

```
Quarterly GC complete for avaya-debug knowledge base:
- Promoted: N lessons
- Marked reviewed: N references
- Merged duplicates: N invariants
- Collapsed to audit stub: N lessons
- New evals drafted: N cases
- Staleness_risks updated: N references
- TBD versions backfilled: N entries

Next quarterly GC recommended: <today + 90 days>
```

Do NOT commit changes automatically — the caller runs `git add / git commit` after reviewing the diff.

## Safety invariants

- This command is **read-and-propose**. Every modification requires explicit user approval per finding.
- L-NNN IDs and frontmatter `id:` fields are **immutable** once assigned — the audit trail depends on stable citation targets.
- When collapsing a promoted lesson to an audit stub, keep the frontmatter and `## L-NNN` heading intact; only the body is replaced with a pointer.
- Never remove a `rejected` lesson — rejection itself is a durable learning that prevents recurrence.
