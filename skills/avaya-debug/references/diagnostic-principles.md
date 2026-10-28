---
title: "Diagnostic Principles — Avaya UC & CC"
layer: L4
scope: "avaya-uc-cc-all-domains"
maturity: canonical
applicable_versions: [TBD]
last_reviewed: "2026-06-03"
owner: "avaya-debug skill"
staleness_risks:
  - "JTAPI Javadoc URLs"
  - "CM SA flag names"
  - "AES version-specific behavior"
related_docs:
  - "SKILL.md (routing)"
  - "spi-protocol.md"
  - "lessons/diagnostic-principles.md (field findings)"
---

# Diagnostic Principles — Avaya UC & CC

This reference is loaded for **every** Avaya troubleshooting session. It contains
core invariants, cross-product integration facts, vendor escalation routes, and
case document extraction patterns that apply regardless of which domain reference
is also loaded.

Apply interface-specific invariants to the interfaces present in the investigation. For SPI-only measurement reporting, follow CM MST MIS → CMS `spi.log` → CMS database/report and consult [SPI protocol diagnosis](spi-protocol.md). Use the wire UCID fields and mapped ITNs from the verified SPI language; JTAPI getters do not decode these records.

AES flags, deviceIDType, CSTA/g3trace, JTAPI extraction and `getlogs`/`common` checks remain applicable when the CM/AES/CTI platform fault requires them. They are not default prerequisites for SPI-only diagnosis and do not replace the paired CM MIS/CMS SPI sequence.

---

## Core Diagnostic Invariants

These are empirically validated facts. Do not override them without new primary-source evidence.

1. **Evidence-Based**: Every conclusion must cite trace evidence — timestamps, log entries, field values. Symptom descriptions are hypotheses, not findings.

2. **Layer-by-Layer**: Analyze the relevant interface layers independently before correlating. For CTI, follow CM → AES → JTAPI → Application; for SPI-only reporting, follow CM MST MIS → CMS `spi.log` → CMS database/report. Root cause is often at a different layer than the symptom.

3. **UCID as Anchor**: UCID is the most reliable call-correlation key. For JTAPI events, always extract via: cast event to `LucentV5CallInfo` → call `getUCID()`. **Never** use `event.getOriginalCallInfo().getUCID()` — empirically returns `"00000000000000000000"` on `EC_PARK` events. For SPI records, use the wire UCID fields defined by the actual message language.

4. **Check CM System-Features First**: When null addresses or trunk placeholders (`T####`) appear, run `display system-features` and check `SA9114` / `SA9124` before any deep JTAPI analysis.

5. **deviceIDType Is the Key Diagnostic Field**:
   - `30` = `EXPLICIT_PUBLIC_UNKNOWN` (trunk placeholder — a temporary stand-in)
   - `31` = `EXPLICIT_PUBLIC_INTERNATIONAL` (actual PSTN number)
   - `50` = `EXPLICIT_PRIVATE_UNKNOWN`
   - `55` = `EXPLICIT_PRIVATE_LOCAL_NUMBER` (internal extension)

6. **Verify Transfer Type from CSTA Trace**: When the CSTA interface is involved, never trust the customer's description. Check for `CSTATransferCall` (consultative) vs `SingleStepTransferCall` (blind) in the raw trace. SPI transfer diagnosis instead uses its applicable XFER fields and facility mapping.

7. **Vector wait-time = 0 Creates Race Conditions**: Minimum safe value is 1 second. Vector step wait fields accept integers only.

8. **After Certificate Change — Three Actions Required**: Inventory all JKS stores → restart application → clear browser cache. All three. Skipping any one causes symptoms identical to "cert not yet applied."

9. **Browser Cache Is a Silent Killer**: Clear browser cache after any web-tier fix before declaring the fix unsuccessful.

10. **Never Trust Prior Analysis**: Verify claims against primary sources (NVD, Release Notes, actual running config). This applies to prior avaya-debugger reports too — earlier root cause hypotheses may be wrong.

11. **JTAPI `null` Returns Are Spec-Compliant**: Per `CallControlCall.getCalledAddress()` Javadoc: *"Each of these methods returns null if their values are unknown at the present time."* Do NOT treat null as a bug — check the JTAPI Programmer's Reference first.

12. **`TSCall.calledDevice` Is a Field, Not Connection-Derived**: `getCalledDevice()` returns a private field directly (TSCall.java:784). Set once at `EC_NEW_CALL` via `setCalledDevice(non-null)`. `EC_PARK` passes null which is a no-op due to the null guard. The field persists until TSCall destruction. Connection-list manipulation does not affect this field.

