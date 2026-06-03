# Lessons — Cross-Product Orchestration & Integration

Field-captured findings for multi-product orchestration failures involving POM, Oceana, AACC, CCMM, AEP, and digital channels. Mirrors `../references/orchestration-integration.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---

## L-001 — POM Campaign Agent Fetch Timeout Masking Oceana Unavailable

- **Symptom**: POM campaign launches successfully. Agent appears to accept dial (alert tone plays). But call never connects to Oceana engagement. Supervisor observes campaign appears "executing" but no engagement created. POM logs show "agent fetch timeout" but do not indicate Oceana service unavailable.
- **Evidence**: POM logs (`$POM_HOME/logs/PIM_AgtMgr.log`): `agent assignment timeout after 30 sec`. Oceana logs: zero incoming route requests during campaign window. Service Health (AACC Dashboard) shows Oceana status = `unavailable`. But POM error message is "agent assignment timeout from AACC skill queue" which masks the root cause (Oceana, not AACC, is unavailable).
- **Root cause**: POM times out waiting for agent availability from AACC (default 30 sec), and reports that timeout rather than checking if upstream Oceana service is unavailable. POM cannot route dial to available agent because Oceana engagement engine is down, but error message does not mention Oceana.
- **Fix**: Before campaign launch, verify Oceana service status. In AACC: Administration > Snap-ins > Oceana > Status field should show "Running". If status = "Stopped" or "Unavailable", restart Oceana service before launching campaign. Add pre-campaign health check script to verify Oceana readiness (check `/var/log/avaya/oceana/OceanaCore/` for recent startup logs and no FATAL errors).
- **Provenance**: SR 1-23087654321 | 2025-01-25
- **Promotion**: pending (awaiting SOP documentation from customer escalation team)
