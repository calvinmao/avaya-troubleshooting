---
title: "Log Collection Procedures Reference"
layer: L4
scope: "Avaya log collection (getlogs, spi.log, TSAPI/DMCC trace), server health, SNMP monitoring, auto-remediation"
maturity: canonical
applicable_versions: [TBD]
last_reviewed: "2026-06-03"
owner: "avaya-debug skill"
staleness_risks:
  - "getlogs syntax across AES/POM versions"
  - "SNMP enterprise MIB OIDs"
  - "log file paths per version"
related_docs:
  - "linux-server.md"
  - "aes-cti-jtapi.md"
  - "lessons/log-collection.md"
---

# Log Collection Procedures Reference


Comprehensive log paths, enable/disable procedures, and capture methods for AES, CMS, AAEP/POM, and WFO/ACR. Use this reference whenever you need to instruct a customer or engineer on which logs to collect and how.

## Table of Contents
- [AES Log Collection](#aes-log-collection)
- [CMS Log Collection](#cms-log-collection)
- [AAEP / EPM / MPP / POM Log Collection](#aaep--epm--mpp--pom-log-collection)
- [WFO / ACR Log Collection](#wfo--acr-log-collection)
- [Network Trace (tcpdump)](#network-trace-tcpdump)

---

## AES Log Collection

### AES General System Logs

Always enabled by default. Located in `/var/log/avaya/aes/`.

| Log | File | Purpose |
|-----|------|---------|
| Error Log | `mvap.log` | General operational status, errors |
| Security Log | `sec.log` | Client access tracking |
| Command Log | `cmd.log` | Administrative command history |
| Reset Log | `reset.log` | System reset events |

### TSAPI Service Tracing

Records CSTA/ASAI message exchange between AES, CM, and third-party applications.

**Enable:**
1. Log in to AES Management Console (OAM)
2. Navigate to **Status → Log Manager → Trace Logging Levels**
3. Locate **TSAPI Service**
4. Select **"Everything on except mutex"** (or "Everything on")
5. Click **Apply Changes** → **Apply** on confirmation page

**Disable:** Return to same menu, set TSAPI Service to **Disabled**, click Apply.

**Log paths:**
- `/var/log/avaya/aes/TSAPI/csta_trace.out` — CSTA messages
- `/var/log/avaya/aes/TSAPI/g3trace.out` — ASAI messages
- `/var/log/avaya/aes/common/trace.out` — Common tracing info

### Transport Layer Trace

Tracks AEP (Application Enablement Protocol) traffic between CM and AES.

**Enable:**
1. OAM → **Status → Log Manager → Trace Logging Levels**
2. Locate **Transport Layer Service**
3. Select **"Everything on except mutex"**
4. Click **Apply Changes** → **Apply**

**Disable:** Set Transport Layer Service to **Disabled**, click Apply.

**Log path:** `/var/log/avaya/aes/trans_serv/trace.out`

### DMCC Service Tracing

Records API calls, errors, and trace information for Device, Media, and Call Control.

**Enable:**
1. OAM → **Status → Log Manager → Trace Logging Levels**
2. For **DMCC Service**, set **Finest** for ALL fields: Default, XML, Java, and Call Control Logging
3. Click **Apply Changes**

**Disable:** Set logging levels back to Disabled or INFO.

**Log paths (in `/var/log/avaya/aes/`):**
- `dmcc-api.log` — API call logs
- `dmcc-error.log` — Error logs
- `dmcc-trace.log` — Trace logs

### SMS (System Management Service) Logging

Records administrative operations on CM managed objects via Web Services.

**Enable:**
1. OAM → **AE Services → SMS → SMS Properties**
2. Set **SMS Logging** to **Verbose** (default: Normal)
3. Set **CM Proxy Trace Logging** to **Normal** or **Verbose** (default: None)
4. Click **Apply Changes**
5. SSH as root, edit `/opt/mvap/web/sms/saw.ini`:
   ```ini
   [Dev]
   tpl_debug=true
   tpl_session=true
   dev_commands=true
   msg_console=true
   msg_debug=true
   msg_log=true
   ```

**Disable:** Revert settings to Normal/None, restore saw.ini defaults.

**Log paths:**
- Linux syslog and Apache logs: `/var/log/httpd/` or `/var/log/avaya/aes/apache/`
- CM Proxy traces: `/var/log/avaya/aes/ossicm.log`

### CVLAN / DLG Service Tracing

**Enable:** OAM → Status → Log Manager → Trace Logging Levels → set service to desired level.

**Log paths:**
- CVLAN: `/var/log/avaya/aes/CVLAN/trace.out`
- DLG: `/var/log/avaya/aes/DLG/trace.out`

### AES getlogs Utility

Master script that collects ALL relevant logs, command outputs, and configuration files into a single archive.

```bash
# Must run as root
getlogs.sh                    # Collect ALL logs
getlogs.sh <days>             # Last N days (e.g., getlogs.sh 6)
getlogs.sh <from> <to>        # Date range: YYYY-MM-DD format
getlogs.sh week               # Last 7 days
getlogs.sh month              # Last 30 days
```

**Data gathered:** command outputs (disk usage, network status), config files (`/etc/hosts`, TSAPI/DMCC properties), system logs (`/var/log/avaya/aes/*`).

**Output:** `.tgz` file in `/tmp/`.

### AES Log Retention Configuration

OAM → **Status → Log Manager → Log and Trace Retention**
- Set retention period: 0–180 days
- Click **Apply**

### AES Service Controller

OAM → **Maintenance → Service Controller**
- Select service (e.g., TSAPI Service)
- Click **Restart Service**

### Client-Side Logs

| Client Type | Log | Enable Procedure |
|-------------|-----|-----------------|
| **TSAPI Windows Client** | TSAPI Spy trace → user-defined file (e.g., `c:\cstatrace.txt`) | Open TSAPI Spy → Options → Check "Log To File" → Check "Log Trace Messages" |
| **TSAPI Linux Client** | CSTA trace → file defined by env var | Set `export CSTATRACE=<filename>` before running app |
| **JTAPI Client** | `jtapiTrace.log`, `jtapiErrors.log` (locations per log4j.properties) | Configure `log4j.properties` for DEBUG level |

### AES Server-Side Log Quick Reference

| Service | Key Files | Path |
|---------|-----------|------|
| TSAPI | `csta_trace.out`, `g3trace.out` | `/var/log/avaya/aes/TSAPI/` |
| DMCC | `dmcc-trace.log`, `dmcc-error.log` | `/var/log/avaya/aes/` |
| CVLAN | `trace.out` | `/var/log/avaya/aes/CVLAN/` |
| DLG | `trace.out` | `/var/log/avaya/aes/DLG/` |
| Transport Layer | `trace.out` | `/var/log/avaya/aes/trans_serv/` |
| System/Error | `mvap.log`, `sec.log`, `cmd.log` | `/var/log/avaya/aes/` |
| Telephony Web Service | `ws-telsvc-*.log` | `/var/log/avaya/aes/tomcat/` |
| Syslog | `messages` | `/var/log/messages` (also OAM → Status → Logs → Syslog) |
| Security | `secure`, `sec.log` | `/var/log/secure`, `/var/log/avaya/aes/sec.log` |
| Install | — | `/var/log/avaya/` (OAM → Status → Logs → Install Logs) |
| Audit | — | OAM → Status → Logs → Audit Logs → Download |

---

## CMS Log Collection

### 1. General System and Process Logs

| Log | Path | Description |
|-----|------|-------------|
| Error Log | `/usr/elog/elog` | Primary error log; everything in customer "Error Log Report" plus internal details. Monitor: `tail -f /usr/elog/elog` |
| Process Log | `/cms/env/cms_mon/proc_log` | History of start/exit activity for every CMS process |
| Message Queue Clean | `/cms/env/cms_mon/mq_clean` | Items removed from message queues; useful for IPC issues |
| GEM Log | `/cms/env/gem/gem_log` | Start/stop times of GEM screens (supervisor GUI) |
| Query Log | `/cms/db/log/qlog` | Historical report queries: start time, user, run time, query text |

### 2. ACD Link and Data Collection Logs

Replace `acd1` with the specific ACD number (e.g., `acd2`).

| Log | Path | Description & Procedure |
|-----|------|------------------------|
| SPI Error Log | `/cms/pbx/acd1/spi.err` | Primary ACD link status log. Records link drops, X.25/TCP/IP session errors, call counting problems. Always running when data collection is on. Monitor: `tail -f /cms/pbx/acd1/spi.err` |
| SPI Log | `/cms/pbx/acd1/spi.log` | Detailed protocol messages (call setup, agent state changes). **Must be manually started.** Enable: `/cms/bin/spilog <acd_num> all`. Disable: `/cms/bin/spilog <acd_num> -all` (**Important: turn off when done to save disk/CPU**) |
| Translation Log | `/cms/pbx/acd1/xln.log` | Protocol messages regarding translations (pump-ups). Captured automatically when spilog is enabled |
| Agent Log | `/cms/pbx/acd1/ag.log` | Protocol messages for agent login/logout activity |
| Link Trace | `/cms/pbx/acd1/spi.lnk` | Link protocol events at session layer. Enable: `/cms/bin/lnktrace <acd_num> spi on` |

### 3. Administration, Backup, and Maintenance Logs

| Log | Path | Description |
|-----|------|-------------|
| Admin Log | `/cms/install/logdir/admin.log` | Execution of `cmsadm` and `cmssvc` commands |
| Admin Change Log | `/cms/db/log/admin_chg.log` | Admin changes from client (Add, Modify, Delete, Copy, Run) |
| User Change Log | `/cms/db/log/user_chg.log` | Add/delete/modify actions on user data |
| Backup Log | `/cms/maint/backup/back.log` | Maintenance Backup Data activities |
| Restore Log | `/cms/maint/restore/rest.log` | Maintenance Restore Data activities |
| Archiver Log | `/cms/dc/archive/arch.log` | Scheduled/manual archive of daily/weekly/monthly data |
| Interval Archive Log | `/cms/dc/harchive/harch.log` | Archiving of real-time data into historical tables |
| Migration Log | `/cms/maint/r3mig/mig.log` | Data migration activities (during upgrades) |

### 4. Web Client and Server Logs

| Log | Path | Description |
|-----|------|-------------|
| CMS Debug Log | `/opt/cmsweb/tomcat/logs/cms_debug.log` | Avaya software logging under Tomcat/browsers |
| Catalina Out | `/opt/cmsweb/tomcat/logs/catalina.out` | Standard Tomcat logging |
| User Log | `/opt/cmsweb/log/<username>.log` | Per-user tracing (OFF/DEBUG/TRACE via GUI Preferences or userlog.properties) |

### 5. Security and Licensing Logs

| Log | Path | Description |
|-----|------|-------------|
| CMS Security Log | `/cms/install/logdir/security/cms_sec.log` | Security activities, LDAP installation/config errors |
| License Log | `/cms/env/lm/license.log` | WebLM status checks, license violations, status changes |
| OS Secure Log | `/var/log/secure` | Linux authentication failures (SSH, LDAP) |

### 6. OS Logs and Crash Dumps

| Log | Path | Description |
|-----|------|-------------|
| System Messages | `/var/log/messages` | General OS messages. Monitor: `tail -f /var/log/messages` |
| Crash Dumps | `/var/crash/<hostname>/` | `vmcore.n` and `unix.n` files if system panics |

### CMS Log Capture Procedures

**Real-time monitoring:**
```bash
tail -f /cms/pbx/acd1/spi.err    # Watch ACD link status
tail -f /usr/elog/elog            # Watch error log
tail -f /var/log/messages         # Watch OS messages
```

**Enable detailed protocol logging (spi.log):**
```bash
/cms/bin/spilog <acd_number> all          # Start (or: err+xln+ag for specific flags)
/cms/bin/spilog <acd_number> -all         # Stop (MUST stop when done!)
```

**Enable link trace:**
```bash
/cms/bin/lnktrace <acd_number> spi on
```

**Bundle logs for escalation:**
```bash
# Bundle specific ACD data + error logs
find cms/pbx/acd1 usr/elog -print | cpio -ocvdumB >/dev/scsi/qtape1

# Bundle crash dumps
tar cvf /storage/cms_crashfiles.tar unix.X vmcore.X dmesg.out rpm_list.out messages
```

---

## AAEP / EPM / MPP / POM Log Collection

### Part 1: AAEP / EPM (Experience Portal Manager)

**VPMS (EPM) Logs:** `/opt/Avaya/ExperiencePortal/VPMS/logs/`
- `avaya.vpms.log`
- `avaya.audit.log`
- `avaya.appintfservice.log`

**Tomcat Logs:** `/opt/Tomcat/tomcat/logs/` (or `$CATALINA_HOME/logs`)
- `catalina.out`
- `localhost_access_log`

**Installation Logs:** `/opt/Avaya/InstallLogs/`
- `aepinstall.log`
- `pvichecker.log`

**Apache HTTPD Logs:** `/var/log/httpd/`
- `ssl_error_log`
- `access_log`

**Capture EPM logs:**
```bash
cd /opt/Avaya/ExperiencePortal/Support/VP-Tools/
./getepmlogs.sh --ALL        # Comprehensive collection
# Options: --EPM (VPMS logs only), --Apache (web server logs), --MainTomcat
```

### Part 2: MPP (Media Processing Platform)

| Component | Path | Files |
|-----------|------|-------|
| Session Manager | `$AVAYA_MPP_HOME/logs/process/SessMgr/` | `SessionManager.log`, `SessionSlot-###.log` |
| Voice/CCXML Browser | `$AVAYA_MPP_HOME/logs/process/VB/` or `.../CXI/` | Voice Browser, CCXML Interpreter logs |
| System Manager (MPP) | `$AVAYA_MPP_HOME/logs/process/SysMgr/` | `logfile.log` |
| Core Dumps | `/opt/Avaya/ExperiencePortal/MPP/logs/core` | (if enabled) |

**Capture MPP logs:**
```bash
cd /opt/Avaya/ExperiencePortal/MPP/bin/
./getmpplogs.sh --logs --transcriptions --debugfiles
# --transcriptions: Include utterance data
# --debugfiles: Include core dump files
```

**Alternative (GUI):** EPM web interface → System Management → MPP Manager → Service Menu → Diagnostics → Pack Files → Select log types → Pack

#### MPP SIP/CCXML Log Invariants for POM Predictive Investigations

- **`SessionManager.log` rotates fast (~1 h retention under POM campaign load)** while `CCXML-SessionSlot-NN.log*` rotates per-session and has longer effective retention for any given call. Rotation is size-based (~21 MB × 8 files = ~168 MB total). Under typical POM campaign load this fills in roughly one hour. **Request `getmpplogs.sh` tarball within ~1 h of any POM incident** to preserve SIP-level evidence. If too late, fall back to CCXML per-slot logs which still hold `hints.sip.replaces`, `AGTCallNotifyDriver`, and other session-level events. Reference: SR `1-23647477802` — BC1 tarball captured ~25 min after incident preserved full SessionManager.log; BC2 tarball at ~1.5 h had cycled past BC2 timestamp in all 8 rotation files but CCXML slot logs were intact.
- **Map Platform Session ID to slot file via trailing `-NN`**: Campaign Detail Report column 33 format is `PVCLIPxxxxxxx-YYDDDHHMMSS-NN`. The trailing `-NN` is the CCXML slot ID. Driver session for a customer call goes to `CCXML-SessionSlot-NN.log*`. The nail-up session that handled the bridging is in a DIFFERENT slot — find it by grepping all `CCXML-SessionSlot-*.log*` for the customer phone or `evt.AGTCallCustomer` containing that phone.
- **`hints.sip.replaces` in a CCXML log is equivalent evidence to `SND ^INVITE Replaces:` in `SessionManager.log`**: When SessionManager.log has rotated past the incident, the CXI Interpreter event `hints.sip.replaces` in the nail-up session's CCXML-SessionSlot log unambiguously proves the Replaces INVITE was generated. POM CXI does not emit this event without immediately invoking `command.createcall` with the Replaces parameter; latency between CXI event and on-the-wire SIP send is consistently 18–20 ms. Reference: SR `1-23647477802` BC2 — direct SIP wire evidence lost to rotation, `hints.sip.replaces` in `CCXML-SessionSlot-020.log.1` accepted as equivalent.
- **SM syslog stream is an independent SIP transaction record useful for pcap cross-validation**: Avaya SM forwards every SIP message it processes to a syslog target (typically UDP from SM IP to log server on `:514` or non-standard high port). Each syslog packet contains the full SIP message in payload (sometimes spanning 2–3 UDP packets — group by `(src_port, dst_port)` tuple to reassemble). The SM syslog stream is visible inside customer pcap because the traffic transits the same capture point. Useful as a second source to corroborate or refute pcap observations. Caveat: absence of a SIP message in SM syslog confirms only that SM did not process it — it is NOT by itself sufficient to attribute root cause to any specific component. Reference: SR `1-23647477802` — SM `PVCLIPBASM0031H` syslog at `172.17.61.10 → 172.17.65.96/.97` used as pcap cross-validation.

### Part 3: POM (Proactive Outreach Manager)

**POM_HOME default:** `/opt/Avaya/avpom/POManager`

#### POM Component Log Reference

| Component | Log Files | Default Path | Description |
|-----------|-----------|--------------|-------------|
| Campaign Manager | `PIM_CmpMgr.log`, `CmpMgrService.out` | `$POM_HOME/logs` | Campaign execution, dialing logic, runtime exceptions |
| Agent Manager | `PIM_AgtMgr.log`, `PAMService.out` | `$POM_HOME/logs` | Agent operations, licensing, router, Pacer activities. FINEST shows login details |
| Campaign Director | `PIM_CmpDir.log`, `CmpDirService.out` | `$POM_HOME/logs` | Campaign life-cycles, data imports/exports |
| Web Services | `PIM_WebService.log`, `PIM_RestService.log` | `$POM_HOME/logs` | Agent and campaign SOAP/REST Web services |
| Rule Engine | `PIM_RuleEngine.log`, `RulEngService.out` | `$POM_HOME/logs` | Rule Engine evaluation of contacts |
| Dashboard | `DashBoard_Supervisor.log`, `POMDashboardService.out` | `$POM_HOME/logs` | Supervisor Dashboard, real-time monitoring |
| ActiveMQ | `PIM_ActMQ.log`, `POMActMQService.out` | `$POM_HOME/logs` | Internal message exchange exceptions |
| Kafka / Zookeeper | `kafkaserver.out`, `zookeeperserver.out` | `$POM_HOME/logs` | Kafka/Zookeeper runtime messages |
| Agent SDK | `PIM_AgtSDKService.log`, `PIM_AgtSDKApi.log` | `$POM_HOME/logs` | Agent SDK service (Workspaces interface), API calls |
| Nailer/Driver | `POM_NailerDriver.log` | `$APPSERVER_HOME/logs` (e.g., `/opt/AppServer/Tomcat/tomcat/logs`) | CCXML application activities |
| AEP EPM | `avaya.vpms.log`, `avaya.appintfservice.log` | `$AVAYA_HOME/VPMS/logs` | EPM application activities |
| Installation | `InstallPOM.log`, `installDB.log`, `aepinstall.log` | `$POM_HOME/logs`, `/opt/Avaya/InstallLogs/` | Installation and DB schema creation |

**Capture POM logs:**
```bash
cd $POM_HOME/bin
./getpomlogs.sh --logs
# -a: Include AppServer logs
# -c: Include MPP CXI logs (if co-resident)
```

**Change POM log level:**
```bash
# Via script
$POM_HOME/bin/changeLogLevel.sh <COMPONENT> <LEVEL>
# Example: changeLogLevel.sh AGTMGR_TRACER FINEST

# Via UI: Configuration > POM Servers > POM Settings
```

**PII scrubbing before sharing logs:**
```bash
$POM_HOME/bin/dataScrubbing.sh <path_to_logs>
# Masks phone numbers, IP addresses
```

### Part 4: POM/EPM/MPP Log Capture Quick Reference

| Component | Tool | Steps |
|-----------|------|-------|
| POM Logs | `getpomlogs.sh` | 1. SSH as root to POM server. 2. `cd $POM_HOME/bin`. 3. `./getpomlogs.sh --logs` (`-a` for AppServer, `-c` for MPP CXI) |
| MPP Logs | `getmpplogs.sh` | 1. SSH as root to MPP. 2. `cd $AVAYA_MPP_HOME/bin`. 3. `./getmpplogs.sh --logs --transcriptions --debugfiles` |
| EPM Logs | `getepmlogs.sh` | 1. SSH as root to EPM. 2. `cd $AVAYA_HOME/Support/VP-Tools/`. 3. `./getepmlogs.sh --ALL` (`--EPM`, `--Apache`, `--MainTomcat`) |
| Log Level | Script / UI | Script: `$POM_HOME/bin/changeLogLevel.sh <COMPONENT> <LEVEL>`. UI: Configuration > POM Servers > POM Settings |
| Log Scrubbing | `dataScrubbing.sh` | `cd $POM_HOME/bin && ./dataScrubbing.sh <path_to_logs>` |
| Network Trace | `tcpdump` | See [Network Trace](#network-trace-tcpdump) section |

---

## WFO / ACR Log Collection

### 1. ACR Server (Linux/Windows Recording Engine)

| Component | Path / File | Capture & Configuration |
|-----------|-------------|------------------------|
| **Main Application Logs** | Linux: `/opt/witness/logs/`<br>Windows: `<Install Path>\logs\` (e.g., `D:\Avaya\ACR152\logs`)<br>Files: `acr.log`, `acr.log.<date>` | **Dynamic level change (no restart):** `http://<server>:8080/log?level=DEBUG` (revert with `level=INFO`)<br>**Permanent:** Edit `acr.properties` → add `log.level=DEBUG` → restart service |
| **Tomcat** | Same as main logs<br>Files: `catalina.out`, `localhost.<date>.log` | Managed by Tomcat service wrapping recorder |
| **Usage & Statistics** | Same as main logs<br>Files: `usage.log`, `partystats.log`, `partystats.yyyy-mm-dd.csv` | Usage Report: `http://<server>:8080/servlet/report...`<br>Party Stats: set `usage.dailystats=true` in acr.properties |
| **Config Snapshot** | Same as main logs<br>File: `nnnnnn_config.csv` (serial number) | Enable: `config.reporting=true` in acr.properties → daily snapshot of recording targets |
| **Syslog / SNMP** | N/A (sent to remote server) | Syslog: Maintenance page (`/servlet/acr?cmd=mtce`) → forward INFO/WARN/ERROR to remote syslog<br>SNMP: Set SNMP Read Community in General Setup; configure MIBs in NMS |

### 2. WFO Framework & Application Servers

| Component | Path / File | Capture & Configuration |
|-----------|-------------|------------------------|
| **Production Server (WebLogic)** | `%IMPACT360DATADIR%\Logs\ProductionServer`<br>Files: `wfo.log4j.log`, `error.log`, `coherence.log` | Use WFO Log Manager in System Monitoring. Select `core.xml` or `debugFile.xml`. Logs zipped at 20MB |
| **Enterprise Manager Agent (EMA)** | `%IMPACT360DATADIR%\Logs\EMA`<br>Files: `ema.log`, `ema.error.log`, `ema.debug.log` | Use WFO Log Manager to enable/disable, change retention |
| **Recorder Manager (RM)** | `%IMPACT360DATADIR%\Logs\RM`<br>Files: `rm.error.log`, `rm.debug.log` | Use WFO Log Manager on local server |
| **Auth / LDAP** | `%VERINT_WEBLOGIC_DOMAIN_HOME%\logs`<br>Files: `ProductionServer.log`, `ProductionDomain.log` | Enable ATN/ATZ debug flags in WebLogic Console: Environment → Servers → Debug → Security. Increase file rotation size if needed |
| **HTTP Access Logs** | `%IMPACT360DATADIR%\Logs\SecureGateway\SGW_Access_CF.ltf`<br>`...Logs\ProductionServer\weblogic\access.log` | Trace incoming HTTP requests, source IPs, auth methods (UserToken, PassphraseToken) |
| **Audit Trails** | `%IMPACT360DATADIR%\Logs\Audit Trail\Audit Trail_mm.dd.yy_....ltf` | Generated daily. System Monitoring → Audit Viewer → search and export to CSV |

### 3. WFO Recorder Components (Windows)

| Component | Path / File | Capture & Configuration |
|-----------|-------------|------------------------|
| **Integration Service (RIS)** | `%IMPACT360DATADIR%\Logs\IntegrationService\IntegrationService.log` | Use `LogManager.exe` (in `%IMPACT360SOFTWAREDIR%\ContactStore`) → set Trace Level to **DebugHigh** for CTI events |
| **Integration Service Wrapper** | `<Install Dir>\conf\log files\IFwrapper-YYYYMMDD.ROLLNUM.log` | Managed via `IntegrationServiceWrapper.conf`. Independent of standard Log Manager |
| **IP Capture / TDM Capture** | `%IMPACT360DATADIR%\Logs\IPCapture` (or `TDMCapture`) | Use LogManager.exe → Trace Level: Debug. Tracks RTP packet processing and signaling |
| **Consolidator** | `%IMPACT360DATADIR%\Logs\callsconsolidator` | Movement of calls from buffer to database. Use Log Manager to adjust levels |
| **Archiver** | `%IMPACT360DATADIR%\Logs\archiver` | Archive campaigns and file transfers. Use Log Manager to adjust levels |

### 4. Desktop Applications

| Component | Path / File | Capture & Configuration |
|-----------|-------------|------------------------|
| **Screen Capture / AIM** | `<Program Files>\Witness Systems\Screen Capture Module\Logs\`<br>Files: `CaptureService.log`, `wcapw32.log` | Verify in CaptureService.log. For triggering issues, also check server-side `integrationservice.log` |
| **Face-to-Face Recorder** | Service: `C:\Program Files (x86)\Face to Face Interaction Recorder\logs`<br>App: `...\F2F Recorder Application\logs`<br>Files: `F2FRecorderService_...log` | Modify `.config` files (e.g., `Verint.Recording.RecorderService.exe.config`) → change `<level>` from DEBUG to TRACE |
| **DPA (Desktop Analytics)** | `%PROGRAMDATA%\Verint\DPA\Logs` | Use Client Trace Files feature in DPA System Tab to remotely collect zipped logs without accessing client machines |
| **Strategic Planner** | `%USERPROFILE%\StrategicPlanner\Logs\`<br>Files: `Planner.log`, `PlannerConsole.log` | Initialization and scenario errors |

### 5. Analytics & Import/Export

| Component | Path / File | Capture & Configuration |
|-----------|-------------|------------------------|
| **Speech Analytics** | `%IMPACT360SOFTWAREDIR%\SpeechCatTomcat64\log\speechcat\`<br>Files: `sclog*.log` | Analyze for index corruption or initialization failures |
| **Import / Export Manager** | `%IMPACT360DATADIR%\Logs\IEM\`<br>Files: `extraction.log`, `extractionManager.log` | Edit `logback.xml` in `IMPACT360SOFTWAREDIR\ExtractionEngine\bin` to change level or file size |
| **Transcription Repository** | `%IMPACT360DATADIR%\Logs\TranscriptionRepositoryService\trs.log` | Connection issues between repository and Speech/Contact databases |
| **Real-Time Analytics** | `%IMPACT360DATADIR%\Logs\AnalyticsService\analyticsservice.log` | Consolidated logs for kwsengine, decisionprocessor. Check `analyticsserviceexternalurlfailures` folder |

### 6. OS & Infrastructure (WFO)

| Component | Path / Tool | Usage |
|-----------|-------------|-------|
| **Windows Event Logs** | Event Viewer (`eventvwr.msc`) → Application / System | Service start/stop events, "File Tampered" alarms, unexpected shutdowns |
| **Performance Monitor** | PerfMon (`perfmon.exe`) | Monitor counters (e.g., Recorder Analytics Service Providers) for CPU, memory leaks, overload |
| **SQL Server Logs** | SSMS → Management → SQL Server Logs | Database engine errors, connectivity issues, job failures (e.g., "LogReader subsystem failed") |
| **KMS Upgrade Logs** | `<drive>:\<KMS_folder>\logs\`<br>Files: `Check_database.log`, `JREInstall.log` | Troubleshoot Key Management Server upgrade failures |

---

## Async Channel & Orchestration Debug Commands

Diagnostic commands and log paths for asynchronous outreach, omnichannel routing, and agent orchestration components. Use these when troubleshooting POM campaigns, Oceana routing, CCMM callbacks, Workspace agent state, or AEP screen-pop behavior.

### POM (Proactive Outreach Manager) Debug Commands

| Diagnostic | Command / Path | Log Search String | Trace Enable |
|-----------|-----------|----------|-----------|
| Campaign state | `display pom-campaign <campaign_ID>` | Check `state` field: pending, active, paused, completed | Set `DEBUG=pom.orchestration` in startup config |
| Agent fetch | `display pom-agent-state <agent_ID>` | Verify Oceana sync status (`AACC_SYNC`, `OCEANA_REGISTERED`) | `DEBUG=pom.agent-assignment` |
| DMCC registration | `status recording-data` | Verify DMCC device status in output | Enable DMCC trace (see AES Log Collection) |
| Campaign execution | `$POM_HOME/logs/PIM_CmpDir.log` | Search: `campaign state change`, `agent assignment`, `orchestration timeout`, `rule engine TIMEOUT` | `changeLogLevel.sh CAMPAIGN_DIRECTOR FINEST` |
| Agent assignment | `$POM_HOME/logs/PIM_AgtMgr.log` | Search: `agent fetch TIMEOUT`, `skill assignment failed`, `AACC unavailable` | `changeLogLevel.sh AGTMGR_TRACER FINEST` |

### Oceana (Omnichannel Engagement) Debug Commands

| Diagnostic | Command / Path | Log Search String | Trace Enable |
|-----------|-----------|----------|-----------|
| Engagement routing | Oceana UI > Administration > Engagement Routing | Verify routing rules enabled, agent skill mapping active | Oceana log4j: set TRACE level for Oceana Core |
| Agent assignment | Verify AACC skill assignment responds <3 sec | Check AACC skill queue for agent availability | Enable TRACE in Oceana connector config |
| SIP trunk status | `display sip-entity <entity>` (in CM) | Cross-verify in Oceana registration table | Enable SIP trace in CM and Oceana |
| Engagement queue | `$OCEANA_HOME/logs/OceanaCore/` | Search: `route decision timeout`, `agent assignment failed`, `context store sync FAIL`, `agent not found in skill queue` | Set log4j level to TRACE in Oceana app config |
| Service health | Oceana UI > Administration > Service Status | Verify all services (Engine, Gateway, Router) = Online | Monitor real-time service dashboard |

### CCMM (Channel Communications Manager) Debug Commands

| Diagnostic | Command / Path | Log Search String | Trace Enable |
|-----------|-----------|----------|-----------|
| Callback queue | CCMM UI > Callback > Active Callbacks | Check `state`: queued, delivering, failed, expired | Set CCMM log level to DEBUG in config |
| Channel gateway status | CCMM UI > Channels | Verify each channel (SMS/Email/Social): heartbeat OK, last sync time <5 min | Enable trace for each channel gateway |
| Email gateway heartbeat | `$CCMM_HOME/logs/` | Search: `gateway heartbeat timeout`, `connection failed`, `delivery retry exceeded` | Increase heartbeat timeout to 2 sec in CCMM config |
| Deduplication | `$CCMM_HOME/logs/` | Search: `deduplication event`, `phone number format invalid`, `duplicate contact detected` | Enable deduplication trace in CCMM config |
| Engagement state | `$CCMM_HOME/logs/` | Search: `engagement state mismatch`, `callback orchestration error`, `engagement not found` | Set log level to TRACE for orchestration module |

### Workspace (Agent Desktop) Debug Commands

| Diagnostic | Command / Path | Log Search String | Trace Enable |
|-----------|-----------|----------|-----------|
| Session cache | Browser console: `console.log(sessionStorage)` | Verify `agentState`, `skillQueue`, `engagement` keys present and non-stale (timestamp <30 sec old) | Browser DevTools > Application > Console |
| Engagement queue | Reload page (F5) | Verify engagement queue state reflects backend after 2-3 sec | DevTools Network tab > filter `/api/engagement` |
| REST API latency | Browser DevTools Network tab > filter `/api/engagement` | Check response time <500ms, status 200 OK | Enable Network logging in DevTools |
| Session cache errors | Browser DevTools Console | Search: `SessionCache.invalidate() FAILED`, `state sync error`, `backend connection lost` | Monitor console for errors/warnings |
| Agent state sync | DevTools Network > XHR/Fetch | Verify polling requests to `/api/agent/state` succeed every 10 sec | Check request/response bodies in DevTools |

### AEP (Avaya Experience Portal / IVR) Debug Commands

| Diagnostic | Command / Path | Log Search String | Trace Enable |
|-----------|-----------|----------|-----------|
| Screen-pop CRM connector | AEP UI > Connectors | Verify connector status, connection heartbeat OK, last sync time <1 min | Enable connector trace in AEP config |
| REST timeout settings | AEP Configuration > Connectors | Default timeout: 1 sec. Increase to 2 sec if CRM slow (latency >500ms) | Set connector REST timeout in AEP config UI |
| CRM screen-pop | `$AEP_HOME/logs/` | Search: `CRM REST timeout`, `screen-pop enrichment failed`, `connector unavailable`, `response timeout after X sec` | Enable CRM connector trace in log4j config |
| IVR context store | `$AEP_HOME/logs/` | Search: `context store sync TIMEOUT`, `engagement context not found`, `state mismatch` | Set IVR log level to TRACE in AEP config |

---

## Network Trace (tcpdump)

Applies to EPM, MPP, POM, AES, CMS, and any Avaya Linux server.

```bash
# Identify network interface
ifconfig
# or
ip addr

# Basic capture
tcpdump -i eth0 -s 0 -w /tmp/capture.pcap

# Filtered capture (RECOMMENDED)
tcpdump -i eth0 -n -nn -v -vv -s 0 host <Target_IP> or port <Port_Number> -w /tmp/issue_trace.pcap
```

**Common port filters:**
| Protocol | Port | Filter |
|----------|------|--------|
| SIP | 5060/5061 | `port 5060` |
| HTTPS | 443 | `port 443` |
| RTP (media) | Dynamic | `host <endpoint_IP>` |
| ASAI (CM↔AES) | Service-specific | `host <CM_IP> or host <AES_IP>` |

**Procedure:**
1. Log in to target server as root
2. Start tcpdump with filter
3. Reproduce the issue while capture runs
4. Stop: `Ctrl + C`
5. Retrieve file via SCP/SFTP (e.g., WinSCP)
6. Open in Wireshark for analysis

**Analysis tips:**
- **TLS Handshakes:** Verify Client/Server Hello and certificate validity
- **SIP/RTP:** Check SIP response codes (408 Timeout, 200 OK) and RTP packet flow

---

## Proactive Server Health Commands

> Applicable to all Avaya Linux servers: AES, Session Manager, EPM, AACC, ACRA. Run ad-hoc or via cron.

### Quick Health Check (A1)

```bash
echo "=== Avaya Server Health: $(hostname) | $(date) ==="
echo "--- CPU (top 5 processes) ---"
top -bn1 | head -15
echo "--- Memory ---"
free -h
echo "--- Disk (Avaya paths: /var/log/avaya, /opt/avaya, /tmp) ---"
df -h | grep -E "Filesystem|avaya|opt|log|tmp"
echo "--- System Load ---"
uptime
echo "--- Network — Avaya ports (5060 SIP | 5061 SIP-TLS | 1099 JTAPI | 8443 AES-HTTPS | 4445 TSAPI | 7001 WebLogic) ---"
ss -tuln | grep -E '5060|5061|1099|8443|4445|7001'
echo "--- Java/Avaya Processes ---"
ps aux | grep -E '[Jj]ava|csta|weblogic|avaya' | grep -v grep
```

### Service Status Check — systemd (A4)

```bash
services=("csta-server" "avaya-aes" "weblogic" "jboss" "sshd" "ntpd" "chronyd")
for svc in "${services[@]}"; do
  if systemctl is-active --quiet "$svc" 2>/dev/null; then
    echo "OK  $svc"
  elif pgrep -f "$svc" > /dev/null 2>&1; then
    echo "OK  $svc (process found, not systemd)"
  else
    echo "ERR $svc — NOT running"
  fi
done
```

### Daily Avaya Health Check Script (F1)

Save as `/opt/avaya/scripts/daily_health_check.sh`, cron: `0 6 * * *`

```bash
#!/bin/bash
LOG=/var/log/avaya/health_$(date +%Y%m%d).log
exec >> $LOG 2>&1

echo "=== Avaya Daily Health Report === $(hostname) | $(date)"
echo "1. Uptime:"; uptime
echo "2. CPU top:"; ps aux --sort=-%cpu | head -8
echo "3. Memory:"; free -h
echo "4. Disk:"; df -h
echo "5. Large files in Avaya dirs (>100MB):"; find /var/log/avaya /opt/avaya -size +100M -ls 2>/dev/null
echo "6. Avaya ports:"; ss -tuln | grep -E '5060|5061|1099|8443|4445|7001'
echo "7. Java/Avaya procs:"; ps aux | grep -E '[Jj]ava|csta|weblogic|avaya' | grep -v grep
echo "8. Recent errors (files with ERROR/EXCEPTION since yesterday):"
find /var/log/avaya /opt/avaya -name "*.log" -newer /tmp/.last_health_check \
     -exec grep -l "ERROR\|EXCEPTION\|FATAL" {} \; 2>/dev/null | head -10
touch /tmp/.last_health_check
echo "=== Done ==="
```

---

## Auto-Remediation Playbooks

### Disk Full → Log Rotation / Cleanup (D2)

> Trigger: disk usage >85% on `/var/log` or `/opt/avaya`. Requires approval on production.

```bash
# Step 1: identify largest consumers
du -sh /var/log/avaya/* 2>/dev/null | sort -rh | head -20
du -sh /opt/avaya/*/logs/* 2>/dev/null | sort -rh | head -20
du -sh /tmp/* 2>/dev/null | sort -rh | head -10

# Step 2: compress logs older than 7 days
find /var/log/avaya -name "*.log" -mtime +7 -exec gzip {} \;
find /opt/avaya -name "*.log" -mtime +7 -exec gzip {} \;

# Step 3: delete compressed logs older than 30 days
find /var/log/avaya -name "*.gz" -mtime +30 -delete
find /opt/avaya -name "*.gz" -mtime +30 -delete

# Step 4: clean /tmp
find /tmp -mtime +1 -delete 2>/dev/null || true

# Step 5: verify
df -h /var/log; df -h /opt/avaya
```

> Policy parameters: `cooldown_seconds: 3600` | `execution_mode: approval` | Verification: `df -h | awk '$6~"avaya"{print $5}'`

### Service Crash → Auto-Restart Rule (D1)

```
Alert keywords: ["down", "stopped", "unreachable", "crash", "failed"]
Cooldown: 300 seconds | Max restarts/hour: 3

Remediation:
  systemctl restart <service>
  # OR for non-systemd Avaya services:
  /opt/avaya/<service>/bin/stop.sh && sleep 10 && /opt/avaya/<service>/bin/start.sh

Verification: systemctl is-active <service>  OR  nc -zv <host> <port>

Safe for auto-restart: AES csta-server, ACRA recorder agent, POM outbound server
ALWAYS require approval: CM, SMGR, WebLM, Avaya Voice Portal, AACC OAM
```

---

## SNMP Monitoring

### SNMP Query Patterns for Avaya Infrastructure (E2)

```bash
AVAYA_HOST="<avaya-server-ip>"
COMMUNITY="<snmp-community>"

# Basic connectivity
snmpwalk -v2c -c $COMMUNITY $AVAYA_HOST sysDescr
snmpwalk -v2c -c $COMMUNITY $AVAYA_HOST sysUpTime

# Interface statistics
snmpwalk -v2c -c $COMMUNITY $AVAYA_HOST ifTable

# CPU / Memory (Host Resources MIB — Linux)
snmpget -v2c -c $COMMUNITY $AVAYA_HOST hrProcessorLoad.1
snmpwalk -v2c -c $COMMUNITY $AVAYA_HOST hrStorageSize

# Avaya enterprise MIB root: .1.3.6.1.4.1.6889
# Install Avaya MIBS package for CM-specific OIDs:
# /usr/share/snmp/mibs/ after package install

# Test SNMP trap reception (from NMS to Avaya):
snmptrap -v2c -c $COMMUNITY <nms-ip> '' .1.3.6.1.6.3.1.1.5.3 \
  .1.3.6.1.2.1.2.2.1.1.1 i 1
```

---

## Monitoring Thresholds

### Alert Threshold Definitions for Avaya Servers (F2)

| Metric | Warning | Critical | Notes |
|--------|---------|----------|-------|
| CPU usage (%) | 70 | 90 | AES/AACC Java GC can spike briefly; don't act on single sample |
| Memory usage (%) | 80 | 95 | AES heap OOM causes CTI failures; collect jstack before restart |
| Disk /var/log (%) | 75 | 85 | Avaya logs grow fast; auto-rotate compresses logs >7 days |
| Disk /opt/avaya (%) | 80 | 90 | ACRA recordings accumulate; alert L2 before cleanup |
| Open FDs — AES (count) | 50000 | 60000 | Default ulimit 65536; AES leaks FDs under load |
| JTAPI connections (% cap) | 80 | 95 | Monitor via AES admin web UI |
| DB idle connections — PG | 20 | 50 | AES PostgreSQL; signals connection leak |
| WebLogic thread pool (%) | 75 | 90 | ACRA WebLogic; monitor via admin console |

**Alert keyword taxonomy for remediation matching:**

```
disk:        ["disk", "space", "full", "filesystem", "inode"]
service:     ["down", "stopped", "unreachable", "crash", "failed", "restart"]
certificate: ["certificate", "expir", "cert", "ssl", "tls", "trust"]
memory:      ["memory", "heap", "OutOfMemory", "oom", "GC overhead"]
cpu:         ["cpu", "load", "high", "utilization"]
database:    ["connection pool", "JDBC", "exhausted", "pg_connect", "timeout"]
```

---

## Command Safety Rules for Avaya Automation

### Blocked / Restricted Commands (F3)

Never issue these without explicit human approval on Avaya production servers:

| Command | Risk | Action |
|---------|------|--------|
| `rm -rf /` or `rm -rf *` | Destroys OS/Avaya data | **ALWAYS blocked** |
| `dd if=/dev/zero` or `mkfs.*` | Wipes partition | **ALWAYS blocked** |
| `iptables -F` | Drops all SIP/JTAPI firewall rules | **ALWAYS blocked** (operator role) |
| `ip link delete` | Kills CM/AES connectivity | **ALWAYS blocked** |
| `kill -9 0` or `killall -9` | Kills all processes including Avaya | **ALWAYS blocked** |
| `cat /etc/shadow` or `cat *.pem` or `cat *.key` | Credential exposure | **Warn + audit log** |
| `systemctl stop <avaya-service>` | Stopping riskier than restart | **Always require approval** |
| `jmap -dump ...` | Heap dump — large file + service degradation | **Always require approval** |
| `UPDATE <table>` or `DELETE FROM <table>` | DB changes on AES/AACC | **Always require approval** |
| `iptables -A` or `iptables -D` | Firewall changes affect SIP/JTAPI | **Always require approval** |

> Auto-safe (no approval needed): `systemctl status`, `ps aux`, `df -h`, `ss -tuln`, `jstat -gcutil`, `netstat`, `grep` on log files, `top -bn1`
