---
title: "SPI - CM/CMS Measurement Reporting Protocol"
layer: L4
scope: "Avaya Switch / Reporting Adjunct SPI, CM/CMS/IQ measurement events, language and translations, ITN/UCID mapping, SETUP/XFER/IDLE, audits, paired capture"
maturity: canonical
applicable_versions:
  - "SPI language 23 / CM 6.0 with CMS R16.1 and IQ 5.1 (historical test plan)"
  - "SPI language 24 / CM 7.0-era syntax baseline (2015)"
  - "CM 10.x with CMS 20.0-21.0 (configuration context; verify maintenance build and wire language)"
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks:
  - "Historical SPI source issue labels, predecessor layouts and language-specific fields"
  - "CM/CMS maintenance-build release negotiation and supported trace enable syntax"
  - "Measured-domain administration, facility mapping and report database definitions"
related_docs:
  - "diagnostic-principles.md"
  - "contact-center.md"
  - "log-collection.md"
  - "aes-cti-jtapi.md"
  - "spi-protocol/index.md"
  - "spi-protocol/coverage.md"
  - "lessons/spi-protocol.md"
---

# SPI - CM/CMS Measurement Reporting Protocol

Shared CM/CMS reference for measurement events, translation mapping, transfer/rename continuity, and sent-versus-received trace comparison.
Vendor-document rules describe protocol behavior and capability. They do not establish the cause or outcome of an individual incident.
This reference covers selected message families, not the complete event catalog. Retain all intermediate SPI messages in the full capture (including QUEUED/DCON/DFWD/HOLD/RECON/COMP when present), and consult the applicable vendor layout for any message not covered below.
For CMS report/database-item definitions, refresh, storage intervals, and capacity, also consult [CMS reporting](contact-center.md#cms-r21-reporting-and-spi-diagnostics).

## Full-source library

This page is a curated topic guide, not the full protocol manual. Use the complete source library for message variants and material not selected below:

- [Full-page source index](spi-protocol/index.md): every page of the 253-page syntax specification and 28-page CM6 development test plan.
- [Message catalogue](spi-protocol/messages.md): all 180 catalogued message entries, including version, direction and source-page ranges.
- [CM6 test catalogue](spi-protocol/cm6-tests.md): all 85 Abstract Tests, preserved as test instructions and expected checks.
- [Coverage and source anomalies](spi-protocol/coverage.md): complete section/page coverage and unresolved source contradictions.

The library includes byte-identical copies of both original PDFs and searchable text for every physical page. The original PDFs remain authoritative for diagrams, tables and bitfield layout. Source commands are documentary data; their presence is never authorization to execute them.

For interpretation, identify the exact message version and direction, then read its full source section and all parent/continuation pages. Preserve source ambiguities and historical/current applicability boundaries; a selected guide entry does not replace the full definition.

<a id="spi-scope"></a>

## Scope and interfaces

- SPI here is the call-center switch/reporting-adjunct measurement protocol and CMS Switch Protocol Interpreter context, not embedded-hardware Serial Peripheral Interface.
- CM supplies measurement/administration events; CMS interprets them and maintains reporting state. The syntax specification also covers other reporting adjuncts with product exceptions (SPI-SYN24 p. 1).
- CMS uses `mis`; Avaya IQ uses `ccr`. Their reporting-adjunct release fields select the respective SPI language (CMS-CON21 p. 37).
- AES/ASAI/TSAPI/JTAPI/DMCC signaling can support call correlation but is not a replacement for the CMS-directed SPI sequence.
- CDR accounting links are a separate interface. Do not use generic `status cdr-link` advice to diagnose the CMS `mis`/SPI path.
- Preserve the distinction between physical trunk occupancy, an ITN's measured-call association, CMS database state, and the selected report's display.

<a id="spi-sources"></a>

## Sources and version boundaries

| Source ID | Bibliographic source | Applicability |
|---|---|---|
| SPI-SYN24 | *Call Center Protocol Specification for Switch / Reporting Adjunct Interface - Overview and Syntax of SPI Messages*, May 19, 2015, COMPAS ID 160965 | Header Issue 0.7 / footer Issue 1.0; language24 and predecessor layouts. Dated syntax baseline, not a current maintenance-build defect determination. |
| CMS-CON21 | *Avaya Call Management System and Communication Manager Connections, Administration, and Troubleshooting*, Release 21.0, Issue 2, November 2024 | Link administration and release-family compatibility; includes older-platform examples requiring applicability checks. |
| SPI-DTP6 | *Avaya Communication Manager 6.0 Call Center DTP: SPI Protocol Enhancements*, Issue 1.1, COMPAS ID 139877, cover April 10, 2010 | Historical CM 6.0 / CMS R16.1 / IQ 5.1 test plan; CMS/IQ requirements excluded (PDF pp. 1-2). |
| CMS-OV21 | *Avaya Call Management System Overview and Specification*, Release 21.0.2, Issue 4, June 2025 | Supporting R21 platform/security context. Product overview, not a defect-fix release note. |

All citations use PDF page numbers. SPI-SYN24 p. 1 directs detailed call-tree semantics to COMPAS ID 21003 and database definitions to a separate document.
Obtain the applicable CMS Database Items and Calculations / Supervisor Reports / Report Designer reference before deciding an exact field's expected behavior.
Do not extend historical/future capacity limits, message layouts, or test values to a current build without checking actual protocol support.
CM 10.x / CMS 20-21 release-family support is documented (CMS-CON21 p. 9); it does not certify every maintenance build or every call-flow outcome.

<a id="spi-language-pumpup"></a>

## Language selection, session establishment, and pumpup

- Check CM software/customer-options version, licensed Call Center Release, reporting-adjunct release, CMS ACD release administration, and actual wire language separately (CMS-CON21 pp. 35-37).
- `CMS (appl mis)` must identify the connected CMS release; blank means CMS is not connected. Do not copy the document's historical R18.1 example as a current target (CMS-CON21 p. 37).
- Verify the configured/advertised language during connection establishment; do not infer it from the CM marketing release alone.
- RTCS is the adjunct's initial request for translation change status and states its maximum measured-entity capacities; accepted capacity normally produces XSTAT and TIME (SPI-SYN24 p. 31, section 3.2.1).
- XFAIL, BUSYOUT or RCODE can reject establishment; investigate the actual response before interpreting an absent call event (SPI-SYN24 p. 31).
- XSTAT carries release/language and translation-change information. `c=1` requests full translations via RFTB; `c=0` normally allows RLTB logon/status refresh (SPI-SYN24 p. 36, section 3.2.5).
- Cleared adjunct shared memory requires RFTB regardless of `c`; a successful session alone does not substitute for required translation initialization (SPI-SYN24 p. 36).
- XSTAT24 defines release/language, vectoring/prompting/EAS flags and fault; the 2015 release/language values are historical examples, not an exhaustive CM10 table (SPI-SYN24 p. 38).
- SPI-DTP6 pp. 3-5 demonstrate that forced language23 against an older adjunct can make CMS spi.log interpretation inaccurate. Do not use its protocol-forcing commands as production repairs.
- Its XSTAT20 release2/language0x17 examples apply to CM6.0/CMSR16.1, not target settings for current CM/CMS releases.
- **TIME:** immediately follows XSTAT in the RTCS response; validates/sets adjunct time and keeps pumpup alive (SPI-SYN24 p. 39, section 3.2.6).
- TIME can appear inside translation blocks. The specification describes a two-minute liveness timeout and session reestablishment, not a screen refresh period (SPI-SYN24 pp. 24,39).
- **Full pumpup:** RFTB response runs from XOPEN block0 to XCLOSE block0; RLTB refresh surrounds logon/status with block5 and measured skill state with block6 (SPI-SYN24 p. 40, sections 3.2.7-3.2.8).
- **XOPEN:** starts a translation block; block2 identifies a trunk group's translations and is followed by one XTRUNK per member (SPI-SYN24 p. 41, section 3.2.9).
- Duplicate XTRUNK for one member can create duplicate adjunct rows and incorrect member reporting; the documented requirement is one record per member (SPI-SYN24 p. 41).
- **XCLOSE:** ends the block; the adjunct validates its count against received items. A discrepancy prevents establishment under the specified protocol until resolved (SPI-SYN24 p. 42, section 3.2.10).
- Enter DATA TRANSFER only after successful pumpup; call-processing messages are then sent continuously, in processed order, with buffering permitted (SPI-SYN24 pp. 24,137).
- TIME20 is the first call-processing message after pumpup and is sent every minute on the minute; subsequent `time_tag` values are seconds past that minute (SPI-SYN24 p. 137, section 3.4.1).
- Use TIME, date/time zone and event tags to align traces. A 59-to-0 minute rollover is not itself reversed event order; check the whole TIME-anchored sequence.
- The historical TIME definition distinguishes switch/Linux and adjunct/Java time-zone offset formats; validate sign conversion rather than assuming equal raw offsets (SPI-SYN24 p. 137).
- The specification describes timer names differently between session and call-processing sections; preserve the two-minute liveness behavior without prescribing an internal timer variable.

<a id="spi-itn-mapping"></a>

## Measured domain and ITN identity

- ITNs identify physical trunks and software facilities used for internal calls or transfers (SPI-SYN24 p. 21, Terminology).
- An old ITN going IDLE does not alone establish physical release of the original incoming circuit.
- A measured trunk belongs to a measured trunk group; CMS receives translations/events and collects trunk/group data (SPI-SYN24 p. 22).
- A measured trunk forwarded to an unmeasured extension still requires event notification and trunk data collection; the endpoint's agent data is not collected (SPI-SYN24 p. 23).
- An unmeasured IVR or endpoint alone does not explain disappearance of data for an unchanged measured incoming trunk.
- Unmeasured/software trunks can still be tracked for measured VDN/vector call data without trunk-group data (SPI-SYN24 p. 23).
- Map each relevant ITN through its translation pumpup and subsequent changes, including its physical/virtual member, trunk group and software role.
- XTRUNK records equipment location, trunk-group assignment, location-id and ITN; later messages refer to that ITN (SPI-SYN24 pp. 51-52, section 3.2.16).
- XTRUNK24 `t=0` means cabinet/carrier/slot/circuit; `t=1` means the virtual H.323/SIP trunk string. Do not decode virtual identity as a physical cabinet location.
- ARTRUNK24 carries add/remove `r=0/1`, ITN, trunk group and the same physical/virtual distinction (SPI-SYN24 pp. 65-66, section 3.3.8).
- Measured trunks cannot be changed/added/removed with active calls; when a group becomes measured with active calls, those existing calls remain treated as unmeasured-group calls (SPI-SYN24 p. 65).
- Verify mapping and measurement at call start; settings observed later do not prove the earlier call's measured domain.

<a id="spi-message-semantics"></a>

## SETUP, XFER, IDLE, TAUDIT, and CPERROR

**SETUP:** sent when a trunk is seized or a call first enters the measured domain; UCID is required at call start/measured-domain entry (SPI-SYN24 pp. 170-171, section 3.4.12).

| SETUP24 field | Documented meaning |
|---|---|
| `reason=0` | New contact, first message for a contact. |
| `reason=1` | Part of a RENAME. |
| `reason=2` | Adding a trunk; outflow is an example. |
| `reason=3` | LAR redirect. |
| `reason=4` | Converse-command connection to the IVR port. |
| `reason=5` | CTI phantom call. |
| `d` | 0 outbound; 1 inbound. |
| `u1/u2` | Presence of call UCID / parent held-call UCID fields. |
| `r` | Re-sent, still-active call returning with the same UCID after an abort; default 0. |
| `m` | Media-added ITN change through SIP INVITE with Replaces for ICR support; default 0. |

- For the documented `m=1` ICR/Replaces case only, SETUP is immediately followed by XFER(rename) and IDLE for the first ITN; all retain the original SETUP's UCID (SPI-SYN24 p. 171).
- Ordinary SIP-IVR routing does not prove ICR/Replaces or `m=1`. Verify signaling and SPI flags before applying this sequence.
- Other transfers can involve distinct call identities; identical UCIDs are not a universal XFER requirement.

**XFER:** instructs the adjunct to copy `xfer` status to `dest` and track as if the call arrived on `dest`; either facility can be measured/unmeasured or tracked/untracked (SPI-SYN24 pp. 234-237, section 3.4.43).

| XFER `type` | Documented meaning and boundary |
|---|---|
| 0 | Transfer. |
| 1 | Conference; both facilities tracked until one or both calls drop. |
| 2 | Special link; two physical trunks participate and neither drops. |
| 3 | Rename; two or more facilities drop and the call continues on `dest`. |
| 4 | Path replacement. |

- Inspect xfer/dest ITNs, each UCID, actual facility changes and initiating endpoint. `pnumber=0` means an unmeasured endpoint initiated transfer and no position is sent (SPI-SYN24 p. 237).
- Do not prescribe type2 solely because an incoming trunk remains occupied or treat type2/type3 as the only alternatives.

**IDLE:** sent when a facility goes idle (SPI-SYN24 p. 167, section 3.4.11). Interpret it against the mapped facility and preceding transfer/call state.

| IDLE23/24 `r_abort` | Documented abort/requeue context (SPI-SYN24 pp. 168-169) |
|---|---|
| 0 | No abort for later requeue; default. |
| 1 | Media/other resources unavailable when agent selected. |
| 2 | Wait time increased drastically. |
| 3 | Uninterruptible treatment still active after agent delivery. |
| 4 | Network failure recovery. |
| 5 | Voice Portal application failure. |
| 6 | Caller changed disposition through ICR. |

- An aborted call may return with the same UCID; nonzero `r_abort` is not an automatic physical-disconnect conclusion.

**TAUDIT:** periodic/on-request reconciliation with switch state; measured agents/facilities are audited every 10 minutes (SPI-SYN24 p. 213, section 3.4.34).

| TAUDIT24 state | Meaning (SPI-SYN24 p. 215) |
|---|---|
| 0 IDLE | Available for calls, in idle pool. |
| 2 QUEUED | Queued to a split. |
| 3 DCON | Connected to an agent position. |
| 6 MBUSY | Maintenance-busy. |
| 9 OTHER | SEIZED/DABN/DFWD/FBUSY/FDISC context; OTHER is acceptable. |
| 15 HOLD | On hold at an agent position. |

- An inconsistent audit can abort call tracking/initialize the facility and set trunk state UNKNOWN; inspect the logged discrepancy and later initializing event/audit (SPI-SYN24 p. 213).
- A periodic audit does not alone prove an earlier transition's timing. Correlate the same mapped facility and contemporaneous state.

**CPERROR:** adjunct-to-switch notification of a detected call-processing protocol violation; `err_opcode` identifies the offending switch message, with ITN and endpoint information (SPI-SYN24 p. 238, section 3.4.44).
- CPERROR is a reported violation, not automatic proof of a CM code defect; absence does not establish a correct event chain or correct decoder.

<a id="spi-trace-diagnosis"></a>

## Complete flow diagnosis (recommendations, not incident conclusions)

1. Define a failing call and a genuinely comparable control: incoming trunk, IVR transport, return path, endpoint, vector, measurement settings, report and operational requirement.
2. An H.323 final agent station after a SIP-IVR segment is not an H.323-IVR control. Verify the whole flow, not just endpoint labels.
3. Record precise timestamps, repeatability, physical CM occupancy and the displayed symptom; preserve successful and contrary samples.
4. Verify release administration, actual SPI language and the correct CMS `mis` channel; retain required translation blocks and changes.
5. Use the **complete CMS spi.log received-side flow** as the primary sequence for what CMS received. Verify logging coverage, rotations, TIME anchors and message continuity across the test.
6. Pair it with CM sent-side evidence. **Operator-provided collection convention:** CMS-directed SPI records are inspected in the MIS section of CM MST; this location is operational knowledge, not a claim proved by these PDFs.
7. Validate CM build/trace coverage. A general MST without relevant MIS records cannot establish that CM omitted a CMS message.
8. Align ingress, IVR transfer, return, connection and release by mapped ITNs, UCIDs, timestamps and per-link sequence numbers; account for buffering, minute boundaries and separate sessions.
9. Compare sent/received SETUP reasons/flags, XFER type and xfer/dest, IDLE/r_abort, TAUDIT, CPERROR, and mapping changes in order.
10. Identify the exact CMS event and database field transition; determine whether the continuing call is tracked on `dest` before judging old-ITN IDLE premature.
11. Compare database state against the actual report/filter/refresh at the same time. Database state and report refresh are different layers.
12. Explain an expected sequence with the applicable rule and matched samples; if unexpected, identify the first divergent layer or precisely missing evidence.

**Hypotheses to test:** incorrect CM event generation/mapping; incomplete transport or capture coverage; CMS mapping/transfer processing; report/filter/refresh behavior; or a valid logical-facility replacement unsuitable for the requested physical-occupancy view.
If a verified sent event is absent on the received side, separate transport loss from capture incompleteness. If the received chain is correct, separate CMS database processing from display/query behavior.
Resource/decoder causes need their own evidence. No default component blame follows from CMS showing the symptom.
Keep the mechanism unknown until trace/configuration evidence closes the alternatives; upgrades, restarts, protocol examples or administrative closure are not causal proof.

## Questions for CM/CMS engineering

- Which report/database field and applicable rule support an expected-behavior explanation, and what exact received event changed its state?
- How are old/new ITNs mapped and continuing calls tracked? Is ICR/Replaces actually present, or a different transfer/path replacement?
- Why do matched transport/control flows differ, or which differences prevent them from being valid controls?
- What is the first unexpected transition, or the exact missing evidence needed to decide? Distinguish a findings update from a promised fix.

<a id="spi-platform-boundaries"></a>

## Encrypted links, platforms, and collection boundaries

- CMS19.1+/CM8.1.2+ messaging is encrypted (CMS-CON21 p. 9; CMS-OV21 p. 29). Packet captures support timing/connectivity analysis, but encrypted payload is not assumed readable as SPI.
- Prefer supported endpoint traces or an authorized decryption method; do not disable production encryption merely to simplify diagnosis.
- CMS-CON21 pp. 55-60 provide CM/CMS link/network checks; these are not substitutes for full SPI event/translation evidence.
- Its p. 60 retains `snoop`, `spray`, `/usr/sbin/ndd /dev/tcp` and `/etc/defaultrouter` examples. CMS R21 runs on RHEL (CMS-OV21 p. 9); validate supported OS/build-specific equivalents rather than copying Solaris-style commands blindly.
- Logging enablement, collection toggles, configuration changes and restarts are separate operational actions requiring the applicable procedure and authorization.
- Preserve existing logs/configuration, use supplied evidence first and request only precisely identified missing material.
