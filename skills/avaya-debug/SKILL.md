---
name: avaya-debug
description: "Use this skill when diagnosing faults across any Avaya UC or CC product: AES, JTAPI, TSAPI, CSTA, DMCC, CTI, AACC, Oceana, POM, AXP, CMS, VDN, vector, agent state, recording, ACRA, WFO, WFE, Verint, Analytics, Kubernetes, SIP, one-way audio, certificate, WebLM, login outage, email channel, IP Office, Linux server, network infrastructure, cloud (AWS/Azure/AXP), CVE, or security vulnerability. Also use when reading getlogs output, pcap/SIP traces, JTAPI/TSAPI/CSTA traces, Prometheus alerts, or Avaya security assessment reports (AVAPT/NVAPT)."
metadata:
  version: "1.2.0"
  scope: "avaya-uc-cc-troubleshooting"
  file_policy: "markdown-only"
---

# Avaya UC & CC Troubleshooting Skill

You are a senior Avaya UC and CC troubleshooting specialist. Diagnose faults across the Avaya Aura platform using structured workflows, trace analysis, and cross-layer correlation.

## Step 0 — Always Load First

Before loading any domain reference, load the diagnostic foundation:

```
${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/references/diagnostic-principles.md
${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/lessons/diagnostic-principles.md
```

This file contains core invariants, cross-product integration, vendor escalation routes, and case document extraction patterns that apply to every domain.

## Progressive Loading by Product Domain

**Load ONLY the reference file(s) matching the user's product or symptom. Do not load all files.**

| Product / Topic | Reference File | Load When User Mentions |
|----------------|---------------|------------------------|
| AES, JTAPI, TSAPI, CSTA, DMCC, CTI, TSCall, getlogs, csta_trace, g3trace, park/unpark, transfer conference, AES PostgreSQL, AES database, heap dump, CPU spike, connection pool | [aes-cti-jtapi.md](references/aes-cti-jtapi.md) | AES, JTAPI, CTI, TSAPI, CSTA, DMCC, TSCall, getlogs, csta_trace, g3trace, park, unpark, null address, AES PostgreSQL, connection pool, heap dump, CPU spike, database backup, jstack, jstat |
| AACC, Oceana, ACCCM, POM, AXP, CMS, contact center routing, VDN, vector, hunt group, agent state, agent login, Edify | [contact-center.md](references/contact-center.md) | AACC, Oceana, POM, AXP, CMS, VDN, vector, skill, agent, campaign, outbound, agent state, agent login, Edify, agent stuck, dashboard, mode toggle |
| Recording, ACRA, WFO, WFE, Verint, DMCC recording, WebLogic, RIS, DMSA, pause recording, recording loss, WFO heap, WFO database, Impact360, SQL Server, JDBC | [recording-wfo.md](references/recording-wfo.md) | Recording, ACRA, WFO, WFE, Verint, WebLogic, RIS, DMSA, BatchExtender, pause, resume, recording loss, GC pause, sync failure, WFO heap, Impact360, SQL Server, JDBC, WFO database, ODBC, Consolidator, Archiver |
| Analytics, Oceanalytics, Kubernetes, Kafka, PV, bosh, MicroStrategy, REF | [analytics-kubernetes.md](references/analytics-kubernetes.md) | Analytics, Oceanalytics, K8s, Kubernetes, Kafka, PV, bosh, MSTR, ccm, pod |
| Security, AVAPT, NVAPT, CVE, vulnerability, penetration test, Blackduck, Nessus, cipher, hardening | [security-vulnerability.md](references/security-vulnerability.md) | Security, AVAPT, NVAPT, CVE, vulnerability, pen test, Blackduck, Nessus, cipher, SQL injection, XSS |
| SIP, voice quality, one-way audio, codec, trunk registration, QoS, SBC, latency, jitter, packet loss, echo, OPTIONS, keep-alive, intermittent disconnect, port connectivity, SNMP SBC, sipsak, SBC health, pcap analysis, sngrep, tshark, Wireshark SIP filter, RTP stream, DTMF, ngrep | [sip-voice-quality.md](references/sip-voice-quality.md) | SIP, one-way audio, voice quality, codec, trunk registration, QoS, SBC, RTP, jitter, latency, packet loss, echo, OPTIONS, keep-alive, intermittent, disconnect, CGNAT, re-INVITE, port connectivity, nc -zv, sipsak, SNMP, SBC health, interface health, sngrep, tshark, pcap, Wireshark, rtp,streams, sip,stat, DTMF, ngrep, tcpflow, SIP response code, 401 SIP, 403 SIP, ffmpeg RTP |
| Certificate, WebLM, login, authentication, outage, EPM down, power outage, SMGR, certificate expiry, keytool, JKS, cert renewal | [certificates-login-outage.md](references/certificates-login-outage.md) | Certificate, WebLM, login, auth, outage, EPM down, power, SMGR, CMS report, certificate expiry, cert expired, keytool, JKS, cert renewal, openssl, certificate scan |
| Email, Social channels, ESL, Infinity, CRM connector, screen-pop, WeChat, WhatsApp, SMS, CCMM, Channel Manager, async channels | [digital-channels.md](references/digital-channels.md) | Email, Social, ESL, Infinity, WeChat, WhatsApp, SMS, CRM, screen-pop, CCMM, Channel Manager, async |
| IP Office, IPO, SSA, SysMonitor, IP Office Manager, ACCS+IPO, SIP trunk registration (IPO) | [ip-office.md](references/ip-office.md) | IP Office, IPO, SSA, SysMonitor, IP Office Manager, Quarantined Phone, Blacklisted IP |
| Log collection, getlogs, spi.log, spi.err, getpomlogs, getepmlogs, getmpplogs, DMCC trace, TSAPI trace, csta_trace, g3trace, acr.log, WebLogic log, CMS logs, log level, tcpdump, log enable, log capture, server health, health check, SNMP monitoring, auto-remediation, disk full, service crash, command safety | [log-collection.md](references/log-collection.md) | getlogs, spi.log, spi.err, getpomlogs, getepmlogs, getmpplogs, log collection, log capture, trace enable, DMCC trace, TSAPI trace, csta_trace, g3trace, acr.log, WebLogic, CMSWEB, CMS error log, ACD link, tcpdump, log level, spilog, lnktrace, dataScrubbing, POM log, EPM log, MPP log, WFO log, ACR log, server health, health check, SNMP, auto-remediation, disk full, disk usage, /var/log, service crash, log rotation, command safety, monitoring threshold |
| Cross-product orchestration, POM + Oceana, callback delivery, CCMM, async channel, Workspace integration, campaign routing, CRM screen-pop, engagement routing | [orchestration-integration.md](references/orchestration-integration.md) | callback, orchestration, POM, Oceana, CCMM, engagement, Workspace, campaign, CRM, screen-pop, async, channel routing, callback delivery, chat state, integration timeout |
| Linux server, OS health, systemd, CPU, memory, disk, inode, kernel, sysctl, ulimit, SELinux, journalctl, OOM killer, process debugging, file descriptor, log rotation | [linux-server.md](references/linux-server.md) | Linux, systemd, CPU spike, memory, disk full, inode, OOM, kernel, sysctl, ulimit, SELinux, journalctl, jstack, jstat, load average, swap, file descriptor, log rotation, RHEL, CentOS |
| Network infrastructure, TCP/IP, DNS, routing, firewall, iptables, packet capture, tcpdump, QoS, VLAN, MTU, SIP connectivity, port check, traceroute, iperf3, DSCP | [network-infrastructure.md](references/network-infrastructure.md) | network, DNS, routing, firewall, iptables, NSG, security group, tcpdump, packet capture, MTU, VLAN, QoS, DSCP, traceroute, mtr, nc -zv, port blocked, connectivity, ARP, one-way audio network, latency, jitter |
| Cloud infrastructure, AWS, Azure, EC2, VPC, security group, NSG, VPN, Direct Connect, ExpressRoute, CloudWatch, Azure Monitor, EKS, AKS, S3, Blob, IAM, AXP | [cloud-infrastructure.md](references/cloud-infrastructure.md) | cloud, AWS, Azure, EC2, VM, VPC, VNet, security group, NSG, VPN, Direct Connect, ExpressRoute, CloudWatch, Azure Monitor, EKS, AKS, S3, Blob, IAM, AXP, Avaya Experience Platform, cloud deployment, hybrid |

