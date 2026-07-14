---
domain: recording-wfo
default_layer: L3
default_type: experience
last_reviewed: "2025-01-14"
---

# Lessons — Recording / ACRA / WFO / WFE / Verint

Field-captured findings for the recording and workforce-optimization stack. Mirrors `../references/recording-wfo.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---
id: L-001
layer: L3
type: experience
maturity: draft
versions: [TBD]
provenance:
  sr: "1-22998412312"
  date: "2025-01-14"
promotion:
  status: pending
  target: null
  date: null
  note: "awaiting second case confirmation"
owner: "@hmao911"
---

## L-001 — GC Pause Causes Recording Duration Mismatch

- **Symptom**: Recording duration shows 30+ seconds longer than actual call duration. Agent paused the call multiple times; paused duration should not be counted in final duration.
- **Evidence**: WebLogic heap monitoring via `jstat -gcutil <pid>` shows Full GC pause >500ms during pause/resume operations. Call log: pause at 14:23:10, resume at 14:23:15; recording timer shows +7 sec instead of +5 sec. Repeated across 8 calls in 1-hour window on 2025-01-14.
- **Root cause**: Recording timer advances during GC pause when DMCC pause operation is held. Resume triggers timer catch-up instead of proper time-slicing calculation. WebLogic's `-XX:MaxGCPauseMillis` default (200ms) is too tight for DMCC device state transitions under load.
- **Fix**: Set `-XX:MaxGCPauseMillis=200` in WebLogic startup (CATALINA_OPTS or setDomainEnv.sh). Monitor GC pause times post-change via `jstat`. Consider increasing heap if GC frequency exceeds 1/sec.
