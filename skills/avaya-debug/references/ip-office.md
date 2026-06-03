# Avaya IP Office Troubleshooting

## Why IP Office Is Different

IP Office (IPO) is a **separate SMB product family from Avaya Aura**. Its
management tooling, log names, and diagnostic procedures differ from Aura.
Do not assume Aura troubleshooting steps apply.

Key implications:
- No Session Manager, no SMGR, no System Manager element inventory
- No `traceSM`, no `tracesbc` — IPO uses its own SysMonitor tracer
- Configuration lives in IPO Manager / Web Manager, not SMGR
- SIP trunk and extension state come from SSA, not from SMGR Entity views
- Logs and event categories use IPO-native naming

When a fault report mentions "IP Office", "IPO", "SSA", "SysMonitor", or
"IP Office Manager", switch to the procedures below — the Aura SIP
signaling guide (`sip-voice-quality.md`) does not apply directly.

---

## Core Tools

| Tool | Purpose |
|------|---------|
| **System Status Application (SSA)** | High-level health dashboard: SIP trunks (Idle / Out of Service / Unregistered), extensions, alarms, module status |
| **IP Office Monitor (SysMonitor)** | Real-time packet/event tracer. Enable categories under `Trace Options -> SIP`, then force re-registration and observe |
| **IP Office Manager / Web Manager** | Configuration (SIP line settings, ITSP proxy, credentials) |
| **Status -> Blacklisted IP Addresses** | Shows IPs blocked after repeated failed attempts; review when registration keeps failing after credentials are corrected |
| **Status -> Quarantined Phone Status** | Shows individual extensions blocked locally by IPO |

### Tool Selection Quick Guide
- "Is this trunk up?" -> **SSA -> SIP Trunks**
- "Why is REGISTER failing?" -> **SysMonitor with SIP trace**
- "Where do I change the proxy / credentials?" -> **IP Office Manager**
  (SIP Line settings, ITSP proxy, credentials)
- "Why does it still fail after I fixed credentials?" -> **Status ->
  Blacklisted IP Addresses** and **Status -> Quarantined Phone Status**

---

## SIP Trunk Registration Triage (IPO-Specific)

Step-by-step procedure when a SIP trunk on IPO will not come up or
keeps dropping:

1. **Open SSA** and confirm trunk status. Look for:
   - `Unregistered`
   - `Failed`
   - `Out of Service`
   - `Idle` (good — trunk is up but no active call)

2. **Start SysMonitor** with SIP tracing enabled:
   - `Trace Options -> SIP`
   - Enable both inbound and outbound SIP categories
   - Capture to file so the trace can be reviewed offline

3. **Trigger re-registration from Manager** (e.g. by toggling the SIP
   Line or sending the unit a configuration update). This forces a
   fresh REGISTER so the failure is captured in the trace.

4. **Read the provider response** in SysMonitor and map to a cause
   (see table below).

5. **If credentials look correct but it still fails**, check both
   local-blocklist panels:
   - `Status -> Blacklisted IP Addresses`
   - `Status -> Quarantined Phone Status`

6. **On the SMGR side** (when both Aura and IPO are deployed
   together — e.g. ACCS+IPO), also check `SSA -> SIP Trunks` for
   status and reason as part of overall SIP signaling triage.

### Provider Response Mapping

| Response | Most Likely Cause | What to Check |
|----------|-------------------|---------------|
| `401 Unauthorized` | Credentials wrong | SIP Line user / password / realm in IPO Manager |
| `407 Proxy Authentication Required` | Credentials wrong (proxy auth) | Same as 401 — check realm carefully |
| `403 Forbidden` | Provider rejects by IP or domain | Confirm ITSP allowlist of the IPO public IP and the SIP domain configured on the SIP Line |
| No response / timeout | Transport problem | Wrong proxy IP/port; firewall/NAT rules on 5060/5061; MTU issues on the WAN link |
| `ICMP Destination Unreachable` | Transport problem | Same as timeout — routing or firewall blocks the proxy |
| Repeated failures after credentials are correct | Local quarantine **or** provider blacklist | Check IPO `Status -> Blacklisted IP Addresses` and `Status -> Quarantined Phone Status`; if clean, ask provider whether the IPO's public IP is on their blacklist |

Key insight: a "credentials are right but it still fails" loop on IPO
is often **self-inflicted** — the IPO has locally quarantined the
extension or the provider has blacklisted the IPO's public IP after
too many bad attempts. Fixing only the credentials does not clear
either list.

---

## Common IPO Patterns

### ACCS + IPO Integration
- **User synchronization failed on IPO server** = check ACCS-IPO
  connectivity. Status may show **green** while sync has actually
  failed (per `1-18875014962`). Do not trust the green light alone —
  verify the user list on both sides.
- **License Manager not coming up after license install on Local
  WebLM** in an ACCS/IPO deployment = verify license file format
  and WebLM connectivity (per `1-19101968712`).

### Voice Quality After Upgrade (ACCS + IPO)
- **Voice quality degraded after IPO and ACCS upgrade** = codec or
  DSP configuration changed during upgrade. Verify codec settings
  post-upgrade; check DSP resources and IP-network-region
  (per `1-19480241832`).

### Combined Aura + IPO SIP Signaling
- When triaging SIP REGISTER in a hybrid environment, after the
  Aura-side validation steps, also check `SSA -> SIP Trunks` on
  the IPO for status and reason.

---

## When to Hand Off

IPO is largely **customer-managed** in many deployments. Escalation
guidance:

- **Hand back to the customer / partner administrator** when:
  - Configuration changes are needed in IPO Manager (SIP Line edits,
    credential changes, codec changes)
  - The ITSP needs to update its allowlist or clear a blacklist on
    the IPO's public IP
  - Local blocklists (`Blacklisted IP Addresses`, `Quarantined Phone
    Status`) need to be cleared — these are local actions

- **Engage Avaya support** when:
  - SysMonitor traces show IPO software faults (crashes, internal
    state errors) rather than configuration issues
  - The IPO licensing or upgrade path is in question
  - HA / SCN failover is misbehaving

- **Engage the ITSP** when:
  - SysMonitor consistently shows `403 Forbidden` after credentials
    have been verified
  - Repeated `no response` from a known-good proxy IP suggests the
    IPO has been blacklisted upstream

A useful triage rule: if the fault is reproducible only on the IPO
side and Aura elements are healthy, do **not** start by tracing on
SMGR/SBC — start with SSA + SysMonitor on the IPO.

---

## Related Reference Files

- For Aura SIP signaling -> `sip-voice-quality.md`
  (procedures there target Session Manager / SBC and are **not**
  directly applicable to IPO; do not run `traceSM` or `tracesbc`
  expecting IPO output)
- For ACCS / contact-center fault patterns that touch IPO ->
  `contact-center.md`
