# Avaya Digital Channels Troubleshooting
<!--
scope: Email/Social channels, ESL/Infinity, CCMM, WeChat/WhatsApp/SMS, CRM connectors, screen-pop
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: Social media API versions, WeChat/WhatsApp Business API changes, ESL webhook formats
related_docs: orchestration-integration.md, lessons/digital-channels.md
-->



Reference for Email, Social, Infinity, ESL, and CRM connector failures across the Avaya digital/async stack. Pulled from `avaya-debugger.md` §1.9, §1.11, §4.10–§4.13, and §5.8.

## Channel Overview

| Channel | Customer-Facing Tech | Avaya Stack | Key Dependency |
|---------|----------------------|-------------|----------------|
| **Email** | Office 365 / Exchange | Email Manager → CCMM → ESL → Infinity | OAuth 2.0, MSGraph API, SMTP relay |
| **Web Chat** | Browser → Customer Portal | Channel Manager snap-in → Oceana | Breeze cluster, Context Store |
| **WeChat** | WeChat Open Platform API | Channel adapter → Channel Manager → Oceana | WeChat API connectivity |
| **WhatsApp** | WhatsApp Business API | Channel adapter → Channel Manager → Oceana | Meta API, vendor adapter |
| **SMS** | Carrier / SMS gateway | Channel Manager → Oceana | SMS gateway provider |
| **Social (generic)** | Twitter / FB Messenger | Channel adapter → Channel Manager → Oceana | Channel manager snap-in health |

All async channels share a common upstream pattern: **Customer → Channel Manager snap-in → Oceana Context Store → Engagement Designer → Agent Assignment → Workspace / WSfE Agent**.

If the channel manager snap-in goes down, **ALL** social channels fail simultaneously. This is the first thing to check on a multi-channel outage.

---

## Email Channel (Email Manager / MSGraph / O365)

### Architecture

```
Inbound:  O365 Mailbox → MSGraph API (OAuth 2.0) → Email Manager
        → CCMM → ESL workflow → Oceana → Agent (Workspace)

Outbound: Agent reply → Infinity → ESL workflow → SMTP relay → Customer
```

Email integration with Office 365 depends on:
- **OAuth 2.0** client cert + Azure AD app registration
- **MSGraph API** permissions on the Azure AD tenant
- **CCMM Dashboard** for email processing health (shows Software Exception on failure)
- **Display Name resolution** in TO/CC fields (failures here can wedge the inbound queue)

### Common Failure Patterns

| Symptom | Root Cause | Fix | Case |
|---------|-----------|-----|------|
| Cannot receive/send emails via O365 | OAuth 2.0 client certificate expired or misconfigured | Renew OAuth cert; verify Azure AD app registration; check MSGraph permissions | `1-19078183662` |
| Emails stuck; CCMM Dashboard Software Exception | MSGraph API error or rate limiting | Check MSGraph API health and rate limits | `1-20143799362` |
| Email stuck on TO/CC parse | Display Name resolution failure in TO/CC fields | Check Display Name resolution path in Email Manager | `1-19482992252` |
| Outbound email delayed | Mail relay DNS or relay config | Check SMTP relay, DNS, mail queue | `1-19738106922` |
| Inbound email not polled (legacy AIC) | IMAP server connectivity / auth / TLS mismatch | Verify IMAP reachability, credentials, TLS | `1-17739428832` |
| AIC email routed to Supervisor instead of Agent | AIC role assignment priority misconfigured | Fix AIC role priority for email channel | `1-18861209222` |

### Diagnostic Order
1. CCMM Dashboard — check for Software Exception state
2. OAuth 2.0 cert expiry on the Azure AD app registration
3. MSGraph API health and rate-limit headers
4. Email Manager queue depth and Display Name resolver state
5. SMTP relay reachability and DNS for outbound

---

## ESL (Email Solution Layer) Workflow

### Architecture

ESL is the email workflow engine that sits between Infinity (the agent reply path) and the SMTP mail relay. Inbound email also passes through ESL workflow rules before being routed to an agent.

### Hard Limits

| Limit | Behavior | Case |
|-------|----------|------|
| **Email body > 200 KB** | **Silently dropped** — no error, no alarm | `INC6481663`, `INC7084814` |

This is the single most-bitten ESL gotcha. If a customer reports "agent replies sometimes don't arrive", check the body size of the missing replies before chasing the SMTP layer.

