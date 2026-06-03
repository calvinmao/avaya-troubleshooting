# Recording / ACRA / WFO (Verint) Troubleshooting Reference
<!--
scope: ACRA, WFO/WFE (Verint), WebLogic, RIS, BatchExtender, pause/resume, recording loss
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: Verint product versioning, WebLogic heap defaults, SQL Server JDBC driver versions
related_docs: aes-cti-jtapi.md (JVM Prometheus rules), linux-server.md, lessons/recording-wfo.md
-->



## Table of Contents
- [WFO / WFE Verint Stack](#wfo--wfe-verint-stack)
- [ACRA / Recording](#acra--recording)
- [Recording Failure Troubleshooting (Workflow 14)](#recording-failure-troubleshooting)
- [WFO / Verint Log Collection](#wfo--verint-log-collection)
- [Recording / WFO Fault Patterns](#recording--wfo-fault-patterns)
- [Historical Fault Patterns (FY21–FY23)](#historical-fault-patterns)

---

## WFO / WFE Verint Stack

Avaya Workforce Optimization (WFO) / Workforce Engagement (WFE) is **OEM Verint Impact360**. Treat it as a Verint stack with Avaya wrapping. Most fixes are Verint KB packages, not Avaya patches.

| Component | Role | Notes |
|-----------|------|-------|
| **WebLogic (Production / Recording / QM / Compliance servers)** | Java app servers hosting WFO modules | Logs: `weblogic.log`, `SecureServer.log`. Enable for LDAP / authentication tracing. |
| **SQL Server (DB tier)** | Persistence for all Verint DBs (Common, QM, Speech, AV, OLTP, IDW, Archive, Contact) | Customer-managed. Driver choice matters (see below). |
| **DB Sync Adapter / BatchExtender** | Synchronizes Avaya↔Verint DB schemas | Fails when KB versions on adapter and target DB don't match — install Database Directory Sync KB (e.g., KB228252). |
| **ETL jobs** | Move data into IDW / reporting | Failure usually = driver / KB mismatch, not data. |
| **Compatibility Kit** | Bridges WFO version to current Avaya/Verint patches | Often required after upgrade or DB driver changes (e.g., KB227778). |
| **Recording Integration Service (RIS) / DMCC Adapter** | Spawns DMCC sessions on AES per data source | Source of `AvayaLicenseSigner` `ConcurrentModificationException` crashes (KB228051). |

### DB driver compatibility (critical)

SQL Server Native Client (`SQLNCLI` / `SQLNCLI11`) is deprecated and is **not present** on SQL Server 2022 / SSMS 19+. Verint DB KBs below the following baselines still use `SQLNCLI11`; updated KBs switch to `MSOLEDBSQL`:

| Verint DB | Baseline KB that switches to MSOLEDBSQL |
|-----------|------------------------------------------|
| Common DB | KB226960 |
| QM DB | KB226708 |
| Speech Products DB | KB226655 |
| Automated Verification DB | KB226653 |
| Contact OLTP DB | KB226652 |
| Interaction Data Warehouse | KB226650 |
| Archive DB | KB226647 |
| Contact DB | KB226253 |

If customer is on SQL Server 2022 with older Verint DB KBs, ETL/search will silently fail. Two valid fixes: (a) apply latest Verint DB KBs, or (b) install `sqlncli.msi` from Microsoft to side-load `SQLNCLI11`.

### Avaya-vs-Verint ticket boundary

If the bug is in Verint code (WebLogic, RIS, DB schema, BatchExtender), open a **Verint ticket** (numeric, e.g. `1471955`) and request the KB. Do not file a PEA against Avaya R&D for these.

---

## ACRA / Recording

**ACRA (Avaya Contact Recorder Advanced)** is a Verint-based recorder integrated with Avaya via DMCC.

| Item | Default | Notes |
|------|---------|-------|
| WebLogic admin port | **7001** | Standard. Login page reachable here. |
| WebLogic alternate / managed port | **7002** | Some patched UIs (after Compatibility Kit install) start redirecting downloaded interaction replay to 7002 — if firewall blocks 7002, replay fails with cert / connection errors. |
| Recording mode | DMCC Single Step Conference / Multi-Registration | Set per `Phones` config in WFO. |
| Free-seating | Agent logs in with hunt-group extension on shared station | Requires the **agent's login VDN** to be added to recording config; otherwise WFO sees only `Service Initiated` + `Connection Cleared` and never matches the agent (per `1-23163052432`). |
| Encrypted file replay | `.avi` wrapper around encrypted audio + Windows Media Player → ACRA logon page → app server | If a replay JS file is corrupted on the app server (path under `E:\AvayaAura\Software\ProductionServer\weblogic\Impact360\ProductionDomain\servers\ProductionServer\tmp\_WL_user\wfoSuite\...\war\uif\js\modules\`), all clients fail identically — Verint provides a replacement file (per `1-23181381262`). |
| Archive vs Live | Archived audio comes from disk-manager paths; un-archived files trigger `Disk Manager Detected Un-Archived Audio Files` alarms | Recurring SR theme. |

---

## ACRA Diagnostics

### Database Sync Failures
- **ACRA ↔ CM Data Divergence**: Search WebLogic logs for `SyncManager EXCEPTION` or `DataSource mismatch`. Indicates DMCC session state on AES doesn't match WFO internal state (per `1-23214561992`). Check DMCC registration, verify CTI link bidirectional.
- **Orphaned DMCC Sessions Consuming Licenses**: Check RIS logs for `Session allocation failed` after crash. Restart RIS service and DMCC device resets to release orphaned sessions (per `1-23089134202`).
- **GC Pause Impact on Recording Duration Mismatch**: Monitor heap pressure in WebLogic via `jstat -gcutil <pid>`. Old Gen collection >500ms causes recording timer lag vs actual call duration. Set `-XX:MaxGCPauseMillis=200` in WebLogic startup (per `1-23167445092`).

### Pause/Resume Timing Issues
- **Pause Recording Not Advancing Call Duration**: DMCC `pauseRecord()` called but `resumeRecord()` never sent if RIS crashes mid-pause. Check IntegrationService.log for `ConcurrentModificationException` in pause handler. Restart RIS and agent must manually resume (per `1-23102456742`).
- **Resume Extends Recording Duration**: Double-resume on same DMCC session causes timer skew. Search RIS logs for `pauseRecord called twice without resume`. Fix: validate DMCC session state before pause/resume operations.

### Recorder Server Stall Detection
- **Recording Stops Mid-Call (WebLogic Resource Exhaustion)**: Verify WebLogic heap via admin console. If free heap <10%, all DMCC operations timeout. Check thread count in `netstat -an | grep ESTABLISHED` — if >500 connections, increase Java `-Xmx` heap (per `1-22998412312`).
- **RIS Service Hangs (ASAI Link Saturation)**: Monitor AES ASAI link via `getlogs -d <aes_host>`. Search for `ASAI buffer overflow` or `session limit reached`. If found, reduce concurrent DMCC sessions or increase AES ASAI pool size (per `1-23045671892`).

### POM Campaign Integration Failure
- **Recording State ≠ Call State (Campaign Lock Mismatch)**: POM campaign marks call "answered" but ACRA never receives DMCC session connect. Verify DMCC is actually registered before campaign launch: `display dmcc-data-module` on AES. If unregistered, campaign will timeout waiting for DMCC (per `1-23076234562`).
- **Call Duration Recorded but State Unknown**: WFO cannot correlate recording to agent/skill if DMCC UUI data mismatch. Check RIS logs for `UUI type mismatch` in DMCC session. Verify `display recording-data` on CM includes correct UUI mapping (per `1-22876543812`).

---

## Recording Failure Troubleshooting

### Workflow 14: Recording Failure / ACRA Troubleshooting

```
When calls are not being recorded or recordings cannot be played back:

Step 1 — Identify the Failure Mode
  - Calls not recorded at all (no file created)
  - Calls recorded but cannot be replayed
  - Partial recording (starts late, stops early)
  - Archive replay fails
  - Pause recording not working
  - Specific station/agent not recorded

Step 2 — Check Recording Dependency Chain
  AES DMCC Service → RIS (Recording Integration Service) → WebLogic → SQL Server
  ↓                 ↓
  CTI Link Up?      DMCC Device Registered?    License Available?

Step 3 — Common Failure Patterns

  DMCC Unregistered Intermittently:
    - Check AES DMCC link status
    - Check AES HA pair cert symmetry — asymmetric certs cause DMCC unreg
      (per `1-23142431892`)
    - DMCC telecommuter mode stations can only be recorded on 1 ACRA
      (per `TASK0603105`)
    - ESS connection: DMCC may not register when connecting to ESS instead of primary

  Recorder Stops Being Functional:
    - Check sync to datacenter (per `1-22763056292`)
    - Intermittent stop usually = resource exhaustion or network partition
    - Total outage after patch: verify recording service restarted (per `1-22892285872`)

  Free-Seating Agent Not Recorded:
    - Agent logs in with hunt-group extension on shared station
    - Must add agent's login VDN to recording config (per `1-23163052432`)
    - WFO sees only Service Initiated + Connection Cleared without VDN match

  Encrypted File Cannot Be Replayed:
    - .avi wrapper around encrypted audio uses Windows Media Player → ACRA login page
    - If replay JS file corrupted on app server → all clients fail identically
    - Path: E:\AvayaAura\Software\ProductionServer\weblogic\Impact360\... (per `1-23181381262`)
    - Fix: Verint provides replacement JS file

  Archive Replay Failure:
    - Archived audio comes from disk-manager paths
    - Verify archive storage mounted and accessible
    - Check disk-manager service status
    - Verify file path mapping matches archive config (per `1-23193629612`)

  SSIS Compliance Deploy Failure:
    - Usually SQL Server connectivity or permission issue
    - Verify SQL Server agent service running
    - Check SSIS package deployment and SQL Server version compatibility

  Disk Manager Un-Archived Audio Files Alarm:
    - Audio files exist in recording path but not archived
    - Check archive job schedule and disk space on archive target
    - Verify disk-manager service is processing the queue
    - If alarm persists after clearing: check archive path permissions

Step 4 — Verify AES DMCC Registration
  From AES web console → Status → DMCC
  - Device should show "Registered" for each recording source
  - If "Unregistered": check AES CTI link, AES license, station configuration
  - For telecommuter mode: verify station link configuration matches

Step 5 — Verify RIS / WebLogic
  Check WebLogic admin port 7001:
    - Login page reachable? If not, WebLogic is down
    - Check WebLogic logs: weblogic.log, SecureServer.log
    - RIS spawns DMCC sessions per data source
    - AvayaLicenseSigner ConcurrentModificationException = known bug (KB228051)

Step 6 — Pause Recording Not Working
  - Verify pause recording is enabled in WFO config per data source
  - Check agent has pause recording permission in WFO
  - Verify DMCC session supports pause/resume (not all recording modes do)
  - Check if agent is using correct pause/resume UI button
```

### WFO Login (HTTP 500) Diagnostic Path

When the WFO web page returns HTTP 500:
- Check WebLogic is up and admin port 7001 is reachable
- Verify DMSA (Directory Mirror Service Account) is valid and not locked in AD
- Check SQL Server connectivity from WebLogic host
- Check LDAP/AD reachability for authentication
- Reference: `SWA-INC6468883`, `1-23153206492`

---

## WFO / Verint Log Collection

```
# WebLogic logs (Production / Recording / QM / Compliance servers)
E:\AvayaAura\Software\ProductionServer\weblogic\Impact360\ProductionDomain\
  servers\ProductionServer\logs\weblogic.log
E:\AvayaAura\Software\ProductionServer\weblogic\Impact360\ProductionDomain\
  servers\ProductionServer\logs\SecureServer.log

# Enable LDAP/auth tracing in WebLogic
# WebLogic Console → ProductionServer → Logging → Advanced → set to Debug

# RIS (Recording Integration Service) logs
# Located within WebLogic deployment directory

# SQL Server queries for WFO troubleshooting
SELECT TOP 20 * FROM [Common].[dbo].[AuditLog] ORDER BY Timestamp DESC
SELECT * FROM [Common].[dbo].[DataSource] WHERE Name = '<source-name>'

# Disk Manager paths
# Un-archived audio file alarm: check recording path vs archive path
# Archive path typically: E:\AvayaAura\Archive\ or network share

# DMSA (Directory Mirror Service Account)
# If WFO service fails after DMSA modification: check account not locked in AD
```

---

## Recording / WFO Fault Patterns

### Current Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **DMSA account locked** | WFO service won't start after account modification | AD locked or expired the Directory Mirror Service Account | Unlock DMSA in AD; update credentials in WFO config (per `1-23153206492`) |
| **WFO login 500 error** | WFO web page returns HTTP 500 | WebLogic, DMSA locked, SQL Server, or LDAP failure | Check WebLogic logs, DMSA account, SQL Server, LDAP (per `SWA-INC6468883`) |
| **SQLNCLI11 missing on SQL 2022** | ETL/search silently fails after SQL Server upgrade | SQLNCLI11 deprecated, not present on SQL Server 2022 / SSMS 19+ | Apply latest Verint DB KBs (switch to MSOLEDBSQL) or install sqlncli.msi side-load |
| **AvayaLicenseSigner crash** | RIS crashes with ConcurrentModificationException | Known Verint bug in Recording Integration Service | Apply KB228051 |
| **Archive replay failure** | Archived interactions cannot be played back | Disk-manager path incorrect, archive storage unmounted, or JS file corrupted | Verify archive storage mount and disk-manager config; Verint replacement JS if corrupted (per `1-23181381262`) |
| **Free-seating agent not recorded** | Agent on shared station not captured by WFO | Agent's login VDN missing from recording config | Add agent's login VDN to recording data source config (per `1-23163052432`) |
| **Pause recording not working** | Pause button has no effect on recording | Recording mode doesn't support pause/resume, or agent lacks permission | Verify recording mode supports pause; check WFO pause recording permission |
| **SSIS compliance deploy fail** | Recording Compliance Deploy SSIS Package job fails to start | SQL Server agent not running, or permission issue | Verify SQL Server agent service; check SSIS package deployment |
| **Recording duration incorrect** | Recording shows calls running longer than actual | Timer sync or clock drift between recording server and CM | Check NTP synchronization; verify recording server system clock |
| **DMCC unregistered intermittently** | Recording gaps, DMCC shows unregistered | AES HA cert asymmetry | Check cert on both HA nodes (per `1-23142431892`) |
| **Recording stops during call** | Starts but stops mid-call | DMCC session drops / AES resource pressure | Check AES resources during peak (per `1-18741463012`) |
| **Recording rule for hunt group not working** | Hunt group calls not recorded | Rule doesn't match hunt group extension pattern | Verify recording rule covers hunt group format (per `1-17866322822`) |
| **Recording stop at 22 seconds** | All recordings truncated at ~22s | DMCC session timeout or resource limit | Check DMCC session config (per `1-17027200982`) |
| **ACRA secondary recorder misses** | Secondary ACRA misses recordings | Data source config mismatch | Verify config matches between primary and secondary (per `1-17436938092`) |
| **Recording length longer than actual** | Duration exceeds actual call | Timer sync or extra silent audio | Check NTP sync; verify start/stop triggers (per `1-20341479402`) |
| **WFO Inbound Transcription Missing** | Transcription data missing | Speech Analytics pipeline failure | Check Speech Analytics service (per `1-22091464012`) |
| **WFO Updates Pending after patch** | Cannot complete updates | Verint KB requires manual post-install | Follow KB post-install instructions (per `1-22427216062`) |
| **WFO service not starting** | WFO services fail to start after server reboot | WebLogic startup dependency or DMSA account issue | Check WebLogic logs, DMSA account, and service dependencies (per `1-18675781982`) |
| **Recording search menu disappears after reboot** | WFO interaction search menu missing from UI after server reboot | WebLogic deployment or cache issue after restart | Clear browser cache; verify WebLogic deployment of search module (per `1-22399419122`) |
| **WFO Customer Feedback stopped working** | WFO feedback module non-functional | Verint KB patch broke feedback module | Apply Verint corrective KB; check feedback module deployment (per `1-17105804802`) |

---

## Historical Fault Patterns

### FY23 Recording-Related Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **ACRA SAML/OKTA integration failure** | ACRA login fails with OKTA as identity provider | SAML assertion mismatch or IDP metadata stale | Verify SAML metadata from OKTA, check assertion attributes, refresh IDP metadata (per `1-20000705804`, `1-19914698372`) |
| **I360 PPA service failure** | ACRA 15.2 alarm: Post Processing Agent service failed | I360 PPA process crash or resource exhaustion | Restart PPA service, check I360 Secure Web Gateway (per `1-19597351662`) |
| **JRE version breaks WFO** | WFO reports fail after JRE update | WFO incompatible with newer JRE version | Revert JRE to supported version; check Verint compatibility matrix (per `1-19830255592`) |
| **Recording stops after link bounce** | Recording stops when CM-AES link bounces | DMCC session not re-established after link recovery | Check DMCC auto-recovery config; manual DMCC re-registration may be needed (per `INC5166579`) |

### FY22 Recording-Related Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **ACR split brain** | Both DMCC ACR and SIPREC ACR suites active simultaneously | Cluster consistency lost; both suites believe they are primary | Manual intervention to designate primary; restart secondary suite (per `1-19103106682`) |
| **ACRA web report errors with 3rd party proxy server** | ACRA reports fail when accessed through corporate proxy | Proxy server modifying or blocking ACRA HTTP responses | Bypass proxy for ACRA URLs or configure proxy exceptions (per `1-18751593912`) |
| **ACR tagging issue (wrong data)** | ACR recording tags show incorrect agent/station info | ACR data source mapping or TSAPI data resolution failure | Verify data source mapping in ACR; check TSAPI link for correct data (per `1-18100814550`) |
| **WFM Pulse data not reflected, staffing adapter fails** | WFM shows no agent activity data, staffing adapter alarm | WFM staffing adapter cannot connect to data source (Analytics or AACC) | Check staffing adapter connectivity to Analytics/AACC; verify API credentials (per `1-18726856152`) |
| **WFM server stopped emailing scheduled reports** | Scheduled WFM reports not delivered via email | SMTP relay configuration or email server authentication changed | Verify SMTP relay settings in WFM; check email server auth (per `1-20410259992`) |
| **WFM password field disappeared from user management** | Password input field missing from WFM admin UI | WFM UI bug after patch or browser compatibility | Clear browser cache; try different browser; apply WFM patch (per `1-18667984032`) |
| **Recording stops during the call** | Recording starts but stops mid-call without warning | DMCC session drops due to AES resource pressure or network glitch | Check AES resources during peak load; verify network stability (per `1-18741463012`) |
| **Recordings download issue (SFTP multiple file)** | SFTP download of multiple recording files not working | SFTP server limit or ACRA batch download configuration | Check SFTP server concurrent session limits; adjust ACRA SFTP config (per `1-18665573222`) |
| **UUI sent to ACR from AES is type UUI_USER_SPECIFIC** | UUI data type mismatch between AES and ACR | AES UUI type mapping differs from what ACR expects | Check AES UUI configuration; verify UUI type in recording rule (per `1-19228553112`) |

### FY21 Recording-Related Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **ACR Unlimited Strength Encryption install failure** | ACR15 setup fails at crypto policy step | Java JCE Unlimited Strength Jurisdiction Policy not installed | Download and install JCE policy files for the Java version on ACR (per `1-16971545822`) |
| **ACR Slave archive error "column mediaid does not exist"** | ACR slave server cannot archive recordings | DB schema mismatch after ACR upgrade; slave missing migration | Run ACR DB migration scripts on slave; verify schema version matches primary (per `1-17154868902`) |
| **ACR hung overnight** | ACR stops recording, web page inaccessible, no alarms | ACR Java process deadlock or resource exhaustion | Restart ACR services; check for known memory leak patches (per `1-17792493002`) |
| **ACR Oceana integration port 443 failure** | ACR cannot send recording metadata to Oceana | Certificate or firewall blocking HTTPS 443 from ACR to Oceana | Verify cert trust, firewall rules, and Oceana REST endpoint availability (per `1-17771923042`) |
| **ACR 12.1 Trunk ID field shows NA** | Trunk ID column blank in ACR replay page | ACR cannot retrieve trunk info from CM via TSAPI | Check TSAPI link, verify trunk group configuration in CM (per `1-17813972732`) |
| **ACRA SIP Stereo recording only agent audio** | SIP stereo recording has agent side only, customer side silent | CM conference bridge not mixing audio correctly, or DMCC monitoring wrong party | Check CM conference configuration; verify DMCC recording mode (per `1-17850923862`) |
| **ACR archive purge failed alarms** | ACR raises alarms about archive purge failures | Archive target disk full or permissions changed | Check archive storage disk space and permissions (per `1-17094360942`) |
| **ACR not archiving (15.1)** | "Unable to set archive on ACR 15.1" — archive configuration cannot be saved | ACR archive path or permissions issue | Verify archive storage path is accessible and writable (per `1-16987614612`) |
| **ACRA missing recording (stopped)** | ACRA recording has stopped, no new recordings created | DMCC device unregistered, RIS service down, or WebLogic failure | Check DMCC registration, RIS service, WebLogic health (per `1-17437995894`) |
| **DMCC StationLink unregistration (Telecommuter)** | Unexpected DMCC device unregister when using StationLink Telecommuter mode | StationLink keepalive timeout or SIP re-INVITE failure for remote workers | Check network stability for remote agents; increase keepalive interval (per `1-1791095361`) |
| **Third-party recorder (NICE) spurious events** | NICE server restart causes logout events sent to Genesis/AIC | NICE sends batch disconnect events on restart, overwhelming AIC | Coordinate NICE restart windows; configure AIC to handle event bursts (per `1-17049217150`) |
| **ACRA consume license unexpectedly** | ACRA uses more licenses than expected | Orphaned DMCC sessions consuming licenses | Restart ACRA to release orphaned sessions; check DMCC session cleanup (per `1-17015499149`) |
| **ACR ValidateFP tool** | Need to verify ACRA recording fingerprint integrity | ACRA includes a fingerprint validation tool | Run ValidateFP tool on ACRA server to verify recording integrity (per `1-18909150572`) |
| **ACR design difference causing ACRA behave differently** | Same config, different behavior across sites | CM design parameters (region, trunk, DSP) affect recording capture | Compare CM design parameters between sites; check IP-network-region and trunk group settings (per `1-18106641046`) |

---

## WFO / ACR Log Collection Procedures

### ACR Server Logs

| Component | Path | Configuration |
|-----------|------|---------------|
| Main Logs | Linux: /opt/witness/logs/<br>Windows: <InstallPath>\logs\<br>Files: acr.log, acr.log.<date> | Dynamic (no restart): http://<server>:8080/log?level=DEBUG<br>Permanent: acr.properties → log.level=DEBUG → restart |
| Tomcat | Same as main<br>Files: catalina.out, localhost.<date>.log | Managed by Tomcat service |
| Usage | Same as main<br>Files: usage.log, partystats.log | usage.dailystats=true in acr.properties |
| Config Snapshot | Same as main<br>File: nnnnnn_config.csv | config.reporting=true in acr.properties |

### WFO Framework Logs

| Component | Path | Notes |
|-----------|------|-------|
| Production Server | %IMPACT360DATADIR%\Logs\ProductionServer\<br>Files: wfo.log4j.log, error.log, coherence.log | WFO Log Manager → core.xml or debugFile.xml. Auto-zip at 20MB |
| EMA | %IMPACT360DATADIR%\Logs\EMA\<br>Files: ema.log, ema.error.log, ema.debug.log | WFO Log Manager to enable/disable |
| Recorder Manager | %IMPACT360DATADIR%\Logs\RM\<br>Files: rm.error.log, rm.debug.log | WFO Log Manager on local server |
| Auth/LDAP | %VERINT_WEBLOGIC_DOMAIN_HOME%\logs\<br>Files: ProductionServer.log, ProductionDomain.log | WebLogic Console → Environment → Servers → Debug → Security |
| HTTP Access | %IMPACT360DATADIR%\Logs\SecureGateway\SGW_Access_CF.ltf | Source IPs, auth methods |
| Audit Trails | %IMPACT360DATADIR%\Logs\Audit Trail\<br>File: Audit Trail_mm.dd.yy_....ltf | System Monitoring → Audit Viewer → export CSV |

### WFO Windows Recorder Components

| Component | Path | Configuration |
|-----------|------|---------------|
| Integration Service (RIS) | %IMPACT360DATADIR%\Logs\IntegrationService\IntegrationService.log | LogManager.exe → Trace Level: DebugHigh for CTI events |
| IP Capture | %IMPACT360DATADIR%\Logs\IPCapture\ | LogManager.exe → Trace Level: Debug |
| TDM Capture | %IMPACT360DATADIR%\Logs\TDMCapture\ | LogManager.exe |
| Consolidator | %IMPACT360DATADIR%\Logs\callsconsolidator\ | Buffer → DB movement |
| Archiver | %IMPACT360DATADIR%\Logs\archiver\ | Archive campaigns, file transfers |

### WFO Desktop Logs

| Component | Path |
|-----------|------|
| Screen Capture | <Program Files>\Witness Systems\Screen Capture Module\Logs\CaptureService.log, wcapw32.log |
| DPA | %PROGRAMDATA%\Verint\DPA\Logs\ (remote collect via DPA System Tab) |
| Strategic Planner | %USERPROFILE%\StrategicPlanner\Logs\Planner.log, PlannerConsole.log |

### WFO Analytics Logs

| Component | Path |
|-----------|------|
| Speech Analytics | %IMPACT360SOFTWAREDIR%\SpeechCatTomcat64\log\speechcat\sclog*.log |
| Import/Export | %IMPACT360DATADIR%\Logs\IEM\extraction.log, extractionManager.log |
| Transcription Repo | %IMPACT360DATADIR%\Logs\TranscriptionRepositoryService\trs.log |
| Real-Time Analytics | %IMPACT360DATADIR%\Logs\AnalyticsService\analyticsservice.log |

---

## Recording Server Java & Database Health (IT Ops Patterns)

Adapted from IT operations automation platform patterns. Applies to ACRA/WFO/WFE
hosts running WebLogic JVMs (ACRA) and SQL Server / Oracle backends (Impact 360).

### A2 — Java Heap & WebLogic Monitoring for ACRA / WFO

ACRA and Impact 360 both run on Java application servers (WebLogic for ACRA,
Tomcat variants for Impact 360 components). Heap exhaustion causes recording
stalls and silent audio loss before any OOM event fires.

```bash
# Identify WebLogic / Tomcat PID on ACRA server
ps -eo pid,pcpu,pmem,comm,args --sort=-pmem | grep -E "java|weblogic" | head -5

# Live GC monitoring — watch for Full GC frequency and pause duration
# Run for 60 seconds (60 samples × 1 sec interval):
jstat -gcutil <WEBLOGIC_PID> 1000 60
# Alert thresholds:
#   O (Old Gen) > 85% between collections → heap leak
#   FGCT increasing faster than 2 sec per 10 min → GC overhead
#   Full GC > 1/min → memory pressure causing recording pauses

# Heap summary (non-disruptive)
jmap -heap <WEBLOGIC_PID> 2>/dev/null | grep -E "Heap|used|capacity|free"

# Thread dump for hung recording threads (safe, repeat 3×)
jstack -l <WEBLOGIC_PID> > /tmp/acra_threads_$(date +%H%M%S).txt
# Look for: BLOCKED threads on RTPListener, PauseResumeHandler, CTIEventQueue

# WebLogic server log tail (last 50 lines):
tail -50 $DOMAIN_HOME/servers/AdminServer/logs/AdminServer.log
# Alert on: OutOfMemoryError, GC overhead limit exceeded, SocketTimeout in CTI

# JVM startup flags verification (confirm -Xmx and GC settings):
ps -p <WEBLOGIC_PID> -o args= | tr ' ' '\n' | grep -E "Xmx|Xms|GC|MaxGC"
# Recommended for ACRA: -Xmx4g -XX:MaxGCPauseMillis=200 -XX:+UseG1GC
```

**Common ACRA heap issues and fixes**:
| Symptom | Heap Indicator | Fix |
|---------|----------------|-----|
| Recording timer drift (L-001) | Full GC >500ms during pause/resume | Set `-XX:MaxGCPauseMillis=200`, increase `-Xmx` |
| Audio gaps at shift start | Old Gen spikes to 95% at login surge | Pre-warm JVM; schedule GC before peak shift |
| Recording stops mid-call | OOM on RTPBuffer thread | Increase heap; check for RTP buffer leak in log |

**Automated WebLogic heap alert** (add to ACRA server cron):
```bash
#!/bin/bash
WL_PID=$(pgrep -f "weblogic" | head -1)
OLD_GEN=$(jstat -gcutil "$WL_PID" 1 1 | awk 'NR==2{print $4}' | cut -d. -f1)
if [ "$OLD_GEN" -gt 85 ]; then
  jstack -l "$WL_PID" > /tmp/acra_heap_alert_$(date +%Y%m%d_%H%M%S).txt
  echo "ACRA WebLogic Old Gen at ${OLD_GEN}% on $(hostname). Thread dump saved." \
    | mail -s "ACRA Heap Alert" avaya-ops@yourcompany.com
fi
```
Add to cron: `*/10 * * * * /opt/avaya/scripts/acra_heap_watch.sh`

---

### C3 — WFO SQL Server / Oracle Connection Health (ODBC / JDBC)

Impact 360 (WFO) uses SQL Server (Windows) or Oracle as its recording metadata
database. Connection failures cause recording jobs to silently drop — calls are
captured as audio files but never indexed in the WFO database.

```bash
# --- Linux-side JDBC connectivity test (if WFO gateway on Linux) ---

# Test SQL Server JDBC connectivity from ACRA/gateway host:
# (Requires: jtds or mssql-jdbc jar in classpath)
java -cp /opt/avaya/lib/jtds-1.3.1.jar \
  net.sourceforge.jtds.jdbc.Driver \
  "jdbc:jtds:sqlserver://<SQL_SERVER_HOST>:1433/Impact360" \
  -u wfo_svc -p '<password>' \
  -e "SELECT COUNT(*) FROM dbo.Call WHERE StartTime > GETDATE() - 1"
# Expected: integer row count. Failure = connectivity or auth problem.

# Check JDBC driver connection pool metrics from WebLogic console:
# WL Console → Domain → Services → JDBC → Data Sources → Impact360DS
#   → Monitoring → Statistics
# Alert: ActiveConnectionsCurrentCount / MaxCapacity > 80%

# TCP reachability to SQL Server (always run before JDBC test):
nc -zv <SQL_SERVER_HOST> 1433 && echo "SQL Server port reachable" \
  || echo "BLOCKED — check firewall/SQL Browser service"

# --- Windows-side ODBC test (run on WFO application server) ---
# From PowerShell:
# Test-NetConnection -ComputerName <SQL_SERVER_HOST> -Port 1433
# odbcconf /a {CONFIGSYSDSN "SQL Server" "DSN=Impact360|Server=<HOST>|Database=Impact360"}

# SQL Server connection pool status (run on SQL Server directly):
# SELECT DB_NAME(dbid) AS db, COUNT(*) AS connections
# FROM sys.sysprocesses
# WHERE dbid > 0 AND DB_NAME(dbid) = 'Impact360'
# GROUP BY dbid;
```

**Connection health thresholds**:
| Metric | Warning | Critical |
|--------|---------|----------|
| JDBC active connections / max | >70% | >90% |
| SQL Server connection count for Impact360 DB | >150 | >200 |
| JDBC connection wait time | >2 sec | >10 sec |

**Common recording-database desync patterns**:
| Symptom | Root Cause | Fix |
|---------|------------|-----|
| Audio exists, call not in WFO search | JDBC pool exhausted; insert failed | Increase JDBC max capacity; add retry in Consolidator |
| Duplicate call records | Consolidator restarted mid-write | Check `callsconsolidator.log` for duplicate-key errors; purge via WFO admin |
| Archiver jobs stuck | Oracle tablespace full | Check `dba_tablespace_usage_metrics`; add datafile or purge old recordings |

**Safety rule**: Never run `DELETE FROM dbo.Call` or `TRUNCATE TABLE` on the
Impact360 database without change control. Recording deletion must go through
the WFO admin UI retention policy, which logs the deletion audit trail.


---

## Prometheus Monitoring — WFO / ACRA Java Services

WFO (WebLogic, RIS, BatchExtender) and ACRA are Java processes. Apply the
**JVM Exporter alert rules** documented in `aes-cti-jtapi.md` → *Prometheus Alert Rules — JVM Exporter*
to these services as well. Key thresholds:

| Metric | Warning | Critical | WFO Service |
|--------|---------|----------|-------------|
| Heap usage | > 80% | > 95% | WebLogic managed servers, BatchExtender |
| GC time (% wall clock) | > 5% | > 15% | Any Java process |
| Old-gen GC rate | > 0.3/min | > 1/min | BatchExtender, Consolidator |
| Blocked threads | > 20 | > 50 | Consolidator (DB I/O blocked) |
| FD exhaustion | > 80% | > 90% | ACRA (recording sessions = sockets) |

**Without Prometheus** (use `jstat` + `jstack` directly — see the `jstat -gcutil` and
`jstack` commands in the `A2 — Java Heap & WebLogic Monitoring` section above).

Apply **node-exporter Linux alert rules** from `linux-server.md` → *Prometheus Alert Rules —
Node Exporter* to the WFO/ACRA servers — especially `HostOutOfDiskSpace` (recording
storage full causes silent recording loss) and `HostSystemdServiceCrashed` (WebLogic OOM
exits without systemd recovery unless a unit file wraps it).
