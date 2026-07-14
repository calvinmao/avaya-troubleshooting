---
layer: L1
purpose: "Fine-grained symptom → domain mapping (fallback for ambiguous SKILL.md matches)"
last_reviewed: "2026-07-08"
related_docs:
  - "../SKILL.md"
  - "session-template.md"
---

# Symptom Catalog — Fine-Grained Triage

Use this catalog when SKILL.md's single-line trigger keywords don't
unambiguously match the customer's symptom. Each row includes:

- The **rough symptom** as customers describe it
- Whether it's **usually signaling / media / control-plane / config**
- The **primary domain(s)** to load
- The **first diagnostic move** — the single action that most rapidly
  disambiguates the layer

Rows are ordered by frequency (most-common Avaya SR symptoms first).

## Voice-call symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "One-way audio" (some or all calls) | media | `sip-voice-quality.md` | **RTP packet counts at customer-edge SBC boundary FIRST** (per L-002 sip-voice-quality). Do NOT start with signaling analysis. |
| "Calls drop after ~90 seconds" | signaling | `sip-voice-quality.md` | Check SIP Entity OPTIONS keep-alive vs carrier firewall (per L-001 sip-voice-quality). |
| "Calls not routing to right skill" | control | `contact-center.md` | Verify VDN vector step-by-step against `list trace vector <vector>`. |
| "Agent stuck in aux / can't log out" | control | `contact-center.md` | Check CM `display agent <ID>` vs AACC OAM state. Look for state divergence per L-001 contact-center. |
| "Recording duration wrong / missing" | control + config | `recording-wfo.md` | Correlate CM call duration vs ACRA recording metadata; check WebLogic GC pauses under load. |
| "Intermittent one-way audio ~2% of calls" | media (structural) | `sip-voice-quality.md`, `contact-center.md` | **Extract carrier-side c= IP from PSTN-facing 183 SDP** for bad and good calls. Correlation, not signaling, is the anchor (per L-004 sip-voice-quality). |

## Login / auth / cert symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "Users can't log in to SMGR / EPM / CMS after power event" | control-plane | `certificates-login-outage.md` | Check WebLM licensing status (first fail-open point after certificate / clock drift). |
| "Certificate expired warnings" | config | `certificates-login-outage.md` | Inventory ALL JKS stores, restart the application, clear browser cache — **all three actions** per diagnostic-principles invariant #8. |
| "Login worked yesterday, now returns 401/403" | config | `certificates-login-outage.md` | Check certificate CN vs actual hostname; verify SMGR trust chain. |

## Campaign / POM symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "POM campaign not launching calls" | control | `contact-center.md`, `orchestration-integration.md` | Verify upstream Oceana service status (POM's error masks this, per L-001 orchestration-integration). |
| "POM Predictive one-way audio on some calls" | media | `contact-center.md`, `sip-voice-quality.md` | Check "Rhythm type" in Campaign Detail Report first — Predictive vs Progressive have different diagnostic workflows (per L-002 contact-center). |
| "Phase D whistle timestamps missing in Campaign Detail Report" | control | `contact-center.md` | Phase D did NOT execute — failure is upstream of bridging, not a Replaces defect (per L-003 contact-center). |

## AES / JTAPI / CTI symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "getCalledAddress() returns null on park" | code | `aes-cti-jtapi.md` | Confirm this is spec-compliant per JTAPI Javadoc invariant #11; NOT a bug. Investigate application handling. |
| "UCID is all zeros in EC_PARK event" | code | `aes-cti-jtapi.md` | Verify UCID extraction path: cast to `LucentV5CallInfo` → `getUCID()`, NOT `getOriginalCallInfo().getUCID()` (invariant #3). |
| "Null address / trunk placeholder T####" | config | `aes-cti-jtapi.md` | `display system-features` — check SA9114 / SA9124 first (invariant #4). |
| "AES PostgreSQL connection pool exhausted" | infra | `aes-cti-jtapi.md`, `linux-server.md` | Check idle connection count + max_connections vs pool config; look for leaked connections in application logs. |
| "AES heap dump / CPU spike" | infra | `aes-cti-jtapi.md`, `log-collection.md` | `jstat -gcutil <pid>`; `jstack` snapshots; correlate with call load. |

## Recording / WFO symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "Recordings missing for some calls" | control | `recording-wfo.md` | Check ACRA session logs for DMCC pause/resume; correlate against CM call log. |
| "WFO Sync failure" | infra | `recording-wfo.md` | Check WebLogic RIS + DMSA services; SQL Server / Oracle JDBC connection status. |
| "Recording duration != call duration under pause/resume" | control | `recording-wfo.md` | Check GC pause histogram; correlate with pause/resume timing (per L-001 recording-wfo). |

## Log-collection / diagnostic-technique symptoms

| Rough symptom | Class | Primary domain(s) | First diagnostic move |
|---|---|---|---|
| "Need MPP SIP evidence for a POM incident but tarball is >1 hour old" | log-hygiene | `log-collection.md` | Fall back to CCXML per-slot logs — SessionManager.log has rotated (per L-001 log-collection). |
| "Need to prove Replaces INVITE was sent but SessionManager.log rotated" | evidence-substitution | `log-collection.md` | Grep CCXML slot log for `hints.sip.replaces` — equivalent evidence (per L-002 log-collection). |
| "Need SIP transaction cross-validation independent of pcap" | evidence-independence | `log-collection.md` | Extract from SM syslog stream inside the pcap (per L-003 log-collection). |

## Anti-patterns to catch during triage

| Anti-pattern | Why it's wrong | What to do instead |
|---|---|---|
| Starting SIP one-way audio investigation with CSeq / re-INVITE / B2BUA hypothesis | Signaling absence is inferentially ambiguous; misled SR 1-23647477802 for 4 days | RTP counters at SBC boundary FIRST (per L-002 sip-voice-quality) |
| Accepting customer's fault-analysis diagram as ground truth | Customer diagrams may reflect their model, not the failing call's evidence | Verify the specific mechanism cited against actual logs (per L-001 diagnostic-principles) |
| "This is probably a POM defect because APC never had this" | TDM is structurally immune to SBC media-plane failures; APC/POM operate in different failure domains | Frame the asymmetry as structural, not defect-based (per L-004 sip-voice-quality) |
| "Restart SM and see if it fixes itself" | Wastes the evidence window; SM logs may rotate during the restart | Capture logs FIRST, form a hypothesis, then restart if warranted |

## When this catalog doesn't cover the symptom

Fall back to SKILL.md's coarse-grained trigger table. If SKILL.md also
doesn't match, load `references/diagnostic-principles.md` (always available)
and reason from the 16 invariants. Add a new row to this catalog via
`/avaya-learn` at SR closure if the symptom recurs.
