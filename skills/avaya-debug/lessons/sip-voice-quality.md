---
domain: sip-voice-quality
default_layer: L3
default_type: experience
last_reviewed: "2026-06-17"
---

# Lessons — SIP / Voice Quality

Field-captured findings for SIP signaling, one-way audio, codec negotiation, QoS, SBC, and RTP/jitter issues. Mirrors `../references/sip-voice-quality.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---
id: L-001
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23156789012"
  date: "2025-01-22"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting second carrier verification"
owner: "@hmao911"
---

## L-001 — OPTIONS Keep-Alive Timeout on Carrier Blocking

- **Symptom**: SIP trunk shows "in service" in CM, but outbound calls drop after exactly 90 seconds. Pattern repeats on all calls regardless of destination or time-of-day.
- **Evidence**: traceSM shows `OPTIONS timeout` after 3 consecutive failures (at 30 sec, 60 sec, 90 sec marks). Carrier firewall ACL only allows outbound REGISTER; inbound OPTIONS response blocked. Wireshark capture shows SIP OPTIONS sent from Session Manager but no 200 OK response returned. CM status command: `display sip-entity <entity>` shows "in service" but OPTIONS health check = FAILED.
- **Root cause**: Session Manager sends OPTIONS keep-alive every 30 sec per SIP RFC 3261. Carrier firewall blocks inbound OPTIONS (asymmetric firewall rule: allows outbound REGISTER/INVITE but not inbound OPTIONS). After 3 timeouts (90 sec), SM marks registration as failed and removes trunk from service, dropping active calls.
- **Fix**: Disable OPTIONS keep-alive on SIP Entity configuration in CM. In CM Administration: Telephony > SIP Trunks > select entity > disable "OPTIONS enable" (or set OPTIONS Interval to 0). Switch to REGISTER refresh only (default REGISTER interval 300 sec). Verify with carrier that inbound SIP REGISTER responses are allowed; if not, escalate to carrier network team to open firewall ACL.

---
id: L-002
layer: L3
type: pattern
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-04"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting 2nd case"
owner: "@hmao911"
---

## L-002 — RTP Packet Presence/Absence Is the Authoritative Diagnostic for SIP Media Issues — Not Signaling Inference

- **Symptom**: One-way audio with SIP signaling completing normally end-to-end. Tempting to start with signaling-level analysis (CSeq distribution, re-INVITE search, Replaces propagation, B2BUA state) — but these can produce misleading "smoking guns" that anchor the investigation on the wrong plane.
- **Evidence**: For SR `1-23647477802`, initial June 4 investigation found `CSeq:2 INVITE = 0` on the SBC-facing dialog and inferred a CM B2BUA defect. June 8 RTP-level pcap analysis (time-correlated by SIP-SDP port + call window) showed the real signal: `CM→SBC = 208 RTP packets, SBC→CM = 0 RTP packets`. The unidirectional RTP gap localized the failure to the media plane upstream of CM — invalidating the CM B2BUA hypothesis entirely. Three-vendor escalation chain confirmed Avaya / SBC / SIP-SP all clean; root cause was inside the SIP-SP's internal network infrastructure.
- **Root cause of diagnostic error**: Signaling-plane absence (no CSeq:2 INVITE) is consistent with multiple root causes — CM defect, SBC issue, intermediate SBC dropping the message, or simply that no re-INVITE was required in this call flow. RTP packet counters at the media boundary directly observe the actual failure plane and are not subject to inferential ambiguity.
- **Fix / workaround**: For any SIP one-way audio investigation, run RTP packet-count analysis at the customer-edge SBC boundary FIRST, before any signaling-plane analysis. Filter by `(src=customer-AMS-IP, dst=SBC-IP)` and `(src=SBC-IP, dst=customer-AMS-IP)` over the exact call time window. Zero packets in one direction = media-plane failure (carrier network, SBC, transcoder), regardless of how signaling looks. Non-zero in both = signaling-plane diagnosis warranted.

---
id: L-003
layer: L3
type: pattern
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-04"
promotion:
  status: pending
  target: null
  date: null
  note: "strong candidate for promotion to references/sip-voice-quality.md after 2nd field case"
owner: "@hmao911"
---

## L-003 — "Signaling Normal + Media Absent" Is a Defined SBC Failure Class — Three Dominant Causes

- **Symptom**: SIP call completes signaling (INVITE → 183 → 200 OK → ACK), call duration is typical, BYE arrives normally, but RTP is absent or unidirectional. No SIP-level error visible at any hop.
- **Evidence**: From SR `1-23647477802` and field experience across global SIP-trunked deployments, this symptom class almost always traces to one of three SBC media-plane failures somewhere in the path. Signaling plane and media plane are independent on every SBC — signaling can complete cleanly while media never establishes.
- **Root cause (three dominant patterns)**:
  1. **RTP latching failure on an intermediate SBC** — SBC ignores SDP `c=`/`m=` and locks the destination from the first inbound RTP packet (symmetric RTP). If forward and reverse RTP traverse different peers, the reverse direction goes into a black hole. Most common worldwide cause of SIP one-way audio.
  2. **Media-inactivity timer firing before first inbound RTP** — Carrier-grade SBCs (Oracle ACME, AudioCodes, Ribbon, Metaswitch) have configurable inactivity timers. If destination MNO is slow to start RTP (mobile setup jitter), the timer can tear down the media context while leaving signaling intact for the full call.
  3. **Transcoder / DSP pool allocation race** — At a SIP↔mobile-network gateway, signaling allocates a logical media path but the transcoder pool fails to assign a DSP under load. No transcoded audio in either direction; signaling never backs out.
- **Fix / workaround**: When engaging an SBC vendor or carrier on this symptom, ask binary diagnostic questions per cause: (a) `show media-session` state for the affected Call-IDs, (b) RTP packet counters per media interface for the call window, (c) media-inactivity timer value, (d) RTP latching mode (symmetric / auto / pinned), (e) transcoder pool utilization at call timestamps, (f) SBC-edge pcap on both ingress and egress interfaces. Any competent NOC can produce these in 30 minutes; refusal to do so is a process problem, not a technical one — escalate.

---
id: L-004
layer: L3
type: decision
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23647477802"
  date: "2026-06-17"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting 2nd field case raising the same comparison"
owner: "@hmao911"
---

## L-004 — APC (ISDN-PRI) vs POM (SIP) 0% / ~2% Incidence Asymmetry Is Structural, Not a POM Defect

- **Symptom**: Customer escalates "the old APC system never had this problem; why does POM have it?" — risk of management drawing the wrong conclusion that the SIP migration was a strategic mistake.
- **Evidence**: TDM (ISDN-PRI) is structurally immune to the three SBC media-plane failure modes documented in L-003 because it has no separate, droppable media plane — voice is a reserved DS0 timeslot established at call setup. There is no per-packet routing, no RTP latching, no media-inactivity timer, no transcoder pool race. Carrier-side anti-fraud and call-attestation systems operate on packet metadata; TDM has no packet metadata to inspect.
- **Root cause of the asymmetry**: APC's 0% comes from constraint (no IP-network surface area), not from superior reliability. POM's ~2% comes from exposure (every IP-layer decision point is a potential failure surface), not from inferior reliability. The two products operate in fundamentally different failure domains.
- **Fix / workaround / framing for the customer**:
  - APC and POM are not directly comparable on reliability metrics — the IP-network failure modes that POM is exposed to do not exist on TDM by design.
  - Every Tier-1 enterprise SIP migration globally has hit the same tuning curve in the first 6–12 months. Most reach < 0.1% after carrier-side audit completes.
  - The 2% is a tunable parameter (route pinning, trunk whitelisting, carrier engagement), not a stable equilibrium.
  - TDM is a sunset technology — NTT Group and most worldwide carriers have announced TDM end-of-service dates.