### Common Failure Patterns

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Reply silently lost | Body > 200 KB ESL hard limit | Trim attachments / inline images; advise customer of limit |
| Agent sees "sent" but customer never receives | SMTP relay rejects no-auth connection | Configure authenticated SMTP; modern mail servers reject open relay |
| ESL workflow not applying signature/disposition | Workflow not deployed or wrong version | Re-deploy ESL workflow; verify against Infinity version |

---

## Infinity (Digital Agent Reply Path)

### Architecture

```
Agent clicks reply in Workspace
  → Infinity processes (digital reply path)
  → ESL applies workflow (signature, footer, disposition tags)
  → SMTP delivers to customer
```

Infinity handles reply path for both email and social workflows. Failures attributed to Infinity are **usually upstream of the mail relay** — it's rare for the relay itself to be the problem.

### Common Failure Patterns

| Symptom | Root Cause | Fix | Case |
|---------|-----------|-----|------|
| Infinity agent reply not delivered | ESL workflow or SMTP relay failure downstream | Trace at ESL → SMTP boundary; check for 200 KB cap | `INC7084814` |
| Reply not delivered, no error to agent | SMTP relay rejects no-auth; agent UI shows "sent" | Add SMTP authentication; verify relay config | `202506` SR |

---

## Social Channels (WeChat, WhatsApp, SMS)

### Channel Manager Snap-in

The Channel Manager snap-in is a Breeze-hosted component that fronts all async channel adapters. Health-check failures on the snap-in take down **every** social channel at once.

```
Protocol:    REST/WebSocket for channel management
             Oceana REST API for routing

Data Flow:
  Customer (WhatsApp/WeChat/SMS/WebChat) → Channel Manager snap-in
  → Oceana Context Store → Engagement Designer → Agent Assignment
  → Workspace / WSfE Agent
```

### Common Failure Patterns

| Symptom | Root Cause | Fix | Case |
|---------|-----------|-----|------|
| ALL social channels fail simultaneously | Channel manager snap-in down | Restart snap-in on Breeze; check health endpoint | — |
| Async messaging not routing to agent | Workflow not deployed OR snap-in down | Verify ED workflow deployed; check snap-in health | `1-22742237162` |
| Intermittent agent reply on social | Channel manager health flaky or network to social platform API | Check snap-in health and platform API connectivity | `INC7021181` |
| WeChat messages lost / not delivered | Channel adapter crash or network to WeChat API | Restart channel adapter; verify WeChat API path | `1-20216833802` |
| Generic Oceana channel offline | Channel manager snap-in health check failed | Restart snap-in; verify network and channel config | `1-19386080466` |
| Oceana WeChat timestamp mismatch with SMH | Timezone or NTP drift between Oceana and channel adapter | Verify NTP across all Oceana nodes and adapter servers | `1-17926954972` |

---

## CRM / Workspace Screen-Pop (Salesforce, etc.)

### Connector Upgrade Caveats

The CRM connector (Salesforce / Siebel / etc.) drives Workspace screen-pop via an embedded URL contract. **Connector upgrades can break this contract.** If screen-pop dies right after a connector upgrade, the canonical fix is to revert the connector and re-test before chasing other layers.

### Common Failure Patterns

| Symptom | Root Cause | Fix | Case |
|---------|-----------|-----|------|
| Screen-pop dies after connector upgrade | Connector upgrade broke embedded URL contract | Revert connector to previous version | `1-23018817492` |
| Screen-pop widget fails to trigger | Widget config or CRM connector issue | Check widget deployment, connector health, screen-pop URL | `INC3846316` |
| CRM panel state desyncs from agent op | CRM connector state machine out of sync with call state | Restart CRM connector; verify version compatibility | `1-18159855606` |
| CRM connector stuck "initiating" on consult transfer | Connector does not map consult transfer states correctly | Update CRM connector; check state machine mapping | `1-18163975468` |
| AIC ↔ Siebel cannot communicate | AIC↔Siebel connector config or connectivity failure | Verify Siebel web service endpoint; check AIC connector config | `1-19172561742` |

### Diagnostic Order
1. When did screen-pop break? Was a connector upgrade applied?
2. Browser console — is the screen-pop URL even being called?
3. Connector logs for the call ID / UCID
4. CRM-side webhook / API endpoint health

---

