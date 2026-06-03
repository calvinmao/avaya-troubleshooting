# avaya-troubleshooting

Senior Avaya UC & CC troubleshooting plugin for Claude Code. Covers AES, JTAPI, TSAPI, CSTA, DMCC, AACC, Oceana, POM, Recording, WFO, Analytics, SIP, certificates, digital channels, IP Office, and security vulnerability assessment.

## Components

### Skill: `avaya-debug`

The main troubleshooting skill. Auto-activates when you mention Avaya product names or fault keywords. Implements progressive reference loading — only loads the domain-specific reference for the product you are troubleshooting.

**Trigger keywords**: AES, JTAPI, TSAPI, CSTA, DMCC, AACC, Oceana, POM, AXP, CMS, VDN, recording, ACRA, WFO, WFE, Verint, analytics, Kubernetes, SIP, one-way audio, certificate, WebLM, login outage, email channel, IP Office, CVE, vulnerability, AVAPT

### Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/avaya-sr` | `/avaya-sr 12345678 AES null address on park` | Start a structured SR troubleshooting session |
| `/avaya-report` | `/avaya-report` | Generate a formal SR report from current session analysis |
| `/avaya-logs` | `/avaya-logs AACC` | Get exact log collection commands for a product |

### Agent: `avaya-debugger`

A specialized subagent you can dispatch for parallel trace analysis tasks. Has the same deep Avaya expertise as the main skill and can be invoked via the `Agent` tool with `subagent_type: "avaya-debugger"`.

### Reference Files (loaded on demand)

| File | Coverage |
|------|----------|
| `aes-cti-jtapi.md` | AES, JTAPI, TSAPI, CSTA, DMCC, park/unpark, TSCall, deviceIDType |
| `contact-center.md` | AACC, Oceana, POM, AXP, CMS, VDN, vector, skill, agent |
| `recording-wfo.md` | Recording, ACRA, WFO/WFE, Verint, WebLogic, RIS, DMSA |
| `analytics-kubernetes.md` | Analytics, Oceanalytics, K8s, Kafka, MicroStrategy, PV |
| `security-vulnerability.md` | AVAPT/NVAPT, CVE, Nessus, cipher hardening, Blackduck |
| `sip-voice-quality.md` | SIP, one-way audio, codec, QoS, SBC, RTP |
| `certificates-login-outage.md` | Certificate, WebLM, login, auth, EPM outage |
| `digital-channels.md` | Email, Social, ESL, Infinity, WeChat, WhatsApp, CCMM |
| `ip-office.md` | IP Office, IPO, SSA, SysMonitor, ACCS+IPO |
| `log-collection.md` | getlogs, trace enable, DMCC/TSAPI/CSTA trace, tcpdump |

## Installation

This plugin is registered in the `local-plugins` marketplace (already configured in your `settings.json`).

```
/plugin install avaya-troubleshooting@local-plugins
```

Then restart Claude Code.

## Usage Examples

**Start a new SR session:**
```
/avaya-sr 00123456 AES Null calledAddress returned on EC_PARK events for outbound calls
```

**Ask about a specific fault:**
```
My AACC agents go into Unknown state after transfer. VDN logs show skill routing failure.
```

**Get log collection steps:**
```
/avaya-logs Recording
```

**Generate the SR report after analysis:**
```
/avaya-report
```
