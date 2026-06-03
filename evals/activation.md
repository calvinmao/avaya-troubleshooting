# Skill Activation Evals — avaya-debug

Tests whether the `avaya-debug` skill activates on the right prompts and stays dormant on unrelated ones.

## How to run

Present each prompt to the agent without prior context. Pass = skill activates and loads the correct reference file(s). Fail = skill does not activate, or activates but loads wrong reference.

---

## Should-Trigger Cases

### AES / JTAPI

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-001 | "JTAPI application is getting null from getCalledAddress() on park events" | `aes-cti-jtapi.md` | Core park/unpark scenario |
| A-002 | "AES PostgreSQL is throwing connection pool exhausted errors" | `aes-cti-jtapi.md` | DB connection pool |
| A-003 | "The CSTA trace shows connBelongToDifferentDeviceIDType, what does it mean?" | `aes-cti-jtapi.md` + `diagnostic-principles.md` | Known smoking-gun pattern |
| A-004 | "getlogs output attached — AES heap dump after 3 days uptime" | `aes-cti-jtapi.md` + `log-collection.md` | Cross-domain |
| A-005 | "UCID comes back as 00000000000000000000 in EC_PARK event" | `aes-cti-jtapi.md` + `diagnostic-principles.md` | Known UCID invariant |

### Contact Center

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-010 | "Agent is stuck in aux mode and can't be force-logged out from AACC" | `contact-center.md` | Agent state machine |
| A-011 | "VDN is routing to wrong skill, vector step 5 looks incorrect" | `contact-center.md` | Vector routing |
| A-012 | "POM campaign nail-up — calls are not launching despite active campaign" | `contact-center.md` | POM |
| A-013 | "Oceana routing decision not matching expected CMS skill assignment" | `contact-center.md` | Oceana + CMS |

### Recording / WFO

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-020 | "Recordings are missing for the last 2 hours, ACRA shows no errors" | `recording-wfo.md` | Silent recording loss |
| A-021 | "WFO Consolidator is throwing JDBC pool exhausted every morning" | `recording-wfo.md` | Database connection |
| A-022 | "WebLogic managed server OOM at 04:00 daily" | `recording-wfo.md` | Java heap |
| A-023 | "Verint BatchExtender sync job stuck at 80% for 6 hours" | `recording-wfo.md` | Vendor escalation candidate |

### Analytics / Kubernetes

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-030 | "KubePersistentVolumeUsageCritical alarm on Analytics node — how to clear?" | `analytics-kubernetes.md` | PV alarm |
| A-031 | "bosh director returns HTTP 500, ccm commands hang" | `analytics-kubernetes.md` | bosh director |
| A-032 | "Pod crashlooping — kubectl logs shows OOMKilled" | `analytics-kubernetes.md` | K8s OOM |

### SIP / Voice Quality

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-040 | "One-way audio on inbound SIP trunk calls — agent hears customer, customer hears nothing" | `sip-voice-quality.md` | RTP asymmetry |
| A-041 | "SIP trunk registration dropping every 30 minutes" | `sip-voice-quality.md` | Keep-alive / OPTIONS |
| A-042 | "How do I read a SIP capture with sngrep without moving the pcap file?" | `sip-voice-quality.md` | On-box tools |
| A-043 | "tshark rtp,streams shows jitter of 150ms — is that a problem?" | `sip-voice-quality.md` | RTP quality |

### Certificates / Login / Outage

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-050 | "EPM is down after power outage — what's the startup sequence?" | `certificates-login-outage.md` | Outage recovery |
| A-051 | "Certificate expired on AES, JTAPI clients can't connect" | `certificates-login-outage.md` | Cert expiry |
| A-052 | "WebLM license server showing invalid signature error" | `certificates-login-outage.md` | WebLM trust |

### Security

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-060 | "Nessus scan found CVE-2024-XXXX on AES 10.1.2 — is it applicable?" | `security-vulnerability.md` | CVE triage |
| A-061 | "AVAPT report shows weak ciphers on SM SIP TLS — how to harden?" | `security-vulnerability.md` | Cipher hardening |

### Infrastructure

| ID | Prompt | Expected Reference | Notes |
|----|--------|--------------------|-------|
| A-070 | "AES server showing 95% disk usage on /var/log — what to clean safely?" | `linux-server.md` + `log-collection.md` | Disk cleanup |
| A-071 | "SIP calls failing intermittently — suspect firewall conntrack table overflow" | `network-infrastructure.md` | Conntrack |
| A-072 | "AWS Security Group blocking SIP from SBC — which ports?" | `cloud-infrastructure.md` | Cloud SG rules |

---

## Should-NOT-Trigger Cases

These prompts should NOT activate the avaya-debug skill. The agent should handle them with general knowledge without loading Avaya reference files.

| ID | Prompt | Reason |
|----|--------|--------|
| N-001 | "Write a Python script to parse a CSV file" | No Avaya context |
| N-002 | "What is the capital of France?" | General knowledge |
| N-003 | "Explain what a SIP INVITE message is" | Educational, not troubleshooting |
| N-004 | "Review my Java code for style issues" | Code review, not Avaya fault |
| N-005 | "How does Kubernetes work?" | Generic K8s, no Avaya context |

---

## Near-Miss Cases (should trigger, but phrased casually)

The skill must activate on informal phrasing, not just formal technical terms.

| ID | Prompt | Expected Activation |
|----|--------|---------------------|
| M-001 | "our call recording is broken again" | `recording-wfo.md` |
| M-002 | "agents can't log in this morning" | `contact-center.md` or `certificates-login-outage.md` |
| M-003 | "the cert expired" | `certificates-login-outage.md` |
| M-004 | "calls are dropping every few minutes" | `sip-voice-quality.md` |
| M-005 | "nothing works after the power came back" | `certificates-login-outage.md` |
| M-006 | "getlogs attached" | `log-collection.md` + domain reference |
| M-007 | "JTAPI keeps crashing" | `aes-cti-jtapi.md` |
