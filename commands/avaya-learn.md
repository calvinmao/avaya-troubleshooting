---
description: Capture lessons from the current SR session into the avaya-debug knowledge base. Scans session findings, drafts L-NNN lesson entries, saves them to skills/avaya-debug/lessons/<domain>.md, and proposes promotion of generalizable ones into the canonical reference files.
argument-hint: "[optional: domain hint, e.g. AES, recording, security]"
---

Run the lesson-capture workflow for the avaya-debug knowledge base. Execute the five steps below in order. Do **not** invent findings — only capture what is evidence-anchored in the current session.

## Step 1 — Scan the session

Re-read the conversation for evidence-anchored findings. Eligible candidates include:

- Trace strings the user reacted to (e.g. `setting flag 'connBelongToDifferentDeviceIDType'`)
- Code paths grep'd or decompiled (e.g. `TSCall.java:784`)
- Config flags inspected (e.g. `SA9114`, `display system-features`)
- Javadoc / Release Note references that resolved an ambiguity
- Vendor responses (BBE / Verint / Nuance / Customer) that closed an open item
- deviceIDType / event-field discoveries
- Surprising empirical observations ("returns all-zeros on EC_PARK")
- CFR / decompile / log-collection technique recoveries

**Skip**: routine confirmations, customer chitchat, generic Avaya facts already documented in the reference files, one-off environmental quirks ("customer rebooted").

## Step 2 — Classify each candidate by domain

Use the same trigger-keyword table from `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/SKILL.md`. If `$ARGUMENTS` provides a domain hint, prefer that domain when classification is ambiguous. A single candidate may belong to two domains — in that case, save it twice with cross-reference notes.

## Step 3 — Draft lesson entries

For each accepted domain, Read the corresponding `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/lessons/<domain>.md` to find the next available `L-NNN` ID (monotonic per file, zero-padded to 3 digits).

Draft each entry using this exact template:

```markdown
## L-<NNN> — <one-line symptom>

- **Symptom**: <what the customer or trace shows>
- **Evidence**: <exact trace string, file:line, config field, javadoc URL, or grep target>
- **Root cause**: <specific, evidence-anchored>
- **Fix / workaround**: <action — config change, PEA, vendor escalation, code fix>
- **Provenance**: SR <number> | <YYYY-MM-DD>
- **Promotion**: pending
```

Present all drafts in a single numbered list to the user, including any candidates you rejected and why:

```
Found N candidate lessons:
[1] aes-cti-jtapi → L-007 — <symptom>
[2] log-collection → L-012 — <symptom>
[3] (rejected) — <symptom> — <reason: too case-specific / already in reference / not evidence-anchored>
```

## Step 4 — Save the approved lessons

Ask the user which to save (multi-select, e.g. "save 1 and 2, skip 3"). For each approved entry:

1. **Idempotency check**: search the target `lessons/<domain>.md` for an existing entry whose Symptom or Evidence line matches. If found, surface "L-NNN already covers this — update instead of duplicate?" and either merge or skip.
2. Append the new entry to `lessons/<domain>.md` using the Edit tool.
3. Confirm by listing the saved entries with their `L-NNN` IDs.

## Step 5 — Propose promotion to the canonical reference

For each saved lesson, evaluate against the promotion rule in `lessons/README.md`:

> Eligible when (a) reproduced across ≥2 cases, OR (b) identifies a code path, trace string, or config flag that is generalizable beyond one customer environment.

For each eligible lesson:

1. Read the matching `references/<domain>.md` and locate the right section header (or propose a new one).
2. Draft a concrete edit — usually a new bullet under that header — written in the same dense invariant style as `SKILL.md` items 14–16.
3. Show the diff (old context + new bullet) and ask: **"Promote L-NNN to references/<domain>.md now?"**
4. On approval: apply the edit AND update the lesson's `Promotion:` line from `pending` to `promoted to references/<domain>.md#<anchor> on <YYYY-MM-DD>`.
5. On rejection: change `Promotion:` to `rejected — <one-line reason>`.

If no candidates are found in Step 1, print: `No new lessons identified in this session.` and stop. Do not fabricate entries to fill the report.
