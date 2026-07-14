---
domain: contact-center
default_layer: L3
default_type: experience
last_reviewed: "2026-06-17"
---

# Lessons — Contact Center (AACC / Oceana / POM / CMS)

Field-captured findings for contact-center routing, agents, vectors, campaigns, and reporting. Mirrors `../references/contact-center.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---
id: L-001
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23156782912"
  date: "2025-01-18"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting verification on second customer site"
owner: "@hmao911"
---

## L-001 — Edify Socket Service State Divergence on LDAP Sync Lag

- **Symptom**: Agent logged out from CM, but visible in AACC OAM "Ready" state for 25 seconds. Other agents see the phantom agent in skill queue, cause routing delays and skill misalignment.
- **Evidence**: CM `display agent <ID>` shows logged-out. AACC logs show `SocketServer EXCEPTION: Connection reset by peer` at 10:23:45 during LDAP sync. Agent state in AACC database query shows "UNKNOWN" status instead of "Offline". LDAP access log shows ldap_sync operation took 42 seconds (threshold default: 30 sec). Phantom agent visible in supervisor dashboard for 25 sec, then transitions to Offline.
- **Root cause**: Edify Socket Service cached agent state during LDAP sync lag. When LDAP took >30 sec to confirm logout, AACC served stale agent state from cache. Socket connection error caused state to remain hung until cache timeout (25 sec) or manual refresh.
- **Fix**: (1) Restart Edify Socket Server service on AACC: `systemctl restart avaya-edify-socket-service`. (2) Reduce LDAP sync timeout from default 30 sec to 5 sec in AACC config (check AACC Administration > Directory Services > LDAP > Sync Timeout). (3) Monitor LDAP server latency; escalate to Directory Services team if consistent >5 sec.

---
id: L-002
layer: L3
type: pattern
maturity: verified
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-04"
promotion:
  status: promoted
  target: "references/contact-center.md#pom-predictive-agent-bridging-invariants"
  date: "2026-06-04"
owner: "@hmao911"
---

## L-002 — POM Predictive Agent Bridging Mechanism Is SIP Replaces, Not Pure AMS Mixing

- **Symptom**: POM Predictive one-way audio cases analyzed under wrong architectural model (assumed AMS-only RTP mixing) lead to misdirected root-cause hypotheses and wasted customer data-collection cycles.
- **Evidence**: `POM simple call flow.docx` (Zhao Jun, Aug 2026) Chapter 4 Step ⑲ explicitly: "Use same CXI agent nail-up call session to initiate a new SIP INVITE with Replace header to replace the previous call leg to customer." Confirmed in MPP `SessionManager.log.6` at 2026-06-01 10:11:58.314 JST for BC1: `SND ^INVITE ... Replaces: e2b0c485c45bf11d64e0011ac2b3e;from-tag=...;to-tag=...`. Three concurrent SIP dialogs exist during bridging — A (nail-up to agent), B (original customer / CCA probe), C (post-Replaces customer).
- **Root cause**: Predictive (Rhythm type = "Automatic control") uses three-dialog SIP Replaces flow. Progressive may use different mechanism — verify per POM version. Misinterpreting Predictive as Progressive-style AMS-only bridging discards SIP-plane evidence chain.
- **Fix / workaround**: Always check Campaign Detail Report column "Rhythm type" first. If "Automatic control" (Predictive), apply Replaces-based diagnostic workflow. Three dialogs to track: A (nail-up Call-ID), B (customer-leg Call-ID, replaced after bridging), C (new Call-ID from Replaces INVITE, MPP port distinct from B).

---
id: L-003
layer: L3
type: pattern
maturity: verified
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-04"
promotion:
  status: promoted
  target: "references/contact-center.md#pom-predictive-agent-bridging-invariants"
  date: "2026-06-04"
owner: "@hmao911"
---

## L-003 — Campaign Detail Report "Duration of the whistle" Confirms Phase D Replaces Triggered

- **Symptom**: Need high-precision time anchor to locate Replaces INVITE in MPP `SessionManager.log` (which can contain hundreds of INVITEs per minute under campaign load).
- **Evidence**: Campaign Detail Report column C74 "Duration of the whistle" and C76 "Proxy connection time" are populated only when Phase D agent-merge executed. For BC1: whistle = 10:11:58.332, proxy connection = 10:11:58.352. MPP log shows `SND ^INVITE ... Replaces:` at 10:11:58.314 — whistle is 18ms after Replaces. For BC2: whistle = 10:14:28.500, CXI `hints.sip.replaces` at 10:14:28.481 — whistle is 19ms after. Per `POM simple call flow.docx` Step ⑲: "CXI will also play a beep tone to agent call leg to notify this call merge" in parallel with Replaces INVITE.
- **Root cause**: The whistle is the in-band beep CXI plays to agent at the same moment it instructs SessionManager to emit the Replaces INVITE. Latency between CXI event and on-the-wire SIP send is consistently ~18–20ms.
- **Fix / workaround**: Use whistle timestamp ± 50ms window when searching MPP `SessionManager.log` for the matching `SND ^INVITE` with `Replaces:` header. If whistle field is empty in Campaign Report, Phase D did NOT execute — the failure is upstream of bridging (no Answer_Human, no agent available, etc.), NOT a Replaces propagation defect.

---
id: L-004
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-17"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting 2nd case to confirm carrier IP correlation generalizes; this lesson replaces an earlier rejected CM B2BUA hypothesis — see body Closure note"
owner: "@hmao911"
---

## L-004 — POM Predictive ~2% One-Way Audio Localized via Carrier IP Correlation in 183 Session Progress SDP

- **Symptom**: ~2% of POM Predictive outbound calls show customer→agent one-way audio after bridging. SIP signaling completes normally end-to-end. Intermittent on the same CM / SBC / campaign / agents — only specific calls hit it. Same site's APC (ISDN-PRI) deployment: 0% incidence.
- **Evidence**: Extract the **carrier-side `c=` IP from the PSTN-facing 183 Session Progress SDP** for each call. In the closed case, all 3 bad calls = `10.128.4.66`; control good call = `10.128.4.67`. RTP-level pcap analysis on bad call #1 (time-correlated by SIP-SDP port + call window): `CM→SBC = 208 RTP packets, SBC→CM = 0 RTP packets` — unidirectional RTP gap proven. CM/AMS, receiving no upstream RTP, sends silence/comfort noise downstream per industry-standard SBC behavior (industry best practice, not a defect). Three-vendor confirmation chain: SBC vendor (Nextgen) clean, SIP-SP (NTT Docomo) clean — both confirmed in writing. Root cause confirmed by customer (2026-06-17) as malfunction inside the SIP-SP's internal network infrastructure.
- **Root cause**: Media-plane failure inside the SIP service provider's internal network on a specific carrier IP / egress path. Signaling completes normally because the failure is in the media plane only. APC is structurally immune because TDM has no separate, droppable media plane.
- **Fix / workaround**: (1) **Immediate**: ask SIP-SP to pin the trunk to the working carrier IP, or whitelist the trunk from anti-fraud / call-attestation systems on the failing path → restores 0% incidence in days. (2) **Permanent**: SIP-SP fixes their internal network. (3) **Diagnostic-first**: never conclude "CM/AMS/MPP issue" until you have proven B5000→CM RTP packet count. Do NOT hypothesize signaling-plane defects (CM B2BUA, MPP) when the signaling completes normally — go to RTP packet counters first.
- **Closure note**: This lesson replaces an earlier rejected hypothesis ("CM B2BUA intermittent failure to propagate Replaces as re-INVITE") that was based on CSeq-distribution analysis of the same SR. The CSeq:2 INVITE absence was a real observation but a misleading anchor — the correct anchor was RTP packet counters, which directly localized the failure to the SP's media plane upstream of all customer-managed components.