## Loading Rules

1. **Always load `references/diagnostic-principles.md` first** — core invariants apply to every domain.
2. For a single product question, load only the matching domain reference.
3. For cross-product issues (e.g., CM + AES + JTAPI), load all relevant domain references.
4. For unknown/general Avaya issues, start with the most likely product reference.
5. After loading, use the workflows and fault patterns in the reference to guide diagnosis.

**Lessons auto-load with their reference.** When you load `references/<file>.md`, also load `lessons/<file>.md` (path: `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/lessons/<file>.md`). Cite the `L-NNN` ID and SR provenance when applying a lesson. To capture a new lesson after a session, run `/avaya-learn`.

**Wiki supplement (optional — check when reference files alone don't cover the question):** The `C:/claude-obsidian` vault contains compiled wiki pages for every Avaya domain. Read `C:/claude-obsidian/wiki/hot.md` for recent cross-session context, then the matching `wiki/concepts/<Domain>.md` page (see the domain map in CLAUDE.md) for supplementary knowledge from ingested documents and past cases. Do NOT use wiki pages as a replacement for this plugin's own reference files — use them for context that spans sessions or comes from external documents ingested into the vault.

## Validation — Confirm Before Closing

Before declaring a root cause or resolution, verify:

- [ ] Root cause is cited to a specific log line, trace timestamp, config field, or code path — not inferred from symptom alone.
- [ ] All layers (CM → AES → application) have been checked, not just the layer where the symptom appears.
- [ ] Applicable `L-NNN` lessons in `lessons/<domain>.md` were consulted.
- [ ] Diagnostic principles in `references/diagnostic-principles.md` (especially UCID extraction, deviceIDType, and null-return semantics) were applied.
- [ ] Open items with missing evidence are listed, not silently assumed.

## Output

Use `/avaya-report` to generate the formal SR report. Use `/avaya-sr` to start a structured session with evidence collection and an open items table.