## Oceana Channel Routing

### Channel Interruptibility

Channel interruptibility controls whether agents can receive new interactions while on an existing one. This is per-channel, per-agent-group config in Oceana.

| Misconfiguration Effect | Symptom |
|-------------------------|---------|
| Interruptibility too permissive | Agents get double-assigned, leading to dropped/missed contacts |
| Interruptibility too restrictive | Agents miss new chats while idle on stale interactions |

**Case:** `1-19769345022` — channel interruptibility misconfigured caused both double-assignments and missed chats.

Related: **channel exclusivity** (`1-18316025090`) — agent receives contacts from multiple channels despite exclusivity on. Cause: exclusivity config not enforced; cached config requires redeploy.

Related: **channel multiplicity** (`1-18262357437`, `1-18378466742`) — agent gets video call when expecting voice only, or while on another contact. Check multiplicity limits and video routing rules.

### Async to Voice Escalation

Avaya supports escalating an async contact (chat / SMS / WhatsApp) to a voice call within Oceana — the customer stays on the same conversation thread, and a voice channel is added.

Common breakage points:
- **Channel manager snap-in** must be healthy on both legs
- **Workflow** must be deployed in Engagement Designer for the escalation path
- **Workspace** must be configured to surface the escalate-to-voice control to the agent

### Common Failure Patterns

| Symptom | Root Cause | Fix | Case |
|---------|-----------|-----|------|
| Async messaging not routing to agent | Workflow not deployed OR snap-in down | Verify ED workflow + snap-in health | `1-22742237162` |
| Oceana Context Store 403 | ACL or cert mismatch between WSfE and Context Store | Verify Context Store ACL; check cert trust | `1-18530118332` |
| Oceana Context Store cluster down | Cluster node failure or split brain | Restart cluster; check node health | `1-18095131115` |
| Oceana token expired on REST API | OAuth token TTL too short / refresh broken | Increase TTL; verify refresh mechanism | `1-17438238042` |
| Contact stuck on HDB in ACTIVE state | HDB write failure or lock contention | Check HDB connectivity; clear stuck records | `1-17816391022` |
| ED not cleaning up completed workflow instances | ED cleanup job not running | Restart ED cleanup job; check retention policy | `1-22469350337` |
| Timed ACW not effective for consult-to-service | ACW config not applied for consult-to-service path | Check ED workflow for consult-to-service ACW config | `1-18875642892` |
| Oceana upgrade fails mid-process | Insufficient resources, version incompatibility, or snapshot needed | Take snapshot pre-upgrade; verify path and resources | `1-17994781082` |

---

## Diagnostic Quick Reference

### Health Check First

```
1. Channel Manager snap-in health   → Breeze cluster admin
2. CCMM Dashboard                   → email Software Exception state
3. Oceana Context Store ACL/cluster → REST 403s, cluster split brain
4. ESL workflow deployed?           → Engagement Designer
5. SMTP relay + DNS                 → outbound email path
```

### Logs to Pull

| Component | Log Source |
|-----------|------------|
| Email Manager | CCMM logs, Email Manager service logs |
| ESL workflow | ESL service logs, workflow trace |
| Infinity | Infinity service logs (digital reply path) |
| Channel Manager | Breeze snap-in logs |
| Oceana Context Store | Context Store service logs, HDB logs |
| CRM connector | Connector service logs, browser console for embedded URL |
| MSGraph / OAuth | Azure AD sign-in logs, MSGraph rate-limit headers |

### Common Triage Questions

- Is **only one** channel failing, or **all** social channels? (All → channel manager snap-in)
- Was a **connector upgrade** applied recently? (Revert before deeper diagnosis)
- Is the email body **near 200 KB**? (ESL silent drop)
- Is the **OAuth cert** within 30 days of expiry? (Email outage incoming)
- Did **NTP** sync recently? (WeChat timestamp mismatch)

---

## Related Reference Files

- For Oceana voice routing, conference handling, and CM/AES core fault patterns → `contact-center.md`
- For login failures (Workspace activation, certificate cascade, WebLM) → `certificates-login-outage.md`
- For Analytics / Oceanalytics Kubernetes fault patterns (HDB, REF pipeline, MSTR) → `analytics-kubernetes.md`
- For vendor escalation routing (when to push to BBE / CPE / Verint / Nuance) → see `avaya-debugger.md` §1.10
