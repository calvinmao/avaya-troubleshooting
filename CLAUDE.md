# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin providing senior Avaya UC & CC troubleshooting expertise. It contains no runnable code — all components are Markdown files interpreted by the Claude Code plugin system.

## Design Alignment

This plugin is designed against the [agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) engineering guide. Key principles applied:

- **SKILL.md is a routing map, not an encyclopedia** — detailed invariants live in `references/diagnostic-principles.md`
- **Progressive disclosure** — only the matching domain reference is loaded per session
- **Lessons feedback loop** — `/avaya-learn` captures field findings; `/avaya-report` nudges capture post-session
- **Evals for skill quality** — `evals/` contains activation and output-quality test cases
- **Metadata on every reference** — `scope`, `last_reviewed`, `staleness_risks` header in each `references/*.md`
- **Entropy/GC workflow** — see "Knowledge Base Maintenance" below

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
  SKILL.md             # Routing map — triggers + progressive loading table (lean)
  references/          # Domain reference files (loaded on demand)
    diagnostic-principles.md  # Always-loaded: core invariants, cross-product, vendor escalation
    aes-cti-jtapi.md           # AES, JTAPI, TSAPI, CSTA, DMCC
    contact-center.md          # AACC, Oceana, POM, CMS, VDN, vector
    recording-wfo.md           # ACRA, WFO/WFE, Verint, WebLogic
    analytics-kubernetes.md    # Oceanalytics, K8s, bosh, Kafka
    security-vulnerability.md  # AVAPT/NVAPT, CVE, cipher hardening
    sip-voice-quality.md       # SIP, RTP, on-box capture tools
    certificates-login-outage.md  # Cert, WebLM, EPM outage, SMGR
    digital-channels.md        # Email/Social, ESL, CCMM
    ip-office.md               # IPO, SSA, SysMonitor
    log-collection.md          # getlogs, trace enables, health checks
    orchestration-integration.md  # POM + Oceana, callback, Workspace
    linux-server.md            # Linux OS health, systemd, kernel, OOM
    network-infrastructure.md  # TCP/IP, DNS, firewall, QoS, MTU
    cloud-infrastructure.md    # AWS, Azure, EKS/AKS, AXP
  lessons/             # Field-captured findings, mirrors references/ 1:1
    README.md          # L-NNN convention, promotion rules
    diagnostic-principles.md  # Cross-domain invariant lessons
    <domain>.md        # One file per reference domain
evals/
  activation.md        # Should-trigger / should-not-trigger / near-miss cases
  output-quality.md    # Output quality rubric (6 criteria, 0-3 scoring) + 6 test cases
commands/
  avaya-sr.md          # /avaya-sr — start SR troubleshooting session
  avaya-report.md      # /avaya-report — generate formal SR report
  avaya-logs.md        # /avaya-logs — get product-specific log commands
  avaya-learn.md       # /avaya-learn — capture lessons from current session
agents/
  avaya-debugger.md    # Subagent for parallel trace analysis tasks
