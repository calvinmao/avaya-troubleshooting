# YAML Frontmatter Schemas — Reform v2.0.0

Two schemas replace the current HTML-comment metadata blocks. Both use YAML
frontmatter fenced by `---` per standard convention (Jekyll, Hugo, Obsidian,
pandoc all support this).

## 1. Lessons L-NNN schema

Applies to every `## L-NNN — …` entry in `skills/avaya-debug/lessons/*.md`.
Each L-NNN entry becomes its own frontmatter-fenced block.

**Note**: Lessons files may contain multiple L-NNN entries. Each entry gets
its own frontmatter block immediately before its `## L-NNN` heading.

```yaml
---
id: L-001                    # must match the `## L-NNN` heading below
layer: L3                    # L1 | L2 | L3 | L4 | L5 (L3 = Vault, default for lessons)
type: experience             # fact | process | decision | experience | pattern
maturity: draft              # draft | verified | canonical
versions:                    # applicable Avaya product versions; use [TBD] if unclear
  - "AEP 8.1.x"
  - "POM 4.0.x"
provenance:
  sr: "1-23647477802"        # SR number (string; may start with letter/digit)
  date: "2026-06-04"         # ISO date of capture
promotion:
  status: pending            # pending | promoted | rejected
  target: null               # when promoted: "references/<file>.md#<anchor>"; else null
  date: null                 # when promoted or rejected: ISO date; else null
owner: "@hmao911"            # GitHub handle of the person who captured this
---

## L-001 — <one-line symptom>

