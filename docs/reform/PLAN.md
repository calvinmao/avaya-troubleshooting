# Reform Plan: avaya-troubleshooting → 5×5×3 Methodology

**Branch**: `reform/5x5x3-methodology`
**Version bump**: 1.0.0 → 2.0.0 (schema breaking change)
**Started**: 2026-07-08

## Motivation

The plugin already implements six correct architectural elements: progressive
loading (SKILL.md routing), lessons capture loop (`/avaya-learn`), lessons
sedimentation (17 L-NNN entries), evals quality gate, per-reference metadata,
and manual GC prose. This positions it strongly against the 5×5×3 knowledge
methodology (5 storage layers × 5 knowledge types × 3 maturity levels).

The current gaps preventing team-wide rollout are:

| Gap | Impact |
|-----|--------|
| No `maturity` field on L-NNN entries | Consumers (humans + AI) cannot filter by trust level |
| No `versions` / `applicable_versions` fields | Avaya version chaos (7.x vs R8.1.2) is not machine-checkable |
| No explicit L1 (Triage) layer | Symptom-to-domain routing is only in SKILL.md, no session template |
| No CI (zero `.github/` presence) | Metadata regressions and eval regressions ship silently |
| Metadata in HTML comments, not YAML frontmatter | Not machine-parseable for lint / tooling |
| Dangling `docs/agents/triage-labels.md` reference in CLAUDE.md | Documentation debt |

## Approach — 6 Phases (strict order, each independently reversible)

### Phase 0 — Preparation (this commit)

- Branch `reform/5x5x3-methodology` from master
- `docs/reform/PLAN.md` (this file)
- `docs/reform/schema.md` (frontmatter contracts, next commit)

### Phase 1 — Define schema

Two YAML frontmatter schemas, one for lessons L-NNN entries and one for
references files. See `schema.md`.

### Phase 2 — Migrate 32 files to YAML frontmatter

- **2.1** 17 L-NNN entries across 11 lessons files → per-file commits with
  intelligent-inference rules for `maturity` and `versions`
- **2.2** 15 references files → batch commit (uniform transform)
- **2.3** Verify all YAML valid; verify SKILL.md load paths unchanged

**Intelligent inference rules** (Phase 2.1):

| Source signal | Inferred field |
|---|---|
| `Promotion: promoted to ...` | `maturity: verified` + extract target + date |
| `Promotion: pending*` | `maturity: draft` |
| Version pattern found in Evidence/Root cause (e.g. `AEP 8.1.2.2`, `POM 4.0.x`) | Extracted into `versions:` list |
| No version pattern found | `versions: [TBD]` |

### Phase 3 — Sync command templates + add `/avaya-gc`

- Update `commands/avaya-learn.md` Step-3 L-NNN template to new schema
- Update `skills/avaya-debug/lessons/README.md` template + maturity ladder doc
- Author `commands/avaya-gc.md` implementing the 7-step quarterly cleanup
  (from CLAUDE.md "Knowledge Base Maintenance" section), plus one new
  step: scan `versions: [TBD]` entries and prompt to backfill

### Phase 4 — L1 Triage layer scaffolding

- Create `skills/avaya-debug/triage/{README,symptom-catalog,session-template}.md`
- Resolve dangling `docs/agents/triage-labels.md` reference in CLAUDE.md

### Phase 5 — CI + evals harness

- `scripts/lint_metadata.py` — YAML validity, field enum checks, L-NNN
  monotonicity, promotion consistency
- `scripts/run_evals.py` — mode A (offline keyword coverage), mode B
  (online LLM scoring, opt-in)
- `.github/workflows/knowledge-lint.yml` — lint + mode A on push/PR
- `.pre-commit-config.yaml` — local pre-commit hook

### Phase 6 — Documentation + version bump

- CLAUDE.md: add 5×5×3 methodology section; update KB maintenance to
  reference `/avaya-gc`; document YAML frontmatter and maturity/layer/type
- AGENTS.md: mirror CLAUDE.md changes
- README.md: `/avaya-gc`, `scripts/`, CI badges
- `.claude-plugin/plugin.json`: version 1.0.0 → 2.0.0

## Risk Register

| Risk | Mitigation |
|------|-----------|
| YAML frontmatter breaks Claude Code loading | Branch isolation; test one reference manually before batch; `## L-NNN` headings preserved (anchor references intact) |
| Wrong `maturity` inference | Only infer where evidence is unambiguous (`promoted to` string); default to `draft` on pending; `versions: [TBD]` where unclear |
| CI too strict → red build | Mode A only structural checks, not content quality; Mode B is opt-in / manual |
| L-NNN body accidentally modified during migration | Diff review before each commit; migration only *prepends* frontmatter, does not touch body |
| Post-commit hook writes to `C:/claude-obsidian/...` (Windows-native path, warns under WSL) | Non-blocking warning; can be tightened later |

## Handoff

After Phase 6:

1. Push branch, open PR
2. Reviewer verifies each commit is independently sensible
3. `/plugin install` from the branch, exercise `/avaya-sr` and `/avaya-learn`
   to confirm progressive loading still works with YAML frontmatter
4. Merge to master, tag v2.0.0
