---
domain: digital-channels
default_layer: L3
default_type: experience
last_reviewed: "2025-01-28"
---

# Lessons — Digital Channels (Email / Social / ESL / Infinity / CCMM)

Field-captured findings for async channels, CRM connectors, screen-pop, and WeChat/WhatsApp/SMS integrations. Mirrors `../references/digital-channels.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---
id: L-001
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-23045671892"
  date: "2025-01-28"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting infrastructure remediation + second case confirmation"
owner: "@hmao911"
---

## L-001 — Email Channel Gateway Heartbeat Timeout on Intermittent Network

- **Symptom**: Email channel shows "connected" in CCMM UI, but outbound emails don't deliver to Oceana engagement queue. No error messages in UI; supervisors see emails "pending" indefinitely. Channel remains marked "online" despite delivery failure.
- **Evidence**: CCMM logs (`$CCMM_HOME/logs/`): `gateway heartbeat timeout` recurring every 5 min at consistent intervals. Network latency trace between CCMM and email gateway measures 800ms average (normal baseline: <100ms). When latency drops <500ms, emails deliver successfully within 2-3 sec. Logs show no ERROR level messages; heartbeat timeout is logged at WARN level only.
- **Root cause**: Email gateway heartbeat timeout configured to 1 sec (default). When network latency spikes >1 sec, heartbeat response exceeds timeout window. CCMM silently marks channel as "degraded" but does not surface error in UI; emails continue to queue but never deliver because channel unreliability suppresses send operation.
- **Fix**: (1) Increase email gateway heartbeat timeout to 2 sec in CCMM config (check `$CCMM_HOME/config/channels/email-gateway.properties` → `heartbeat.timeout.ms=2000`). (2) Investigate upstream network latency: run `traceroute` from CCMM to email gateway; if latency >500ms consistently, escalate to infrastructure/network team for path analysis and possible SLA violation with ISP. (3) Monitor CCMM logs for `gateway heartbeat timeout` after remediation; should drop to <1 per hour.
