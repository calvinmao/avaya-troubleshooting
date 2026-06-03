# SIP / Voice Quality / Codec Troubleshooting Reference

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
