# Lessons — Contact Center (AACC / Oceana / POM / CMS)

Field-captured findings for contact-center routing, agents, vectors, campaigns, and reporting. Mirrors `../references/contact-center.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---

## L-001 — Edify Socket Service State Divergence on LDAP Sync Lag

- **Symptom**: Agent logged out from CM, but visible in AACC OAM "Ready" state for 25 seconds. Other agents see the phantom agent in skill queue, cause routing delays and skill misalignment.
- **Evidence**: CM `display agent <ID>` shows logged-out. AACC logs show `SocketServer EXCEPTION: Connection reset by peer` at 10:23:45 during LDAP sync. Agent state in AACC database query shows "UNKNOWN" status instead of "Offline". LDAP access log shows ldap_sync operation took 42 seconds (threshold default: 30 sec). Phantom agent visible in supervisor dashboard for 25 sec, then transitions to Offline.
- **Root cause**: Edify Socket Service cached agent state during LDAP sync lag. When LDAP took >30 sec to confirm logout, AACC served stale agent state from cache. Socket connection error caused state to remain hung until cache timeout (25 sec) or manual refresh.
- **Fix**: (1) Restart Edify Socket Server service on AACC: `systemctl restart avaya-edify-socket-service`. (2) Reduce LDAP sync timeout from default 30 sec to 5 sec in AACC config (check AACC Administration > Directory Services > LDAP > Sync Timeout). (3) Monitor LDAP server latency; escalate to Directory Services team if consistent >5 sec.
- **Provenance**: SR 1-23156782912 | 2025-01-18
- **Promotion**: pending (awaiting verification on second customer site)
