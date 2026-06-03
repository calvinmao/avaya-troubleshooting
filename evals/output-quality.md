# Output Quality Evals — avaya-debug

Tests whether the skill produces responses that meet the evidence, structure, and escalation standards defined in the diagnostic principles.

## Scoring rubric

For each test case, score the response 0–3 per criterion:
- **0** = missing / wrong
- **1** = partially present
- **2** = present and accurate
- **3** = present, accurate, and with specific evidence citation

Minimum acceptable total: **14 / 18** for a production-quality response.

---

## Quality Criterion Checklist

| # | Criterion | Max Score |
|---|-----------|-----------|
| Q1 | Root cause cites a specific log line, trace string, config field, or code path | 3 |
| Q2 | Layer-by-layer analysis covers CM → AES → Application (not just symptom layer) | 3 |
| Q3 | UCID extracted via correct path when call identity is discussed | 3 |
| Q4 | deviceIDType values interpreted correctly (30 vs 31) | 3 |
| Q5 | Vendor escalation route identified when root cause is in vendor code | 3 |
| Q6 | Open items listed with owner and evidence needed (not silently assumed) | 3 |
| **Total** | | **18** |

---

## Test Cases

### OQ-001 — Park/Unpark UCID Loss

**Scenario**: Engineer provides a CSTA trace excerpt showing `EC_PARK` event. UCID appears as all-zeros in the application log.

**Input evidence**:
```
2024-11-15 14:23:11 EC_PARK event received
  calledDevice: T12345 (deviceIDType=30)
  callingDevice: 7801
  UCID: 00000000000000000000  ← application logged this
  LucentV5CallInfo available in event
```

**Expected output must include**:
- Root cause: `getOriginalCallInfo().getUCID()` was called (returns all-zeros on park); correct path is cast to `LucentV5CallInfo` → `getUCID()`
- Cite invariant #3 from diagnostic-principles.md
- deviceIDType 30 explanation (trunk placeholder, expected on park)
- Check SA9114/SA9124 recommendation (invariant #4)
- No vendor escalation unless code path analysis confirms AES bug

**Failure patterns to flag**:
- Recommending PEA without first checking UCID extraction method
- Treating deviceIDType=30 as an error rather than expected behavior
- Closing without verifying which UCID extraction path the customer code uses

---

### OQ-002 — Agent Stuck in Aux Mode

**Scenario**: AACC agent is stuck in Aux mode. Supervisor cannot force a state change from the dashboard.

**Input evidence**:
```
Agent ID: 7045
Last state change: 09:14:22 (4 hours ago)
CMS shows: AuxWork
AACC agent state: AuxWork
Vector skill: S12 (inbound queue)
```

**Expected output must include**:
- Layer-by-layer: CM agent state vs AACC agent state vs CMS — are they consistent?
- Ask for `display station 7045` and `display agent-loginID 7045` from CM
- Ask for AACC `agentStateHistory` log for agent 7045
- If CM and AACC disagree: CTI link resync or AES TSAPI state mismatch
- If both agree: check if agent is in an active call holding the aux state

**Failure patterns to flag**:
- Immediately suggesting "restart AACC" without evidence
- Not distinguishing CM state vs AACC state vs CMS state
- Not asking for the TSAPI agent state log

---

### OQ-003 — Recording Gap (Silent Failure)

**Scenario**: 2-hour recording gap from 10:00–12:00. ACRA shows no errors. Calls appear in CMS but not in WFO search.

**Expected output must include**:
- Distinguish between: (a) ACRA didn't start recording, (b) ACRA recorded but file wasn't ingested, (c) WFO DB insert failed
- Check ACRA log for `recordingStarted` events during the gap window
- Check WFO Consolidator log for JDBC failures or insert errors
- Check `df -h` on ACRA server — disk full causes silent drop
- If audio files exist on ACRA but not in WFO: Consolidator or BatchExtender fault → Verint escalation path

**Failure patterns to flag**:
- Assuming the gap is a "known WFO issue" without checking ACRA
- Not checking disk space
- Escalating to Verint before confirming audio files exist on disk

---

### OQ-004 — Cert Expired / Login Failure

**Scenario**: After weekend maintenance, engineers cannot log into EPM. Certificate error shown in browser.

**Expected output must include**:
- Three-phase check: (1) cert expired? (2) cert renewed but JKS not updated? (3) cert updated but browser cache not cleared?
- Commands: `keytool -list -v -keystore <jks>`, `openssl s_client -connect <host>:443`
- Order of operations: update JKS → restart app → clear browser cache (all three required, invariant #8)
- Check WebLM trust chain if login proceeds but license check fails

**Failure patterns to flag**:
- Telling customer to "renew the cert" without verifying which step in the three-step sequence failed
- Not checking browser cache as a diagnosis step
- Skipping WebLM trust chain when license errors appear post-cert-change

---

### OQ-005 — SIP One-Way Audio

**Scenario**: Inbound SIP calls — agent can hear customer, customer hears nothing. Issue is intermittent, happens on ~30% of calls.

**Expected output must include**:
- Distinguish: media path asymmetry (RTP) vs signaling issue (re-INVITE failed)
- Check: does the SBC send a 200 OK with correct `c=` address in SDP?
- Capture tshark: `tshark -q -z rtp,streams` to confirm one-way RTP
- Check CGNAT / NAT traversal if customer is behind NAT
- Check DSCP marking — if RTP EF marking is lost, QoS policy may be dropping return path
- 30% intermittent → suspect load balancer or specific SBC blade

**Failure patterns to flag**:
- Recommending "restart SM" without capturing RTP stream data first
- Not checking both the outbound SDP and the in-call re-INVITE
- Closing with "NAT issue" without confirming via pcap

---

### OQ-006 — CVE Triage (Security)

**Scenario**: Nessus scan flags CVE-2024-12345 (hypothetical) affecting OpenSSL 1.1.1x on the AES server.

**Expected output must include**:
- NVD lookup for CVE-2024-12345 CVSS score and affected component
- Determine: is OpenSSL used directly by AES, or only by the OS? (library vs application exposure)
- Check Avaya PSN (Product Support Notice) for acknowledgment
- If unpatched: cipher hardening workaround vs upgrade path
- Risk rating must be evidence-based: CVSS + Avaya exposure + customer exposure profile

**Failure patterns to flag**:
- Accepting the Nessus "risk: critical" rating without checking if the vulnerability is actually reachable in the Avaya deployment context
- Not checking for an Avaya PSN before advising emergency patching
- Recommending cipher disablement without testing SIP TLS impact

---

## Regression Eval — Add After Every Production Incident

When a production fault produces a new finding, add a test case here:

```markdown
### OQ-NNN — [brief symptom]

**Scenario**: [what happened in the field SR]

**Input evidence**: [anonymized log excerpt or trace fragment]

**Expected output must include**:
- [specific finding 1]
- [specific finding 2]

**Failure patterns to flag**:
- [what the skill got wrong before this eval was added]

**Provenance**: SR <number> | <YYYY-MM-DD>
```