```

## Architecture: Progressive Reference Loading

The core design pattern is **load-on-demand**: `SKILL.md` contains a routing table that maps trigger keywords → reference files. When the skill activates:
1. Always loads `references/diagnostic-principles.md` first (core invariants, always applicable)
2. Reads ONLY the domain reference file(s) matching the user's product/symptom

Each reference file is self-contained for its domain. The metadata block at the top of each reference file records `scope`, `last_reviewed`, `staleness_risks`, and `related_docs` for maintenance purposes.

### Reference file → domain mapping

| File | Domain |
|------|--------|
| `diagnostic-principles.md` | **Always loaded** — core invariants, cross-product integration, vendor escalation, case doc extraction |
| `aes-cti-jtapi.md` | AES, JTAPI, TSAPI, CSTA, DMCC, park/unpark |
| `contact-center.md` | AACC, Oceana, POM, CMS, VDN, vector, agent state, agent login |
| `recording-wfo.md` | ACRA, WFO/WFE, Verint, WebLogic, RIS, pause/resume, recording loss |
| `analytics-kubernetes.md` | Oceanalytics, K8s, Kafka, bosh, MicroStrategy |
| `security-vulnerability.md` | AVAPT/NVAPT, CVE, Nessus, cipher hardening |
| `sip-voice-quality.md` | SIP, one-way audio, codec, QoS, SBC, voice quality, intermittent disconnect |
| `certificates-login-outage.md` | Certificate, WebLM, EPM outage, SMGR |
| `digital-channels.md` | Email/Social, ESL, Infinity, CCMM, WeChat |
| `ip-office.md` | IP Office, SSA, SysMonitor, ACCS+IPO |
| `log-collection.md` | getlogs, trace enables, tcpdump, log levels, health checks |
| `orchestration-integration.md` | POM + Oceana, callback delivery, CCMM, Workspace, async channels |
| `linux-server.md` | Linux OS health, systemd, CPU/memory/disk, kernel, sysctl, SELinux, journalctl, OOM |
| `network-infrastructure.md` | TCP/IP, DNS, routing, firewall, packet capture, QoS, VLAN, MTU, iperf3, tcpdump |
| `cloud-infrastructure.md` | AWS, Azure, EC2/VM, VPC/VNet, NSG/SG, VPN, CloudWatch, EKS/AKS, S3/Blob, AXP |

## Extending the Plugin

### Add a new reference domain
1. Create `skills/avaya-debug/references/<new-domain>.md` — include the metadata header block
2. Create `skills/avaya-debug/lessons/<new-domain>.md` — stub file with domain description
3. Add a row to the progressive loading table in `SKILL.md` with trigger keywords
4. Add `<new-domain>.md` row to `lessons/README.md`
5. Add the same mapping entry in `agents/avaya-debugger.md` if subagent coverage is needed

### Add a new command
Create `commands/<command-name>.md` with frontmatter:
```markdown
---
description: One-line description for /help listing
argument-hint: "[optional arg hint]"
---
```

### Add evals for a new domain
Append a `### Should-Trigger Cases` block to `evals/activation.md` and a `### OQ-NNN` block to `evals/output-quality.md`. Run both files against the agent before shipping new domains.

## Learning Loop

The plugin grows from real cases through a two-tier capture flow:

1. **Capture** — At the end of a session run `/avaya-learn` (or accept the post-report nudge in `/avaya-report`). It scans the session for evidence-anchored findings, drafts `L-NNN` entries, and on approval appends them to the matching `skills/avaya-debug/lessons/<domain>.md`.
2. **Promote** — If a lesson meets the promotion rule in `skills/avaya-debug/lessons/README.md` — reproduced across ≥2 SR cases OR identifies a generalizable code path / trace string / config flag — `/avaya-learn` proposes a concrete edit to the canonical `references/<domain>.md`. On approval the edit is applied and the lesson's `Promotion:` line is updated with the target anchor and date.

Lessons auto-load whenever their matching reference loads, so accumulated field knowledge is always available the moment the right domain activates. When an `L-NNN` ID appears in a report or analysis, find it under `skills/avaya-debug/lessons/` — the `Provenance:` line gives the source SR for verification.

## Knowledge Base Maintenance (Entropy / GC)

Run periodically (suggested: quarterly, or after 10+ new lessons):

```
1. Scan lessons/ for L-NNN entries with Promotion: pending — propose promotion if ≥2 SRs
2. Check each reference file's last_reviewed date — flag files not reviewed in >6 months
3. Scan for duplicate or near-duplicate invariants across references/
4. Remove or merge lesson entries that have been promoted (keep Promotion: line as audit trail)
5. Update evals/activation.md with any new product triggers added in SKILL.md
6. Update evals/output-quality.md with OQ-NNN entries from production incidents
7. Review staleness_risks metadata in each reference — update version-specific content
```

