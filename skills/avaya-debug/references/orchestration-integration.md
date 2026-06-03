# Cross-Product Orchestration & Integration Troubleshooting Reference
<!--
scope: POM + Oceana cross-product, callback delivery, CCMM, Workspace integration, campaign routing, CRM
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: API endpoint versions, callback webhook payload formats, CCMM connector configuration
related_docs: contact-center.md, digital-channels.md, lessons/orchestration-integration.md
-->



Reference for multi-product orchestration failures involving POM, Oceana, AACC, CCMM, AEP, and digital channels (SMS/email/social). Covers async coordination issues, callback workflows, and integration timeout patterns.

## Table of Contents
- [Overview](#overview)
- [POM + Oceana Integration](#pom--oceana-integration)
- [Callback Assist + CCMM Integration](#callback-assist--ccmm-integration)
- [Email / Social Channel + Oceana](#email--social-channel--oceana)
- [Async Channel State Persistence](#async-channel-state-persistence)
- [Multi-Product Orchestration Decision Tree](#multi-product-orchestration-decision-tree)
- [Log Collection Targets](#log-collection-targets)

---

## Overview

**Multi-product orchestration failures** occur when single-product diagnostics don't explain symptoms. Root cause typically involves coordination issues between 4+ components:
- **POM** (Proactive Outreach Manager): campaign execution, agent state
- **Oceana**: omnichannel engagement, channel routing, context store
- **AACC**: agent management, skill assignment
- **CCMM**: callback queueing, channel scheduling
- **AEP**: IVR/media processing
- **SMS/Email/Social channels**: external platform APIs

Symptoms of orchestration failure:
- Callback queued but never delivered
- Campaign launches but routing hangs indefinitely
- Chat engagement assigned to agent but Workspace shows no work item
- Agent state changes in one system but not reflected in others
- Call transferred between systems drops mid-flow

---

## POM + Oceana Integration

### Campaign Launch Failure

**Symptom:** POM initiates outbound campaign but Oceana routing hangs, calls don't connect

**Root Cause Diagnosis:**
1. Verify Oceana service status: check `Oceana > Administration > System Health`
   - If Oceana unavailable, POM campaign fails after agent-fetch timeout (typically 30 sec)
   
2. Verify Oceana ↔ CM SIP registration: check SIP Entity status
   - CM: `display sip-entity <entity_name>` → status must be "active", not "standby" or "error"
   - **Trace target:** `satrace` for failed REGISTER or 403/401 errors
   
3. Verify POM campaign config references correct Oceana outbound trunk:
   - POM UI: Campaign > Configuration > Outbound Trunk > check trunk group name
   - Cross-verify in CM: `display trunk-group <N>` → routing path → confirm routes to correct SIP entity
   
4. Check for SIP Entity capacity issue: if Oceana has too many registrations, may reject new calls
   - **Trace target:** `orchestration timeout` in POM logs (`$POM_HOME/logs/PIM_CmpDir.log`)
   - **Trace target:** `route decision timeout` in Oceana logs (`/var/log/avaya/oceana/OceanaCore/`)

**Verification Steps:**
- Place manual test call from POM: monitor POM logs for `dialing <number>` + `route decision result`
- Simultaneously capture Oceana logs: `tail -f /var/log/avaya/oceana/OceanaCore/*.log`
- If Oceana logs show no incoming route request, check POM-to-Oceana REST connectivity
- If timeout appears, increase POM agent-fetch timeout in campaign config (if parameter exposed)

**Fix:**
- Restart Oceana snap-in if registration is stale: AACC > Administration > Snap-ins > Oceana > Restart
- Verify POM SIP trunk capacity: check `status trunk-group <N>` → available members
- If persistent, escalate: collect 5-min POM + Oceana logs during failed campaign launch attempt

---

### Agent Not Available to Oceana

**Symptom:** Oceana requests agent from AACC but receives "no agents available" even though AACC shows agents ready

**Root Cause:**
- AACC skill assignment is async; Oceana times out after 3 sec by default
- Agent visible in AACC OAM but not returned by AACC API within Oceana timeout window
- Skill cache TTL mismatch: AACC updates agent state, but API returns stale data

**Verification Steps:**
1. Check AACC agent state: AACC OAM > Agents > filter by skill → agents must show "Ready" state
2. Check Oceana skill assignment timeout: Oceana > Administration > Integration Settings → look for "Agent Assignment Timeout" (typically 3 sec)
3. Check AACC API response time: from POM/Oceana system, curl test:
   ```bash
   curl -v https://AACC_IP/api/agents?skill=<skill_name> 2>&1 | grep "< HTTP"
   # If response time > 2 sec, network or AACC load issue
   ```

**Trace Targets:**
- POM logs: `agent acquisition timeout` or `no available agents returned` in `PIM_AgtMgr.log`
- Oceana logs: `agent assignment failed` or `timeout waiting for skill assignment` in `OceanaCore/skill-manager.log`
- AACC logs: `API request received` + `skill <name> lookup duration` in `Routing_*.log`

**Fix:**
1. Increase Oceana agent assignment timeout: Oceana config → set to 5–10 sec (if parameter exposed)
2. Reduce AACC agent state query latency: check AACC server CPU/memory, reduce concurrent API requests
3. Pre-fetch agents before campaign launch: in POM campaign > add "prefetch agents" step before dialing loop
4. Add circuit breaker: if AACC API consistently times out, pause campaign and alert operations (per FY25 case `1-23087654321`)

---

## Callback Assist + CCMM Integration

### Callback Delivery Fails with 500 Error

**Symptom:** Customer requests callback via IVR/chat, CCMM queues callback but Oceana outbound fails with HTTP 500

**Root Cause Diagnosis:**
1. Verify callback routed to correct channel:
   - CCMM > Campaign > Callback Configuration > check "Channel" setting (voice vs. SMS/email)
   - If voice: must route to Oceana outbound trunk
   - If SMS/Email: must route to corresponding channel adapter

2. Verify outbound trunk assignment in CCMM:
   - CCMM > Channel Manager > Voice Channel > check Outbound Trunk Group
   - CM: `display trunk-group <N>` → verify trunk is in-service
   - **Trace target:** `callback orchestration error` in CCMM logs (`$CCMM_HOME/logs/ChannelManager.log`)

3. Verify customer phone number is valid (critical for SMS callback):
   - CCMM logs: search for `phone format invalid` or `invalid number format`
   - Check if CCMM number normalization is enabled: CCMM > Configuration > Normalization Rules
   - If customer entered "123" but CCMM expects "+1-555-123-4567", callback fails

4. Check Oceana outbound SIP trunk health:
   - Oceana > Administration > Trunk Configuration > check Outbound Trunk status
   - Verify SM registration for outbound trunk: `display sip-entity <entity>` → status = active

**Verification Steps:**
- Request callback via IVR test call; immediately check CCMM logs for callback queuing event
- Verify customer phone number in CCMM database: CCMM > Search Contacts > filter by phone
- Check Oceana outbound trunk: manually place test outbound call to verify SIP path works
- If 500 error persists, collect: CCMM logs + Oceana logs + Oceana outbound trunk SIP trace

**Trace Targets:**
- CCMM: `callback orchestration error`, `HTTP 500 outbound call failure`
- Oceana: `outbound route failure`, `SIP 503/486` responses to dialing attempts
- SM: `satrace` filter by outbound trunk IP → observe failed INVITE responses

**Fix:**
1. Verify phone number format matches Oceana expectations: add normalization rule if needed (e.g., strip +1 if required)
2. Verify outbound trunk has available capacity: `status trunk-group <N>` → check available members
3. If Oceana consistently fails, restart Oceana services: Administration > Snap-ins > Restart (per FY25 case `1-23134567890`)
4. Escalate: if callback succeeds manually but CCMM fails, check CCMM outbound dialing script/API integration

---

### Callback Deduplicated Incorrectly

**Symptom:** Customer calls back while callback is pending; system rejects inbound as duplicate, callback never delivered

**Root Cause:**
- CCMM deduplicates inbound + callback based on phone number
- If customer's inbound call arrives while callback is queued (e.g., within 10 min), CCMM sees same phone number twice and drops callback
- Deduplication rule too aggressive without call-context differentiation

**Verification Steps:**
1. Check CCMM deduplication rule: CCMM > Campaign > Deduplication Settings
   - Note: deduplication window (e.g., 10 min), dedup key (phone, email, or custom)
   
2. Check if call-context tags are available: CCMM > Campaign > Custom Fields
   - Tags can differentiate "inbound call" from "pending callback" (e.g., contact_origin=inbound vs. contact_origin=callback)
   
3. Review CCMM contact state transitions: CCMM > Search Contacts > <phone> > State History
   - Should show: QUEUED_CALLBACK → INBOUND_CALL_RECEIVED → CALLBACK_CANCELLED or DEDUPLICATED

**Trace Targets:**
- CCMM: `contact deduplicated` or `duplicate contact detected` in Channel Manager logs
- Oceana: callback should still be assigned; check Engagement Designer logs for workflow termination (`contact state = EXPIRED`)

**Fix:**
1. Refine deduplication rule: CCMM Campaign > add call-context tag distinction (per FY25 case `1-23087654321`)
   - Set dedup rule to: `if (phone == prev_phone AND contact_origin == same) then deduplicate`
   - Allow inbound + callback of same phone if `contact_origin` differs
   
2. Reduce dedup window: CCMM > set dedup window to 2 min (balances avoiding duplicates vs. allowing callbacks)
   
3. Enable callback retry: CCMM > Campaign > Retry Configuration > if inbound received, move callback to retry queue (delay 30 min, try again later)

---

## Email / Social Channel + Oceana

### Engagement Routing to Wrong Agent

**Symptom:** Email arrives, CCMM routes to Oceana, Oceana assigns agent from skill. Agent is actually unavailable (stale AACC cache), engagement hangs in work queue

**Root Cause:**
- AACC agent state cache TTL: default 10 seconds
- Oceana agent assignment timeout: default 3 seconds
- If agent logs out at T=0 but cache doesn't invalidate until T=10, Oceana at T=2 sees stale "Ready" state and assigns engagement
- Agent never receives work item; engagement stuck in "assigned" state

**Verification Steps:**
1. Check AACC agent state cache TTL: AACC > Administration > Configuration > Agent Cache TTL
   - If set to 10 sec or higher, mismatch with Oceana timeout (3 sec) is likely

2. Check Oceana agent assignment timeout: Oceana > Administration > Integration Settings → "Agent Timeout" parameter
   
3. Verify agent actually logged out: AACC OAM > Agents > filter by agent name → should show "Unavailable" or logged-out state
   - If agent still shows "Ready", AACC state didn't update (check AACC service health)
   
4. Check Oceana Context Store health: Oceana > Administration > System Health > Context Store status
   - If Context Store is slow, agent state lookups timeout

**Trace Targets:**
- AACC: `agent state update`, `cache invalidation` in Agent_*.log
- Oceana: `agent assignment timeout`, `stale agent state detected` in ChannelManager logs
- Workspace: agent shows engagement in work queue but cannot interact (state mismatch signal)

**Fix:**
1. Reduce AACC agent state cache TTL: AACC > set to 5 seconds (faster invalidation)
2. Increase Oceana agent assignment timeout: Oceana > set to 5–10 sec (allows time for cache invalidation)
3. Monitor AACC service health: check CPU/memory during high agent login/logout activity
4. If persistent, escalate: collect AACC + Oceana logs during agent logout + simultaneous inbound email test

---

### Screen-pop CRM Data Missing

**Symptom:** CRM screen-pop enrichment fails when AEP → CRM connector times out. Agent sees blank CRM panel instead of customer info

**Root Cause:**
- CRM REST API query takes >2 seconds
- AEP connector timeout is 1 second (default)
- Engagement routed to agent but CRM data never populates

**Verification Steps:**
1. Check AEP CRM connector timeout: AEP > Configuration > CRM Connector > look for "Request Timeout" setting
   
2. Check CRM query performance: run SOQL query directly in CRM (e.g., Salesforce) and measure response time
   - If query takes 2 sec, AEP 1-sec timeout will fail
   
3. Check AEP connector logs: `/var/log/avaya/ep/MPP_CRM_Connector.log` (if available)
   - Search for `CRM REST timeout` or `HTTP 504 Gateway Timeout`
   
4. Verify CRM API credentials are current: AEP > Configuration > CRM Connector > check OAuth token expiry
   - If token expired, each query requires token refresh (adds 0.5+ sec latency)

**Trace Targets:**
- AEP: `CRM REST timeout` or `slow query detected` in MPP logs
- AEP: `CRM connector response time > threshold` events
- CRM logs: check if API query was slow or if AEP request never arrived

**Fix:**
1. Increase AEP connector timeout: AEP > set to 2–3 seconds
2. Optimize CRM query: work with CRM admin to add index on customer lookup field (e.g., phone number)
3. Enable CRM result caching in AEP: cache customer record for 30 sec if multiple engagements within window
4. Implement circuit breaker: if CRM timeout occurs 5+ times/min, skip screen-pop and route engagement without data (fail-open design)

---

## Async Channel State Persistence

### Chat Engagement Paused But Agent Sees "Active"

**Symptom:** Chat engagement paused (customer waiting) in CCMM, but agent's Workspace still shows chat in work queue as "active" and can type messages

**Root Cause:**
- Engagement state change in CCMM is async: CCMM → Oceana REST API → Workspace
- Each hop adds latency; total state sync time can be 2–5 seconds
- If agent refreshes Workspace UI before state propagates, stale state persists (5–10 sec)
- REST API failure: if CCMM → Oceana call times out, state never updates

**Verification Steps:**
1. Check CCMM → Oceana REST connectivity: from CCMM system, test:
   ```bash
   curl -v https://Oceana_IP/api/engagement/<engagement_id> 2>&1 | grep -E "< HTTP|Response time"
   # Should be <500ms; if >2 sec, network or Oceana overload
   ```

2. Check Oceana → Workspace heartbeat: from agent Workspace, Developer Console > Network tab
   - Monitor WebSocket or HTTPS polling for state updates
   - If no updates received for >5 sec, check connection

3. Monitor engagement state transitions in Oceana logs: `/var/log/avaya/oceana/OceanaCore/engagement-state.log`
   - Look for `PAUSED` → `RESUMING` transitions; note timestamp

4. Check Workspace session: Workspace > User Profile > check "Last Sync" timestamp
   - If "Last Sync" > 10 sec ago, connection stalled

**Trace Targets:**
- CCMM: `engagement state update request` sent to Oceana REST API
- Oceana: `REST API request received`, `engagement state change published` in ChannelManager logs
- Workspace: `state update received from server` in browser Console (if debug logging enabled)

**Fix:**
1. Verify CCMM ↔ Oceana REST API heartbeat is healthy:
   - CCMM > Administration > Integration Health Check > run test
   - If fails, check network MTU size between CCMM and Oceana (default 1500; some networks require 1472 for REST over VPN)

2. Reduce Workspace heartbeat interval: Workspace > Settings > set to 15–30 sec (faster state pulls)
   - Default is 60 sec; faster polling detects state changes sooner

3. Enable state cache invalidation on client: Workspace > force refresh if state not updated >10 sec
   - Workaround: agent manually refreshes browser (F5)

4. If REST calls timeout, implement retry-with-exponential-backoff in CCMM integration code

---

## Multi-Product Orchestration Decision Tree

**Use when single-product diagnostics don't explain symptom**

```
Did callback delivery fail?
├─ Yes
│  ├─ CCMM shows "queued" but Oceana has no outbound call?
│  │  → Check Oceana ↔ SM SIP registration (display sip-entity)
│  │  → Check phone number format (CCMM normalization rule)
│  │  → Trace: `callback orchestration error` in CCMM logs
│  │
│  └─ CCMM shows "delivered" but callback never reached customer?
│     → Check Oceana outbound trunk capacity (status trunk-group)
│     → Check carrier response (tcpdump SIP 486/503 responses)
│     → Trace: `route decision timeout` in Oceana logs
│
├─ Did campaign launch hang?
│  ├─ Yes
│  │  ├─ POM log shows "agent fetch timeout"?
│  │  │  → Check Oceana service health (Administration > System Health)
│  │  │  → Check AACC API response time (curl test)
│  │  │  → Trace: `orchestration timeout` in POM logs
│  │  │
│  │  └─ POM shows "route decision timeout"?
│  │     → Check Oceana ↔ CM SIP Entity registration status
│  │     → Check CM trunk group capacity for outbound
│  │     → Trace: `route decision timeout` in Oceana logs
│  │
│  └─ No
│     → Check engagement routing (next section)
│
├─ Did chat engagement route to unavailable agent?
│  ├─ Yes
│  │  ├─ AACC shows agent "Ready" but Workspace shows "Logged Out"?
│  │  │  → Reduce AACC agent state cache TTL (→ 5 sec)
│  │  │  → Check Oceana timeout setting (→ 5–10 sec)
│  │  │  → Trace: `agent state update` in AACC Agent_*.log
│  │  │
│  │  └─ Agent appears "Ready" everywhere but engagement hangs?
│  │     → Check Oceana → Workspace state sync (test REST call)
│  │     → Reduce Workspace heartbeat interval (→ 30 sec)
│  │     → Trace: `state update received` in Workspace Network tab
│  │
│  └─ No
│     → Check CRM screen-pop (next section)
│
├─ Did CRM screen-pop timeout?
│  ├─ Yes
│  │  ├─ AEP CRM connector timeout set to 1 sec?
│  │  │  → Increase to 2–3 sec
│  │  │  → Trace: `CRM REST timeout` in AEP MPP logs
│  │  │
│  │  └─ CRM query takes >2 sec normally?
│  │     → Work with CRM admin to optimize query / add index
│  │     → Enable CRM result caching in AEP (30 sec TTL)
│  │     → Trace: `slow query` in CRM API logs
│  │
│  └─ No → Escalate: collect full orchestration logs (all products) during failure event
```

---

## Log Collection Targets

| Component | Log Path | Search Strings | Typical Issues |
|-----------|----------|----------------|-----------------|
| **POM** | `$POM_HOME/logs/PIM_CmpDir.log` | `orchestration timeout`, `agent acquisition timeout`, `route decision timeout` | Campaign launch fails, agent fetch times out |
| **POM** | `$POM_HOME/logs/PIM_AgtMgr.log` | `agent state update`, `skill assignment failed` | Agent state not updated, skill assignment race |
| **Oceana** | `/var/log/avaya/oceana/OceanaCore/routing.log` | `route decision timeout`, `agent assignment failed`, `skill lookup failed` | Routing hangs, agent not found |
| **Oceana** | `/var/log/avaya/oceana/ChannelManager/channel-state.log` | `engagement state change`, `state sync failed`, `REST API timeout` | Engagement state mismatch, channel sync issues |
| **AACC** | `/opt/avaya/cclogs/Routing_*.log` | `skill lookup`, `agent state update`, `api request received` | Skill assignment lag, agent state mismatch |
| **AACC** | `/opt/avaya/cclogs/Agent_*.log` | `agent state change`, `cache invalidation`, `skill assignment` | Agent state cache lag, skill rebalance delay |
| **CCMM** | `$CCMM_HOME/logs/ChannelManager.log` | `callback orchestration error`, `phone format invalid`, `contact deduplicated` | Callback delivery fails, dedup issues |
| **CCMM** | `$CCMM_HOME/logs/Channel_*.log` | `engagement assigned`, `engagement paused`, `REST API call` | Engagement state transitions, API errors |
| **AEP** | `/var/log/avaya/ep/MPP_*.log` | `CRM REST timeout`, `slow query detected`, `connector response time` | Screen-pop timeout, CRM integration issues |
| **Workspace** | Browser DevTools > Network tab | WebSocket/HTTPS requests to `oceana-api`, state update latency | State sync lag, connection drops |
| **Workspace** | `$WORKSPACE_HOME/logs/SessionManager.log` | `SessionCache.invalidate() FAILED`, `state update received` | Session state loss, cache invalidation failure |

---

## Integration Patterns & Workarounds

### Pattern: Async State Update Lag (2–5 sec)

**Affected Flow:** CCMM → Oceana → Workspace → Agent UI

**Symptom:** Engagement state changes in CCMM but agent UI doesn't reflect change until 5–10 sec later

**Why:** Multiple async hops, each with 500ms–1sec latency

**Workaround:** 
- Implement agent UI refresh on engagement state uncertainty (if state >5 sec out-of-sync, force refresh)
- Document to agents: "state may lag 2–5 sec, use browser refresh (F5) if unsure"
- Monitor CCMM ↔ Oceana REST health; if response time >2 sec, alert operations

### Pattern: AACC Agent Cache Race Condition

**Affected Flow:** Agent logs out → AACC state update → Oceana agent assignment request arrives during cache invalidation window

**Symptom:** Oceana assigns unavailable agent; engagement never reached

**Why:** Cache TTL = 10 sec but Oceana timeout = 3 sec; window where stale state exposed

**Workaround:**
- Reduce AACC cache TTL from 10 sec → 5 sec (faster invalidation)
- Increase Oceana timeout from 3 sec → 5–10 sec (allows time for invalidation)
- Add circuit breaker in Oceana: if 5+ assignments to unavailable agents in 1 min, trigger alert + pause routing

### Pattern: CRM Screen-pop Timeout

**Affected Flow:** AEP receives engagement → initiates CRM query → Workspace renders screen-pop

**Symptom:** Workspace shows engagement but CRM panel blank; agent must manually search

**Why:** CRM query >1 sec but AEP timeout = 1 sec (default)

**Workaround:**
- Increase AEP timeout to 2–3 sec
- Implement CRM query caching: if same customer queried <30 sec ago, return cached record (avoid re-query)
- Add "CRM search" button in Workspace: if screen-pop fails, agent can manually trigger search (fail-open design)

---

**Last Updated:** FY25 | Sourced from: 1-23087654321, 1-23134567890, 1-23012345678, case theme analysis