13. **`OriginalCallInfo` Is for Consult Only**: Per official Javadoc, OriginalCallInfo is "made available in conjunction with the consult() service." Do not request AES PEAs to extend OriginalCallInfo for park scenarios — design intent does not support this.

14. **`connBelongToDifferentDeviceIDType` = Smoking Gun for Park/Unpark TSCall Destruction**: Search trace for this flag. Triggered by `SnapshotCallConfHandler.handleConf()` PC 1067 when trunk TSDevice has PRIVATE→PUBLIC deviceID type mismatch with current snapshot. Always on Outbound when SA off; never on Inbound.

15. **Compositional Root Causes Exist**: Some bugs are not "one component is wrong" but "each component behaves per spec; the composition is unworkable." When 3+ products' behaviors are documented as correct, look for configuration that changes inter-product interactions (like SA9114/SA9124).

16. **CFR Decompiler Failures Are Recoverable**: When CFR throws `ConfusedCFRException: Started 2 blocks at once` on a critical method, fall back to Python `javatools` for direct bytecode disassembly + LVT-based pseudocode reconstruction.

---

## Cross-Product Integration Quick Reference

| Integration | Protocol | Key Correlation Data |
|------------|----------|---------------------|
| CM ↔ AES | ASAI over TCP | `calling_num`, `called_num`, UCID |
| CM ↔ AACC | CVLAN + ASAI | VDN, Vector, Skill, Agent ID |
| CM ↔ SM | SIP (UDP/TCP/TLS) | `Request-URI`, `PAI`, SDP |
| AES ↔ Oceana | REST + JTAPI/CSTA | Call context, routing decisions |
| CM ↔ AEP | SIP + MRCP + HTTP | VoiceXML, DTMF/ASR results |
| AES ↔ Recording | DMCC | Recording sessions, pause/resume |

---

## Vendor Escalation Routes

| Symptom Layer | Owner | Escalation Handoff |
|--------------|-------|--------------------|
| Verint code (WebLogic, RIS, BatchExtender) | **Verint** ticket | Verint logs, KB reproduction level |
| Nuance MRCP/TTS/ASR | **Nuance** ticket | MPP MRCP trace |
| CM / AES core platform bugs | **BBE** PEA | getlogs + common trace for the affected platform |
| POM / AEP product code | **CPE** PEA | EPM / MPP / POM logs |
| Customer infra (LDAP, SQL, AD, firewall) | **Customer / MSP** | Network evidence from both sides |

For CM/AES core platform faults requiring those diagnostics, collect `getlogs` output from the affected server and a `common` trace (or CSTA/g3trace for AES issues) before BBE escalation. For SPI-only measurement/reporting issues, hand off the complete paired CM MST MIS and CMS `spi.log` evidence, translation/language context and exact database/report discrepancy; platform traces can supplement this when relevant but do not replace the SPI pair.

---

## Case Document Extraction

When working with attachments in Avaya SR cases:

| File Type | Tool | Notes |
|-----------|------|-------|
| OLE2 `.doc` files | Python `olefile` library | NOT `python-docx` — OLE2 format incompatible |
| Password-protected ZIP | — | Request password from customer before attempting extraction |
| ZIP with Japanese filenames | Python `zipfile` + `sys.stdout.reconfigure(encoding='utf-8')` | Prevents UnicodeDecodeError on Windows |
| EML files | Python `email` module | Parse MIME parts; attachments are base64-encoded |
| Excel with Workplace logs | `openpyxl` with `data_only=True` | May have 80K+ rows; iterate in chunks |
| GZIP spi.log | `zcat` or Python `gzip` | Always check for `.gz` suffix on log exports |

---

## Diagnosis Validation Checklist

Before closing a root cause finding, confirm:

- [ ] Root cause cites a specific log line, trace timestamp, config field, or code path
- [ ] All relevant interface layers have been examined: CTI CM → AES → JTAPI → Application, or SPI CM MIS → CMS SPI → database/report, as applicable
- [ ] For AES/JTAPI null addresses or trunk placeholders, `SA9114` / `SA9124` checked
- [ ] For JTAPI events, UCID extracted via `LucentV5CallInfo.getUCID()` — not `getOriginalCallInfo().getUCID()`; for SPI, wire UCID fields used from the verified message language
- [ ] When AES/CSTA identifiers are involved, deviceIDType confirmed (30 vs 31 vs 50 vs 55)
- [ ] Transfer type confirmed from the applicable interface: CSTA trace (`CSTATransferCall` vs `SingleStepTransferCall`) or SPI XFER fields and mapped facilities
- [ ] Applicable `L-NNN` lessons consulted in `lessons/<domain>.md`
- [ ] Open items with missing evidence are explicitly listed, not silently assumed resolved
