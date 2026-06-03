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
| `linux-server.md` | Linux OS health, systemd, CPU/memory/disk, kernel, sysctl, SELinux, journalctl, OOM |
| `network-infrastructure.md` | TCP/IP, DNS, routing, firewall, packet capture, QoS, VLAN, MTU, iperf3, tcpdump |
| `cloud-infrastructure.md` | AWS, Azure, EC2/VM, VPC/VNet, NSG/SG, VPN, CloudWatch, EKS/AKS, S3/Blob, AXP |

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

## IT Ops Maintenance Patterns

Reference files have been enriched with general Linux/Java/database health patterns adapted
from IT operations automation best practices. These apply to all Avaya Linux-based servers
(AES, SM, AACC, ACRA, CCMM, EPM, etc.) without modification.

### What was added (and where)

| Pattern Category | Reference File | Section |
|------------------|---------------|---------|
| Proactive server health (CPU, memory, disk, systemd) | `log-collection.md` | Proactive Server Health Commands |
| Auto-remediation playbooks (log rotation, service restart) | `log-collection.md` | Auto-Remediation Playbooks |
| SNMP monitoring (Avaya enterprise MIB `.1.3.6.1.4.1.6889`) | `log-collection.md` | SNMP Monitoring |
| Monitoring thresholds table | `log-collection.md` | Monitoring Thresholds |
| Command safety rules (blocked / approval-required) | `log-collection.md` | Command Safety Rules |
| Certificate expiry detection + live HTTPS probe | `certificates-login-outage.md` | Certificate Health Commands (B1) |
| Certificate near-expiry remediation playbook | `certificates-login-outage.md` | Auto-Remediation: Cert Near-Expiry (B2) |
| Post-cert-change restart sequence | `certificates-login-outage.md` | Post-Cert-Change Restart Sequence (B3) |
| AES PostgreSQL connection pool monitoring | `aes-cti-jtapi.md` | C1 — AES PostgreSQL Connection Pool |
| AES database backup + integrity check | `aes-cti-jtapi.md` | C2 — AES Database Backup |
| CPU spike → jstack + automated alert | `aes-cti-jtapi.md` | D3 — CPU Spike → Heap Dump |
| Alert → Diagnose → Remediate 3-node workflow | `aes-cti-jtapi.md` | F4 — Workflow Template |
| WebLogic/ACRA heap monitoring + GC watch | `recording-wfo.md` | A2 — Java Heap & WebLogic Monitoring |
| WFO SQL Server / Oracle JDBC connection health | `recording-wfo.md` | C3 — WFO SQL Server Connection Health |
| SIP stack port connectivity verification | `sip-voice-quality.md` | A3 — Port Connectivity Verification |
| SBC/router SNMP + sipsak OPTIONS health check | `sip-voice-quality.md` | E1 — SBC / Router Interface Health |

### Auto-remediation safety invariants

Adapted from the IT ops command safety filter. These constraints are embedded in the
reference files above and must be preserved when adding new playbooks:

- **Never auto-execute** `systemctl stop/start` on CM, SMGR, WebLM, or AES without
  explicit change-control approval.
- **Always read-only first**: health check commands (`ps`, `jstat`, `netstat`, `df`,
  `snmpget`) require no approval; use them freely.
- **Cooldown 300 s**: do not retry the same remediation action within 5 minutes.
- **Rollback trigger**: if a metric does not improve within 10 minutes of remediation,
  stop and escalate — do not loop.
- **Never run**: `rm -rf /`, `iptables -F`, `kill -9 0`, `DROP DATABASE` without
  explicit human approval outside of automated tooling.

---

## Key Diagnostic Invariants (Do Not Change Without Evidence)

These are empirically validated facts encoded in `SKILL.md` and the agent:

- **UCID extraction**: Always `cast event to LucentV5CallInfo` → `getUCID()`. Never `event.getOriginalCallInfo().getUCID()` — returns all-zeros on EC_PARK events.
- **deviceIDType 30** = trunk placeholder (EXPLICIT_PUBLIC_UNKNOWN); **31** = actual PSTN number.
- **`connBelongToDifferentDeviceIDType` flag** in trace = smoking gun for park/unpark TSCall destruction.
- **OLE2 .doc files**: parse with `olefile`, not `python-docx`.
- **SA9114/SA9124** on `display system-features` must be checked before deep JTAPI null-address analysis.
