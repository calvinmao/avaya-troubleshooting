# AES / CTI / JTAPI Troubleshooting Reference
<!--
scope: AES, JTAPI, TSAPI, CSTA, DMCC, CTI, park/unpark, TSCall lifecycle
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: AES version-specific TSCall.java line numbers, PostgreSQL version, Java heap defaults
related_docs: diagnostic-principles.md (invariants 3-16), lessons/aes-cti-jtapi.md
-->



## Table of Contents
- [AES Product Knowledge](#aes-product-knowledge)
- [CTI Developer Interfaces](#cti-developer-interfaces)
- [AES Service and Link Troubleshooting (Workflow 5)](#aes-service-and-link-troubleshooting)
- [JTAPI / CTI Integration Debugging (Workflow 2)](#jtapi--cti-integration-debugging)
- [Park / Unpark / Transfer / Conference Debugging (Workflow 7)](#park--unpark--transfer--conference-debugging)
- [AES Connector Race Condition (Workflow 8)](#aes-connector-race-condition)
- [Cross-Product Integration: CM <-> AES](#cross-product-integration-cm--aes)
- [AES Fault Patterns](#aes-fault-patterns)
- [CTI / JTAPI Fault Patterns](#cti--jtapi-fault-patterns)
- [AES Log Collection](#aes-log-collection)
- [JTAPI Client-Side Trace](#jtapi-client-side-trace)

---

## AES Product Knowledge

| Interface | Protocol | Transport | Use Case |
|-----------|----------|-----------|----------|
| **TSAPI** | CSTA over TCP | AES ↔ Third-party CTI | Call control, monitoring, snapshot |
| **JTAPI** | Java API (CSTA underneath) | AES ↔ Java CTI app | Call control, terminal/connection events |
| **CSTA** | ASN.1 / XML | AES ↔ Application | Device/call monitoring, snapshot, routing |
| **ASAI** | Proprietary (CM internal) | CM ↔ AES | Adjunct routing, call events, UCD/VDN |
| **DMCC** | CSTA + media control | AES ↔ Recording/QM | Call recording, silent monitoring |
| **AE Services REST** | HTTPS/REST | AES ↔ Web apps | Token-based call/device management |

AES Logs: `getlogs` (csta_trace, g3trace, tsapi_trace, jtapi_trace), common trace

---

## CTI Developer Interfaces

| Interface | Protocol | Transport | Use Case |
|-----------|----------|-----------|----------|
| **TSAPI** | CSTA over TCP | AES ↔ Third-party CTI | Call control, monitoring, snapshot |
| **JTAPI** | Java API (CSTA underneath) | AES ↔ Java CTI app | Call control, terminal/connection events |
| **CSTA** | ASN.1 / XML | AES ↔ Application | Device/call monitoring, snapshot, routing |
| **ASAI** | Proprietary (CM internal) | CM ↔ AES | Adjunct routing, call events, UCD/VDN |
| **DMCC** | CSTA + media control | AES ↔ Recording/QM | Call recording, silent monitoring |
| **AE Services REST** | HTTPS/REST | AES ↔ Web apps | Token-based call/device management |

---

## AES Service and Link Troubleshooting

**Workflow 5: AES Service and Link Troubleshooting**

```
Step 1 — Check AES Service Status
  AE Services web console → Status → Services
  Verify: CTI Link, TSAPI Link, JTAPI Link, DMCC Link, ASAI Link

Step 2 — Check CM Link Status (from AES)
  AES CLI: status cti-link <n>
  AES CLI: status asai-link <n>
  From CM: status essver (AES registration)
  From CM: display signal-group (AES signaling)

Step 3 — Check AES Logs
  getlogs collection:
    - g3trace: CM ASAI message content
    - csta_trace: CSTA events sent to applications
    - tsapi_trace: TSAPI protocol between AES and apps
    - jtapi_trace: JTAPI SDK internal processing
    - common trace: full AES debug (for PEA creation)

Step 4 — Common AES Issues
  - CTI link flapping: TCP keepalive, CM switchover, network
  - CSTA events delayed: AES queue buildup, CPU/memory pressure
  - JTAPI null addresses: TSCall lifecycle, ASAI timing (see Workflow 2)
  - Snapshot returns incomplete data: CM merge timing issue
  - AE Services won't start: license, database, certificate issues
```

---

## JTAPI / CTI Integration Debugging

**Workflow 2: JTAPI / CTI Integration Debugging**

```
Step 1 — Confirm Environment
  - AES version, JTAPI SDK version (must match AES major.minor)
  - AES service status: CTI, TSAPI, JTAPI, DMCC links
  - CM link status: ASAI links up, CSTA links up
  - JTAPI provider registration: check user/password/extension mapping
  *** CRITICAL: If JTAPI SDK major.minor differs from AES, TSCall object
      lifecycle behavior may differ. Always test with matched versions first.

Step 2 — Collect JTAPI Trace
  Application-side trace (if available):
    - Enable JTAPI SDK trace: com.avaya.jtapi.tsapi.TsapiTrace=true
    - Capture TSCall, TSConnection lifecycle events
  AES-side trace:
    - getlogs with debug level: csta_trace, g3trace, tsapi_trace

Step 3 — Analyze JTAPI Object Lifecycle (CRITICAL)
  Key objects to track:
    - TSCall[callID]@<hashcode> — note the hashcode to detect reconstruction
    - TSConnection[conn:(callID,address)] — state transitions
    - TSProvider — registration, link status

  TSCall Object Reuse vs Reconstruction (most common root cause):
    REUSE indicator: Same @hashcode across events
      → TSCall[5738]@5e0dc17a appears at MakeCall AND first unpark
      → Object retains cached TSConnection objects from original call
      → getCalledAddress() returns data from cached Connections

    RECONSTRUCTION indicator: New @hashcode with same callID
      → TSCall[5738]@5e0dc17a deleted, later TSCall[5738]@8d7c597 constructed
      → Fresh object built from CSTASnapshotCallConfEvent only
      → If snapshot response lacks external party, new object lacks it too
      → getCalledAddress() returns null — no cached data exists

  Trace evidence patterns to search for:
    Object reuse:    "Dumping Call TSCall[NNNN]@SAMEHASH"
    Object deletion: "Call object= TSCall[NNNN]@HASH being deleted"
    Object creation: "Constructing call TSCall[NNNN]@NEWHASH"
    Connection loss: "TSConnection[conn:(NNNN,EXTERNAL_NUMBER)] being deleted"
    Audit cleanup:   "AUDIT: removing call TSCall[NNNN]@HASH"

  *** When TSCall is deleted, ALL TSConnection objects are destroyed.
      This means every cached address (external number, trunk, extensions)
      is irrecoverably lost. A new TSCall for the same callID starts empty.

Step 4 — Map CSTA Events to Application Events
  CSTAEstablishedEvent → ConnectionEvent → Application callback
  Verify: cause code, callingDevice, calledDevice, originalCallInfo
  Check: UCID propagation across call legs

  CRITICAL — Three Distinct Operations (do NOT conflate):
  | Operation | Type | Network? | Data Source |
  | getCallingAddress() | Local Java getter | No | Historical ANI in TSCall memory |
  | Call.getConnections() | Local Java getter | No | Connection list in same TSCall |
  | cstaSnapshotCallReq | CSTA network request | Yes | Queries CM real-time call state |

  All three may return different results. A null from getCallingAddress()
  does NOT mean cstaSnapshotCallReq will also return null (and vice versa).

Step 5 — Identify Data Loss Point Using Cross-Layer Analysis
  If getCallingAddress()/getCalledAddress() returns null, check THREE layers:

  Layer A — CM ASAI (check g3trace):
    - What does CM actually send? (calling_num, called_num, connect_num)
    - What is the addr_type/numb_plan? (7=internal, other=external)
    - Is the external number present in ANY ASAI field?
    - Compare MULTIPLE events (initial call vs unpark) for differences

  Layer B — AES CSTA Mapping (check csta_trace):
    - How does AES map the ASAI data to CSTA fields?
    - Are internal extensions mapped to answeringDevice/lastRedirectionDevice
      instead of callingDevice/calledDevice?
    - What cause code is set? (EC_NEW_CALL vs EC_PARK changes mapping rules)
    - What is deviceIDType and deviceIDStatus for null fields?

  Layer C — JTAPI SDK (check jtapi_trace):
    - Is TSCall reused or reconstructed? (check @hashcode)
    - Does the connections list include the external number TSConnection?
    - Was the external number TSConnection deleted before this event?

  *** Use the "Evidence Chain Validation" technique:
      For each call event, build a table across all three layers showing
      the SAME field (e.g., calledDevice) and identify where it diverges.

Step 6 — Workaround Design
  Primary: UCID-based cache recovery
    - Cache external number keyed by UCID when first available
    - Recover on null-address events by looking up UCID in cache
    - UCID extraction: MUST use outer LucentPrivateData.ucid
      (originalCallInfo.ucid is always "00000000000000000000" — zeroed)
    - UCID is stable across all park/unpark/transfer cycles

  Secondary: Delayed CSTASnapshotCall request (1-2s after event)
    - Only useful if CM completes call merge AFTER the initial event
    - MUST be empirically tested — trace evidence may show that even
      the automatic snapshot returns incomplete data
    - Do NOT assume delayed snapshot will help; verify with trace data

  Tertiary: Application-level fallback handling

  NOT RECOMMENDED:
    - Retrying getCallingAddress() on the same Call object — it reads
      from the same empty in-memory cache; no network request is made
    - Relying on SDK automatic snapshot — may return same incomplete data
```

---

## Park / Unpark / Transfer / Conference Debugging

**Workflow 7: Park / Unpark / Transfer / Conference Feature Debugging**

```
Step 1 — Understand the Call Flow
  Document exact sequence:
    - Who initiates, who is involved, which feature is invoked
    - Park: call park code, park extension
    - Transfer: consultative vs blind
    - Conference: add vs join

Step 2 — Identify Transfer Type from CSTA Trace (CRITICAL)
  The transfer type can be definitively determined from the CSTA trace:

  CONSULT TRANSFER evidence:
    - CSTA message: CSTATransferCall (NOT SingleStepTransferCall)
    - Request structure contains BOTH heldCall AND activeCall
    - Confirmed by: TransferredEvent with primaryOldCall + secondaryOldCall

  BLIND TRANSFER evidence:
    - CSTA message: CSTASingleStepTransferCall (NOT CSTATransferCall)
    - Single call leg, no held/active distinction
    - No consultMode parameter present

  IMPORTANT: If the customer claims blind transfer but the trace shows
  CSTATransferCall, it is actually a consult transfer. The SIP client
  (Avaya IX Workplace / StationLinkWeb) may internally perform a consult
  transfer even when the UI shows "blind transfer" option.

Step 3 — Collect Full Call Lifecycle Traces
  - CM list trace for all involved stations from call start to end
  - AES getlogs covering entire call duration
  - JTAPI trace covering all Call/Connection events
  - Workplace/SIP client logs (if available) for SIP INVITE/BYE sequencing

Step 4 — Measure CSTA Event Timing (Critical for Race Condition Analysis)
  For transfer-related issues, measure the time between key CSTA events:
  a) Find the relevant call in csta_trace
  b) Extract event timestamps with millisecond precision:
     DeliveredEvent (call arrives at destination) → EstablishedEvent (answer)
     The gap between these events = the "race condition window"
  c) If an AES Connector / JTAPI app queries GetCallInfo during this window,
     the call is in "Delivered" (not "Established") state → error occurs

  CRITICAL: When Vector wait-time = 0, this race window is exposed because
  the vector executes immediately. Setting wait-time = 1 provides ~5x margin.

Step 5 — Track UCID Across the Call
  UCID must remain consistent across initial call, all park/unpark cycles,
  transfers, conference additions. If UCID changes, identify which product
  changed it and why.

Step 6 — Track CallID / CRV at Each Layer
  CM CallID (numeric) → AES internal tracking → CSTA callID
  Watch for: CallID reuse after call clear, CRV assignment changes

Step 7 — Compare Event Data Across Layers
  For each feature event:
    - What does CM ASAI report? (g3trace)
    - What does AES CSTA report? (csta_trace)
    - What does JTAPI SDK expose? (jtapi_trace)
    - What does the application see? (application log)
  Identify the layer where data is lost or transformed

Step 8 — AES ASAI-to-CSTA Field Mapping Rules (CRITICAL)
  For EC_NEW_CALL (initial call establishment):
    ASAI calling_num → CSTA callingDevice (deviceIDType=IMPLICIT_PUBLIC)
    ASAI called_num  → CSTA calledDevice  (deviceIDType=IMPLICIT_PUBLIC)
    ASAI connect_num → CSTA answeringDevice
    trunk info       → LucentPrivateData.trunkGroup/trunkMember
    originalCallInfo → populated (callingDevice, calledDevice, ucid)

  For EC_PARK (unpark/retrieval events):
    ASAI calling_num → does NOT map to CSTA callingDevice
    ASAI called_num  → does NOT map to CSTA calledDevice
    ASAI connect_num → CSTA answeringDevice (ID_PROVIDED)
    ASAI callingDev  → CSTA lastRedirectionDevice (ID_PROVIDED)
    callingDevice    → null, deviceIDType=IMPLICIT_PUBLIC, ID_NOT_KNOWN
    calledDevice     → null, deviceIDType=IMPLICIT_PUBLIC, ID_NOT_KNOWN
    trunk info       → null
    originalCallInfo → all fields null, ucid zeroed

  KEY INSIGHT: In EC_PARK events, AES deliberately reserves callingDevice
  and calledDevice for the ORIGINAL external parties. Since CM ASAI only
  provides internal extension numbers for unpark events, AES has no data
  for these fields and sets them to ID_NOT_KNOWN.

Step 8a — CM System-Features SA9114/SA9124 (ROOT CAUSE for Park/Unpark)
  *** This is the most common root cause for "unknown number on unpark" ***

  When SA9114/SA9124 is DISABLED (default):
    CM ASAI snapshot → returns trunk placeholder (T####, deviceIDType 30)
    → JTAPI getCalledAddress() returns T#### (unusable)

  When SA9114/SA9124 is ENABLED:
    CM ASAI snapshot → returns actual external party number
    → JTAPI getCalledAddress() returns usable number

  How to enable: CM SAT: change system-features → SA9114: y, SA9124: y
  Live-changeable — NO CM restart required.

  Good vs Bad comparison:
  | Layer | SA Disabled (Bad) | SA Enabled (Good) |
  | CM ASAI | T####, type 30 | actual number, type 31 |
  | AES CSTA | passes T#### through | passes actual number |
  | JTAPI 1st unpark | works via SDK cache (accidental) | works via snapshot |
  | JTAPI 2nd+ unpark | FAILS — only T#### | works — snapshot has real number |

Step 8b — JTAPI SDK Internal Mechanism: connBelongToDifferentDeviceIDType Flag
  *** Per SR 1-23524018078, the SDK-level mechanism is now precisely known ***

  The cascade from "T#### snapshot" to "TSCall destruction" works as follows:

  (1) Snapshot returns deviceOnCall T#### (deviceIDType=30 PUBLIC_UNKNOWN)
      with localConnectionState=CS_NONE (-1) for outbound trunks specifically.

  (2) SnapshotCallConfHandler.handleConf() (bytecode PC 1019-1067) calls:
      device = createDevice(extDevID, callIdentifier);
      if (device.isForExternalDeviceMatchingLocalExtensionNumber(extDevID)) {
          // PATH A: trunk's TSDevice has PRIVATE history vs current PUBLIC
          conn = createConnection(callId, device, null);
          conn.setDoNotExpectConnectionClearedEvent(true);  // ★ FLAG SET
      } else {
          // PATH B: no flag (Inbound trunks fall here because they're recreated fresh)
          conn = createTerminalConnection(...);
      }

  (3) The check (TSDevice.java:2834):
      isForExternalDeviceMatchingLocalExtensionNumber returns true when:
        - TSDevice.devNameVector.lastElement() has PRIVATE deviceID type, AND
        - Current snapshot devIDOnCall has PUBLIC deviceID type

  (4) On the NEXT ConnectionCleared event (e.g., 2nd park), TSEventHandler:
      if (allConnections.equals(listOfConnsBelongToDiffDevIDType)) {
          // ALL remaining connections have flag → batch clear
          for each conn: setConnectionState(89);  // → DISCONNECTED
      }

  (5) Batch clear → connections.size()==0 → setState(34) INACTIVE → TSCall.delete()
      → calledDevice/callingAddress fields destroyed → next unpark returns null.

  Diagnostic log signatures (search jtapi_trace for these exact strings):
    "setting flag 'connBelongToDifferentDeviceIDType'"
       → Flag was just set; downstream TSCall destruction is now fated.
       → Always on T#### connections, only in Outbound park scenarios.
    "has 'connBelongToDifferentDeviceIDType' flag set. Clearing connection."
       → Batch clear is firing; TSCall about to be destroyed.
    "Call object= TSCall[NNNN]@HASH being deleted"
       → TSCall.delete() executed; cached fields are gone.
    "Constructing call TSCall[NNNN]@DIFFERENT_HASH"
       → New TSCall for same callID; calledDevice/callingAddress = null.

  Outbound vs Inbound differential signature (use to identify scenario):
    Outbound trunk T#### in unpark snapshot:
      localConnectionState = -1 (CS_NONE)
      → setStateFromLocalConnState(-1) maps to internal 91 → public state 54 UNKNOWN
    Inbound trunk T#### in unpark snapshot:
      localConnectionState = 3 (CS_CONNECT)
      → setStateFromLocalConnState(3) maps to internal 88 → public state 51 CONNECTED
    Note: state 54 vs 51 is a SIDE EFFECT of CM's representation, NOT the cause
    of TSCall destruction. The flag (set by deviceID type heuristic) is the cause.

  KEY CORRECTION (vs older reports):
    "TSConnection caching" is NOT the mechanism for first-unpark success.
    The actual mechanism is TSCall.calledDevice FIELD persistence:
      - Set once in EC_NEW_CALL via setCalledDevice(non-null TSDevice)
      - Never updated by EC_PARK because setCalledDevice(null) is no-op (null guard)
      - Persists as long as the TSCall object lives
      - getCalledDevice() returns this.calledDevice directly — does NOT iterate
        Connections list

Step 8c — Verification Signals for SA9114/SA9124 Effectiveness
  After enabling SA, capture a new trace and verify all 6 signals flip:

  | Signal | Before SA (Bad) | After SA (Good) |
  | Snapshot deviceID for trunk | "T####" | actual number "0909..." |
  | Snapshot deviceIDType for trunk | 30 EXPLICIT_PUBLIC_UNKNOWN | 31 EXPLICIT_PUBLIC_INTERNATIONAL |
  | Snapshot localConnectionState | -1 CS_NONE | 3 CS_CONNECT |
  | "setting flag 'connBelong...'" log | present on every Outbound unpark | absent |
  | "has flag set. Clearing connection." log | present at 2nd park | absent |
  | "TSCall[NNNN] being deleted" between 2nd park and 2nd unpark | present | absent |

  All 6 signals flipping = root cause confirmed and fix verified.
  Partial flip = there may be additional CM configuration affecting trunk state
  reporting independently of SA9114/SA9124 — escalate to BBE.

Step 8d — Application-Layer UCID Cache Implementation
  Even with SA enabled, recommended as defense-in-depth. Per JTAPI spec
  (CallControlCall.getCalledAddress official documentation):
    "Each of these methods returns null if their values are unknown at the
     present time."  — null is SPEC-COMPLIANT, not a SDK bug.
  Application MUST handle null returns safely.

  Official UCID extraction path (from LucentV5CallInfo.getUCID() Javadoc):
    "may be cast to LucentV5CallInfo to use the getUCID() method"

    if (event instanceof LucentV5CallInfo) {
        ucid = ((LucentV5CallInfo) event).getUCID();
    }
    // Do NOT use event.getOriginalCallInfo().getUCID() — always zeroed in EC_PARK

  Cache strategy:
    Time 1: On EC_NEW_CALL Established event — store {ucid → externalNumber}
    Time 2: On EC_PARK with null calling/called — fallback lookup by UCID
    Time 3: On final ConnectionCleared (cause=EC_NORMAL) — purge entry

Step 9 — Number Format Normalization
  Same external number may appear in different formats across layers.
  Normalize: strip trunk access codes (9, 09), CM-internal prefixes,
  extract canonical digits based on number plan.

Step 10 — Known Platform Behaviors
  - CM ASAI events may fire before call merge completes
  - JTAPI SDK may destroy and recreate TSCall objects across park cycles
  - Second/third park-unpark may lose cached data in JTAPI SDK
  - First unpark "working" may be JTAPI SDK caching accident
  - SA9114/SA9124 is the root cause — always check system-features FIRST
  - deviceIDType is the key diagnostic: 30=UNKNOWN (trunk placeholder),
    31=INTERNATIONAL (actual number)
```

---

## JTAPI SDK Bytecode Reverse Engineering

**Workflow 8b: When Java Source Decompilation Fails**

When CFR or other decompilers fail on a critical SDK method (typically reported as
`ConfusedCFRException: Started 2 blocks at once`), use Python `javatools` for direct
bytecode disassembly. Per SR 1-23524018078, this technique recovered
`SnapshotCallConfHandler.handleConf()` (2316 bytes, ~230 source lines) when CFR failed.

```
Step 1 — Identify the method that failed
  Check the decompiler's `summary.txt` for entries like:
    com.avaya.jtapi.tsapi.impl.core.SnapshotCallConfHandler
      handleConf(com.avaya.jtapi.tsapi.csta1.CSTAEvent)
        Exception : org.benf.cfr.reader.util.ConfusedCFRException: Started 2 blocks at once
  This indicates CFR could not produce Java source — but the .class file is intact.

Step 2 — Install javatools (Python)
  pip install javatools

Step 3 — Disassemble bytecode with constant pool resolution
  Use this script as starting point:

    from javatools import unpack_classfile, opcodes as ops

    OPCODE_NAMES = {getattr(ops, n): n[3:] for n in dir(ops) if n.startswith('OP_')}

    cls = unpack_classfile(r'path/to/Class.class')
    cpool = cls.cpool
    method = [m for m in cls.methods if m.get_name() == 'methodName'][0]
    code = method.get_code()
    lnt_dict = dict(code.get_linenumbertable() or [])

    for entry in code.disassemble():
        offset = entry[0]
        opcode = entry[1]
        args   = entry[2] if len(entry) > 2 else ()
        mnem   = OPCODE_NAMES.get(opcode, f"op_{opcode}")
        line   = lnt_dict.get(offset)
        # Resolve constant pool refs:
        if mnem in ('invokevirtual','getfield','putfield','new','ldc',...) and args:
            resolved = cpool.pretty_deref_const(args[0])
            print(f"{offset}: {mnem} {resolved}")
        else:
            print(f"{offset}: {mnem} {args}")

Step 4 — Map LocalVariableTable to friendly names
  Each LVT entry: (start_pc, length, name_idx, desc_idx, var_index)
  Use cpool.get_const(name_idx) to retrieve variable name as string.
  This makes aload/astore opcodes readable as "// device", "// extDevID" etc.

Step 5 — Reconstruct Java pseudocode from disassembly
  Look for these patterns:
    if-else:           ifeq <target> ... goto <after_else> ... <else_body>
    method call:       invokevirtual <className>.<methodName><signature>
    field access:      getfield/putfield <className>.<fieldName>
    object creation:   new <className> ... dup ... invokespecial <init>

Step 6 — Validate reconstruction against trace
  Cross-check log messages emitted by your reconstructed code path against
  the actual jtapi_trace. If both match, the reconstruction is sound.

Tools and Documentation Sources:
  - CFR (primary): java -jar cfr.jar <jar_or_class>
  - javatools (fallback): pip install javatools
  - Avaya JTAPI Javadoc: typically at C:/jtapi-sdk/javadoc/
    Use this to validate reconstructed method signatures match official API.
  - AE Services JTAPI for Communication Manager Programmer's Reference:
    Document at support.avaya.com — describes Avaya private data versions.
```

---

## AES Connector Race Condition

**Workflow 8: AES Connector Race Condition Troubleshooting**

```
Step 1 — Confirm the Error Pattern
  - Error occurs in: AES Connector application log (NOT in AES getlogs)
  - Error message: "call on extension:XXXX was never established or never on hold"
  - AES CSTA trace: shows NORMAL call flow (no errors)

Step 2 — Determine Transfer Type
  Search CSTA trace for CSTATransferCall or CSTASingleStepTransferCall

Step 3 — Measure the Race Condition Window
  From CSTA trace, find millisecond timestamps for the IVR port extension:
  Race window = (Established ms) - (Delivered ms)
  Typical values: 100-300ms

Step 4 — Check Vector wait-time Setting
  When wait-time = 0: Vector executes immediately → race condition
  When wait-time = 1: 1 second delay ensures Established fires first
  Recommended: wait-time 1 seconds (integer only, no decimals)

Step 5 — Compare Success vs Failure Cases
  Success: INVITE → 487 Request Terminated (no 180 Ringing)
  Failure: INVITE → 180 Ringing → BYE → 487 Request Terminated

Step 6 — Recommend Resolution
  Primary fix: Set Vector wait-time from 0 to 1
  Optional: Add retry logic in AES Connector (delay 500ms, retry 2-3 times)
```

---

## Cross-Product Integration CM <-> AES

```
Protocol:    ASAI over TCP
AES Service: CTI Link Manager
CM Service:  ESS/VER (Valued Endpoint Registration)

Data Flow:
  CM Call Event → ASAI Message → AES TSAPI → CSTA/JTAPI → Application

Key Fields:
  calling_num, called_num, connect_num → CSTA callingDevice, calledDevice
  callID → CSTA callID (may be remapped)
  UCID → LucentPrivateData.ucid

CM System-Features Controlling ASAI Behavior:
  SA9114/SA9124 — External party identification in ASAI snapshot
    When DISABLED: CM returns trunk placeholder for external party
    When ENABLED: CM returns actual external party number
    How to check: display system-features → look for SA9114 and SA9124
    How to change: change system-features → SA9114: y, SA9124: y (live, no restart)
    *** Always check these SAs FIRST when troubleshooting "unknown number on unpark"
```

---

## AES Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **CTI link cycling** | Links up/down repeatedly | CM switchover, network issue, TCP keepalive timeout | Check CM status, network stability, TCP settings |
| **AES Connector race condition** | "call on extension:XXXX was never established or never on hold" | Race condition: GetCallInfo BEFORE EstablishedEvent fires. Caused by Vector wait-time = 0 | Set Vector wait-time to 1 second |
| **AES Connector ANI = AgentID** | IVR receives agent extension as ANI instead of customer number | CM default: transferor becomes originator | Enable "Retain Original Calling Number on Transfer/Forward" |
| **crossID exhausted** | AES cannot establish new cross-references | Cross-reference ID pool depleted | Restart AES services to reset crossID pool (per `1-18125845232`) |
| **HA sync issue** | AES HA pair out of sync | HA replication channel broken | Check HA sync status; manually resync (per `1-19910774792`) |
| **PostgreSQL service stopped** | MAJ alarm, CTI services down | PostgreSQL crash: disk full, corrupt WAL, OOM | Check disk space, restart PostgreSQL (per `1-17013543201`) |
| **Tomcat out-of-heap-memory** | AES web console slow/unresponsive | Java heap exhaustion | Increase Tomcat heap; check for memory leaks (per `1-17384352722`) |
| **CPU 100% usage alarm** | Services degraded | Runaway process, excessive tracing | Disable debug tracing, check for runaway processes (per `1-16977852323`) |
| **License error after deleting default cert** | License enters error mode | Deleting default server cert breaks internal TLS | Do NOT delete default cert; re-import if deleted (per `1-19844950102`) |
| **DMCC weak cipher alarm** | Security scan reports weak ciphers | DMCC supports deprecated cipher suites | Apply cipher hardening per Avaya security advisory (per `1-20221132752`) |

---

## CTI / JTAPI Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **SA9114/SA9124 disabled** | getCalledAddress returns T#### on unpark | CM returns trunk placeholder instead of actual number | Enable SA9114 and SA9124 via change system-features |
| **TSCall reconstruction** | getCalledAddress returns null on second unpark | JTAPI SDK destroys and recreates TSCall object | Fix root cause (enable SA9114/SA9124). UCID cache as workaround |
| **`connBelongToDifferentDeviceIDType` flag triggered** | "setting flag" log on Outbound trunk during 1st unpark; "Clearing connection" log at 2nd park; TSCall destroyed | SnapshotCallConfHandler.handleConf detects PRIVATE→PUBLIC deviceID type change on existing trunk TSDevice → sets flag → batch-clear at next ConnectionCleared | Enable SA9114/SA9124 (changes snapshot devID, eliminates type mismatch); UCID cache as defense-in-depth (per `1-23524018078`) |
| **TSCall.calledDevice field persistence misconception** | Engineer assumes "TSConnection cache" enables first-unpark success | Wrong mechanism — `getCalledDevice()` reads field directly (TSCall.java:784), not Connections | TSCall.calledDevice is a FIELD set once via setCalledDevice(non-null); EC_PARK passes null which is no-op due to null guard (per `1-23524018078`) |
| **getCalledAddress null is spec-compliant** | App treats null return as SDK bug | Per JTAPI Programmer's Reference (CallControlCall.html): "Each of these methods returns null if their values are unknown at the present time" | Application MUST handle null safely; not an SDK bug |
| **OriginalCallInfo unfilled in EC_PARK PEA rejected** | PEA requesting AES to fill originalCallInfo for park returned | OriginalCallInfo per official Javadoc: "made available in conjunction with the consult() service" — designed for consult, not park | Do not file PEAs requesting OriginalCallInfo extension for park scenarios; use SA9114/SA9124 path instead |
| **UCID extraction wrong field** | originalCallInfo.ucid = all zeros | Wrong API path | Use `event.getUCID()` after `cast LucentV5CallInfo` (official Javadoc-recommended path); do NOT use `event.getOriginalCallInfo().getUCID()` |
| **CS_NONE vs CS_CONNECT diagnostic signal** | Same Outbound vs Inbound park scenario, different SDK behavior | CM reports localConnectionState=-1 (CS_NONE) for Outbound trunks vs 3 (CS_CONNECT) for Inbound trunks in unpark snapshots → maps to JTAPI state 54 vs 51 | This is a DIAGNOSTIC signal not a cause; the flag mechanism is the actual cause. Use as additional verification dimension (per `1-23524018078`) |
| **EC_PARK mapping** | callingDevice/calledDevice null but answeringDevice populated | AES design for EC_PARK events | Application-level recovery using UCID cache |
| **JTAPI SDK version mismatch** | Unexpected TSCall lifecycle | SDK version differs from AES | Match SDK version to AES version |
| **First-unpark success is accidental** | Works on 1st, fails on 2nd | Both receive identical CSTA data; 1st works via TSCall.calledDevice field persistence (not Connection cache) | Check SA9114/SA9124 first |
| **getCallingAddress() retry ineffective** | Retrying returns same null | Local in-memory read; no network request | Enable SA9114/SA9124 or use UCID cache |
| **CFR fails on SnapshotCallConfHandler.handleConf** | "ConfusedCFRException: Started 2 blocks at once" | Decompiler bug, not bytecode issue | Use Python javatools for direct bytecode disassembly (see Workflow 8b, per `1-23524018078`) |

---

## AES Log Collection Procedures

### Enabling Trace Logging (via OAM)

**TSAPI Service:**
1. OAM → Status → Log Manager → Trace Logging Levels
2. Locate TSAPI Service → select "Everything on except mutex"
3. Click Apply Changes → Apply

**DMCC Service:**
1. OAM → Status → Log Manager → Trace Logging Levels
2. For DMCC Service, set **Finest** for ALL fields: Default, XML, Java, Call Control Logging
3. Click Apply Changes

**Transport Layer:**
1. OAM → Status → Log Manager → Trace Logging Levels
2. Transport Layer Service → "Everything on except mutex"
3. Click Apply Changes → Apply

**SMS (System Management Service):**
1. OAM → AE Services → SMS → SMS Properties
2. SMS Logging: Verbose; CM Proxy Trace Logging: Normal or Verbose
3. Apply Changes
4. SSH as root, edit `/opt/mvap/web/sms/saw.ini`:
   ```ini
   [Dev]
   tpl_debug=true
   tpl_session=true
   dev_commands=true
   msg_console=true
   msg_debug=true
   msg_log=true
   ```

**CVLAN / DLG:** OAM → Status → Log Manager → Trace Logging Levels → set service level

### AES Server-Side Log Paths

| Service | Files | Path |
|---------|-------|------|
| TSAPI | csta_trace.out, g3trace.out | /var/log/avaya/aes/TSAPI/ |
| DMCC | dmcc-api.log, dmcc-error.log, dmcc-trace.log | /var/log/avaya/aes/ |
| CVLAN | trace.out | /var/log/avaya/aes/CVLAN/ |
| DLG | trace.out | /var/log/avaya/aes/DLG/ |
| Transport | trace.out | /var/log/avaya/aes/trans_serv/ |
| System | mvap.log, sec.log, cmd.log, reset.log | /var/log/avaya/aes/ |
| TWS | ws-telsvc-*.log | /var/log/avaya/aes/tomcat/ |
| SMS/CM Proxy | ossicm.log | /var/log/avaya/aes/ |
| Common trace | trace.out | /var/log/avaya/aes/common/ |

### Client-Side Traces

| Client | Method |
|--------|--------|
| TSAPI Windows | TSAPI Spy → Options → "Log To File" + "Log Trace Messages" |
| TSAPI Linux | `export CSTATRACE=<filename>` before running app |
| JTAPI | Configure log4j.properties for DEBUG level |

### Log Retention
OAM → Status → Log Manager → Log and Trace Retention → 0–180 days → Apply

---

## AES Log Collection

```bash
# Login to AES CLI (SSH)
ssh admin@<aes-ip>

# Collect all logs
getlogs

# Collect specific debug logs
getlogs -d

# Output location on AES
/var/log/avaya/
  ├── csta_trace*.log     # CSTA events to/from applications
  ├── g3trace*.log        # ASAI messages between AES and CM
  ├── tsapi_trace*.log    # TSAPI protocol logs
  ├── jtapi_trace*.log    # JTAPI SDK processing logs
  └── common*.log         # Full AES debug (verbose, for PEA)
```

---

## JTAPI Client-Side Trace

```properties
# Enable in application VM arguments or trace properties
com.avaya.jtapi.tsapi.TsapiTrace=true
com.avaya.jtapi.tsapi.TsapiTraceLevel=DEBUG

# Trace file location
./jtapi_trace_<date>.log or configured path
```

### JTAPI Trace Analysis Quick Reference

```
Key search patterns:

1. TSCall lifecycle tracking:
   grep -n "TSCall\[.*\]@" jtapi_trace.log | grep -i "constructing\|deleted\|dumping"

2. TSConnection tracking for specific callID:
   grep -n "conn:(5738," jtapi_trace.log | grep -i "constructing\|deleted"

3. CSTA event dumps:
   grep -n "CSTAEstablishedEvent\|CSTASnapshotCallConfEvent" jtapi_trace.log

4. CSTA field-level details (null detection):
   grep -n "deviceID <null>\|ID_NOT_KNOWN\|IMPLICIT_PUBLIC" jtapi_trace.log

5. Private data / UCID extraction:
   grep -n "ucid\|LucentV.*EstablishedEvent" jtapi_trace.log

6. Snapshot request and response:
   grep -n "CSTASnapshotCall\|CSTASnapshotCallConfEvent" jtapi_trace.log

7. Audit thread cleanup:
   grep -n "AUDIT.*removing" jtapi_trace.log

Critical trace fields per event:

  CSTAEstablishedEvent:
    - establishedConnection: { callID, deviceID, devIDType }
    - answeringDevice: { deviceID, deviceIDType, deviceIDStatus }
    - callingDevice: { deviceID, deviceIDType, deviceIDStatus }
    - calledDevice: { deviceID, deviceIDType, deviceIDStatus }
    - lastRedirectionDevice: { deviceID, deviceIDType, deviceIDStatus }
    - cause: EC_NEW_CALL / EC_PARK / EC_NONE

  LucentPrivateData:
    - trunkGroup, trunkMember (present in initial call, null in unpark)
    - originalCallInfo.callingDevice/calledDevice/ucid
    - ucid (outer level — the REAL UCID)

  CSTASnapshotCallConfEvent:
    - Each deviceOnCall: { deviceID, deviceIDType, deviceIDStatus }
    - localConnectionState: CS_CONNECT / CS_NONE

  TSCall object:
    - @hashcode: same = reuse, different = reconstruction
    - connections list: TSConnection[conn:(callID,address)] with state
```

---

## AES Server Health & Database Diagnostics (IT Ops Patterns)

Adapted from IT operations automation platform patterns. Applies to AES Linux hosts
running PostgreSQL (CDR/CTI store), Java/JTAPI service JVMs, and DMCC provisioning.

### C1 — AES PostgreSQL Connection Pool Monitoring

AES relies on PostgreSQL for CDR storage, DMCC device-state persistence, and
CTI route data. Connection pool exhaustion silently degrades JTAPI performance
before producing visible errors.

```bash
# Connection pool usage snapshot
psql -U postgres -c "
  SELECT state, count(*) AS connections,
         max(now() - state_change) AS longest_idle
  FROM pg_stat_activity
  WHERE datname = 'aes'
  GROUP BY state
  ORDER BY connections DESC;
"

# Identify long-running or idle-in-transaction connections (>5 min)
psql -U postgres -c "
  SELECT pid, usename, state,
         round(extract(epoch FROM now() - state_change)) AS idle_secs,
         left(query, 80) AS query_snippet
  FROM pg_stat_activity
  WHERE datname = 'aes'
    AND state_change < now() - interval '5 minutes'
  ORDER BY idle_secs DESC;
"

# Table bloat / dead-tuple accumulation (run weekly)
psql -U aes -c "
  SELECT schemaname, tablename,
         n_dead_tup, n_live_tup,
         round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 1) AS dead_pct
  FROM pg_stat_user_tables
  WHERE n_dead_tup > 1000
  ORDER BY n_dead_tup DESC;
"

# Replication lag (if AES geo-redundant standby configured)
psql -U postgres -c "
  SELECT client_addr, state, sent_lsn, write_lsn, replay_lsn,
         (sent_lsn - replay_lsn) AS replay_lag_bytes
  FROM pg_stat_replication;
"
```

**Thresholds**:
| Metric | Warning | Critical |
|--------|---------|----------|
| Active connections | >80% of `max_connections` | >95% |
| Idle-in-transaction | >30 sec | >120 sec |
| Dead-tuple ratio | >10% | >25% |
| Replication lag | >10 MB | >50 MB |

**Remediation**: Kill idle-in-transaction connections with
`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction';`
then run `VACUUM ANALYZE` on bloated tables. Never terminate `pg_wal_sender` processes.

---

### C2 — AES Database Backup & Integrity Check

```bash
# Daily PostgreSQL dump (run from cron, AES backup user)
pg_dump -U aes -Fc aes > /opt/avaya/backup/aes_$(date +%Y%m%d).dump
# Verify dump integrity immediately after
pg_restore --list /opt/avaya/backup/aes_$(date +%Y%m%d).dump | wc -l
# Should be >0; if 0 or error — dump is corrupt, re-run immediately

# Purge backups older than 14 days
find /opt/avaya/backup -name "aes_*.dump" -mtime +14 -delete

# Check PostgreSQL data directory disk usage
du -sh /var/lib/pgsql/data/
df -h /var/lib/pgsql/

# Verify WAL archiving is not accumulating (geo-redundancy mode)
ls -lh /var/lib/pgsql/data/pg_wal/ | tail -5
# If WAL files accumulate >1 GB, archiving stalled — check standby connectivity
```

**Safety rules**:
- NEVER run `DROP DATABASE` or `TRUNCATE` on the `aes` database without explicit change-control approval.
- Backup job should use a dedicated `aes_backup` role with `pg_read_all_data` only.
- Verify backup disk is separate from data disk (single-disk failure must not lose both).

---

### D3 — CPU Spike → Heap Dump + Thread Analysis

When AES JVM (JTAPI service, WebSphere, or DMCC) shows sustained CPU >90%:

```bash
# Step 1 — Identify the AES JVM process
ps -eo pid,pcpu,pmem,comm --sort=-pcpu | head -10
# Look for: java (jtapi), java (WebSphere/dmcc), postgres

# Step 2 — Thread-level CPU breakdown
top -H -p <PID> -b -n 1 | head -30
# Note the top 3 thread IDs (TIDs) in hex for jstack correlation

# Step 3 — Capture thread dump (safe, non-disruptive)
sudo -u avaya jstack -l <PID> > /tmp/aes_threaddump_$(date +%H%M%S).txt
# Repeat 3× at 10-sec intervals to identify stuck vs. spinning threads

# Step 4 — Correlate high-CPU TIDs to stack frames
# Convert top TID (decimal) → hex, then grep jstack output:
printf "%x\n" <TID_DECIMAL>
grep -A 20 "nid=0x<TID_HEX>" /tmp/aes_threaddump_*.txt

# Step 5 — Heap snapshot if OOM suspected (requires approval — pauses JVM)
# sudo -u avaya jmap -dump:format=b,file=/tmp/aes_heap_$(date +%Y%m%d).hprof <PID>

# Step 6 — GC health check (no pause)
sudo -u avaya jstat -gcutil <PID> 1000 10
# Columns: S0, S1, E (Eden), O (Old), M (Metaspace), YGC, YGCT, FGC, FGCT
# Alert if: O > 85% between Full GC cycles; FGCT increases faster than 1 min/hour
```

**Automated alert rule** (add to `/opt/avaya/scripts/cpu_watch.sh` for cron):
```bash
#!/bin/bash
THRESHOLD=90
PID=$(pgrep -f "jtapi|dmcc" | head -1)
CPU=$(ps -p "$PID" -o pcpu= | tr -d ' ')
if (( $(echo "$CPU > $THRESHOLD" | bc -l) )); then
  jstack -l "$PID" > /tmp/aes_threaddump_$(date +%H%M%S).txt
  echo "CPU spike on AES JVM PID $PID: ${CPU}%. Thread dump saved." \
    | mail -s "AES CPU Alert $(hostname)" avaya-ops@yourcompany.com
fi
```
Add to cron: `*/5 * * * * /opt/avaya/scripts/cpu_watch.sh`

---

### F4 — Alert → Diagnose → Remediate Workflow Template

Three-node workflow for repeatable AES incident response. Mirrors the IT ops
agent platform pattern: detect → classify → act.

```
┌─────────────────────────────────────────────────────────┐
│  NODE 1: ALERT DETECTION                                │
│  Trigger: monitoring threshold crossed OR SR opened     │
│  Actions:                                               │
│    1. Capture snapshot: ps, top, df, free, netstat      │
│    2. Tail last 200 lines of relevant log               │
│    3. Classify: CPU / Memory / Disk / Network / Service │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  NODE 2: DIAGNOSIS                                      │
│  Based on classification from Node 1:                   │
│                                                         │
│  CPU spike    → jstack × 3, jstat -gcutil              │
│  Memory/OOM   → jmap -heap (approval required)          │
│  Disk full    → du -sh /var/log/avaya; find old logs    │
│  Network      → ss -s; netstat -anp; ping gateway       │
│  Service down → systemctl status; journalctl -u -n 100  │
│  DB           → pg_stat_activity; check connections     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  NODE 3: REMEDIATION                                    │
│  Auto-safe (no approval):                               │
│    - Compress/rotate logs >7 days                       │
│    - VACUUM ANALYZE on bloated tables                   │
│    - systemctl restart avaya-jtapi (if not CM/SMGR)    │
│                                                         │
│  Require approval:                                      │
│    - systemctl stop/start for CM, SMGR, WebLM, AES     │
│    - pg_terminate_backend (idle-in-transaction)         │
│    - jmap heap dump                                     │
│    - Any config file change                             │
│                                                         │
│  Always:                                                │
│    - Document before/after in SR notes                  │
│    - Set rollback trigger (if metric doesn't improve    │
│      within 10 min → escalate, do not retry)           │
└─────────────────────────────────────────────────────────┘
```

**Cooldown rule**: Do not retry remediation within 300 seconds of a previous
attempt on the same service. Repeated restart loops mask root cause and risk
data corruption on in-flight JTAPI transactions.


---

## Prometheus Alert Rules — JVM Exporter (AES / WFO / WebLogic)

> Source: [samber/awesome-prometheus-alerts](https://github.com/samber/awesome-prometheus-alerts) (MIT License)
> Apply to Avaya Java services: AES (JTAPI/TSAPI stack), ACRA/WebLogic, WFO Consolidator/Archiver.
> Requires `jmx_exporter` or `micrometer` metrics endpoint on the Java service.

### Heap Memory

```yaml
# JvmMemoryFillingUp — heap > 80% of max
- alert: JvmMemoryFillingUp
  expr: |
    (sum by(instance)(jvm_memory_used_bytes{area="heap"})
    / sum by(instance)(jvm_memory_max_bytes{area="heap"})) * 100 > 80
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "JVM heap > 80% on {{ $labels.instance }} — GC pressure rising"

# JvmMemoryCritical — heap > 95%
- alert: JvmMemoryCritical
  expr: |
    (sum by(instance)(jvm_memory_used_bytes{area="heap"})
    / sum by(instance)(jvm_memory_max_bytes{area="heap"})) * 100 > 95
  for: 0m
  labels: { severity: critical }
  annotations:
    summary: "JVM heap > 95% on {{ $labels.instance }} — OOM imminent; take heap dump NOW"
```

### Garbage Collection

```yaml
# JvmGcTimeTooHigh — GC consuming > 5% of wall clock
- alert: JvmGcTimeTooHigh
  expr: sum(rate(jvm_gc_collection_seconds_sum[5m])) > 0.05
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "JVM GC time > 5% — stop-the-world pauses affecting JTAPI event processing"

# JvmOldGenGcFrequency — Full GC more than 0.3/min
- alert: JvmOldGenGcFrequency
  expr: |
    rate(jvm_gc_collection_seconds_count{gc=~".*old.*|.*major.*"}[5m]) > 0.3
  for: 5m
  labels: { severity: warning }
  annotations:
    summary: "Old-gen (Major) GC rate > 0.3/min — heap sizing or memory leak suspected"
```

### Threads

```yaml
# JvmThreadsDeadlocked — deadlock detected
- alert: JvmThreadsDeadlocked
  expr: jvm_threads_deadlocked > 0
  for: 0m
  labels: { severity: critical }
  annotations:
    summary: "JVM deadlock detected on {{ $labels.instance }} — take jstack IMMEDIATELY"

# JvmThreadCountHigh — thread count > 300
- alert: JvmThreadCountHigh
  expr: jvm_threads_live > 300
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "JVM thread count > 300 on {{ $labels.instance }} — thread leak or executor runaway"

# JvmThreadsBlocked — > 50 threads in BLOCKED state
- alert: JvmThreadsBlocked
  expr: jvm_threads_states{state="BLOCKED"} > 50
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "> 50 BLOCKED threads — lock contention; run jstack and look for holding thread"
```

### File Descriptors

```yaml
# JvmFileDescriptorsExhaustion — FD usage > 90%
- alert: JvmFileDescriptorsExhaustion
  expr: (process_open_fds / process_max_fds) * 100 > 90
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "JVM FD usage > 90% on {{ $labels.instance }} — socket/log handle leak"
```

### JVM Alert-to-Action Table (Avaya Services)

| Alert | Avaya Service Impact | Immediate Action |
|-------|---------------------|-----------------|
| JvmMemoryFillingUp | AES: JTAPI event queue slows; WFO: inserts delayed | Check heap with `jstat -gcutil <pid> 5000 12`; identify leak |
| JvmMemoryCritical | Imminent OOM crash — AES drops CTI sessions | `jmap -dump:format=b,file=/tmp/heap.hprof <pid>`; restart after dump |
| JvmGcTimeTooHigh | JTAPI deliverEvent() latency spikes; WFO SQL timeouts | `jstat -gccause <pid>`; check GC log for pause duration |
| JvmOldGenGcFrequency | Memory leak in old gen — heap growing monotonically | Heap dump + MAT analysis; check JTAPI TSCall retention |
| JvmThreadsDeadlocked | AES stops processing events; WFO Consolidator hangs | `jstack <pid> > /tmp/jstack.txt`; look for deadlock section at end |
| JvmThreadCountHigh | Thread pool leak — executor not releasing threads | `jstack <pid>`; tally runnable vs blocked; identify leaked pool |
| JvmThreadsBlocked | Connection pool lock contention; DB I/O blocked | `jstack <pid>`; find holding thread; check if DB is responding |
| JvmFileDescriptorsExhaustion | New sockets/files cannot open; CTI connections fail | `lsof -p <pid> | wc -l`; identify leaked handles; increase `ulimit -n` |

### Collecting jvm_exporter Metrics (Without Prometheus)

When Prometheus is not deployed, replicate key JVM metrics manually:

```bash
# Heap usage (via jstat — equivalent to JvmMemoryFillingUp)
jstat -gcutil $(pgrep -f AESServer) 5000 3
# Output: S0  S1   E   O   M  CCS  YGC  YGCT  FGC  FGCT   GCT
# O (Old Gen) > 80% → JvmMemoryFillingUp threshold crossed

# Thread count + state snapshot (equivalent to JvmThreadCountHigh / JvmThreadsBlocked)
jstack $(pgrep -f AESServer) > /tmp/jstack_$(date +%s).txt
grep -c "java.lang.Thread.State:" /tmp/jstack_*.txt          # Total thread count
grep -c "BLOCKED" /tmp/jstack_*.txt                          # Blocked thread count
grep "deadlock" /tmp/jstack_*.txt                            # Deadlock detection

# FD usage (equivalent to JvmFileDescriptorsExhaustion)
PID=$(pgrep -f AESServer)
ls /proc/$PID/fd | wc -l                                     # Current open FDs
cat /proc/$PID/limits | grep "open files"                    # Max FD limit
```