- **Symptom**: <what the customer or trace shows>
- **Evidence**: <exact trace string, file:line, config field, javadoc URL, or grep target>
- **Root cause**: <specific, evidence-anchored>
- **Fix / workaround**: <action — config change, PEA, vendor escalation, code fix>
```

### Field enums

| Field | Allowed values | Meaning |
|-------|---------------|---------|
| `layer` | `L1`, `L2`, `L3`, `L4`, `L5` | 5 storage layers; lessons default to L3 (Vault). L1 (Triage) is for session artifacts only. |
| `type` | `fact`, `process`, `decision`, `experience`, `pattern` | 5 knowledge types. Lessons are usually `experience`; promoted lessons often become `pattern` or `decision`. |
| `maturity` | `draft`, `verified`, `canonical` | Trust level. Consumers filter by this. |
| `promotion.status` | `pending`, `promoted`, `rejected` | Promotion audit trail. Existed pre-reform; now structured. |

### Maturity ladder (rules for advancement)

```
draft ──┬─(≥2 SR OR generalizable code path/trace/flag)──> verified
        │                                                       │
        │                                                       │
        └─(rejected by new SR closure)──> maturity: draft       │
                                          promotion.status:     │
                                          rejected              ▼
                                                          (promoted to
                                                          references/*.md;
                                                          content itself is
                                                          then canonical
                                                          when it lives in
                                                          references/)
```

- **draft**: newly captured L-NNN, ≤1 SR observation, or awaiting verification
- **verified**: reproduced in ≥2 SR cases, OR identifies a generalizable code
  path / trace string / config flag (per current `lessons/README.md` promotion
  rule)
- **canonical**: not applicable to lessons files themselves; canonicity is
  achieved by *promoting* the lesson into `references/<domain>.md`. The lesson
  entry stays in lessons/ as audit trail with `promotion.status: promoted` and
  `maturity: verified`.

### Rejection handling

When a new SR closure invalidates a previously-verified lesson (as happened
with SR 1-23647477802 for the CM B2BUA lessons), set:

```yaml
maturity: draft            # demoted from verified
promotion:
  status: rejected
  target: null             # or keep prior target for audit
  date: "2026-06-17"       # date of invalidation
```

The lesson body should be rewritten to reflect corrected understanding,
citing the SR that invalidated it. This is the reform's operational answer to
the KB hygiene problem demonstrated by SR 1-23647477802.

## 2. References schema

Applies to every `skills/avaya-debug/references/*.md` file. One YAML block at
top of file.

```yaml
---
title: "AES / CTI / JTAPI Troubleshooting Reference"
layer: L4                    # references default to L4 (Standard)
scope: "AES, JTAPI, TSAPI, CSTA, DMCC, CTI, park/unpark, TSCall lifecycle"
maturity: canonical          # references are canonical by default; verified allowed for WIP
applicable_versions:         # explicit version applicability; [TBD] if unspecified
  - "AES 10.x"
  - "AES 8.1.x"
last_reviewed: "2026-06-03"  # ISO date of last content review
owner: "avaya-debug skill"
staleness_risks:             # list of things likely to drift (version-specific, vendor-specific)
  - "AES version-specific TSCall.java line numbers"
  - "PostgreSQL version"
  - "Java heap defaults"
related_docs:                # sibling references and companion lessons file
  - "diagnostic-principles.md"
  - "lessons/aes-cti-jtapi.md"
---

# AES / CTI / JTAPI Troubleshooting Reference

<content unchanged>
```

### Field enums

| Field | Allowed values | Notes |
|-------|---------------|-------|
| `layer` | `L4` (default), rarely `L5` for strategy docs | References are Standard layer |
| `maturity` | `canonical` (default), `verified` for WIP | Downgrade to `draft` if being actively rewritten |

## 3. Migration rules (Phase 2)

### Lessons file structure

**Before** (current — single file may contain multiple L-NNN entries, each
with `**Field**: value` markdown lines):

```markdown
# SIP / Voice Quality Lessons

Free-text intro.

## L-001 — Symptom short line

- **Symptom**: ...
- **Evidence**: ...
- **Root cause**: ...
- **Fix / workaround**: ...
- **Provenance**: SR 1-23156789012 | 2025-01-22
- **Promotion**: pending

## L-002 — Another symptom
...
```

**After** (each L-NNN gets its own frontmatter block):

```markdown
# SIP / Voice Quality Lessons

Free-text intro.

---
id: L-001
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23156789012"
  date: "2025-01-22"
promotion:
  status: pending
  target: null
  date: null
owner: "@hmao911"
---

## L-001 — Symptom short line

- **Symptom**: ...
- **Evidence**: ...
- **Root cause**: ...
- **Fix / workaround**: ...

---
id: L-002
...
---

## L-002 — Another symptom
...
```

Original `- **Provenance**:` and `- **Promotion**:` bullet lines are
**removed from body** (moved into frontmatter). Body keeps only Symptom,
Evidence, Root cause, Fix/workaround.

### Stub lessons files

Six files are stubs (7 lines: header + README link, no L-NNN entries):
`aes-cti-jtapi.md`, `analytics-kubernetes.md`,
`certificates-login-outage.md`, `ip-office.md`, `security-vulnerability.md`.

For these, add a single file-level frontmatter block establishing the domain
default, no per-entry blocks needed:

```yaml
---
domain: aes-cti-jtapi
default_layer: L3
default_type: experience
last_reviewed: null   # no entries yet
---

# AES / CTI / JTAPI Lessons

Field-captured findings for AES, JTAPI, TSAPI, CSTA, DMCC. Auto-loaded
alongside references/aes-cti-jtapi.md.

(No L-NNN entries yet — use /avaya-learn after an SR to capture the first one.)
```

### Reference migration (Phase 2.2)

Straight replacement of the HTML comment block with an equivalent YAML
frontmatter block. Content unchanged. New fields added:

- `title:` (extract from first `# H1` line)
- `layer: L4` (all references default)
- `maturity: canonical` (all references default; downgrade later if needed)
- `applicable_versions: [TBD]` (explicit; backfill in Phase 6 or later)

Existing fields preserved verbatim: `scope`, `last_reviewed`, `owner`,
`staleness_risks`, `related_docs`.

## 4. Lint rules (enforced in Phase 5 by `scripts/lint_metadata.py`)

1. Every lessons file has valid YAML frontmatter blocks; every `## L-NNN`
   heading has a preceding frontmatter block whose `id` matches.
2. L-NNN IDs are monotonic per file (`L-001`, `L-002`, …).
3. `layer`, `type`, `maturity`, `promotion.status` values are within the
   allowed enum.
4. `promotion.status: promoted` requires non-null `target` and `date`.
5. `promotion.status: rejected` requires non-null `date`.
6. Every references file has valid YAML frontmatter with all required fields:
   `title`, `layer`, `scope`, `maturity`, `applicable_versions`,
   `last_reviewed`, `owner`, `staleness_risks`, `related_docs`.
7. `related_docs` entries exist as files (dangling reference check).

## 5. Migration checklist

- [x] Phase 0: PLAN.md + schema.md (this commit)
- [ ] Phase 1: schema definition (this file is the schema definition)
- [ ] Phase 2.1: 11 lessons files migrated (per-file commits)
- [ ] Phase 2.2: 15 references files migrated (batch commit)
- [ ] Phase 2.3: YAML validity + SKILL.md path check
- [ ] Phase 3: command templates synced + `/avaya-gc` added
- [ ] Phase 4: `triage/` scaffolding + dangling ref fixed
- [ ] Phase 5: `scripts/`, `.github/workflows/`, `.pre-commit-config.yaml`
- [ ] Phase 6: CLAUDE.md/AGENTS.md/README.md rewrite + plugin.json 2.0.0