Per the agents-best-practices guide: *"Repeated failures should become tools, validators, docs, evals, or policies rather than repeated prompt advice."* When a diagnostic error recurs, add an OQ-NNN eval case, not just a SKILL.md reminder.

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
| Prometheus node-exporter alert rules (Linux) | `linux-server.md` | Prometheus Alert Rules — Node Exporter |
| Prometheus kube-state-metrics alert rules (K8s) | `analytics-kubernetes.md` | Prometheus Alert Rules — Kubernetes |
| Prometheus JVM exporter alert rules (AES/WFO) | `aes-cti-jtapi.md` | Prometheus Alert Rules — JVM Exporter |

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

These are empirically validated facts. Full details in `references/diagnostic-principles.md`.

- **UCID extraction**: Always `cast event to LucentV5CallInfo` → `getUCID()`. Never `event.getOriginalCallInfo().getUCID()` — returns all-zeros on EC_PARK events.
- **deviceIDType 30** = trunk placeholder (EXPLICIT_PUBLIC_UNKNOWN); **31** = actual PSTN number.
- **`connBelongToDifferentDeviceIDType` flag** in trace = smoking gun for park/unpark TSCall destruction.
- **OLE2 .doc files**: parse with `olefile`, not `python-docx`.
- **SA9114/SA9124** on `display system-features` must be checked before deep JTAPI null-address analysis.

## Wiki Knowledge Base

**Vault:** `C:/claude-obsidian` (claude-obsidian plugin, v1.9.2)

The wiki is a SUPPLEMENT to this plugin's reference files — check it when you need cross-session context, recently ingested documents, or synthesis that spans multiple cases. Do NOT use it to replace the plugin's own `references/*.md` files.

**Reading protocol:**
1. Read `C:/claude-obsidian/wiki/hot.md` first — recent context (~500 words)
2. If not enough, read `C:/claude-obsidian/wiki/index.md` — full catalog
3. For domain specifics, read the matching wiki concept page directly (see mapping below)

**Domain → wiki page mapping (for Avaya topics):**

| Domain | Wiki Page |
|--------|-----------|
| AES, JTAPI, TSAPI, CSTA, DMCC, CTI | `wiki/concepts/AES CTI JTAPI.md` |
| AACC, Oceana, POM, CMS, VDN, agent | `wiki/concepts/Avaya Contact Center.md` |
| Recording, ACRA, WFO, WFE, Verint | `wiki/concepts/Avaya Recording WFO.md` |
| SIP, RTP, voice quality, SBC | `wiki/concepts/Avaya SIP Voice Quality.md` |
| Certificate, WebLM, login outage | `wiki/concepts/Avaya Certificates WebLM.md` |
| Analytics, Kubernetes, bosh, Kafka | `wiki/concepts/Avaya Analytics Kubernetes.md` |
| Security, AVAPT, NVAPT, CVE | `wiki/concepts/Avaya Security Assessment.md` |
| Email, Social, ESL, CCMM | `wiki/concepts/Avaya Digital Channels.md` |
| Log collection, getlogs, trace | `wiki/concepts/Avaya Log Collection.md` |
| Cross-product, POM+Oceana, callback | `wiki/concepts/Avaya Cross-Product Orchestration.md` |
| Linux, systemd, OOM, kernel | `wiki/concepts/Avaya Linux Server Diagnostics.md` |
| Network, TCP, DNS, firewall, QoS | `wiki/concepts/Avaya Network Infrastructure.md` |
| Core invariants (all domains) | `wiki/concepts/Avaya Diagnostic Principles.md` |

Do NOT read the wiki for general coding questions or content already fully covered by the plugin's own reference files.

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical label strings (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo — one `CONTEXT.md` + `docs/adr/` at the root. See `docs/agents/domain.md`.
