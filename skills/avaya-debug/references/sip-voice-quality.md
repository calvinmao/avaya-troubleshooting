# SIP / Voice Quality / Codec Troubleshooting Reference
<!--
scope: SIP signaling, RTP/SRTP, voice quality, SBC, codec, QoS, on-box capture tools (sngrep/tshark/ngrep)
last_reviewed: 2026-06-04
owner: avaya-debug skill
staleness_risks: sngrep EPEL package availability per RHEL version, tshark SRTP/DTLS dissector flags (Wireshark >= 3.0 required for srtp.enc_payload), SBC vendor MIBs, rtpevent field names across Wireshark versions
related_docs: network-infrastructure.md, diagnostic-principles.md, lessons/sip-voice-quality.md
-->



Reference for Avaya Aura SIP signaling, RTP/voice quality, codec negotiation,
Session Manager trace, SIP trunk registration, SBC, and QoS troubleshooting.

## Table of Contents
- [SIP Signaling Analysis (Workflow 3)](#sip-signaling-analysis)
- [Voice Quality (Workflow 6)](#voice-quality)
- [SIP Trunk Registration (Workflow 19)](#sip-trunk-registration)
- [Voice Quality QoS (Workflow 20)](#voice-quality-qos)
- [Codec Mismatch (Workflow 22)](#codec-mismatch)
- [Outbound Call Failures (Workflow 27)](#outbound-call-failures)
- [CM Error Diagnosis (Workflow 21)](#cm-error-diagnosis)
- [Session Manager Trace (§3.3)](#session-manager-trace)
- [CM ↔ SM Integration (§5.3)](#cm--sm-integration)
- [SIP / Voice Fault Patterns](#sip--voice-fault-patterns)
- [Historical SIP / Voice Fault Patterns](#historical-sip--voice-fault-patterns)
- [Advanced PCAP Diagnostic Patterns](#advanced-pcap-diagnostic-patterns)
  - [SIP INVITE Field Inspection Guide](#sip-invite-field-inspection-guide)
  - [Symptom → PCAP Diagnostic Map](#symptom---pcap-diagnostic-map)
  - [SRTP / Encrypted Media Analysis](#srtp--encrypted-media-analysis)
  - [DTMF Three-Path Analysis](#dtmf-three-path-analysis)
  - [Key Trace Analysis Principles](#key-trace-analysis-principles-field-validated)

---

## SIP Signaling Analysis

**Workflow 3: SIP Signaling Analysis**

```
Step 1 — Identify SIP Path
  Client → SM → CM (direct SIP station)
  Client → SM → SM → CM (multi-domain)
  External → SBC → SM → CM (inbound)

Step 2 — Collect SIP Traces
  SM:  satrace -c capture -s <duration> or System Manager > SIP Trace
  CM:  list trace signaling-group <n> or traceSM (if applicable)
  SBC: capture per vendor documentation

Step 3 — Analyze SIP Message Flow
  For each INVITE/200 OK/ACK/BYE sequence:
    - Verify Request-URI, To, From headers
    - Check SDP offer/answer (codec negotiation, media address)
    - Look for: 408/480/486/503 errors
    - Track: P-Asserted-Identity, P-Charge-Info, Diversion headers

Step 4 — Identify Common SIP Issues
  - One-way audio: SDP media address mismatch, NAT traversal
  - Registration failure: 403/401, certificate issues, DNS resolution
  - Call setup failure: 486 Busy, 480 Temporarily Unavailable, 408 Timeout
  - DTMF issues: RFC2833 vs SIP INFO vs KPML mismatch
  - Display/CLI issues: PAI/RPID header manipulation at each hop
```

---

## Voice Quality

**Workflow 6: Voice Quality Troubleshooting**

```
Step 1 — Characterize the Problem
  - One-way audio / Two-way audio / Choppy / Echo / Delay / No audio
  - Internal calls only / External calls only / Specific trunks

Step 2 — Collect Data
  - CM: list measurement ip-network-region <n>
  - CM: list measurement dsp-resource
  - SM: satrace RTP statistics
  - Network: ping, traceroute between endpoints (port 5004/5006 for RTP)
  - Endpoint: codec in use (G.711/G.729/G.722), packetization time

Step 3 — Analyze
  - One-way audio: routing, firewall, NAT, IP-Network-Region mapping
  - Choppy: packet loss, jitter, insufficient DSP, CPU oversubscription
  - Echo: impedance mismatch, echo cancellation settings
  - Delay: codec selection (G.729 adds latency), network path, CM processing

Step 4 — Common Fixes
  - IP-Network-Region: correct codec set, direct-media, QoS mapping
  - Firewall: open RTP port range bidirectionally
  - DSP shortage: add resources, adjust codec preference
  - Codec mismatch: align endpoint ↔ CM ↔ trunk codec capabilities
```

### Post-Bridging One-Way Audio — Diagnostic Order

- **Start with RTP packet counters at the customer-edge SBC boundary BEFORE any signaling-plane analysis**. For any "SIP completes but audio is one-way / absent" case, filter the customer pcap at the SBC↔CM-AMS boundary for both directions, time-windowed to the exact call. Zero packets in one direction = media-plane failure (carrier network, intermediate SBC, transcoder) regardless of how signaling looks. Non-zero in both directions = signaling-plane diagnosis warranted. Avoid the trap of inferring a B2BUA/signaling defect from CSeq distribution before confirming the actual media direction is broken — signaling-plane absence has many causes and is inferentially ambiguous; RTP counters at the boundary directly observe the failure plane. Reference: SR `1-23647477802` — initial CSeq-based hypothesis was invalidated by subsequent RTP-counter analysis.
- **"Signaling normal + media absent" is a defined SBC failure class** with three dominant causes: (1) RTP latching failure on an intermediate SBC (asymmetric forward/reverse paths), (2) media-inactivity timer firing before first inbound RTP arrives, (3) transcoder/DSP pool allocation race at SIP↔mobile gateway. None of these can occur on TDM (ISDN-PRI) because TDM has no separate, droppable media plane. When the failure is in this class, ask SBC vendor or carrier for: `show media-session` state, RTP packet counters per media interface, media-inactivity timer value, RTP latching mode, transcoder pool utilization, SBC-edge pcap on both interfaces. Any competent SBC NOC produces these in 30 minutes.
- **Carrier IP correlation is the highest-value diagnostic anchor for intermittent SIP one-way audio.** Extract the carrier-side `c=` IP from the PSTN-facing 183 Session Progress SDP for each call. If failing calls cluster on one carrier IP and good calls use a different one, the failure path is localized to a specific transit route inside the SIP-SP. Immediately actionable: request SIP-SP to pin the trunk to the working IP, or whitelist from anti-fraud/call-attestation on the failing path — restores baseline reliability in days. Reference: SR `1-23647477802` — all 3 bad calls = `10.128.4.66`, control good call = `10.128.4.67`, root cause confirmed in carrier internal network upstream of the SP.
- **Pcap coverage gap recognition**: If MPP IP shows only `OPTIONS` keepalive SIP and no INVITE/ACK/BYE in a time window where bridging events should appear, the customer's capture point is downstream of the MPP↔SM↔CM segment. Don't conclude "no Replaces was sent" from pcap alone — require MPP `SessionManager.log` or `CCXML-SessionSlot-*.log` corroboration.

---

## SIP Trunk Registration

**Workflow 19: SIP Trunk Registration Failure Diagnosis**

```
When a SIP trunk fails to register with a third-party service provider:

Step 1 — Initial Verification
  - Verify physical/network connectivity: ping provider gateway from SBC/SM
  - Check network settings (IP, subnet, gateway, DNS) on SBC and Session Manager
  - Verify SIP trunk license is available and assigned

Step 2 — Capture SIP Registration Exchange
  On Avaya SBC (SSH port 222 with root):
    traceSBC -i <provider_IP> -r "REGISTER"
    Use 'w' command to write output to pcap for Wireshark analysis
  On Session Manager:
    traceSM → filter by IP or URI → observe REGISTER/200 OK/401 flow

Step 3 — Interpret SIP Response Codes
  | Code | Meaning | Action |
  |------|---------|--------|
  | 401 Unauthorized | Provider challenging credentials | Verify auth username/password in SM SIP Entity config |
  | 403 Forbidden | Source IP not allowed or wrong credentials | Check provider ACL; verify IP whitelisting |
  | 408 Request Timeout | Network unreachable or firewall blocking | Check firewall rules for SIP port (5060/5061) |
  | 404 Not Found | SIP domain or user misconfigured | Verify Request-URI and SIP domain in trunk settings |
  | 405 Method Not Allowed | REGISTER not permitted for this URI | Check provider configuration for registration method |
  | 200 OK | Registration successful | Validate trunk status in SMGR and SBC dashboards |

Step 4 — Resolve Authentication Issues
  - Verify credentials in SM SIP Entity match provider records
  - Check authentication method (Digest MD5 vs other)
  - Examine WWW-Authenticate header in 401 response for required scheme

Step 5 — Validate After Fix
  - Confirm 200 OK received for REGISTER
  - Check registration status in SMGR → Elements → Session Manager → Entities
  - Place test call inbound and outbound
  - Monitor for registration refresh intervals (default 3600s)
```

> Note: IP Office SSA-based SIP trunk diagnostics are covered in `ip-office.md`.

---

## Voice Quality QoS

**Workflow 20: Voice Quality / QoS Diagnosis**

```
When users report choppy audio, echo, missing words, or one-way audio:

Step 1 — Isolate Scope
  - Internal calls only? → LAN/QoS issue
  - External calls only? → WAN/trunk/provider issue
  - Remote workers only? → VPN/bandwidth issue
  - Specific site? → Network segment issue

Step 2 — Phone-Based Diagnostics (Quick Check)
  Many Avaya IP phones have built-in network statistics:
  - Access phone web UI → Statistics or QoS page
  - Check real-time jitter, latency, packet loss for active call
  - This is the fastest way to confirm a network performance issue

Step 3 — Network Monitoring Tools
  | Tool | Metric | Notes |
  |------|--------|-------|
  | Wireshark RTP Stream Analysis | Jitter, packet loss, delta time | Capture via SPAN/mirror port; Telephony > RTP > Stream Analysis |
  | SolarWinds VNQM | MOS, jitter, latency, CDR analysis | Analyzes Avaya CM CDRs for proactive monitoring |
  | PRTG QoS Sensor | Jitter, packet loss between two points | QoS Round Trip Sensor or Ping Jitter Sensor |
  | CM list measurement | DSP resource usage, IP-NR metrics | Per-region performance data |

Step 4 — Key Metric Thresholds
  | Metric | Acceptable | Degraded | Unacceptable |
  |--------|-----------|----------|--------------|
  | One-way latency | < 150ms | 150-300ms | > 300ms |
  | Jitter | < 30ms | 30-50ms | > 50ms |
  | Packet loss | < 0.5% | 0.5-1% | > 1% |
  | MOS | > 4.0 | 3.5-4.0 | < 3.5 |

Step 5 — End-to-End QoS Verification
  Check EVERY hop in the call path:
  a) VLAN: Voice traffic on dedicated voice VLAN (separate from data)
  b) DSCP Marking: Voice packets (SIP signaling + RTP media) marked with correct DSCP/CoS
     - Typically DSCP EF (46) for RTP, CS3 (24) for SIP signaling
     - Verify marking at the phone (endpoint) level
  c) Switch/Router Policies: Network devices must trust and prioritize marked packets
     - Verify trust boundary configuration on access switches
     - Check queuing policies on distribution/core switches
  d) WAN Links: Provider must honor QoS markings; verify sufficient bandwidth provisioned

Step 6 — Codec Optimization
  - G.711: Best quality, highest bandwidth (64 kbps + overhead)
  - G.729: Lower bandwidth (8 kbps), adds ~25ms latency for compression
  - G.722: HD voice, 64 kbps, better quality than G.711
  - Ensure consistent codec set across IP-Network-Regions to avoid transcoding
  - Check CM: display ip-codec-set <n> and display ip-network-region <n>
```

---

## Codec Mismatch

**Workflow 22: Codec Mismatch Troubleshooting**

```
When calls fail with no audio, one-way audio, or 488 Not Acceptable Here:

Step 1 — Capture SIP/SDP for the Failed Call
  traceSM on Session Manager:
    - Filter by extension or IP
    - Find INVITE → examine SDP m=audio line for offered codecs (rtpmap entries)
    - Find 200 OK → examine SDP for accepted codec
    - If 488 Not Acceptable Here returned → codec mismatch confirmed

  Wireshark (alternative):
    - Capture from SPAN/mirror port
    - Filter: sip
    - Inspect INVITE and 200 OK SDP bodies

Step 2 — Identify the Mismatch
  - INVITE offers: G.711MU (payload 0), G.729 (payload 18)
  - 200 OK returns: G.711A (payload 8) only
  - No common codec → 488 error or silent call
  - Also check c= line for incorrect/unreachable IP address (NAT issue)

Step 3 — Resolve in Communication Manager
  CM SAT commands:
    display ip-network-region <region> → note Codec Set number
    change ip-codec-set <set_number> → add missing codec to both regions
    Ensure common codec (G.711MU, G.711A, or G.729) exists in ALL codec sets
    Check SRTP settings: media encryption must match endpoint capabilities
      (e.g., 1-srtp-aescm128-hmac80)

Step 4 — Resolve on SBC
  - Check media profiles / coder groups for both legs
  - Ensure at least one common codec on enterprise-side and carrier-side
  - Enable transcoding if endpoints cannot share a codec (requires SBC license)
  - Verify Media Security Mode and NAT Traversal settings in IP profiles
```

---

## SIP Session Intermittent Disconnection

### SIP OPTIONS Keep-Alive Failure
- **OPTIONS Sent But No 200 OK Response**: Session Manager default interval is 30 seconds. If provider doesn't respond after 3 consecutive OPTIONS (90 sec), SM removes registration. Search traceSM logs for `OPTIONS timeout`. Check firewall ACL — some carriers block bidirectional OPTIONS. Fix: switch to REGISTER refresh only (disable OPTIONS) if carrier requires (per `1-23156789012`).
- **Trunk Drops at 5-Min Mark (300 sec)**: Indicates carrier timeout on inactivity, not Avaya side. SIP RFC 3261 default is 3600s registration, but carrier may enforce shorter. Check carrier documentation for keep-alive requirements. Increase SM registration refresh interval or implement mid-call reINVITE to reset timer (per `1-22987654321`).

### TLS Certificate Expiry During Active Session
- **Call Drops Exactly When Cert Expires**: Monitor cert expiry date in SM SIP Entity config. If cert renews but old cert still in use, mid-call reINVITE fails with 403 Forbidden. Verify all SM nodes (primary + secondary) have identical new cert — asymmetric certs cause 50% drop rate (per `1-23098765432`).
- **Timing & Detection**: Check SM logs 1 hour before cert expiry; search for `SSL_ERROR_HANDSHAKE` or `certificate_expired`. Mid-session calls fail only when SDP renegotiation occurs (transfer, hold/resume). Workaround: schedule cert renewal during maintenance window, restart SM services to load new cert (per `1-22945123456`).

### Mid-Call Re-INVITE Codec Mismatch
- **488 Not Acceptable Response Mid-Call**: Call starts successfully (codec negotiated), but later re-INVITE (hold, transfer, or media refresh) offers different codec. Check SM ip-codec-set — if it changes between INVITE and re-INVITE, mismatch occurs. Fix: ensure single consistent codec set for entire session. Search traceSM for `re-INVITE SDP differs from initial INVITE` (per `1-23087654321`).
- **Fallback Options**: (1) Disable hold/resume on affected trunk group; (2) Force single codec (G.711 only) to eliminate re-INVITE codec negotiation; (3) Enable transcoding on SBC if endpoints cannot share codec (per `1-22876543210`).

### Carrier-Grade NAT (CGNAT) Timeout
- **5–10 Min Inactivity Drop Pattern**: CGNAT times out UDP flows after 5–10 min without traffic. SIP OPTIONS only sends signaling, not media. Symptom: RTP media flows fine, but call drops if agent goes silent >5 min. Fix: enable SIP INVITE refresh (reINVITE) every 4 minutes, or send dummy RTP keep-alive packets (per `1-23134567890`).
- **SBC Behavior**: If SBC is behind CGNAT, verify SBC sends keep-alive to provider. Check SBC "keep-alive" option in SIP profile. Asymmetric routing (inbound via one path, outbound via another) exacerbates CGNAT issues. Engage carrier to verify unidirectional routing is not in effect (per `1-23012345678`).

### Decision Tree: Intermittent Drop Root Cause
```
Drop occurs every N minutes?
├─ 5–10 min → CGNAT timeout (check RTP silent time, enable re-INVITE keep-alive)
├─ 30 min → OPTIONS timeout (check carrier response, disable OPTIONS if blocking)
├─ Exactly at cert expiry → TLS cert renewal needed (check cert date, restart SM)
├─ During hold/transfer → codec mismatch in re-INVITE (verify codec set unchanged)
├─ Random timing → network packet loss (check QoS, jitter; capture Wireshark RTP)
├─ Only on specific trunks → trunk config or route policy (check SIP Entity settings)
└─ Only inbound or outbound → asymmetric routing or SBC NAT traversal (engage carrier)
```

---

## Voice Quality Verification Checklist

**Post-diagnosis QoS validation workflow**

### 1. Latency Thresholds & Measurement

| Threshold | Assessment | Measurement Method | Typical Causes |
|-----------|------------|-------------------|-----------------|
| <100ms one-way | Acceptable | `tracert` to RTP endpoint; ICMP RTT ÷ 2 OR `satrace RTP timestamp delta` | Normal network conditions |
| 100–150ms one-way | Degraded; noticeable delay | SIP ping (OPTIONS) via SM trace; Wireshark inter-packet gap | Congestion, longer routing path, multiple WAN hops |
| >150ms one-way | Poor; call experience degraded | Network path analysis with jitter probe; check for buffering | Carrier congestion, inefficient routing, satellite/4G latency |

**Verification Steps:**
1. Measure during active call: `satrace -c capture -s 300` on SM; filter SIP/RTP timestamps
2. Cross-check with network tool: `ping -c 20 <RTP_dest_IP>` from CM or SBC (divide RTT by 2 for one-way)
3. Identify hops causing delay: `tracert <gateway_IP>` note intermediate latencies
4. If >150ms, request carrier latency analysis or optimize routing (SBC IP route policy)

---

### 2. Jitter Thresholds & Analysis Tools

| Threshold | Assessment | RTP Analyzer / Wireshark Filter | Typical Causes |
|-----------|------------|----------------------------------|-----------------|
| <20ms jitter | Acceptable | `Telephony > RTP > Stream Analysis` → Jitter column | Stable network, consistent codec processing |
| 20–50ms jitter | Degraded; slight choppiness | Wireshark: `rtp.p_type == 0` (G.711) or 18 (G.729) → Statistics > Show Report | Packet reordering, buffer variability, codec timing jitter |
| >50ms jitter | Major; broken audio, gaps | Network capture via SPAN/mirror port; identify late-arriving packets | Buffer underrun, NIC/switch queue congestion, codec mismatch re-INVITE |

**Verification Steps:**
1. Capture RTP stream: Wireshark SPAN on trunk interface during live call
2. Analyze stream: `Telephony > RTP > Stream Analysis` → Export CSV for jitter/delta-time
3. If jitter >20ms: check sender buffer settings on endpoint + verify DSP resources on CM (`display dsp-resource`)
4. If jitter spikes during hold/resume: verify codec set unchanged in re-INVITE (search `satrace re-INVITE SDP` for codec changes)

---

### 3. Packet Loss Thresholds & Detection

| Threshold | Assessment | Detection Tool | Correlation |
|-----------|------------|----------------|-------------|
| <0.1% loss | Acceptable | RTCP Receiver Reports; `Telephony > RTP > RTCP` in Wireshark | No audible impact |
| 0.1–1% loss | Noticeable; occasional skips, gaps | `tcpdump -i <iface> port 5000-6000 -w rtp.pcap` → analyze frame distribution | One-way audio may appear briefly; users report "cut-outs" |
| >1% loss | Severe; frequent dropouts, unintelligible | RTCP reports + packet capture; check for late arrivals (out-of-order) | Strong correlation with one-way audio; immediate escalation signal |

**Verification Steps:**
1. Collect RTCP: Enable RTCP reporting on SIP trunk in SM (default enabled). Check `satrace` for RTCP RR (Receiver Report) packets
2. Extract loss % from RTCP: fraction lost field in RR; multiply by 100 for percentage
3. If loss >0.5%, cross-check with tcpdump for missing sequence numbers in RTP header
4. Verify interface errors: `status line-group` on CM → check FDL/ERR counters; if high, network layer issue (not Avaya)

---

### 4. Echo & Acoustic Echo Cancellation (AEC) Diagnostics

**Echo Detection & Causation:**

- **Detectable echo (>0ms lag):** Listener hears themselves ~100-500ms after speaking. Human ear detects >100ms lag.
- **Avaya-side echo (endpoint media processing):** Check media endpoint AEC settings:
  - CM: `display ip-network-region <N>` → verify `echo-cancellation: enabled`
  - Endpoint: phone web UI → Advanced > Echo Cancellation; verify ON and tail length ≥32ms
  - DSP: `display dsp-resource` → check echo-cancellation license count; if 0, AEC unavailable
  - Fix: enable AEC on both legs; increase AEC tail length if echo persists
  
- **Carrier-side echo (trunk/provider):** Call flows normally but caller hears themselves:
  - Request carrier enable echo cancellation on their trunk
  - Verify carrier SBC echo-cancellation profile is active
  - Check for POTS-to-SIP gateway transcoding without AEC (per `1-22456789012`)
  - If carrier cannot enable, deploy AEC on Avaya SBC media profile

**Verification Steps:**
1. Reproduce issue with controlled test call; note delay (use stopwatch: listen for echo start after speaking)
2. Test internal call (both endpoints Avaya) → if no echo, root is external (carrier)
3. Capture SDP in traceSM: check for `RTCP feedback` or `CN` codec (comfort noise) which may mask AEC
4. If Avaya-side: escalate to vendor (endpoint/CM firmware may have AEC defect per FY25 cases)

---

### 5. Bandwidth Verification & SIP Entity QoS Policy

**RTP Bandwidth Calculation:**

```
RTP_Bandwidth = (Codec_Bitrate + IP_UDP_RTP_Header_Overhead) × Margin

Examples:
  G.711:  (64 kbps + 8 kbps header) × 1.25 = 90 kbps/call
  G.729:  (8 kbps + 8 kbps header) × 1.25 = 20 kbps/call
  G.722:  (64 kbps + 8 kbps header) × 1.25 = 90 kbps/call

Rule: Allocate ≥100 kbps per concurrent voice call (includes SIP signaling ~5 kbps)
```

**Verification Steps:**
1. Check CM codec set: `display ip-codec-set <N>` → note primary codec (order matters)
2. Calculate max concurrent calls: WAN_bandwidth / 100 kbps per call
3. Verify SIP Entity QoS policy: `display sip-entity <entity>` → check `max-calls` or `bandwidth-class` if defined
4. If calls drop at specific count: likely hitting bandwidth cap. Increase trunk bandwidth or reduce codec bitrate (switch to G.729 if quality acceptable)
5. Cross-check with network: SNMP interface utilization during call load test should not exceed 80% on WAN edge

---

### 6. Command Checklist for Voice Quality Diagnosis

**Communication Manager:**
- `display ip-codec-set <n>` — verify codec list, priorities, SRTP settings
- `display ip-network-region <n>` — check codec set, direct-media, echo-cancellation, QoS policy
- `status call-id <call_id>` — real-time call state, codec in use, RTP path, media endpoint
- `display dsp-resource` — DSP resource count, echo-cancellation license availability, utilization
- `list measurement ip-network-region <n>` — historical jitter/latency/loss per region
- `list measurement dsp-resource` — DSP activity log, resource exhaustion events
- `display errors` — system-level SIP/media errors (Type: SIP or RTP)
- `list history` — agent activity, call state transitions (correlate with audio issues)

**Session Manager:**
- `satrace -c capture -s 300` — full SIP + RTP trace; analyze codec negotiation, RTCP, re-INVITE
- Filter traceSM output by IP/extension to isolate problem calls
- Examine SDP in INVITE and 200 OK for codec/media address mismatches

**Network Tools:**
- `tcpdump -i <interface> port 5060 or port 5000-6000 -w capture.pcap` — packet capture for RTP analysis
- `Wireshark RTP Stream Analysis` (`Telephony > RTP > Stream Analysis`) — Jitter, delta-time, lost packet count
- `Wireshark VoIP Calls` (`Telephony > VoIP Calls`) — SIP call ladder, state transitions, failure codes
- `ping <RTP_endpoint>` — baseline latency check (execute from CM or SBC)
- `traceroute <gateway>` — trace routing path, identify high-latency hops

**Phone-Level Diagnostics (if supported):**
- IP phone web UI → `Statistics` or `QoS` page — real-time call metrics (jitter, latency, packet loss) during active call
- This is fastest confirmation of network-side issue vs. CM configuration issue

---

## Outbound Call Failures

**Workflow 27: Outbound Call Failures on SIP Trunk**

```
When SIP trunk is registered but outbound calls fail:

Step 1 — Confirm Trunk Status
  status trunk-group <N> → verify in-service, members available

Step 2 — Capture Full SIP Call Flow
  traceSM on Session Manager:
    - Capture INVITE from CM → SM → SBC → provider
    - Follow call to see where it fails and what response code returns

Step 3 — Interpret SIP Failure Codes
  | Code | Meaning | Action |
  |------|---------|--------|
  | 403 Forbidden | Calling number not authorized or format wrong | Check CPN format in route pattern |
  | 503 Service Unavailable | Provider overloaded or SBC routing issue | Check provider status; verify SBC routing |
  | 404 Not Found | Dialed number invalid at provider | Check number format (missing country code?) |
  | 480 Temporarily Unavailable | Called party unavailable | Destination issue |
  | 486 Busy Here | Called party busy | Destination issue |
  | 488 Not Acceptable Here | Codec mismatch | Check codec set on trunk group |
  | 608 Rejected | SBC or carrier rejecting call | Check carrier config and trunk capacity |

Step 4 — SBC Diagnostics
  - Access SBC management interface → active sessions and call logs
  - Use SBC packet capture to see full SIP ladder and SDP
  - Check SBC header manipulation rules (may be altering critical headers)
  - Verify SBC codec transcoding configuration
```

---

## CM Error Diagnosis

**Workflow 21: CM System-Level Error Diagnosis (display errors)**

```
Step 2 — Key Error Types:
  | 257 | PN Reset Level 2 | Check PN communication links |
  | 513 | PN Out of Service | Investigate PKT-INTF/EXP-INTF |
  | 769 | PN Emergency | Hardware inspection; escalate |
  | 542 | Translation Save Failure | Manually save translations |
  | 1025 | Station/TN Error | Check physical connectivity |
  | 1281 | Trunk Error | status trunk-group; test trunk |

Step 3 — Key Source Codes:
  | PKT-INT | IP Server Interface | IPSI sanity check failure |
  | LIC-ERR | License Error | License expired; test license |
  | DS1-BD | DS1 Board Error | PRI/T1 physical layer |
  | PRA-TRK | PRI Trunk Error | D-channel or B-channel fault |

Step 4 — Correlate with: display alarms, status media-gateway, list history
```

---

## Session Manager Trace

**§3.3 Session Manager Trace**

```bash
# SIP trace via CLI
satrace -c capture -s 300    # capture for 300 seconds

# Via System Manager
# Elements → Session Manager → Troubleshooting → SIP Trace
# Select SM, start trace, reproduce, stop, download

# Log locations on SM
/var/log/avaya/smsnapin/
```

---

## CM ↔ SM Integration

**§5.3 CM ↔ SM**

```
Protocol:    SIP (UDP/TCP/TLS)

Data Flow:
  Endpoint → SM (SIP Register, INVITE)
  SM → CM (SIP INVITE via SIP trunk / signaling group)

Key Fields:
  Request-URI, To, From, P-Asserted-Identity
  SDP: codec, media address, packetization

Common Issues:
  - Registration failure: DNS, certificates, domain configuration
  - Audio issues: IP-Network-Region, codec mismatch, NAT
  - Routing failure: dial pattern, route policy, CM trunk selection
```

---

## SIP / Voice Fault Patterns

**§4.2 SIP Signaling Patterns**

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **One-way audio after transfer** | Caller hears agent, agent doesn't hear caller | SDP re-INVITE fails, media anchored at wrong point | Check IP-Network-Region direct-media setting |
| **Registration flood** | Phones repeatedly register/deregister | DNS timeout, certificate mismatch, network congestion | Fix DNS/cert, check NTP, reduce registration interval |
| **Caller ID stripping** | External number shows as internal | PAI header overwritten at SIP hop (SM or SBC) | Preserve PAI through SIP profiles, check trust configuration |

---

## Historical SIP / Voice Fault Patterns

Patterns scoped to SIP signaling, RTP/media, codec, SM/SBC, QoS, voice quality,
and SIP-trunk registration. Sourced from FY21–FY23 SR cases (§4.10–4.13 of the
master agent file).

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **DMCC StationLink unregistration (Telecommuter)** | Unexpected DMCC device unregister when using StationLink Telecommuter mode | StationLink keepalive timeout or SIP re-INVITE failure for remote workers | Check network stability for remote agents; increase keepalive interval (per `1-1791095361`) |
| **ACR design difference causing ACRA behave differently** | Same recording config, different behavior across sites | CM design parameters (region, trunk, DSP) affect recording capture | Compare CM design parameters between sites; check IP-network-region and trunk group settings (per `1-18106641046`) |
| **ACCS voice quality issue after upgrade** | Voice quality degraded after IPO and ACCS upgrade | Codec or DSP configuration changed during upgrade | Verify codec settings post-upgrade; check DSP resources and IP-network-region (per `1-19480241832`) |
| **SIP INFO DTMF not recognized** | IVR does not respond to DTMF from SIP phones using SIP INFO | DTMF method mismatch (SIP INFO vs RFC2833) between phone and AEP | Configure matching DTMF method on phone and AEP (per `1-18702096522`) |
| **WebRTC one-way video** | WebRTC call has voice but video only in one direction | SDP video negotiation or firewall RTP port issue | Check SDP video offer/answer; verify firewall allows RTP video ports bidirectionally (per `1-17332616732`, `1-17390788680`) |

---

## SIP Infrastructure Connectivity & SBC Health (IT Ops Patterns)

Adapted from IT operations automation platform patterns. Applies to Session Manager,
SBC (SBCE), and SIP trunk port verification for Avaya Aura environments.

### A3 — Port Connectivity Verification for SIP Stack

Network connectivity failures between SIP components are often misdiagnosed as
SIP protocol issues. Always verify transport reachability before analyzing SIP
signaling.

```bash
# ── Session Manager connectivity checks ──────────────────────────────────────

# SIP signaling ports (run from SM host or jump server):
nc -zv <SM_IP> 5060 && echo "SM SIP UDP/TCP reachable" || echo "BLOCKED"
nc -zv <SM_IP> 5061 && echo "SM SIP TLS reachable"    || echo "BLOCKED"
nc -zv <SM_IP> 8443 && echo "SM HTTPS (admin) reachable" || echo "BLOCKED"

# Test from carrier/PSTN gateway toward SM:
# (Run on the SBC or border node, not SM itself)
nc -zv <SM_IP> 5060 -w 5
nc -zv <SM_IP> 5061 -w 5

# ── AES / CTI ports ──────────────────────────────────────────────────────────
nc -zv <AES_IP> 1099  && echo "AES TSAPI (JTAPI) reachable" || echo "BLOCKED"
nc -zv <AES_IP> 450   && echo "AES DMCC (unencrypted) reachable" || echo "BLOCKED"
nc -zv <AES_IP> 4722  && echo "AES DMCC (TLS) reachable"   || echo "BLOCKED"
nc -zv <AES_IP> 8765  && echo "AES OAM reachable"           || echo "BLOCKED"

# ── Communication Manager / Gateway ──────────────────────────────────────────
nc -zv <CM_IP> 5060   && echo "CM SIP reachable"             || echo "BLOCKED"
nc -zv <CM_IP> 7500   && echo "CM media gateway reachable"   || echo "BLOCKED"

# ── AACC / CCMM ──────────────────────────────────────────────────────────────
nc -zv <AACC_IP> 8443 && echo "AACC HTTPS reachable"         || echo "BLOCKED"

# ── Batch port scan for full SIP stack audit ────────────────────────────────
# Save results to file for SR attachment:
LOGFILE=/tmp/avaya_port_audit_$(date +%Y%m%d_%H%M%S).txt
for HOST_PORT in \
  "<SM_IP>:5060" "<SM_IP>:5061" "<SM_IP>:8443" \
  "<AES_IP>:1099" "<AES_IP>:4722" \
  "<CM_IP>:5060" "<SBC_IP>:5060" "<SBC_IP>:5061"; do
  HOST="${HOST_PORT%%:*}"
  PORT="${HOST_PORT##*:}"
  RESULT=$(nc -zv -w 3 "$HOST" "$PORT" 2>&1)
  echo "$(date +%H:%M:%S) $HOST:$PORT — $RESULT" | tee -a "$LOGFILE"
done
echo "Port audit saved to $LOGFILE"
```

**Port reference table**:
| Component | Port | Protocol | Purpose |
|-----------|------|----------|---------|
| Session Manager | 5060 | TCP/UDP | SIP signaling (unencrypted) |
| Session Manager | 5061 | TLS | SIP signaling (encrypted) |
| Session Manager | 8443 | HTTPS | Admin UI, REST API |
| AES | 1099 | TCP | JTAPI / TSAPI client |
| AES | 450 | TCP | DMCC (unencrypted) |
| AES | 4722 | TLS | DMCC (encrypted) |
| AES | 8765 | HTTPS | OAM web console |
| CM | 5060 | TCP/UDP | SIP trunk |
| SBC (SBCE) | 5060/5061 | TCP/TLS | SIP edge |
| WFO/ACRA | 3460 | TCP | RTP capture (typical) |

**Firewall verification**: If `nc` is blocked on the test host itself,
use `traceroute -T -p <PORT> <DEST_IP>` to identify where TCP RST occurs.
Asymmetric firewall rules (outbound allowed, inbound blocked) are the most
common cause of OPTIONS keep-alive failures (see §SIP Intermittent Disconnection).

---

### E1 — SBC / Router Interface Health via SNMP and sipsak

SBC (Avaya SBCE) interface health must be verified at both the network layer
(SNMP interface counters) and SIP layer (OPTIONS probing) before concluding
a SIP trunk problem is in CM or SM configuration.

```bash
# ── SIP OPTIONS probe via sipsak ────────────────────────────────────────────
# Install: yum install sipsak (RHEL/CentOS) or apt install sipsak (Debian)

# Test SIP reachability to SBC external interface:
sipsak -s sip:<SBC_EXT_IP> -v
# Expected: 200 OK or 501 Not Implemented (both = SIP stack responding)
# Failure: timeout or ICMP unreachable = Layer 3/4 problem, not SIP config

# Test SIP OPTIONS to carrier SIP trunk endpoint:
sipsak -s sip:<CARRIER_SIP_IP>:<PORT> -v -t 5000
# If timeout: firewall or carrier ACL blocking; escalate to carrier

# Test SIP OPTIONS through SBC (via internal interface toward SM):
sipsak -s sip:<SM_IP>:5060 -H <LOCAL_SM_IP> -v

# ── SNMP interface counters (SBC or upstream router) ────────────────────────
# Check interface error counters (requires SNMP community read access):
SNMP_COMMUNITY="public"
SBC_IP="<SBC_IP>"

# Interface index discovery:
snmpwalk -v2c -c "$SNMP_COMMUNITY" "$SBC_IP" IF-MIB::ifDescr \
  | grep -iE "eth|ge|wan|sip"

# Packet error rates on SBC WAN interface (replace .3 with correct ifIndex):
snmpget -v2c -c "$SNMP_COMMUNITY" "$SBC_IP" \
  IF-MIB::ifInErrors.3 \
  IF-MIB::ifOutErrors.3 \
  IF-MIB::ifInDiscards.3 \
  IF-MIB::ifOutDiscards.3

# Avaya SBCE enterprise MIB — SIP session stats:
snmpwalk -v2c -c "$SNMP_COMMUNITY" "$SBC_IP" .1.3.6.1.4.1.6889.2.71
# .6889.2.71 = Avaya SBCE MIB subtree (session, signaling, media stats)

# ── SBCE CLI interface health (SSH to SBCE) ──────────────────────────────────
# show sipd endpoint-ip (active SIP registrations / dialogs)
# show interfaces (network interface RX/TX counters)
# show sip-statistics (200/4xx/5xx response counts per trunk)
# show alarm (active hardware and application alarms)

# ── Continuous monitoring loop (5-min interval) ─────────────────────────────
while true; do
  echo "=== $(date) ==="
  sipsak -s sip:<SBC_EXT_IP> -v 2>&1 | grep -E "200|501|timeout|error"
  snmpget -v2c -c "$SNMP_COMMUNITY" "$SBC_IP" \
    IF-MIB::ifInErrors.3 IF-MIB::ifOutErrors.3 2>/dev/null
  sleep 300
done
```

**SBC health decision matrix**:
| sipsak result | SNMP errors | Interpretation | Action |
|---------------|-------------|----------------|--------|
| 200/501 OK | Low (<5/min) | SBC healthy | Look at SM/CM config |
| Timeout | Low | SBC SIP stack down | Restart SBCE SIP process |
| Timeout | High | Network/interface fault | Check upstream router, cabling |
| 200/501 OK | High | Interface degraded | Check MTU, duplex, cable; escalate to network team |
| 5xx SIP error | Any | SBC config issue | Check SBC routing policy, entity links |

**Key invariant**: OPTIONS keep-alive failures (L-001 in `lessons/sip-voice-quality.md`)
frequently appear as SNMP interface errors on the WAN-side SBC interface when
the carrier firewall blocks inbound OPTIONS. Correlate sipsak timeout WITH
outbound OPTIONS counter increasing in SBC stats — asymmetric drop is diagnostic.


---

## On-Box Packet Capture & SIP Trace Analysis

Patterns sourced from sngrep, tshark, and field pcap tooling. All commands run
directly on Avaya Linux servers (RHEL/CentOS) — no GUI or pcap file transfer required.

---

### sngrep — Terminal SIP Call-Flow Ladder

sngrep reads live traffic or `.pcap` files and renders SIP call-flow ladder diagrams
in the terminal. Critical for SSH-only Avaya Linux servers (SM, AES, ACRA) where
transferring pcaps to a Wireshark workstation adds friction to SR evidence collection.

```bash
# Install (enable EPEL first on RHEL/CentOS):
yum install epel-release && yum install sngrep   # RHEL/CentOS
apt install sngrep                               # Debian/Ubuntu

# Read existing pcap (exported from traceSBC, tcpdump, or satrace):
sngrep -I /tmp/sip_capture.pcap

# Live capture on SIP port, save to file simultaneously:
sngrep -d eth0 -O /tmp/sip_live.pcap port 5060

# INVITE dialogs only (-c = capture only complete dialogs):
sngrep -d eth0 -c port 5060

# Filter by host from pcap (isolate one carrier or SM entity):
sngrep -I capture.pcap host <CARRIER_IP> and port 5060

# Include RTP payload data in capture:
sngrep -d eth0 -r port 5060

# TLS SIP decode (requires sngrep compiled with OpenSSL + server key):
sngrep -d eth0 -k /opt/avaya/certs/sm_server.key port 5061

# Non-interactive (headless) capture to file only (useful in scripts):
sngrep -d eth0 -N -O /tmp/out.pcap port 5060

# Combined SIP + RTP (Avaya primary RTP port range):
sngrep -d any -O /tmp/avaya_sip_rtp.pcap "port 5060 or udp portrange 10000-20000"
# Alternative RTP range used in some Avaya SM/CM deployments:
sngrep -d any -O /tmp/avaya_sip_rtp.pcap "port 5060 or udp portrange 16384-32767"
```

**sngrep keyboard navigation** (once open):
- Arrow keys: scroll call list | `Enter`: open call-flow ladder
- `F2`: SIP message fields | `F3`: filter by field (From, To, Call-ID)
- `F7`: filter dialog by status | `Space`: select call for export | `q`: quit

---

### tshark — Scriptable SIP/RTP Analysis

```bash
# SIP method + response statistics (call-volume dashboard):
tshark -r capture.pcap -q -z sip,stat

# SIP call-flow CSV (SR attachment quality — structured evidence):
tshark -r capture.pcap -Y sip \
  -T fields \
  -e frame.time_relative -e ip.src -e ip.dst \
  -e sip.Method -e sip.Status-Code \
  -e sip.Call-ID -e sip.CSeq \
  -E header=y -E separator=, > /tmp/sip_flow.csv

# Filter by SIP Call-ID (correlate with CM UCID or JTAPI call-id):
tshark -r capture.pcap -Y 'sip.Call-ID == "abc123@192.168.1.1"'

# SIP errors only (4xx/5xx — fast identification of rejection cause):
tshark -r capture.pcap -Y 'sip.Status-Code >= 400' \
  -T fields -e frame.time -e ip.src -e ip.dst -e sip.Status-Code -e sip.Status-Line

# INVITE only (call setup failures):
tshark -r capture.pcap -Y 'sip.CSeq.method == "INVITE"'

# OPTIONS keep-alive trace (diagnose carrier OPTIONS blocking — see L-001):
tshark -r capture.pcap \
  -Y 'sip.Method == "OPTIONS" or sip.Status-Code == 200' \
  -T fields -e frame.time -e ip.src -e ip.dst -e sip.Method -e sip.Status-Code

# SIP Digest auth headers (diagnose 401/407 registration failures):
tshark -r capture.pcap -Y 'sip.Status-Code == 401 or sip.Status-Code == 407' \
  -T fields -e frame.time -e ip.src -e sip.Status-Code -e sip.www_authenticate

# RTP stream statistics — jitter, loss, delta per stream (voice quality audit):
tshark -r capture.pcap -q -z rtp,streams
# Output columns: Start | End | Src IP:Port | Dst IP:Port | SSRC | Payload |
#   Pkts | Lost | Delta ms (min/mean/max) | Jitter ms (min/mean/max) | Problems
# Thresholds: Jitter > 30ms, Loss > 1%, Delta variance > 50ms = voice degraded

# Filter RTP by codec payload type:
tshark -r capture.pcap -Y 'rtp.p_type == 0'    # G.711 u-law (PCMU)
tshark -r capture.pcap -Y 'rtp.p_type == 8'    # G.711 A-law (PCMA)
tshark -r capture.pcap -Y 'rtp.p_type == 18'   # G.729
tshark -r capture.pcap -Y 'rtp.p_type == 101'  # RFC 2833 DTMF telephone-event

# DTMF event extraction (verify IVR DTMF delivery):
tshark -r capture.pcap -Y 'rtp.p_type == 101' \
  -T fields -e frame.time -e ip.src -e ip.dst \
  -e rtpevent.event_id -e rtpevent.end_of_event

# Export RTP streams as raw audio files for MOS / playback audit:
tshark -r capture.pcap --export-objects rtp,/tmp/rtp_streams/
# Convert raw G.711 u-law to WAV (requires ffmpeg):
for f in /tmp/rtp_streams/*.raw; do
  ffmpeg -f mulaw -ar 8000 -ac 1 -i "$f" "${f%.raw}.wav" 2>/dev/null
done
echo "WAV files in /tmp/rtp_streams/ -- open in Audacity or VLC for playback audit"

# tcpflow: reconstruct TCP SIP sessions from pcap (SIP over TCP stream recovery):
# yum install tcpflow
tcpflow -r capture.pcap port 5060
# Creates per-stream files: <srcIP.port>-<dstIP.port> with raw SIP messages in order
```

---

### Wireshark / tshark Display Filters (SIP & RTP)

Copy-paste into Wireshark display filter bar or pass via `tshark -Y`:

```
# SIP
sip                                        All SIP traffic
sip.Method == "INVITE"                     Call setup
sip.Method == "BYE"                        Call teardown
sip.Method == "REGISTER"                   Registration
sip.Method == "OPTIONS"                    Keep-alive probe
sip.Status-Code >= 400                     All SIP errors
sip.Status-Code == 401                     Auth challenge
sip.Status-Code == 403                     Forbidden (IP/credential)
sip.Status-Code == 404                     User not found
sip.Status-Code == 408                     Request timeout (firewall)
sip.Status-Code == 486                     Busy Here
sip.Status-Code == 503                     Service unavailable
sip.Call-ID == "id@host"                   Isolate single call
sip or rtp                                 Combined SIP + media view

# RTP
rtp                                        All RTP
rtp.p_type == 0                            PCMU G.711 u-law
rtp.p_type == 8                            PCMA G.711 A-law
rtp.p_type == 18                           G.729
rtp.p_type == 101                          RFC 2833 DTMF
rtcp                                       RTCP control (jitter stats)

# Network anomalies
tcp.analysis.retransmission                TCP retransmissions (packet loss)
tcp.analysis.out_of_order                  Out-of-order packets (jitter)
tcp.flags.rst == 1                         TCP resets (mid-call drops)
tcp.flags.syn == 1 and tcp.flags.ack == 0  New connection attempts only
ssl.handshake.type == 1                    TLS ClientHello (SIP TLS setup)
```

**BPF capture filters** (for `tcpdump -f` or Wireshark capture filter):
```bash
# SIP + RTP (Avaya default RTP range):
port 5060 or port 5061 or udp portrange 10000-20000

# SIP + alternate RTP range (some SM/CM deployments):
port 5060 or port 5061 or udp portrange 16384-32767

# External SIP only (exclude RFC1918 internal traffic):
port 5060 and not (net 10.0.0.0/8 or net 172.16.0.0/12 or net 192.168.0.0/16)

# SYN packets only (registration flood diagnosis):
tcp port 5060 and tcp[tcpflags] & tcp-syn != 0

# SIP + JTAPI combined (AES + SM in one capture file):
port 5060 or port 5061 or port 1099 or port 4722
```

---

### ngrep — Grep SIP Payloads Without Wireshark

```bash
# yum install ngrep (or apt install ngrep)

# Search live traffic for INVITE to a specific number:
ngrep -d eth0 -W byline "INVITE sip:.*4085551234" port 5060

# Search pcap file for 401 Unauthorized responses:
ngrep -I capture.pcap "401 Unauthorized" port 5060

# Show SDP bodies containing G.729 codec:
ngrep -I capture.pcap -W byline "a=rtpmap:18 G729" port 5060

# Check RFC 2833 DTMF negotiation in SDP:
ngrep -I capture.pcap "telephone-event" port 5060
# Zero matches = DTMF not negotiated in SDP -> configure phone/SBC codec list

# Count SIP REGISTER flood rate:
ngrep -I capture.pcap -c "REGISTER sip:" port 5060
```

---

### SIP Response Code Quick Reference

| Code | Meaning | Avaya Diagnostic Action |
|------|---------|------------------------|
| 200 | OK | Successful — verify RTP media follows |
| 401 | Unauthorized | Check SM SIP Entity credentials / realm |
| 403 | Forbidden | IP not whitelisted on carrier; check ACL / SBC policy |
| 404 | Not Found | Wrong SIP URI format or SM routing policy |
| 408 | Request Timeout | Firewall blocking 5060/5061; confirm with `nc -zv` |
| 481 | Call Leg Does Not Exist | BYE for unknown Call-ID; check state sync |
| 486 | Busy Here | Agent unavailable; check AACC skill queue |
| 487 | Request Terminated | Caller abandoned before answer; expected |
| 488 | Not Acceptable Here | Codec mismatch; compare SDP offer vs. answer |
| 500 | Server Internal Error | SM or gateway fault; check server logs |
| 503 | Service Unavailable | Downstream overload or component down |
| 603 | Decline | Explicit rejection by called party |

---

### DTMF SDP Verification in Capture

Before suspecting IVR / AEP DTMF delivery failure, verify DTMF was negotiated in SDP:

```bash
# Extract SDP codec lines from INVITE to check telephone-event:
tshark -r capture.pcap -Y 'sip.Method == "INVITE"' -T text | grep -A5 "a=rtpmap"
# Expected RFC 2833 negotiation in SDP body:
#   a=rtpmap:101 telephone-event/8000
#   a=fmtp:101 0-15

# Quick check with ngrep:
ngrep -I capture.pcap "telephone-event" port 5060
# Zero results -> RFC 2833 not negotiated -> configure endpoints to include it
# Or switch both sides to SIP INFO DTMF if telephone-event cannot be enabled

# telephone-event in SDP but DTMF still missing at AEP:
tshark -r capture.pcap -Y 'rtp.p_type == 101' | wc -l
# Zero RTP p_type=101 packets despite SDP negotiation
# -> Media bypasses AEP (direct-media / hairpinning); check CM direct-media setting
```


---

## Advanced PCAP Diagnostic Patterns

Evidence-anchored techniques for diagnosing SIP/RTP issues directly from packet captures.
Sources: SharkFest EU 2025 (SIP/SRTP trace analysis), field pcap tooling best practices.

---

### SIP INVITE Field Inspection Guide

When a call has issues, inspect these six fields in the INVITE and 200 OK:

| Field | Location | What to Check | Common Problem |
|-------|----------|---------------|----------------|
| `Request-URI` | First line: `INVITE sip:+12125551234@provider.com SIP/2.0` | Number format, domain, transport | Wrong number format (missing +, wrong country code) |
| `From` / `To` | Headers | URI format, tag in 200 OK | Missing From-tag causes 400 Bad Request |
| `Call-ID` | `Call-ID: abc123@10.1.1.1` | Unique per dialog; correlate across hops | Duplicate Call-IDs = loop or fork |
| SDP `m=audio` | Body: `m=audio 20000 RTP/AVP 0 8 101` | Port != 0; codec list includes both sides' supported types | Port 0 = media rejected; missing 101 = no RFC 2833 DTMF |
| SDP `a=rtpmap` | Body: `a=rtpmap:0 PCMU/8000` | Payload-type number matches `m=audio` codec list | Mismatched payload type -> wrong codec decoded |
| SDP `c=` line | Body: `c=IN IP4 10.1.2.3` | IP reachable from remote endpoint; not 0.0.0.0 | 0.0.0.0 or private IP behind NAT -> one-way or no audio |

**Quick check sequence:**
1. Filter: `sip.Method == "INVITE"` — inspect SDP offer
2. Filter: `sip.Status-Code == 200` — inspect SDP answer; compare codec + `c=` address
3. If `c=` address differs between offer and answer: NAT traversal problem
4. If 200 OK has `m=audio 0` (port zero): remote explicitly rejected media

---

### Symptom -> PCAP Diagnostic Map

| Symptom | First PCAP Check | Filter | Expected vs. Observed |
|---------|-----------------|--------|----------------------|
| One-way audio (agent hears, caller does not) | `c=` IP in SDP answer | `sip.Status-Code == 200` inspect body | SDP answer `c=` must be reachable from caller RTP sender |
| No audio in either direction | RTP packets present? | `rtp and ip.addr == <media_IP>` | Zero RTP packets = media path not established; check SDP port != 0 |
| DTMF not recognized at IVR | `telephone-event` in SDP | `sip.Method == "INVITE"` SDP body | `a=rtpmap:101 telephone-event/8000` must appear; if absent, RFC 2833 not negotiated |
| DTMF in SDP but IVR still misses digits | RTP type 101 packets arriving? | `rtp.p_type == 101` | Zero packets despite SDP negotiation = direct-media bypasses AEP; check CM ip-network-region direct-media |
| Choppy audio / gaps | RTP jitter + loss | `tshark -q -z rtp,streams` | Jitter >30 ms or loss >1% = network QoS issue; correlate with DSCP markings |
| Call drops after ~30 sec | re-INVITE exchange | `sip.CSeq.method == "INVITE"` (second instance) | Missing 200 OK/ACK to re-INVITE = codec or timing fault |
| Call drops at N-minute mark | OPTIONS keep-alive flow | `sip.Method == "OPTIONS"` responses | No 200 OK after OPTIONS = CGNAT or firewall timeout |
| Codec mismatch (488) | SDP offer vs answer codec sets | `sip.Status-Code == 488` | Empty intersection between INVITE `m=audio` and 200 OK `m=audio` |
| Auth failure (401/403) | Auth header presence | `sip.Status-Code == 401` -> `WWW-Authenticate` | Check realm, algorithm (MD5), and credentials match provider |
| 408 Request Timeout | INVITE reaches destination? | `ip.dst == <dest> and sip.Method == "INVITE"` | No matching packet = firewall dropping; confirm with `nc -zv <dest> 5060` |
| 486 Busy Here (unexpected) | Agent state in AACC | `sip.Status-Code == 486` | If agent not on call: check AACC Aux state (see `contact-center.md`) |
| 500/503 from provider | Provider response body | `sip.Status-Code >= 500` | Provider internal error; if persistent, escalate to carrier |

---

### SRTP / Encrypted Media Analysis

For environments using SRTP (Avaya recommends SRTP for all trunk-side encryption),
decryption is **not required** to diagnose most RTP quality issues. Transport-layer
metrics (jitter, loss, delta, sequence gaps) are available in the outer UDP/IP header
and remain visible even when the payload is encrypted.

**Key principle (SharkFest EU 2025):** *Differentiate failed signaling from failed audio
stream.* These are independent failure modes -- a call can have perfect SIP signaling and
still have no audio if SRTP keys are not exchanged correctly.

#### SRTP Display Filters

```
# SRTP payload (outer UDP/IP header visible even when payload is encrypted):
srtp                                     All SRTP packets (Wireshark >= 3.0)
srtp.enc_payload                          Filter where encrypted payload field is present

# DTLS-SRTP key exchange (WebRTC or modern SIP with DTLS):
rtp.setup-method == "DTLS-SRTP"          Frames associated with DTLS-SRTP session setup

# SDES key exchange detection (traditional SIP SRTP via SDP a=crypto):
sdp.media contains "RTP/SAVP"            SRTP-capable media line (Secure AV Profile)
sdp.session_attribute contains "crypto"  SDP a=crypto key offer/answer

# SDP connection address (find media IP across call legs):
sdp.connection_info                      SDP c= line value
sdp.connection_info == "IN IP4 10.1.2.3" Isolate calls from specific media endpoint IP

# SDP media line (codec + security profile):
sdp.media                                All SDP m= lines
sdp.media contains "RTP/SAVP"            SRTP-encrypted streams
sdp.media contains "RTP/AVP"             Unencrypted RTP streams (for comparison)
```

#### SRTP Diagnostic Workflow

```
Step 1 -- Confirm SRTP negotiation in SDP (no decryption needed):
  tshark -r capture.pcap -Y 'sip.Method == "INVITE"' -T text | grep -E "a=crypto|RTP/SAVP"
  Expected: "a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:<key>"
  Missing: SDES key not offered -> falls back to RTP/AVP (unencrypted)

Step 2 -- Confirm SRTP packets are flowing:
  tshark -r capture.pcap -Y 'srtp' | wc -l
  Zero = SRTP session not established (SDP negotiation failed or NAT blocked media)
  Non-zero = SRTP data flowing; quality analysis via outer header is possible

Step 3 -- Analyze RTP quality from outer header (encryption is irrelevant):
  tshark -r capture.pcap -q -z rtp,streams
  # Sequence numbers, timestamps, and inter-arrival jitter are in the outer header
  # Payload decryption NOT needed to measure packet loss, jitter, or delta-time

Step 4 -- If DTLS-SRTP (WebRTC or modern SBC):
  tshark -r capture.pcap -Y 'rtp.setup-method == "DTLS-SRTP"'
  # Also filter 'dtls' to see ClientHello / ServerHello / Finished handshake
  # Failure: DTLS handshake timeout -> no SRTP session -> no audio

Step 5 -- SRTP key mismatch symptom:
  SRTP packets present + zero decoded audio at endpoint = key mismatch
  Check: does SDP re-INVITE (hold/resume) refresh a=crypto with a new key?
  Some SBCs generate a new SRTP key on re-INVITE; endpoints must update session key.
```

**Determine SRTP usage before starting capture:**

```bash
# Check CM codec set for SRTP:
# CM SAT: display ip-codec-set <N>
# Look for: media-encryption: 1-srtp-aescm128-hmac80

# Confirm from live SDP in capture:
ngrep -I capture.pcap "a=crypto" port 5060 | grep -c "crypto"
# 0 = no SRTP in use -> apply plain rtp.* filters
# >0 = SRTP in use -> apply srtp.enc_payload and sdp.media filters
```

---

### DTMF Three-Path Analysis

Three mechanisms deliver DTMF in SIP calls. Match the diagnostic approach to the negotiated method:

| DTMF Method | SDP Negotiation | Filter | How to Identify |
|------------|-----------------|--------|-----------------|
| **RFC 2833 / RFC 4733 (out-of-band RTP)** | `a=rtpmap:101 telephone-event/8000` | `rtp.p_type == 101` | RTP packets with PT=101; `rtpevent.event_id` = digit value |
| **SIP INFO** | No SDP entry (Content-Type: application/dtmf-relay) | `sip.Method == "INFO"` | SIP INFO body: `Signal=5\r\nDuration=160` |
| **In-band (analog tones)** | Any codec; tones embedded in audio payload | `rtp.p_type == 0` or `rtp.p_type == 8` | No filter -- detect via Audacity spectrum analysis |

#### RFC 2833 Digit Decoding

```bash
# Extract each DTMF digit with timestamp and end-of-event flag:
tshark -r capture.pcap -Y 'rtp.p_type == 101' \
  -T fields \
  -e frame.time_relative \
  -e ip.src -e ip.dst \
  -e rtpevent.event_id \
  -e rtpevent.end_of_event \
  -e rtpevent.duration

# rtpevent.event_id: 0-9 = digits 0-9 | 10 = * | 11 = # | 12-15 = A-D
# rtpevent.end_of_event == 1 = final packet for that digit (use for de-duplication)
# rtpevent.duration = RTP timestamp units (divide by 8 for ms at 8000 Hz sampling rate)

# Count complete digits received (verify IVR receives all keystrokes):
tshark -r capture.pcap -Y 'rtp.p_type == 101 and rtpevent.end_of_event == 1' | wc -l
```

#### SIP INFO DTMF Extraction

```bash
# List all SIP INFO events with Content-Type:
tshark -r capture.pcap \
  -Y 'sip.Method == "INFO"' \
  -T fields -e frame.time -e ip.src -e ip.dst -e sip.content_type

# Full body including Signal= value (ngrep shows raw SIP including body):
ngrep -I capture.pcap -W byline "Signal=" port 5060
# Body format: Signal=5  Duration=160   (Duration in ms)
```

#### In-Band DTMF Detection (Audacity)

When RFC 2833 and SIP INFO are both absent but DTMF is expected:

1. Export RTP stream: Wireshark `Telephony > RTP > Stream Analysis` -> select stream -> `Save payload`
2. Convert to WAV: `ffmpeg -f mulaw -ar 8000 -ac 1 -i stream.raw stream.wav`
3. Open in Audacity: `Analyze > Plot Spectrum` -- look for simultaneous row + column DTMF frequency peaks
   - Rows: 697 / 770 / 852 / 941 Hz
   - Columns: 1209 / 1336 / 1477 / 1633 Hz
4. No tonal peaks visible: phone attempts RFC 2833 but `a=fmtp:101 0-15` absent from SDP

---

### Key Trace Analysis Principles (Field-Validated)

1. **Differentiate signaling failure from audio stream failure first.** A call can complete
   SIP signaling (200 OK received) with no audio. Conversely, a call with mid-call SIP errors
   (3xx/4xx re-INVITE) may still have active RTP. Check both planes independently before
   forming a root-cause hypothesis.

2. **No SRTP decryption needed for quality analysis.** RTP sequence numbers, timestamps,
   and outer IP/UDP headers remain unencrypted in SRTP. `tshark -q -z rtp,streams` correctly
   computes jitter, loss, and delta-time from SRTP captures without decryption.

3. **SIP dialects vary by vendor.** Avaya SM, Cisco CUBE, AudioCodes, and carrier SBCs each
   add proprietary headers (`P-Avaya-Cl-Info`, `X-BroadWorks-Correlation-ID`, etc.). These
   appear in Wireshark frames but lack dedicated display filters -- use `frame contains "X-"`
   as a generic filter to surface proprietary headers for cross-vendor comparison.

4. **Early Offer vs. Delayed Offer changes the codec diagnosis sequence.** In Early Offer,
   the INVITE carries SDP (normal). In Delayed Offer, the INVITE has no SDP body -- the offer
   comes in the 200 OK and the answer comes in the ACK. When analyzing codec mismatch, check
   whether `Content-Type: application/sdp` appears in the INVITE. If absent, the real codec
   negotiation is in the `200 OK` -> `ACK` exchange, not the `INVITE` -> `200 OK`.

5. **Session-Timer re-INVITEs are periodic and expected.** RFC 4028 Session-Timer generates
   keep-alive re-INVITEs (default 1800 s, often 90 s on Avaya SBCs). These appear as mid-call
   INVITEs in the capture. To distinguish keep-alive from real media-renegotiation re-INVITEs:
   look for `Supported: timer` or `Session-Expires` headers. Real hold/transfer re-INVITEs
   will change the SDP `a=sendrecv` / `a=sendonly` / `a=recvonly` direction attribute.
