# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin providing senior Avaya UC & CC troubleshooting expertise. It contains no runnable code — all components are Markdown files interpreted by the Claude Code plugin system.

## Installation & Reload

```bash
# Install from local marketplace
/plugin install avaya-troubleshooting@local-plugins

# After any edit to plugin files, restart Claude Code to pick up changes
```

## Plugin Structure

```
.claude-plugin/
  plugin.json          # Plugin identity (name, version, author)
  marketplace.json     # Local marketplace registration pointing to ./
skills/avaya-debug/
  SKILL.md             # Main skill — triggers + diagnostic principles
  references/          # Domain reference files (loaded on demand)
  lessons/             # Field-captured findings, mirrors references/ 1:1
commands/
  avaya-sr.md          # /avaya-sr — start SR troubleshooting session
  avaya-report.md      # /avaya-report — generate formal SR report
  avaya-logs.md        # /avaya-logs — get product-specific log commands
  avaya-learn.md       # /avaya-learn — capture lessons from current session
agents/
  avaya-debugger.md    # Subagent for parallel trace analysis tasks
```

## Architecture: Progressive Reference Loading

The core design pattern is **load-on-demand**: `SKILL.md` contains a routing table that maps trigger keywords → reference files. When the skill activates, it reads ONLY the reference file(s) matching the user's product/symptom. This keeps context lean.

Each reference file is self-contained for its domain. Commands reference them via `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/references/<file>.md`.

### Reference file → domain mapping

| File | Domain |
|------|--------|
| `aes-cti-jtapi.md` | AES, JTAPI, TSAPI, CSTA, DMCC, park/unpark |
| `contact-center.md` | AACC, Oceana, POM, CMS, VDN, vector, agent state, agent login |
| `recording-wfo.md` | ACRA, WFO/WFE, Verint, WebLogic, RIS, pause/resume, recording loss |
| `analytics-kubernetes.md` | Oceanalytics, K8s, Kafka, bosh, MicroStrategy |
| `security-vulnerability.md` | AVAPT/NVAPT, CVE, Nessus, cipher hardening |
| `sip-voice-quality.md` | SIP, one-way audio, codec, QoS, SBC, voice quality, intermittent disconnect |
| `certificates-login-outage.md` | Certificate, WebLM, EPM outage, SMGR |
| `digital-channels.md` | Email/Social, ESL, Infinity, CCMM, WeChat |
| `ip-office.md` | IP Office, SSA, SysMonitor, ACCS+IPO |
| `log-collection.md` | getlogs, trace enables, tcpdump, log levels |
| `orchestration-integration.md` | POM + Oceana, callback delivery, CCMM, Workspace, async channels, cross-product orchestration |

## Extending the Plugin

### Add a new reference domain
1. Create `skills/avaya-debug/references/<new-domain>.md`
2. Add a row to the progressive loading table in `SKILL.md` with trigger keywords
3. Add the same mapping entry in `agents/avaya-debugger.md` if subagent coverage is needed

### Add a new command
Create `commands/<command-name>.md` with frontmatter:
```markdown
---
description: One-line description for /help listing
argument-hint: "[optional arg hint]"
---
```

## Learning Loop

The plugin grows from real cases through a two-tier capture flow:

1. **Capture** — At the end of a session run `/avaya-learn` (or accept the post-report nudge in `/avaya-report`). It scans the session for evidence-anchored findings, drafts `L-NNN` entries, and on approval appends them to the matching `skills/avaya-debug/lessons/<domain>.md`.
2. **Promote** — If a lesson meets the promotion rule in `skills/avaya-debug/lessons/README.md` — reproduced across ≥2 SR cases OR identifies a generalizable code path / trace string / config flag — `/avaya-learn` proposes a concrete edit to the canonical `references/<domain>.md`. On approval the edit is applied and the lesson's `Promotion:` line is updated with the target anchor and date.

Lessons auto-load whenever their matching reference loads, so accumulated field knowledge is always available the moment the right domain activates. When an `L-NNN` ID appears in a report or analysis, find it under `skills/avaya-debug/lessons/` — the `Provenance:` line gives the source SR for verification.

## Key Diagnostic Invariants (Do Not Change Without Evidence)

These are empirically validated facts encoded in `SKILL.md` and the agent:

- **UCID extraction**: Always `cast event to LucentV5CallInfo` → `getUCID()`. Never `event.getOriginalCallInfo().getUCID()` — returns all-zeros on EC_PARK events.
- **deviceIDType 30** = trunk placeholder (EXPLICIT_PUBLIC_UNKNOWN); **31** = actual PSTN number.
- **`connBelongToDifferentDeviceIDType` flag** in trace = smoking gun for park/unpark TSCall destruction.
- **OLE2 .doc files**: parse with `olefile`, not `python-docx`.
- **SA9114/SA9124** on `display system-features` must be checked before deep JTAPI null-address analysis.
