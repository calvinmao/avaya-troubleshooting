# avaya-troubleshooting — User Guide

> Version 2.0.0 · English · 中文版:[USER_GUIDE.zh-CN.md](USER_GUIDE.zh-CN.md)

This guide walks you through installing and using the `avaya-troubleshooting`
Claude Code plugin day-to-day. It assumes you are an Avaya UC/CC support
engineer working real Service Requests (SRs) with Claude Code as your
diagnostic assistant.

If you want to know **why** the plugin is built the way it is (the 5×5×3
knowledge methodology), read this guide's *Core Concepts* section, and
optionally `docs/reform/PLAN.md` for the reform history.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Core Concepts](#3-core-concepts)
4. [Daily Workflow — Handling an SR](#4-daily-workflow--handling-an-sr)
5. [Daily Workflow — Closing an SR](#5-daily-workflow--closing-an-sr)
6. [Auxiliary Commands](#6-auxiliary-commands)
7. [Quarterly Maintenance](#7-quarterly-maintenance)
8. [Adding New Content](#8-adding-new-content)
9. [Contributing / Development](#9-contributing--development)
10. [Troubleshooting FAQ](#10-troubleshooting-faq)
11. [Appendix](#11-appendix)

---

## 1. Introduction

### What this plugin does

`avaya-troubleshooting` is a Claude Code plugin that turns Claude Code
into a senior Avaya UC/CC troubleshooting specialist. When you paste an
SR symptom, a trace excerpt, or a getlogs output into Claude, the plugin:

1. **Auto-activates** based on Avaya product/keyword triggers.
2. **Progressively loads** only the reference file(s) matching the
   symptom domain (never all 7,851 lines).
3. **Auto-loads matching L-NNN lessons** captured from previous SRs so
   you inherit the team's historical knowledge on the same class of
   problem.
4. **Applies 16 core diagnostic invariants** (UCID extraction,
   `deviceIDType`, `SA9114/SA9124`, certificate-change three-action
   sequence, etc.) to every diagnosis regardless of domain.

### Who this guide is for

- **First-time users**: read sections 1–5 in order.
- **Occasional users / refresher**: skim section 3, then use sections
  4–7 as reference.
- **KB maintainers / contributors**: sections 7–9 cover quarterly GC,
  content authoring, and the CI harness.

### The 5×5×3 architecture at a glance

The knowledge base is organized on three orthogonal axes:

```
5 storage layers × 5 knowledge types × 3 maturity levels
    L1 Triage           fact              draft
    L2 Process          process           verified
    L3 Vault            decision          canonical
    L4 Standard         experience
    L5 Strategy         pattern
```

Every knowledge file declares where it sits on these axes via YAML
frontmatter, so both humans and CI can reason about it. See section 3
for the full model.

---

## 2. Getting Started

### 2.1 Prerequisites

- **Claude Code** installed (`claude` command available on your PATH).
- **Anthropic account** with API access (Claude Code handles this).
- **Git** for cloning and updates.
- **Python 3.9+** (only if you want to run the lint / evals locally —
  optional).
- **A local plugins marketplace** entry pointing at the plugin
  directory (see 2.2).

### 2.2 Installation

**Option A — clone from the calvinmao org** (recommended for most users):

```bash
# Choose a location for local Claude Code plugins
mkdir -p ~/.claude/plugins/local
cd ~/.claude/plugins/local
git clone https://github.com/calvinmao/avaya-troubleshooting.git
cd avaya-troubleshooting
```

**Option B — internal fork / mirror** (recommended for teams):

```bash
git clone <your-internal-git-url> avaya-troubleshooting
cd avaya-troubleshooting
```

Register the plugin in your `~/.claude/settings.json` under a local
marketplace (only needed once, follow whatever pattern your team uses).
Then in Claude Code:

```
/plugin install avaya-troubleshooting@local-plugins
```

Restart Claude Code so it picks up the plugin.

### 2.3 First-time verification

Verify the plugin is active by asking Claude a domain question and
watching which files it loads:

```
JTAPI is returning null on getCalledAddress() for park events.
Which invariant applies?
```

Expected behavior:

- Claude reads `skills/avaya-debug/references/diagnostic-principles.md`
  (always-loaded baseline).
- Claude reads `skills/avaya-debug/references/aes-cti-jtapi.md` (matched
  by AES/JTAPI keywords).
- Claude reads `skills/avaya-debug/lessons/aes-cti-jtapi.md` (auto-load
  companion lessons).
- Claude answers citing invariant #11 (JTAPI `null` returns are
  spec-compliant) and points to the Javadoc reference.

If Claude does not activate the skill, jump to
[section 10.1](#101-skill-does-not-activate).

### 2.4 Optional: install git hooks and dev tooling

If you plan to contribute changes to the KB (author or edit
lessons/references), install the pre-commit and post-commit hooks:

```bash
# From the plugin directory
./scripts/install-git-hooks.sh          # post-commit hook (Obsidian sync marker)
pip install pre-commit PyYAML
pre-commit install                       # runs lint + evals on every commit
```

---

## 3. Core Concepts

You can use the plugin without reading this section, but understanding
these five concepts unlocks the maintenance workflows in sections 5–7.

### 3.1 Progressive loading

`skills/avaya-debug/SKILL.md` contains a **routing table**, not the
knowledge itself. When you mention "AACC", Claude loads only
`references/contact-center.md` + `lessons/contact-center.md`, not the
15 other domain files. This keeps context usage low and prevents
cross-domain contamination.

Always-loaded baseline: `references/diagnostic-principles.md` and
`lessons/diagnostic-principles.md` (16 core invariants that apply to
every domain).

### 3.2 The five storage layers (L1–L5)

| Layer | Purpose | Lifetime | Lives in |
|-------|---------|----------|----------|
| **L1 Triage** | Session-level: symptom routing, working notes, hypothesis chain | 1 SR | `skills/avaya-debug/triage/` |
| **L2 Process** | Reusable playbooks, log-collection commands, slash commands | Months | `commands/`, `skills/avaya-debug/references/log-collection.md` |
| **L3 Vault** | Evidence-anchored L-NNN lessons from closed SRs | Years, mutable | `skills/avaya-debug/lessons/` |
| **L4 Standard** | Canonical domain references and diagnostic invariants | Years, curated | `skills/avaya-debug/references/` |
| **L5 Strategy** | Long-lived design decisions and cross-product architecture | Semi-permanent | `CLAUDE.md`, `AGENTS.md`, `docs/reform/` |

**Rule of thumb**: knowledge flows *upward* over time. L1 triage notes
graduate to L3 lessons via `/avaya-learn`; L3 lessons graduate to L4
references via promotion.

### 3.3 The five knowledge types

Each L-NNN lesson declares its `type:` field:

| Type | Meaning | Typical use |
|------|---------|-------------|
| `fact` | Objective invariant, can be verified against docs | "AEP 8.1.2.2 incompatible with POM 4.0.2.x (PSN006373u)" |
| `process` | Step-by-step "how to do X" | POM log collection commands, cert renewal procedure |
| `decision` | "Why we do it this way" — framing or judgment | How to explain APC/POM reliability asymmetry to a customer |
| `experience` | Field-captured single-SR finding | "SM SessionManager.log rotates within ~1 hour under POM load" |
| `pattern` | Reusable diagnostic rule extracted from multiple observations | "Signaling normal + media absent = SBC failure class (three causes)" |

The type is a hint about how to reuse the knowledge — `pattern` and
`decision` types are most reusable across future SRs, so they are the
strongest promotion candidates.

### 3.4 The three maturity levels (M1/M2/M3)

Every L-NNN carries a `maturity:` field with one of three values:

| Level | Meaning | You should |
|-------|---------|------------|
| **`draft`** | Single-SR finding, not cross-validated | Use as a diagnostic hint; **do not** apply blindly to a customer; get senior review |
| **`verified`** | Reproduced in ≥2 SRs OR generalizable code path/trace/flag OR promoted into references | Trust for direct application |
| **`canonical`** | Achieved by promoting the lesson body into `references/*.md`. The lesson entry stays in `lessons/` as an audit stub. | Cite freely; this is the team's official position |

**Why this matters**: when Claude finds two lessons that contradict
each other (e.g. old `draft` says "CM B2BUA defect"; new `verified`
says "SBC media plane"), the maturity label tells you which to trust.

### 3.5 Promotion and demotion

**Promotion** (`draft` → `verified` → into `references/`) is proposed by
`/avaya-learn` when a lesson meets the promotion rule:

- **(a)** it has reproduced across **≥2 SR cases**, OR
- **(b)** it identifies a **code path, trace string, or config flag**
  generalizable beyond one customer environment.

**Demotion** happens when a new SR closure invalidates a previously
`verified` lesson (as happened with SR 1-23647477802 in June 2026). The
lesson is:

- Demoted back to `maturity: draft`
- Its `promotion.status` set to `rejected` with the invalidating SR
  cited in `promotion.note`
- Its body rewritten to reflect corrected understanding

The lesson is **not deleted** — the rejection itself is durable
learning that prevents recurrence.

---

## 4. Daily Workflow — Handling an SR

### 4.1 Start a session

Open Claude Code in this plugin's directory (or any project — the
plugin is user-scoped once installed) and run:

```
/avaya-sr <SR-number> <one-line symptom>
```

Example:

```
/avaya-sr 00123456 AES returns null calledAddress on EC_PARK events for outbound calls
```

This starts a **structured session** with:

- A session header (SR number, product, symptom)
- An open-items table (Status / Item / Owner)
- Claude auto-loads the matching reference + lessons based on your
  symptom string

### 4.2 Reference triage (optional but recommended)

If Claude's automatic domain match feels off, or if the symptom is
ambiguous, consult the **L1 symptom catalog** manually:

- Read `skills/avaya-debug/triage/symptom-catalog.md` — fine-grained
  symptom → domain rows with the *first diagnostic move* for each
- Read `skills/avaya-debug/triage/README.md` if you want to understand
  the L1 layer's role

For serious/long-running SRs, copy the template from
`skills/avaya-debug/triage/session-template.md` into your working notes
and fill it in as you go. This structured note is what `/avaya-learn`
reads at closure to extract L-NNN entries.

### 4.3 Investigate

Paste evidence into the conversation as you collect it:

- traceSM / traceSBC excerpts
- `list trace vector <N>` output
- getlogs / pcap findings
- CM `display` command output
- Vendor responses

Claude's default behavior with this plugin loaded:

- **Cites specific L-NNN lessons** when they apply, e.g. *"Per L-002 in
  `lessons/sip-voice-quality.md` (SR 1-23647477802, 2026-06-04), run
  RTP packet counters first before signaling analysis."*
- **Applies diagnostic invariants**, e.g. *"Invariant #4 says check
  `SA9114`/`SA9124` before deep JTAPI analysis when null addresses
  appear."*
- **Refuses to over-conclude** — if evidence is missing for a layer,
  it flags the gap as an open item rather than guessing.

### 4.4 Maintain the hypothesis chain

For non-trivial SRs, keep a numbered hypothesis chain in your working
notes:

```
H1 (2026-07-14): CM B2BUA fails to propagate Replaces
  - Evidence: CSeq:2 INVITE absent in SBC-facing dialog
  - Test: run RTP packet counter analysis
  - Result: INVALIDATES — CM→SBC = 208 RTP, SBC→CM = 0 RTP
             media plane failure, not signaling

H2 (2026-07-14): SBC RTP relay failure
  - ...
```

**Key discipline** (per lesson L-002 in `diagnostic-principles.md`):
when H1 is invalidated, discard it fully — do not preserve fragments
of it in H2. The rejected chain is itself learning material for the
L-NNN captured at closure.

### 4.5 Generate the SR report

When you have enough evidence to draft a formal response, run:

```
/avaya-report
```

Claude generates a structured report with:

- Problem statement
- Evidence (with timestamps and sources)
- Layer-by-layer analysis (CM → AES → application, etc.)
- Root cause with evidence anchors
- Recommended resolution
- Open items
- Vendor escalation section (if needed)
- Citations to any L-NNN lessons applied

The report ends with a nudge: *"Capture lessons from this session? Run
`/avaya-learn`."*

---

## 5. Daily Workflow — Closing an SR

Closing an SR is where knowledge gets captured. **This is the most
important step for the plugin's long-term value.**

### 5.1 Run `/avaya-learn`

```
/avaya-learn                          # scan the whole session
/avaya-learn AES                      # hint: prefer AES domain when ambiguous
```

`/avaya-learn` executes five steps in order:

#### Step 1 — Scan the session

Claude re-reads the conversation for evidence-anchored findings:

- Trace strings you reacted to
- Code paths grep'd or decompiled
- Config flags inspected
- Javadoc / Release Note references that resolved an ambiguity
- Vendor responses that closed an open item
- Surprising empirical observations

It skips: routine confirmations, customer chit-chat, generic Avaya
facts already documented, one-off environmental quirks.

#### Step 2 — Classify each candidate

Each candidate is assigned to a domain using the same trigger-keyword
table as SKILL.md. If a finding spans two domains (e.g. AES + logs),
it's saved twice with cross-references.

#### Step 3 — Draft L-NNN entries

Claude drafts each entry as a **YAML frontmatter block + Markdown
body**:

```markdown
---
id: L-007
layer: L3
type: experience              # fact | process | decision | experience | pattern
maturity: draft               # ALWAYS draft on first capture
versions:
  - "AEP 8.1.x"
provenance:
  sr: "1-23647477802"
  date: "2026-07-14"
promotion:
  status: pending
  target: null
  date: null
  note: null
owner: "@your-github-handle"
---

## L-007 — <one-line symptom>

- **Symptom**: ...
- **Evidence**: ...
- **Root cause**: ...
- **Fix / workaround**: ...
```

**Field inference rules** (Claude follows these automatically):

- `type`: default `experience` for single-SR captures; upgrade to
  `pattern` if the finding is a reusable diagnostic rule.
- `versions`: extract from Evidence text (e.g. "AEP 8.1.2.2", "POM
  4.0.x"). If none found, use `[TBD]`.
- `maturity`: **always** `draft` on first capture. Promotion is a
  separate step.

Claude presents all drafts as a numbered list including rejected
candidates and why:

```
Found 3 candidate lessons:
[1] aes-cti-jtapi → L-007 — Symptom X
[2] log-collection → L-012 — Symptom Y
[3] (rejected) — Symptom Z — one-off, no reusable pattern
```

#### Step 4 — Save approved lessons

Tell Claude which to save (e.g. "save 1 and 2, skip 3"). Claude:

1. Checks for existing entries with matching Symptom/Evidence
   (idempotency).
2. Appends the new entry to `lessons/<domain>.md`.
3. Bumps the file-level `last_reviewed` date if this is the first
   entry.
4. Confirms saved entries by listing L-NNN IDs.

#### Step 5 — Propose promotion (if eligible)

For each saved lesson that meets the promotion rule (≥2 SR or
generalizable code/trace/flag), Claude:

1. Reads the matching `references/<domain>.md` and locates the right
   section.
2. Drafts a concrete edit — usually a new bullet under an existing
   header, in the same dense invariant style as `SKILL.md`.
3. Shows you the diff and asks: **"Promote L-NNN to
   references/<domain>.md now?"**
4. On approval: applies the edit to the reference AND updates the
   lesson's YAML frontmatter:
   - `maturity: draft` → `maturity: verified`
   - `promotion.status: pending` → `promoted`
   - `promotion.target` → the anchor
   - `promotion.date` → today
5. On rejection: sets `promotion.status: rejected` with a one-line
   `promotion.note` reason. `maturity` stays `draft`.

### 5.2 Commit and push

`/avaya-learn` writes files but does not commit. Review the diff and:

```bash
git add skills/avaya-debug/
git commit -m "feat(lessons): capture L-007 from SR 00123456"
git push
```

Pre-commit hook (if installed) runs the lint locally. CI re-runs on
push and blocks merges if the L-NNN schema is broken.

### 5.3 Handling demotion (root-cause reversal)

If a new SR overturns a previously `verified` lesson, do NOT just
edit the lesson body silently. Follow this procedure:

1. Open the invalidated `L-NNN` frontmatter.
2. Set `maturity: draft` (demoted).
3. Set `promotion.status: rejected`, `promotion.date: <today>`,
   `promotion.note: "invalidated by SR <new-SR-number> — <one-line reason>"`.
4. Rewrite the body to describe the corrected understanding, citing
   the invalidating SR in the Evidence field.
5. If the lesson had been promoted into `references/`, audit that
   promotion too: rewrite or remove the promoted content and note the
   change in the lesson's `promotion.note`.

This is exactly the pattern the SR 1-23647477802 KB hygiene commit
followed — see `git log --grep="B2BUA"` for the reference.

---

## 6. Auxiliary Commands

### 6.1 `/avaya-logs <product>`

Prints the exact log-collection commands for a given product, plus
what to look for in each output.

```
/avaya-logs AACC
/avaya-logs Recording
/avaya-logs AES
```

Use this before asking a customer for logs — you save time (they
send the right files first try) and demonstrate command of the
product to the customer.

### 6.2 `/avaya-report`

Covered in section 4.5. Also available anytime during a session — the
report reflects whatever evidence is in scope at the moment you run it.

### 6.3 Subagent: `avaya-debugger`

For long parallel trace analyses, Claude Code's `Agent` tool can
dispatch a specialized subagent with the same Avaya expertise:

```
Please dispatch the avaya-debugger subagent to grep this 500 MB
pcap for all SIP dialogs matching Call-ID d6c229d2*, and return
a per-dialog CSeq distribution.
```

This offloads the heavy trace parsing to a separate context so your
main conversation stays focused on synthesis.

---

## 7. Quarterly Maintenance

Run `/avaya-gc` quarterly (or after every 10+ new lessons). It is
**read-and-propose only** — every mutation requires per-finding
approval.

### 7.1 When to run

- Beginning of a quarter (calendar-driven cadence).
- After a burst of `/avaya-learn` activity (10+ new L-NNN captured).
- After a major SR closure that touched multiple domains.
- Before an internal training or KB-share session (guarantees a
  clean slate).

### 7.2 The seven steps

```
/avaya-gc                        # interactive, all domains
/avaya-gc --dry-run              # report only, no approvals asked
/avaya-gc --domain=aes-cti-jtapi # restrict to one domain
```

The seven-step interactive workflow:

| Step | What it does | Your action |
|------|--------------|-------------|
| 1 | Scan `pending` L-NNN for promotion candidates (≥2 SR reproduction, or generalizable) | Approve promotion / defer / reject-with-reason |
| 2 | Flag references with `last_reviewed` >6 months | Mark reviewed today / defer / queue for content review |
| 3 | Detect duplicate or near-duplicate invariants across references | Merge / keep both with cross-reference / not a duplicate |
| 4 | Post-promotion cleanup — collapse promoted lessons to audit stubs | Collapse (default) / keep full / remove entirely (rare) |
| 5 | Detect SKILL.md triggers with no covering A-NNN case | Draft new eval / defer / not needed |
| 6 | Refresh `staleness_risks` per reference (add newly emerged, remove realized) | Approve per reference |
| 7 | Sweep `versions: [TBD]` entries and propose backfills from Evidence text | Apply suggestion / different value / defer |

At the end you get a summary:

```
Quarterly GC complete:
- Promoted: 3 lessons
- Marked reviewed: 8 references
- Merged duplicates: 1 invariant
- Collapsed to audit stub: 2 lessons
- TBD versions backfilled: 5 entries
```

### 7.3 Safety invariants

- L-NNN IDs are **immutable** once assigned — citations depend on them.
- When collapsing a promoted lesson to an audit stub, keep the
  frontmatter and `## L-NNN` heading intact; only the body is replaced
  with a pointer to the promoted section.
- Never remove a `rejected` lesson — the rejection itself is durable
  learning.

---

## 8. Adding New Content

### 8.1 Add a new L-NNN manually (without a full SR)

If you have a finding that qualifies as a lesson but wasn't captured
during a session, add it manually:

1. Open `skills/avaya-debug/lessons/<domain>.md`.
2. Find the highest existing `L-NNN` (grep `^## L-`); use the next
   number, zero-padded to 3 digits.
3. Add the YAML frontmatter block + `## L-NNN` heading + body per the
   template in `skills/avaya-debug/lessons/README.md`.
4. Update the file-level `last_reviewed` to today.
5. Commit — pre-commit lint validates the frontmatter.

### 8.2 Add a new domain

If a new Avaya product/technology needs its own reference (rare):

1. Create `skills/avaya-debug/references/<new-domain>.md` with the
   YAML frontmatter header (see any existing reference for the
   template).
2. Create `skills/avaya-debug/lessons/<new-domain>.md` as a stub file
   with the domain-defaults frontmatter (see `lessons/aes-cti-jtapi.md`
   for a stub example).
3. Add a routing row to `skills/avaya-debug/SKILL.md` with trigger
   keywords.
4. Add a row to `skills/avaya-debug/lessons/README.md` in the Files
   table.
5. Add `### <New Domain>` sub-table with Should-Trigger A-NNN cases
   to `evals/activation.md`.
6. Run `python3 scripts/lint_metadata.py` and
   `python3 scripts/run_evals.py --mode a` to verify.

### 8.3 Add a new activation eval case

When you notice a real customer prompt that *should* have triggered the
skill but only borderline did:

1. Open `evals/activation.md`.
2. Under the correct domain's "Should-Trigger Cases" sub-table, add a
   row: `| A-NNN | "<prompt>" | <expected-ref>.md | <notes> |`.
3. Number monotonically within that domain's ID range.
4. Run `python3 scripts/run_evals.py` — if the case fails, extend
   `SKILL.md`'s trigger keywords to cover the new phrasing.

---

## 9. Contributing / Development

### 9.1 Repository layout (short version)

```
skills/avaya-debug/     # the skill; SKILL.md is the routing map
  triage/               # L1 session artifacts
  references/           # L4 canonical domain knowledge
  lessons/              # L3 field-captured L-NNN entries
commands/               # slash commands
agents/                 # subagent definitions
evals/                  # activation + output-quality test cases
scripts/                # lint_metadata.py, run_evals.py, install-git-hooks.sh
scripts/hooks/          # version-controlled git hooks
.github/workflows/      # CI: knowledge-lint.yml (auto), eval-full.yml (manual)
docs/reform/            # reform history + schema definition
docs/                   # this guide
```

### 9.2 Local pre-commit setup

```bash
pip install pre-commit PyYAML
pre-commit install
```

After this, every `git commit` runs `scripts/lint_metadata.py` and
`scripts/run_evals.py --mode a` locally. Bypass with
`git commit --no-verify` if needed (but CI will still catch you on
push).

### 9.3 Manual lint / eval runs

```bash
python3 scripts/lint_metadata.py                    # full KB lint
python3 scripts/lint_metadata.py --verbose          # show OK lines
python3 scripts/lint_metadata.py --domain=aes-cti-jtapi  # single domain

python3 scripts/run_evals.py                        # mode A (offline)
python3 scripts/run_evals.py --verbose              # verbose mode A
python3 scripts/run_evals.py --mode b               # mode B (needs API key)
```

### 9.4 CI workflows

Two workflows in `.github/workflows/`:

- **`knowledge-lint.yml`** — runs on every push and PR touching
  `skills/`, `evals/`, or `scripts/`. Two jobs:
  - Frontmatter schema lint (from `lint_metadata.py`)
  - Activation coverage check (from `run_evals.py --mode a`)
  Fails the build if either job fails, blocking merges to master.
- **`eval-full.yml`** — manual trigger only (Actions tab → Run
  workflow). Runs mode B LLM-scored evals. Consumes API tokens, so
  kept opt-in. Requires an `ANTHROPIC_API_KEY` repo secret.

### 9.5 Git hooks (post-commit)

The `scripts/hooks/post-commit` hook writes a sync marker to a
`claude-obsidian` vault if one is present locally, so that vault's
own SessionStart hook prompts a re-ingest of the plugin content on
your next Claude Code session.

The hook is cross-platform: it probes WSL, Git Bash, Windows native,
and Linux locations in that order. Silently skips if no vault is
found. Override with `AVAYA_KB_MARKER_DIR=/path/to/.vault-meta`.

Install:

```bash
./scripts/install-git-hooks.sh          # interactive
./scripts/install-git-hooks.sh --force  # overwrite without prompting
```

---

## 10. Troubleshooting FAQ

### 10.1 Skill does not activate

**Symptoms**: you mention an Avaya product, but Claude doesn't seem to
load any reference file.

**Checks**:

1. Verify plugin is installed: `/plugin` — the plugin should be listed
   as enabled.
2. Restart Claude Code (plugins are only loaded at startup).
3. Try a stronger trigger keyword: instead of "the phone system", say
   "AACC" or "AES" or "SIP one-way audio". See SKILL.md for the full
   trigger list.
4. If a specific prompt fails to activate but should, add an A-NNN
   case to `evals/activation.md` (section 8.3) and extend SKILL.md's
   trigger keywords.

### 10.2 Wrong reference loaded

**Symptoms**: skill activates but loads a reference from the wrong
domain (e.g. contact-center instead of sip-voice-quality).

**Checks**:

1. Read `skills/avaya-debug/triage/symptom-catalog.md` — the fine-grained
   symptom catalog often disambiguates cases that SKILL.md's coarse
   trigger table doesn't.
2. Add an explicit product name to your prompt.
3. If a class of prompts consistently loads the wrong reference,
   update SKILL.md's routing table to move the ambiguous trigger to
   the correct domain (or split it across two rows).

### 10.3 `scripts/lint_metadata.py` fails

**Symptoms**: `FAIL <file>.md: <error>` output; exit code 1.

**Common causes**:

| Error | Fix |
|-------|-----|
| `no file-level YAML frontmatter block found` | The file is missing the top-of-file `---...---` block; add one per `docs/reform/schema.md`. |
| `id 'L-XXX' does not match heading 'L-YYY'` | The `id:` field in frontmatter must exactly match the `## L-NNN` heading below it. |
| `id 'L-XXX' not monotonically increasing` | You added a new L-NNN with an ID lower than an existing one; use the next unused ID. |
| `promotion.status=promoted requires non-null promotion.target` | Fill in `promotion.target` with `"references/<file>.md#<anchor>"`. |
| `layer 'X' not in [L1, L2, L3, L4, L5]` | Typo or wrong layer; lessons default to L3, references default to L4. |

### 10.4 `scripts/run_evals.py --mode a` finds a coverage gap

**Symptoms**: `FAIL A-NNN: <prompt> — expected reference X (0 matching triggers among N)`.

**Fix**: extend SKILL.md's routing row for reference X to include a
keyword that appears in the prompt. Example: A-070 originally failed
because its prompt said "disk usage" but SKILL.md only listed "disk
full". The fix was to add "disk usage" and "/var/log" to
log-collection.md's trigger list.

### 10.5 Push fails with credential error (WSL)

**Symptoms**: `fatal: could not read Password for '<url>': No such device or address`
or `Password authentication is not supported for Git operations`.

**Fix (one-time setup)**: point WSL git at Windows Git Credential
Manager:

```bash
git config --global credential.helper '!"/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe"'
```

If Windows GCM has no valid OAuth token cached, do a push from
Windows Git Bash first — GCM will open a browser OAuth flow and cache
a fresh token. After that, WSL push works too.

### 10.6 Post-commit hook prints an error

**Symptoms**: after `git commit`, a warning about
`C:/claude-obsidian/.vault-meta/...: No such file or directory`.

**Fix**: your `.git/hooks/post-commit` is the old hard-coded version.
Reinstall the cross-platform hook:

```bash
./scripts/install-git-hooks.sh --force
```

---

## 11. Appendix

### 11.1 Glossary

| Term | Definition |
|------|-----------|
| **5×5×3** | The knowledge methodology: 5 storage layers × 5 knowledge types × 3 maturity levels |
| **L-NNN** | A lesson identifier, monotonically numbered per file (L-001, L-002, …). Immutable once assigned. |
| **L1–L5** | Storage layers (Triage / Process / Vault / Standard / Strategy) |
| **M1–M3** | Maturity levels — `draft`, `verified`, `canonical` |
| **Promotion** | Elevating a `draft` lesson to `verified` by incorporating it into `references/*.md` |
| **Demotion** | Reverting a `verified` lesson to `draft` because a new SR invalidated it |
| **Progressive loading** | The pattern where SKILL.md is a routing table and only matched domains' reference/lesson files are loaded |
| **SR** | Service Request — the Avaya support ticket that motivates a session |
| **SKILL.md** | The routing table + core skill instructions at `skills/avaya-debug/SKILL.md` |
| **frontmatter** | YAML block at top of a file (or before each L-NNN entry) declaring machine-parseable metadata |
| **canonical** | Content lives in `references/` — the team's official position |
| **GC** | Garbage collection — the `/avaya-gc` quarterly cleanup workflow |

### 11.2 File map (where things live)

| Concern | File(s) |
|---------|---------|
| Skill routing table | `skills/avaya-debug/SKILL.md` |
| Core invariants (always loaded) | `skills/avaya-debug/references/diagnostic-principles.md` |
| Domain references (L4) | `skills/avaya-debug/references/<domain>.md` × 15 |
| Field lessons (L3) | `skills/avaya-debug/lessons/<domain>.md` × 16 |
| L1 triage layer | `skills/avaya-debug/triage/{README,symptom-catalog,session-template}.md` |
| Slash commands (L2) | `commands/avaya-{sr,report,logs,learn,gc}.md` |
| Subagent | `agents/avaya-debugger.md` |
| Activation evals | `evals/activation.md` |
| Output-quality evals | `evals/output-quality.md` |
| Metadata lint | `scripts/lint_metadata.py` |
| Eval harness | `scripts/run_evals.py` |
| Git hooks (version-controlled) | `scripts/hooks/` + `scripts/install-git-hooks.sh` |
| CI workflows | `.github/workflows/knowledge-lint.yml`, `eval-full.yml` |
| Pre-commit config | `.pre-commit-config.yaml` |
| Reform history | `docs/reform/PLAN.md` |
| Frontmatter schema | `docs/reform/schema.md` |
| Plugin identity | `.claude-plugin/plugin.json` |
| Guidance to Claude | `CLAUDE.md` |
| Guidance to Codex | `AGENTS.md` |
| High-level intro | `README.md` |

### 11.3 L-NNN YAML schema (quick reference)

```yaml
---
id: L-NNN                    # matches the ## L-NNN heading below
layer: L3                    # L1 | L2 | L3 | L4 | L5 (lessons default to L3)
type: experience             # fact | process | decision | experience | pattern
maturity: draft              # draft | verified | canonical
versions:                    # applicable versions; [TBD] if unclear
  - "AEP 8.1.x"
provenance:
  sr: "1-23647477802"        # SR number as string
  date: "2026-07-14"         # ISO date of capture
promotion:
  status: pending            # pending | promoted | rejected
  target: null               # when promoted: "references/<file>.md#<anchor>"
  date: null                 # when promoted or rejected: ISO date
  note: null                 # optional free text
owner: "@github-handle"
---
```

### 11.4 References file frontmatter (quick reference)

```yaml
---
title: "<Human-Readable Title>"
layer: L4
scope: "<one-line scope description>"
maturity: canonical
applicable_versions:
  - "AES 10.x"
  - "AES 8.1.x"
last_reviewed: "2026-06-03"
owner: "avaya-debug skill"
staleness_risks:
  - "<risk 1>"
  - "<risk 2>"
related_docs:
  - "diagnostic-principles.md"
  - "lessons/aes-cti-jtapi.md"
---
```

### 11.5 Related documents

- `CLAUDE.md` — guidance to Claude Code (also covers the 5×5×3
  overview)
- `AGENTS.md` — guidance to Codex (mirrors CLAUDE.md)
- `README.md` — high-level plugin intro
- `docs/reform/PLAN.md` — the six-phase reform that produced v2.0.0
- `docs/reform/schema.md` — the YAML frontmatter contract
- `skills/avaya-debug/lessons/README.md` — L-NNN template and
  promotion rule
- `skills/avaya-debug/triage/README.md` — L1 layer explained

---

*Guide version 1.0 — 2026-07-14. Report issues at
https://github.com/calvinmao/avaya-troubleshooting/issues.*
