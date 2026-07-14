# Contact Center (AACC / Oceana / AEP / POM / AXP / CMS / WFM) Troubleshooting Reference
<!--
scope: AACC, Oceana, POM, AXP, CMS, VDN, vector routing, agent state machine
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: AACC version-specific menu paths, Oceana API endpoints, POM log file locations
related_docs: diagnostic-principles.md, orchestration-integration.md, lessons/contact-center.md
-->



## Table of Contents
- [Contact Center Products](#contact-center-products)
- [AXP / Experience Portal Infrastructure Notes](#axp--experience-portal-infrastructure-notes)
- [AACC Deployment / Upgrade Failure Patterns](#aacc-deployment--upgrade-failure-patterns)
- [AIC (Avaya Interaction Center) Notes](#aic-avaya-interaction-center-notes)
- [ACCS (Avaya Contact Center Select) / IPO Notes](#accs-avaya-contact-center-select--ipo-notes)
- [Live Transcription / AI Services](#live-transcription--ai-services)
- [Contact Center Routing (Workflow 4)](#contact-center-routing)
- [AEP / IVR / VoiceXML (Workflow 9)](#aep--ivr--voicexml)
- [POM Campaign / Nail-up / Outbound (Workflow 18)](#pom-campaign--outbound)
- [CMS Historical Report Discrepancies (Workflow 24)](#cms-historical-report-discrepancies)
- [AXP Workflow / API (Workflow 25)](#axp-workflow--api)
- [AACC Agent Not Receiving Calls (Workflow 26)](#aacc-agent-not-receiving-calls)
- [Contact Center Fault Patterns](#contact-center-fault-patterns)
- [Historical Fault Patterns (FY21 / FY22 / FY23)](#historical-fault-patterns)
- [Contact Center Logs](#contact-center-logs)
- [CMS Log Collection](#cms-log-collection)
- [POM Log Capture](#pom-log-capture)
- [Cross-Product Integration](#cross-product-integration)

---

## Contact Center Products

| Product | Role | Key Interfaces | Primary Logs |
|---------|------|----------------|--------------|
| **AACC (Aura Contact Center)** | Contact center routing, agent management | CVLAN to CM, SIP, ASAI | AACC logs (`/opt/avaya/cclogs/`), OAM, CM SAT vectors |
| **ACCCM (Contact Center Control Manager)** | Multi-site CC management, reporting | SNMP, HTTPS, SIP | ACCCM application logs, database logs |
| **Oceana / Oceana Connect** | Omnichannel engagement platform | REST, WebSocket, SIP | Oceana snap-in logs (`/var/log/avaya/oceana/`), engagement designer logs |
| **Experience Portal (AEP)** | IVR, self-service, media server | MRCP v2, SIP, HTTP, VoiceXML | AEP logs (`/var/log/avaya/ep/`), MPP logs, VXML logs |
| **Proactive Outreach Manager (POM)** | Outbound campaign management | ASAI, SIP, REST | POM logs, campaign manager logs |
| **Voice Portal (AVP)** | Legacy IVR | SIP, MRCP, HTTP | AVP application logs, call flow logs |
| **Workforce Management (WFM)** | Agent scheduling, forecasting | REST, database | WFM application logs |
| **Call Management System (CMS)** | Real-time/historical reporting | CMS API, ODBC | CMS reports, supervisor logs |
| **AXP (Avaya Experience Platform)** | Cloud CCaaS platform | REST, SIP, WebSocket | AXP dashboard, VPMS page, SMMC logs |
| **Proactive Contact (MTC)** | Legacy outbound dialer platform | ASAI, SIP | enserver logs, dialer process logs |

---

## AXP / Experience Portal Infrastructure Notes

- VPMS (Voice Portal Management System) page inaccessible = Tomcat or license issue (per `1-20151243702`)
- SMMC (Session Manager Media Controller) connectivity loss after ACCS reboot = service dependency order (per `1-19555227082`)
- EP license expired = all calls get sysError.wav (per `1-19810768322`, `1-20057180512`)
- AXP chats abandoned from queue despite active agents = routing configuration or capacity issue (per `INC4764562`)
- MPP degraded mode = resource exhaustion, check CPU/memory and active call count (per `1-19865962552`)

---

## AACC Deployment / Upgrade Failure Patterns

- Ignition Wizard failure on Windows 2019 = check .NET framework, IIS, SQL Server prerequisites (per `1-19435632932`)
- CCMA access denied after standby AACC starts = database replication sync delay; wait or manually sync (per `1-19239977942`)
- Workspace patch error 4000013 = typically AACC OAM service or certificate issue; restart OAM and verify cert trust (per `1-19055052752`)
- Orchestration Designer cannot connect CCMA = check CCMA service, database, and network connectivity (per `1-19344117912`)
- AACC music on hold not playing after upgrade from 6.4 to 7.1 = MOH file path or format changed in new version; reconfigure MOH file path in AACC 7.1 (per `1-17197901402`)

---

## AIC (Avaya Interaction Center) Notes

AIC is a legacy agent desktop / CTI platform distinct from Workspace. Common issues:

- Agent state stuck or failed to change state = IC client connectivity to AIC server (per `1-18108389162`)
- CRM connector desync: panel display does not match agent's actual operation (per `1-18159855606`)
- AIC SDK login failure = check AIC server, SDK version compatibility, user mapping (per `1-18159038026`)
- Tsqueuestatistics service down = restart AIC services in dependency order (per `1-18295097972`)
- Email routing to wrong role (Supervisor before Agent) = AIC role assignment config (per `1-18861209222`)

---

## ACCS (Avaya Contact Center Select) / IPO Notes

- User synchronization failed on IPO server = check ACCS-IPO connectivity; status may show green but sync actually failed (per `1-18875014962`)
- License Manager not coming up after license install on Local WebLM = verify license file format, WebLM connectivity (per `1-19101968712`)
- ACCS voice quality issue after upgrade = codec or DSP configuration changed during upgrade; verify codec settings post-upgrade and check DSP resources (per `1-19480241832`)

---

## Live Transcription / AI Services

| Component | Role | Notes |
|-----------|------|-------|
| **Live Transcription** | Real-time speech-to-text for agent calls | Depends on ASR server connectivity and license. Failure shows as "transcription not working" with no specific error in Workspace (per `INC7015954`). |
| **Call Summary** | AI-generated call summary after interaction | Depends on transcription pipeline. If transcription fails, summary is also unavailable. |
| **ASR Server** | Speech recognition backend | `ACK timeout after 30 seconds` indicates network or license issue between AEP/MPP and ASR server (per `1-22666145272`). |

---

## Agent State & Login Diagnostics

### Edify Socket Service State Divergence
- **Agent Logged Out in CM But Still Visible in AACC Dashboard**: Restart `Edify Socket Server` service on AACC. Check AACC logs for `SocketServer EXCEPTION` or `Connection reset by peer`. If recurring after restart, check LDAP sync lag — AACC may cache agent state for up to 30 seconds (per `1-23156782912`).
- **AACC Agent State Stuck (Ready → Work Mode Stuck)**: Query AACC database: `SELECT * FROM Agent WHERE Status='UNKNOWN'`. Indicates agent session timed out but AACC never updated. Manual fix: agent logs out from desktop phone + Workspace, wait 2 min, re-login (per `1-23098765432`).

### Workspace ↔ AES Sync Delay
- **Agent Login Accepted in Workspace But Missing from AES**: Normal sync delay is 2–5 seconds. If >10 seconds, check network MTU size between Workspace server and AES. Search AES logs for `socket timeout` or `incomplete packet`. Set Workspace heartbeat interval to 30 seconds (default: 60) if delays exceed 15 sec (per `1-23087654321`).
- **AES Reports Agent as "Not Logged In" But Workspace Shows Ready**: Check CVLAN link status in AACC. If CVLAN down, AACC cannot confirm agent state to AES. Verify with `status cvlan-link` in CM (per `1-22945123456`).

### Agent Logged Out But Still Visible (Dashboard Caching)
- **Verification Steps**: (1) CM: `display agent <login_ID>` — should show logged-out; (2) AACC OAM: agent should show "unavailable" state; (3) Clear browser cache in Workspace and refresh (Ctrl+Shift+Delete, then reload).
- **Root Cause**: Workspace UI caches agent state for 5–10 seconds. If agent logs out but immediate re-checks show "Ready", force UI refresh. If agent still visible >30 sec after logout, check Workspace session manager logs for `SessionCache.invalidate() FAILED` (per `1-22876543210`).

### Agent Mode Toggle Stuck
- **Campaign Lock Preventing Mode Change**: Check POM campaign manager: is agent currently in inbound campaign? If yes, agent cannot toggle to outbound. Verify campaign config allows mode switching during active campaign. Restart POM Campaign Manager if toggle repeatedly fails (per `1-23134567890`).
- **Unlock Procedures**: (1) POM UI: Force-release agent from campaign via Supervisor dashboard; (2) CM: `change agent <login_ID>` → set work-mode to OFF, wait 10 sec, then change to desired mode; (3) If CM change fails, check for phantom AACC skill still assigned (per `1-23012345678`).

### Agent Concurrent Inbound + Outbound Race Condition
- **Agent Receives Inbound While Dialing Outbound**: AACC cannot distinguish if agent is in inbound-only or blended skill. Check skill configuration: blend setting in POM vs AACC must match exactly. Search AES logs for `skill state conflict` when call arrives during outbound dial. Root: POM grants inbound before AACC confirms outbound release (per `1-22998876543`).
- **Component Ordering**: CM handles trunk outbound → AACC agent state → POM skill assignment. If skill state changes before CM releases trunk, race occurs. Log signature: `ASAI route decision mismatch` or `adjunct routing timeout` in AACC logs. Fix: add 1-second guard delay between inbound release and outbound origination in campaign logic (per `1-23045234567`).

---

## Contact Center Routing

**Workflow 4: Contact Center Routing (AACC / Oceana)**

```
Step 1 — Verify CM Side
  - VDN configuration: display vdn <n>
  - Vector configuration: display vector <n>
  - Hunt group / skill configuration: display hunt-group <n>
  - Station configuration for agents: display station <ext>
  - COR/COS: verify agent can access VDN/trunk

Step 2 — Verify AACC Side
  - AACC OAM: check skill status, agent status, master
  - CM-AACC CVLAN link: check link status
  - AACC routing: verify skill-to-agent mapping
  - Agent licensing: verify available agent licenses

Step 3 — Verify Oceana Side (if applicable)
  - Oceana snap-in health: check each component status
  - Engagement Designer: verify workflow deployment
  - Channel configuration: voice/chat/email routing rules
  - Agent assignment: skill-based vs attribute-based routing

Step 4 — Trace the Call Path
  CM vector execution → VDN → ASAI adjunct route → AACC skill selection
  → Agent selection → Station alert → Answer

Step 5 — Common Issues
  - Call rings but no agent available: skill config, agent state
  - Vector stops at step: vector syntax error, adjunct timeout
  - Wrong agent selected: skill priority, agent capability mismatch
  - ASAI route failure: CVLAN link down, AACC service down
  - Call abandoned in queue: timeout, threshold settings
```

---

## Call Routing Failure Decision Tree

**Root cause diagnosis for inbound call routing failures in AACC / Oceana**

### Symptom: Inbound Call Arrives, Agent Never Receives It

**Decision Path:**
1. **Vector executes but skill is unavailable** → Call plays denial message (or silence), disconnects
   - CM: `list trace vector <N>` during test call → observe vector execution path
   - Look for `queue-to skill <skill_name> result = denial` or `unavailable` message
   - Check AACC OAM: is skill in-service? `display skill <name>` → status = active
   - **Fix:** Enable skill in AACC OAM; verify skill is assigned to agent group

2. **Vector executes, CM doesn't route to CM/AACC trunk** → Call flows to default destination (announcement, hunt group)
   - CM: `display vector <N>` → verify adjunct-routing step exists and is before final routing
   - Check SIP trunk assignment in AACC: `display sip-entity <entity>` → verify trunk is "in-service"
   - CM-AACC CVLAN link: `status cvlan-link` → must be "active" not "standby" or "down"
   - **Trace target:** Search CM logs for `adjunct route request` — if missing, vector logic doesn't reach adjunct step
   - **Fix:** Add/verify adjunct-routing step in vector; ensure skill step precedes adjunct step

3. **AACC receives route request but returns "no agents available" immediately** → Call queues indefinitely (no agent ever assigned)
   - AACC logs: search for `route decision timeout` or `no-agents-available` response
   - Check agent state: AACC OAM Dashboard → agents should show "Ready" or "Work"
   - **Root cause:** All agents in after-call-work (ACW) state OR skill assignment race condition
   - **Fix:** (1) Reduce ACW time; (2) add more agents to skill; (3) increase AACC queue timeout (default 5 min)

---

### Symptom: Call Queued But Agent Doesn't Accept

**Decision Path:**
1. **Agent in "Busy" state when call assigned** → Agent phone doesn't ring, call stays in queue
   - CM: `status agent <login_ID>` → check work-mode, call state
   - If agent shows busy on a call that should have cleared: phantom call
   - **Fix:** `busyout station <ext>` then `release station <ext>` to clear phantom busy

2. **AACC skill queue timeout (default 5 min)** → Call abandoned if no agent answers within timeout
   - AACC config: verify queue timeout setting (typically 5 min, 300 sec)
   - Check AACC logs: `call abandoned timeout` → confirm timeout fired
   - If timeout occurs <5 min, check for race: AACC rebalancing agents while call queued
   - **Trace target:** `adjunct skip count` in CM logs — if high, AACC rejecting assignments
   - **Fix:** (1) Increase AACC timeout if needed; (2) reduce agent logout/login churn; (3) verify skill distribution rebalance interval (default 30 sec)

3. **Agent receives call but doesn't answer (UI state incorrect)** → Workspace shows agent "Ready" but not ringing
   - AACC cache lag: agent state in Workspace may lag CM state by up to 10 sec
   - Check Workspace session logs: `SessionCache.invalidate() FAILED` → state update did not propagate
   - **Trace target:** AACC AES link health; if REST timeout occurs, state won't sync
   - **Fix:** Reduce Workspace heartbeat interval (default 60 sec → try 30 sec); verify AES network connectivity

---

### Symptom: Call Transfers But Drops After Transfer

**Decision Path:**
1. **CM releases original agent before new agent answers (blind transfer risk)** → Caller hears disconnect
   - Check transfer type: `display vector <N>` → look for `xfer <agent> consult` vs `xfer <agent> blind`
   - Consult transfer: agent conference required; both agents must be connected before release
   - Blind transfer: first agent released immediately; risky if second agent doesn't answer in time
   - **Trace target:** `transfer request type blind/consult` in vector trace
   - **Fix:** Use consult transfer for inbound calls. If blind transfer required, add delay: `wait <N> seconds` step before `xfer` step

2. **SDP media address changes after transfer (IP-Network-Region mismatch)** → One-way audio after transfer
   - Check IP-Network-Region settings on original trunk vs. transfer destination
   - If regions differ, media re-negotiation occurs; check for codec/address mismatch
   - **Trace target:** `satrace re-INVITE SDP` — examine c= line (connection address) in initial INVITE vs. re-INVITE
   - **Fix:** Ensure all trunks in transfer path use same IP-Network-Region; verify direct-media settings consistent

---

### Symptom: Agent Answers But Caller Hears Silence

**Decision Path:**
1. **VDN → trunk path has missing voice codec** → Media negotiation fails silently
   - Check vector `announcement` step codec: if announcement plays on different codec than trunk, mismatch occurs
   - CM: `display ip-codec-set <N>` on both VDN trunk and agent trunk → verify G.711 or G.729 in both sets
   - If VDN codec-set has G.722 but agent trunk only has G.711, transcoding fails (no DSP allocated)
   - **Trace target:** `satrace` filter SDP m= line (media) → look for codec offer mismatch in 488 response
   - **Fix:** (1) Add common codec to both codec-sets; (2) verify DSP resources available for transcoding; (3) reduce codec priority mismatch

2. **Voice path has broken media stream (asymmetric routing)** → CM shows call active but RTP not flowing
   - CM: `status call-id <ID>` during active call → check media endpoint IP, RTP port
   - Verify media endpoint can reach both caller and agent (firewall rule, NAT traversal)
   - If caller NAT'd but agent local: RTP firewall may be blocking return path
   - **Trace target:** tcpdump RTP packets on agent trunk; if <2 RTP packets/sec, media stalled
   - **Fix:** (1) Verify NAT traversal enabled in SBC; (2) check firewall bidirectional RTP rules; (3) test with audio recon after call routed

---

### Symptom: Overflow / Denial Event Fires Incorrectly

**Decision Path:**
1. **Vector condition is "abandon-time > 60 sec" but fires at 30 sec** → Check wait-time setting
   - CM: `display vector <N>` → look for `wait-time=0` in vector definition
   - wait-time=0 is race condition: time counter may not start properly; minimum safe value is 1 second
   - **Verify:** `change vector <N>` → set `wait-time: 1` minimum; recompile vector
   - **Trace target:** `monitor traffic vector <N>` during high-load test → observe when abandon fires vs. expected time

2. **Gate condition in vector source evaluates incorrectly** → Denial fires when skill queue full (per FY25 case themes)
   - CM: `display vector <N>` → check `if ... then denial` logic before queue-to step
   - Common bug: `if <skill> gate full then denial` evaluated too early (before queue wait)
   - **Fix:** Restructure vector: queue-to skill first, then check gate status in re-entry logic

---

### Symptom: Load Balancer Distributes Calls Unevenly

**Decision Path:**
1. **AACC skill rebalance is async; agents log in/out faster than rebalance cycle** → Queue shows skew
   - AACC default rebalance interval: 30 seconds
   - If agent logs in/out at 20-sec intervals, next rebalance may miss availability window
   - **Trace target:** AACC logs: `skill rebalance initiated` → check timestamp; should fire every 30 sec
   - **Verify:** AACC skill distribution report: `display skill <name>` → check member distribution across agents
   - **Fix:** (1) Increase rebalance interval to 60 sec if stable; (2) reduce agent login churn by training; (3) monitor skill member list for outliers

2. **Agent state cache TTL mismatch between Workspace and AACC** → Workspace thinks agent is Ready but AACC sees Busy
   - AACC agent state cache TTL: default 10 seconds
   - Workspace heartbeat interval: default 60 seconds
   - If Workspace updates faster than AACC cache, skew occurs
   - **Trace target:** AACC logs: `agent state update` followed by cache timeout
   - **Fix:** Reduce Workspace heartbeat (30 sec) OR increase AACC cache TTL (20 sec) to sync better

---

---

## AEP / IVR / VoiceXML

**Workflow 9: AEP / IVR / VoiceXML Troubleshooting**

```
Step 1 — Identify the IVR Call Flow
  - Which AEP application is executing?
  - What is the entry point (VDN → AEP, direct SIP to AEP)?
  - What is the expected call path through the IVR?

Step 2 — Collect AEP Logs
  - MPP (Media Processing Platform) logs: call handling, media
  - VXML logs: VoiceXML execution, grammar results
  - EP Manager logs: application deployment, configuration
  - SIP trace at AEP: call signaling

Step 3 — Common IVR Issues
  - DTMF not recognized: grammar mismatch, RFC2833 configuration
  - ASR/TTS failure: MRCP server connection, license exhaustion
  - Database query failure: ODBC/JDBC connectivity, query timeout
  - Application not answering: SIP offer/answer failure, MPP resource
  - Call transfer failure: refer/blade, SIP re-INVITE handling

Step 4 — Trace VoiceXML Execution
  - Track form/item execution sequence
  - Verify grammar match results
  - Check ECMAScript variable values at each step
  - Validate <submit>/<data> HTTP responses
```

---

## POM Campaign / Outbound

**Workflow 18: POM Campaign / Nail-up / Outbound Troubleshooting**

```
When POM campaigns fail, nail-up calls don't connect, or outbound calls drop:

Step 1 — Identify the POM Issue
  - Agent cannot log in to POM
  - Nail-up call not received / stuck at pending
  - Outbound calls dropping
  - Monitor page blank after patch
  - Agent blending moving agents incorrectly
  - DTMF tone not heard by agent during outbound

Step 2 — Check POM Dependencies
  POM Service → EPM → CM (ASAI/SIP) → Agent Station
                 ↓
                WebLM (License)

Step 3 — Nail-up Call Issues

  Agent Not Receiving Nail-up Call (per 1-22953479082):
    1. Is agent in Ready state in POM?
    2. Check agent extension mapping in POM campaign
    3. Check CM station status for the agent
    4. Verify ASAI link between POM and CM
    5. Check nail-up call routing in CM vector

  Agent Stuck at Pending Nailup (per 1-23230152292):
    1. Check POM adaptor service (may have crashed)
    2. Verify POM can place calls via CM
    3. Check campaign configuration: are outbound numbers valid?
    4. Check trunk group availability for outbound calls
    5. Restart POM adaptor if needed

Step 4 — Outbound Call Drops
  - Check trunk group capacity
  - Verify CPN format for outbound calls
  - Check carrier response codes (SIP 503, 486)
  - Per `1-22598266902`: UOB POM outbound call drop = carrier rejection

Step 5 — POM Monitor Page Blank After EPM Patch (per 1-22931333623)
  1. Clear browser cache
  2. Verify EPM services are running post-patch
  3. Check POM adaptor connectivity to EPM
  4. Restart POM web service if needed

Step 6 — Agent Blending Issues (per 1-22690737092)
  - Agent blending moves agent to inbound unexpectedly
  - Check blending rules in POM campaign configuration
  - Verify inbound/outbound skill configuration
  - Check if AACC is also managing agent state (conflict)

Step 7 — DTMF Not Heard During Outbound (per 1-22375528763)
  - RFC2833 DTMF payload type mismatch between POM and IVR
  - Check MPP DTMF configuration
  - Verify codec negotiation includes RFC2833 support

Step 8 — Proactive Contact (Legacy MTC) / Dialer Issues
  Enserver Process Stopped (per 1-19310287072):
    1. Check enserver process on each dialer: ps aux | grep enserver
    2. Restart enserver process if stopped
    3. Check system resources (CPU, memory, disk) on dialer servers
    4. Verify dialer-to-EPM connectivity

  Campaign Stale Data (per 1-19805023222):
    1. Mobile numbers from previous campaign appearing in new campaign
    2. Verify campaign data isolation between campaigns
    3. Clear stale campaign data before starting new campaign
    4. Check dialer database for orphaned contact records

  POM Tomcat / Kafka Service Down (per 1-20078440122):
    1. Check POM Tomcat service status
    2. Check POM Kafka service status (POM embeds its own Kafka)
    3. Restart both services in order: Kafka first, then Tomcat
    4. Verify EPM connectivity after restart
```

### POM Predictive Agent Bridging Invariants (per `POM simple call flow.docx` Step ⑲)

- **POM Predictive uses SIP Replaces** — not pure AMS RTP mixing. Three concurrent SIP dialogs during bridging: A (nail-up to agent, long-lived), B (original customer leg / CCA probe, torn down after Replaces), C (post-Replaces customer leg, distinct MPP RTP port from B). The nail-up CXI session — NOT the driver session — emits the `INVITE` with `Replaces:` header. CM B2BUA then performs (a) 200 OK + BYE on MPP-facing side of Dialog B, (b) re-INVITE on PSTN-facing dialog with new SDP, (c) bridges endpoints at AMS mixer. Reference: `POM simple call flow.docx` (Zhao Jun, Aug 2026) Chapter 4 Step ⑲.
- **Verify campaign pacing before applying Predictive diagnostics**: Campaign Detail Report column "Rhythm type" = `Automatic control` means Predictive (Replaces-based). Other values may use different bridging — Progressive in particular may not use Replaces in some POM versions (verify before recommending Predictive→Progressive as workaround).
- **"Duration of the whistle" field in Campaign Detail Report is the high-precision time anchor for Phase D**: Populated only when bridging executed. The whistle timestamp falls within ~18–20 ms of the actual Replaces INVITE send on the wire (CXI plays the beep tone to the agent leg in parallel with `command.createcall`). Use whistle ± 50 ms window when searching MPP `SessionManager.log*` for `SND ^INVITE` with `Replaces:` header. If whistle is empty, Phase D did NOT execute — the failure is upstream of bridging (no Answer_Human, no agent), NOT a Replaces propagation defect.

---

## CMS Historical Report Discrepancies

**Workflow 24: CMS Historical Report Discrepancies**

```
When CMS historical reports show incorrect or missing data:

Step 1 — Define the Discrepancy
  - Identify specific report, data points, and time frame
  - Compare CMS report with CM real-time data or other sources

Step 2 — Verify CMS-CM Link
  CM: status cdr-link → should be "connected"
  If not: check network connectivity and CDR link config (change cdr-link)
  CM: display errors → look for CDR-related entries (Type: CDR)

Step 3 — Agent Trace for Data Validation
  CM: change agent <agent_id> → enable Agent Trace
  CMS: observe real-time events for the traced agent
  If real-time data correct but historical wrong → CMS data processing issue
  If real-time data also wrong → CM-side data issue

Step 4 — Cross-Reference CM Data
  CM: list history → compare agent state changes with CMS data
  CM: display alarms → look for CTI link or data collection alarms
  CMS HA: verify Admin-Sync connector between primary and secondary

Step 5 — Check CMS Internal Processes
  CMS: check ECS logs (/var/log/ecs/) for CDR processing errors
  CMS: verify data storage parameters and archiving processes
  If data corruption suspected: run reconciliation with caution (may cause data loss)
```

---

## AXP Workflow / API

**Workflow 25: AXP Workflow / API Integration Troubleshooting**

```
When AXP (Avaya Experience Platform / Infinity) omnichannel workflows or APIs fail:

Step 1 — Analyze Workflow in Visual Designer
  - Open AXP workflow designer
  - Trace customer path through decision points, routing rules, integrations
  - Use real-time monitoring to identify where interaction failed

Step 2 — Check API Integrations
  - Examine API logs within AXP: requests, responses, HTTP status codes
  - Common API errors:
    401 Unauthorized → credentials expired or OAuth token invalid
    500 Internal Server Error → external system failure
    Timeout → network or external system overloaded
  - Validate API endpoint URLs, authentication (OAuth/API Key), and credentials
  - Use Postman to test API calls bypassing AXP entirely

Step 3 — Digital Channel Diagnostics
  Web Chat: browser developer tools → check for JS errors, network failures
  Social Media: verify API keys and webhooks in both AXP and platform developer portal
  Email: check ESL workflow, SMTP relay, OAuth 2.0 cert for O365

Step 4 — Leverage AXP Analytics
  - Check unified dashboards for error rate spikes
  - Identify patterns: time-of-day, specific channel, user subset
  - Generate audit reports for compliance tracking

Step 5 — Escalation
  - Gather: workflow diagrams, API traces, logs, error screenshots
  - Escalate to Avaya specialized AXP support for core platform or AI issues
```

---

## AACC Agent Not Receiving Calls

**Workflow 26: AACC Agent Not Receiving Calls**

```
When an agent is logged in, available, correctly skilled, but not receiving calls:

Step 1 — Verify Agent State in Communication Manager
  list trace station <ext>        → observe call routing to agent during test call
  display agent <login_ID>         → check logged-in state, work mode, skills
  monitor traffic hunt-group <N>   → verify agent appears available in hunt group
  display station <ext>            → check Send All Calls, coverage path, forwarding

Step 2 — Verify Agent State in AACC
  - Supervisor Desktop: agent should show "Ready" state
  - Check skill assignment in AACC admin: correct skill, appropriate skill level
  - Look for state discrepancy between CM and AACC ("stuck" agent state)
  - Solution: agent logout from desktop and phone, wait, re-login

Step 3 — Check for Common Issues
  - Agent permissions: user must have 'Agent' role to receive calls
  - "Phantom" calls: station busy on a call that already cleared
    Fix: busyout station <ext> then release station <ext>
  - Ghost sessions: status station <ext> shows busy when agent is idle
    Fix: manual release of stuck port/session
  - Browser cache: stale cache can show incorrect agent state in UI

Step 4 — Vector Analysis
  - list trace vector <N> during test call
  - Verify queue-to skill step executes correctly
  - Check goto conditions not misdirecting the call
  - Verify adjunct routing step (if used) gets valid route from AACC
```

---

## Contact Center Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Calls stuck in queue** | Callers hear music forever, no agent assigned | All agents in after-call-work, skill misconfigured, AACC service down | Check agent states, skill assignment, AACC health |
| **Vector execution stops** | Call processes but never reaches agent | Vector step error, adjunct route timeout, ASAI link down | Review vector steps, check AES link, verify CVLAN |
| **Wrong skill assignment** | Call goes to wrong agent group | VDN-to-vector mapping, vector skill selection logic | Check VDN vector, vector step logic, skill priorities |
| **Oceana channel failure** | Chat/email not routing | Channel manager snap-in down, workflow deployment error | Check snap-in status, redeploy workflow |
| **POM agent cannot login** | Rejected at POM login | POM adaptor down, EPM unreachable | Check POM adaptor, EPM, agent mapping |
| **AXP chats abandoned** | Chats abandoned despite active agents | Routing capacity or config mismatch | Check routing config, capacity (per `INC4764562`) |
| **Oceana channel interruptibility** | Double assignments, missed chats | Channel interruptibility misconfigured | Check settings per agent group (per `1-19769345022`) |
| **WeChat messages missing** | Messages lost or not delivered | Channel adapter or network issue | Check adapter, API connectivity (per `1-20216833802`) |
| **POM completion code wrong** | Marked answered when not | PAM dialer detection settings | Check completion code mapping (per `1-17239603132`) |
| **POM makes multiple calls** | Same number dialed repeatedly | Campaign data duplicate or retry misconfigured | De-duplicate; check retry settings (per `1-19222384441`) |

---

## Historical Fault Patterns

### FY23 Patterns (AXP / AEP / Oceana / Proactive Contact)

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **AXP/EP license expired** | All calls hear sysError.wav, VPMS page inaccessible | Experience Portal license file expired | Renew EP license, restart EPM services (per `1-19810768322`, `1-20151243702`) |
| **AXP SMMC connection lost** | After ACCS reboot, no media connectivity | Service startup dependency order incorrect | Reboot in order: SMMC → ACCS → verify connectivity (per `1-19555227082`) |
| **AXP chats abandoned despite active agents** | Chats go to abandoned queue even with agents ready | Routing capacity or configuration mismatch | Check AXP routing config, channel capacity, agent skill assignment (per `INC4764562`) |
| **Oceana channel interruptibility** | Agent receives double assignments or misses chats | Channel interruptibility misconfigured in Oceana | Check channel interruptibility settings per agent group (per `1-19769345022`) |
| **WeChat messages missing** | WeChat channel messages lost or not delivered | Channel adapter crash or network issue to WeChat API | Check channel adapter health, verify WeChat API connectivity (per `1-20216833802`) |
| **Oceana generic channel offline** | Chat channel shows offline in Oceana dashboard | Channel manager snap-in health check failed | Restart channel manager snap-in, check network, verify channel config (per `1-19386080466`) |
| **Proactive Contact enserver stopped** | Dialer processes stopped on one or more dialers | Resource exhaustion or process crash | Restart enserver process, check dialer system resources (per `1-19310287072`) |
| **Campaign stale data** | Previous campaign mobile numbers captured by new campaign | Campaign data not properly isolated between campaigns | Verify campaign isolation config; clear stale campaign data (per `1-19805023222`) |
| **MPP degraded mode** | MPP enters degraded mode, limited call capacity | CPU/memory exhaustion or too many active calls | Check MPP resources, reduce active call load, restart if needed (per `1-19865962552`) |

### FY22 Thematic Patterns (AIC / Oceana)

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **AIC agent state stuck** | Agent unable to transfer calls, IC client not responding | AIC server connectivity loss or service degradation | Restart AIC services; check IC client connectivity to AIC server (per `1-18146836412`, `1-18108389162`) |
| **AIC CRM connector desync** | CRM panel display does not match agent's actual operation | CRM connector state machine out of sync with call state | Restart CRM connector; check connector version compatibility (per `1-18159855606`) |
| **AIC email routed to wrong role** | Incoming email sent to Supervisor role before Agent role | AIC role assignment priority misconfigured | Check AIC role assignment config; verify role priority for email channel (per `1-18861209222`) |
| **Oceana Context Store 403** | WSfE requests to Context Store return 403 Access Denied | Context Store ACL or certificate mismatch | Verify Context Store ACL, check cert trust between WSfE and Context Store (per `1-18530118332`) |
| **Oceana Context Store cluster down** | Context Store cluster unavailable, all context lost | Cluster node failure or split brain | Restart Context Store cluster; check node health (per `1-18095131115`) |
| **Oceana channel exclusivity failure** | Agent receives contacts from multiple channels despite exclusivity on | Channel exclusivity setting not enforced | Check channel exclusivity config in Oceana; redeploy if config was cached (per `1-18316025090`) |
| **Oceana upgrade failure** | Oceana upgrade fails mid-process | Insufficient resources, version incompatibility, or snapshot needed | Take VM snapshots before upgrade; verify resource requirements; check upgrade path (per `1-17994781082`) |

### FY21 Patterns (CMS / AACC / AEP / POM / Oceana)

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **CMS high CPU utilization alarm** | CMS server reports high CPU, reports slow | CMS database bloat, excessive report scheduling, or query performance | Optimize CMS reports, check database maintenance, reduce concurrent report load (per `1-17398090216`) |
| **CMSWEB report export garbled format** | CMS reports exported via CMSWEB are unreadable | Character encoding or format conversion issue in CMSWEB | Check CMSWEB encoding settings, browser locale, export format configuration (per `1-17747820582`) |
| **IC Poller-server failed to connect IMAP** | AIC cannot poll email server for incoming messages | IMAP server connectivity, authentication, or SSL/TLS mismatch | Verify IMAP server reachability, credentials, and TLS configuration (per `1-17739428832`) |
| **POM completion code incorrectly marked as answered** | POM marks call as "answered" when customer did not pick up | PAM dialer logic treating ringing/no-answer as answered | Check POM campaign completion code mapping; verify dialer detection settings (per `1-17239603132`) |
| **AACC music on hold not playing after upgrade** | MOH silent after AACC upgrade from 6.4 to 7.1 | MOH file path or format changed in new version | Reconfigure MOH file path in AACC 7.1; verify audio file format (per `1-17197901402`) |
| **AAEP/AXP upgrade fail** | AAEP upgrade process fails | Insufficient disk space, snapshot conflict, or version jump unsupported | Verify disk space, take pre-upgrade snapshot, follow upgrade path (per `1-17109894872`) |
| **Oceana token expired** | Oceana REST API calls fail with token expiry | OAuth token TTL too short or token refresh not working | Increase token TTL; verify token refresh mechanism in Oceana config (per `1-17438238042`) |

### FY22 Comprehensive Patterns (Oceana / WFM / AACC / CMS / EP / POM)

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Oceana WeChat timestamp mismatch** | Oceana shows different timestamp than SMH for social messages | Timezone or clock sync issue between Oceana and channel adapter | Verify NTP sync across all Oceana nodes and channel adapter servers (per `1-17926954972`) |
| **Oceana Timed ACW not effective for consult-to-service** | Timed ACW per-service does not trigger after consult transfer to service | Timed ACW config not applied for consult-to-service path | Check Oceana engagement designer workflow for consult-to-service ACW config (per `1-18875642892`) |
| **Oceana contact stuck on HDB** | Contact record stuck in ACTIVE state indefinitely | HDB (Historical Database) write failure or lock contention | Check HDB connectivity; clear stuck contact records (per `1-17816391022`) |
| **Oceana ED not cleaning up completed workflow instances** | Completed workflow instances remain active, consuming resources | Oceana Engagement Designer cleanup job not running | Restart ED cleanup job; check ED configuration for retention policy (per `1-22469350337`) |
| **WFM Pulse data not reflected, staffing adapter fails** | WFM shows no agent activity data, staffing adapter alarm | WFM staffing adapter cannot connect to data source (Analytics or AACC) | Check staffing adapter connectivity to Analytics/AACC; verify API credentials (per `1-18726856152`) |
| **WFM server stopped emailing scheduled reports** | Scheduled WFM reports not delivered via email | SMTP relay configuration or email server authentication changed | Verify SMTP relay settings in WFM; check email server auth (per `1-20410259992`) |
| **WFM password field disappeared from user management** | Password input field missing from WFM admin UI | WFM UI bug after patch or browser compatibility | Clear browser cache; try different browser; apply WFM patch (per `1-18667984032`) |
| **ACCCM upgrade failed** | ACCCM upgrade process fails mid-way | Insufficient resources or database migration failure | Verify pre-upgrade requirements; restore from snapshot if needed (per `1-18979951682`) |
| **ACCS voice quality issue after upgrade** | Voice quality degraded after IPO and ACCS upgrade | Codec or DSP configuration changed during upgrade | Verify codec settings post-upgrade; check DSP resources and IP-network-region (per `1-19480241832`) |
| **AACC CCMA SSO redirection issue** | CCMA login redirects in loop when SSO enabled | SSO/SAML configuration mismatch between CCMA and IdP | Verify SAML metadata, assertion URLs, and IdP configuration (per `1-18704921472`) |
| **AACC prompt manager fails to load** | AACC prompt management page does not load | Certificate renewal on AAMS broke prompt manager access | Re-import new cert to AAMS; restart prompt manager service (per `1-22199459912`) |
| **CCMA configuration page error "Access failed False"** | CCMA configuration page shows access error, no servers listed | CCMA database connection or admin service failure | Restart CCMA services; verify database connectivity (per `1-17973241952`) |
| **CCMA deleted user still appears** | Deleted AACC user still visible in CCMA and AAAD phonebook | AACC database not fully cleaned after user deletion | Manual database cleanup; clear AACC cache (per `1-23041764302`) |
| **Video contact unexpectedly received by agent** | Agent gets video call when expecting voice only, or while on another contact | Oceana channel multiplicity or video routing misconfiguration | Check channel multiplicity limits and video routing rules in Oceana (per `1-18262357437`, `1-18378466742`) |
| **AIC Siebel integration issue** | AIC cannot communicate with Siebel CRM | AIC↔Siebel connector configuration or connectivity failure | Verify Siebel web service endpoint; check AIC connector configuration (per `1-19172561742`) |
| **AIC ORB service failed to start** | AIC services won't start, icadmin reports ORB failure | CORBA ORB initialization failure after migration or IP change | Reconfigure ORB with correct IP/hostname; restart AIC services (per `1-22144546352`) |
| **CMS unable to install LDAP** | CMS LDAP integration installation fails | LDAP client package dependency or configuration error | Check CMS OS version compatibility; verify LDAP server connectivity (per `1-19567443342`) |
| **CMS create tenant agent group failed** | CMS multi-tenant configuration fails to create agent group | CMS tenant configuration conflict or limit reached | Verify CMS tenant limits; check for duplicate group names (per `1-18215257711`) |
| **CMS link with CM up and down** | CMS-to-CM connection flapping | Network instability or CMS process resource issue | Check network between CMS and CM; verify CMS process resources (per `1-22943592802`) |
| **EP backup not running** | EPM backup job does not execute on schedule | Backup cron job misconfigured or storage target unreachable | Verify backup schedule and storage path; check EPM cron configuration (per `1-20156773112`) |
| **EPM services cannot start** | EPM services fail to start after reboot or patch | Disk full, database corruption, or license issue | Check disk space, PostgreSQL health, and WebLM connectivity (per `1-19038422922`) |
| **AAEP Web interface not responsive** | AEP web UI loads but does not respond to clicks | Tomcat resource exhaustion or session memory leak | Restart EPM Tomcat; check Java heap usage (per `1-19733243412`) |
| **ASR doesn't work after Nuance reinstalled** | ASR fails after Nuance server reinstallation | Nuance MRCP configuration or certificate regenerated during reinstall | Reconfigure AEP MPP MRCP settings; re-import Nuance certificate (per `1-19086842832`) |
| **POM unable to load JQuery from AUX servers** | POM web interface broken, missing UI components | AUX server Tomcat serving corrupted or missing JQuery files | Restart AUX Tomcat; verify JQuery file integrity (per `1-18820961992`) |
| **POM makes multiple calls to same number** | POM dials same contact multiple times in campaign | Campaign data duplicate or dialer retry logic misconfigured | De-duplicate campaign contact list; check dialer retry settings (per `1-19222384441`) |
| **POM certificate cannot be trusted in web** | POM web page shows certificate warning | Self-signed or expired POM certificate | Renew POM certificate; import CA cert to browser trust store (per `1-19150594372`) |
| **NDLOAM service not up after switchover** | License manager service fails after EPM HA switchover | NDLOAM service not starting on secondary EPM after failover | Manually start NDLOAM service; check service dependency on secondary EPM (per `1-22144653762`) |
| **SIP INFO DTMF not recognized** | IVR does not respond to DTMF from SIP phones using SIP INFO | DTMF method mismatch (SIP INFO vs RFC2833) between phone and AEP | Configure matching DTMF method on phone and AEP (per `1-18702096522`) |

---

## Contact Center Logs

### AACC Logs

```bash
# AACC log directory
/opt/avaya/cclogs/

# Key logs
CCLogs/CC_*.log          # Core contact center processing
OAM_*.log                # OAM (Operations, Admin, Maintenance)
CVLAN_*.log              # CM-AACC CVLAN communication
Routing_*.log            # Call routing decisions
Agent_*.log              # Agent state management
```

### Oceana Logs

```bash
# Oceana snap-in logs
/var/log/avaya/oceana/

# Key components
ContextStore/             # Context store operations
ChannelManager/           # Channel routing
EngagementDesigner/       # Workflow execution
UnifiedReporting/         # Reporting data
OceanaCore/               # Core platform services
```

---

## CMS Log Collection

### Key CMS Log Paths

| Category | Path | Description |
|----------|------|-------------|
| Error Log | /usr/elog/elog | Primary error log. Monitor: tail -f |
| Process Log | /cms/env/cms_mon/proc_log | Process start/exit history |
| Query Log | /cms/db/log/qlog | Historical report queries |
| SPI Error | /cms/pbx/acd1/spi.err | ACD link status (always running) |
| SPI Log | /cms/pbx/acd1/spi.log | Protocol messages (MANUAL start/stop) |
| Translation | /cms/pbx/acd1/xln.log | Translation protocol |
| Agent | /cms/pbx/acd1/ag.log | Agent login/logout protocol |
| Link Trace | /cms/pbx/acd1/spi.lnk | Session layer trace |
| Admin | /cms/install/logdir/admin.log | cmsadm/cmssvc execution |
| Admin Changes | /cms/db/log/admin_chg.log | Client admin changes |
| Backup | /cms/maint/backup/back.log | Backup activities |
| Restore | /cms/maint/restore/rest.log | Restore activities |
| Archiver | /cms/dc/archive/arch.log | Data archive |
| CMS Debug | /opt/cmsweb/tomcat/logs/cms_debug.log | Tomcat Avaya logging |
| Catalina | /opt/cmsweb/tomcat/logs/catalina.out | Standard Tomcat |
| User Log | /opt/cmsweb/log/<username>.log | Per-user trace |
| Security | /cms/install/logdir/security/cms_sec.log | Security/LDAP errors |
| License | /cms/env/lm/license.log | WebLM status |
| OS Messages | /var/log/messages | General OS |

### Enabling CMS SPI Logging (Protocol Trace)

SPI log is NOT enabled by default (performance impact). Must manually start/stop:

```bash
# Start ALL protocol logging:
/cms/bin/spilog <acd_number> all

# Start specific flags:
/cms/bin/spilog <acd_number> err+xln+ag

# STOP when done (saves disk/CPU):
/cms/bin/spilog <acd_number> -all
```

### Enabling CMS Link Trace

```bash
/cms/bin/lnktrace <acd_number> spi on
```

### Real-Time Monitoring

```bash
tail -f /cms/pbx/acd1/spi.err     # ACD link status
tail -f /usr/elog/elog              # Error log
tail -f /var/log/messages           # OS messages
```

---

## POM Log Capture

### POM Log Collection Scripts

```bash
# POM logs
cd $POM_HOME/bin
./getpomlogs.sh --logs         # Core POM logs
# -a: Include AppServer logs
# -c: Include MPP CXI logs (if co-resident)

# EPM logs
cd /opt/Avaya/ExperiencePortal/Support/VP-Tools/
./getepmlogs.sh --ALL          # --EPM, --Apache, --MainTomcat

# MPP logs
cd /opt/Avaya/ExperiencePortal/MPP/bin/
./getmpplogs.sh --logs --transcriptions --debugfiles
```

### POM Component Log Files (in $POM_HOME/logs)

| Component | Log File | Key Content |
|-----------|----------|-------------|
| Campaign Manager | PIM_CmpMgr.log | Campaign execution, dialing logic |
| Agent Manager | PIM_AgtMgr.log | Agent ops, licensing, Pacer (FINEST = login details) |
| Campaign Director | PIM_CmpDir.log | Campaign life-cycles, data import/export |
| Web Services | PIM_WebService.log | SOAP/REST services |
| Rule Engine | PIM_RuleEngine.log | Contact evaluation |
| Dashboard | DashBoard_Supervisor.log | Supervisor real-time monitoring |
| ActiveMQ | PIM_ActMQ.log | Internal messaging exceptions |
| Kafka | kafkaserver.out | Kafka runtime |
| Agent SDK | PIM_AgtSDKService.log | Workspaces interface |
| Nailer/Driver | POM_NailerDriver.log | CCXML activities ($APPSERVER_HOME/logs) |

### Change POM Log Level

```bash
$POM_HOME/bin/changeLogLevel.sh <COMPONENT> <LEVEL>
# Example: changeLogLevel.sh AGTMGR_TRACER FINEST
# Via UI: Configuration > POM Servers > POM Settings
```

### Scrub PII from POM Logs

```bash
$POM_HOME/bin/dataScrubbing.sh <path_to_logs>
```

---

## Cross-Product Integration

### CM ↔ AACC

```
Protocol:    CVLAN (Client Vector LAN) over TCP
             ASAI for adjunct routing

Data Flow:
  CM VDN → Vector step → Adjunct Route Request → AACC
  AACC → Skill/Agent Selection → ASAI Route → CM → Agent Station

Key Fields:
  VDN, Vector, Skill, Agent ID, Work Mode

Common Issues:
  - CVLAN link failure: AACC cannot receive route requests
  - Agent stuck in after-call: work mode configuration
  - Vector timeout: AACC response too slow, CM vector times out
```

### AES ↔ Oceana

```
Protocol:    REST API over HTTPS (for context)
             JTAPI/CSTA (for call control)

Data Flow:
  CM Call Event → AES CSTA → Oceana Context Manager
  Oceana → Engagement Designer → Routing Decision → AES → CM

Common Issues:
  - REST timeout: Oceana snap-in overloaded
  - Context loss: Context store replication failure
  - Routing failure: Workflow logic error, skill resolution failure
```

### CM ↔ AEP

```
Protocol:    SIP for call signaling
             MRCP v2 for ASR/TTS
             HTTP for VoiceXML fetch

Data Flow:
  CM → Vector → Route to VDN → AEP (SIP INVITE)
  AEP → Execute VoiceXML → Collect DTMF/ASR → Route back to CM

Common Issues:
  - AEP not answering: MPP resource, SIP negotiation failure
  - DTMF not detected: RFC2833 payload type mismatch
  - Transfer failure: SIP Refer handling, route back to CM
```

### AXP + Workspace + CRM Integration

```
Protocol:    REST API for CRM connector
             SIP for Workspace voice
             ESL for AXP email/social workflows

Data Flow:
  Customer → AXP (digital channel) → Oceana → Workspace Agent
  Workspace → CRM Connector (screen-pop) → Salesforce / third-party CRM

Common Issues:
  - CRM connector upgrade breaks embedded URL contract → screen-pop dies
    (per `1-23018817492`): revert connector if screen-pop breaks after upgrade
  - AXP ESL workflow email body >200 KB silently dropped
    (per `INC6481663`, `INC7084814`)
  - Infinity agent reply → ESL workflow → SMTP relay: if SMTP rejects,
    agent sees "sent" but customer never receives
```
