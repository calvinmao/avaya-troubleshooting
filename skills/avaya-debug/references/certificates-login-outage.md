# Certificates / WebLM / Login / Outage Recovery Reference
<!--
scope: Certificate lifecycle, WebLM, EPM/SMGR login, outage recovery, JKS trust store
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: keytool flag syntax across JDK versions, Avaya WebLM license server URLs, cert SAN requirements
related_docs: diagnostic-principles.md (invariant 8), linux-server.md, lessons/certificates-login-outage.md
-->



## Table of Contents
- [Certificates / WebLM Trust-Store Ecosystem](#certificates--weblm-trust-store-ecosystem)
- [Certificate DR / Geo Redundancy](#certificate-dr--geo-redundancy)
- [Certificate Cascade Failure (Workflow 16)](#certificate-cascade-failure)
- [Certificate Cascade Across Products](#certificate-cascade-across-products)
- [Login / Authentication Failure (Workflow 13)](#login--authentication-failure)
- [Outage / Total System Down (Workflow 17)](#outage--total-system-down)
- [SMGR Troubleshooting (Workflow 23)](#smgr-troubleshooting)
- [CMS Historical Report (Workflow 24)](#cms-historical-report)
- [Login / Auth Fault Patterns](#login--auth-fault-patterns)
- [Historical Cert / Login / SAML / Outage Patterns](#historical-cert--login--saml--outage-patterns)

---

## Certificates / WebLM Trust-Store Ecosystem

WebLM (Web License Manager) deployment matters. In **local-master** mode the local WebLM must trust **itself** because it makes an internal HTTPS request to install the temp ALF after receiving it from the master.

### Key trust stores (AEP 8.1.2 example)

| Trust store | Path | Purpose |
|-------------|------|---------|
| EPM → local WebLM | `/opt/Tomcat/tomcat/webapps/VoicePortal/WEB-INF/lib/trusted_weblm_certs.jks` | Lets EPM acquire license from local WebLM. |
| Master WebLM (SMGR) → local WebLM | SMGR trust store (System Manager → Security → Certificates) | Lets master WebLM push ALF to local WebLM. |
| Local WebLM → itself | `/opt/Tomcat/tomcat/webapps/WebLM/admin/trusted_weblm_certs.jks` | Lets local WebLM finish the internal handshake and install ALF. |

On AEP 8.1.2 the local WebLM trust-store pointer in `/opt/Tomcat/tomcat/webapps/WebLM/admin/trustedcert.properties` defaults to `truststore` (not `trusted_weblm_certs.jks`); confirm before importing. New WebLM certs must include **FQDN + hostname + IP** in SAN; renewal scripts: `renew_weblm_cert.sh`, KB **SOLN385385** (per `1-23280139504`).

### Tomcat in-memory keystore reload race

Per `George_1-22940142572`: even after the on-disk JKS is updated, a running Tomcat application can keep an old/wrong keystore in memory and still send/validate against it. After cert rollover always:

1. Inventory **every** JKS on the appliance: `find / -name '*.jks'`. Per-application keystores often live outside Tomcat (e.g., `/opt/Avaya/ING/ingivr.keystore.jks`) and also need the new CA.
2. Restart the app to force keystore reload.
3. Clear browser cache before re-testing.

### HA cert symmetry

In an AES HA pair, both servers must have the new cert at the same time. Asymmetric expiry presents as `HA Far End is unreachable` while CTI services look healthy on each node individually (per `1-23193638232`).

### WebLM License Management Failure Patterns

- **Grace Mode**: WebLM unreachable → check service, network path, certificate trust between product and WebLM (per `1-18185450724`).
- **Host ID Changed**: WebLM ties licenses to server Host ID. VM migration, hardware change, or MAC change invalidates licenses → contact Avaya to re-issue file with new Host ID (per `1-18627666022`, `1-22825450182`).
- **Products Cannot Connect to WebLM**: Verify URL accessible, certificate trusted, firewall allows HTTPS to WebLM port. Per `1-19044928952`: ACCCM could not connect after network change.
- **License Not Coming Up After Install**: Verify file matches product version, Host ID, entitlement; check WebLM logs (per `1-19101968712`).

---

## Certificate DR / Geo Redundancy

| Component | Considerations |
|-----------|---------------|
| **Certificate DR** | Cluster certificate rotation must be performed on **ALL nodes**; partial rotation causes cascade failures (per `202509` Dubai Police case). |
| **Analytics DR** | Primary and DR cluster replication; slow replication is common after initial configuration. DR site may show minor alarms for pods that haven't fully synced. |
| **Oceana DR** | UCAStoreService backup/restore on new WSfE/Oceana nodes may fail if backup was from different version (per `202505` SCB case). |

---

## Certificate Cascade Failure

**Workflow 16: Certificate Cascade Failure Diagnosis** — when certificate expiration or rotation causes failures across multiple products.

```
Step 1 — Identify the Scope
  Single product affected?         → Local cert issue
  Multiple products simultaneously?→ Shared CA or chain issue
  Failure after cert rotation?     → Incomplete rollout or app not restarted

Step 2 — Map Certificate Dependencies
  Common cascade paths:
    SMGR cert expires        → WebLM fails → all products lose license
    Analytics cert expires   → Oceana REF connection fails → no data pipeline
    CA cert updated          → all products using that CA need truststore update
    APC Oracle cert expires  → APC services fail → dependent apps fail

Step 3 — After ANY Cert Change, Verify ALL THREE
  1. On-disk JKS updated?     → find / -name '*.jks' to inventory ALL keystores
                                (per-app keystores exist outside Tomcat,
                                 e.g., ingivr.keystore.jks)
  2. Application restarted?   → in-memory keystore may still have old cert
                                (Tomcat reload race, per George_1-22940142572)
  3. Browser cache cleared?   → UI may show old cert state

Step 4 — Common Cascade Scenarios

  Scenario A: All CA certs updated → calls encounter silence
    - CA cert changed on SMGR, but endpoints still trust old CA
    - SIP signaling may work (TCP) but media (RTP) may fail
    - Fix: ensure new CA is in ALL truststores across ALL products
    - Verify: test call after each product's cert update; don't batch

  Scenario B: Analytics cert expired → cascade to WFO, Oceana
    - Analytics goes down → WFO Adherence loses data source
    - Oceana REF connection breaks → no real-time/historical data
    - Fix: renew Analytics cert, restart, clear browser cache, verify REF

  Scenario C: Cluster cert rotation partially failed
    - Some nodes have new cert, some have old → inter-node TLS fails
    - Fix: complete rotation on ALL nodes before testing
    - Per `202509` Dubai Police case: rotation must be atomic

Step 5 — Verify Certificate SAN Requirements
  New certificates MUST include in SAN:
    - FQDN
    - Hostname (short name)
    - IP address
  Missing SAN entries cause silent failures that don't appear in standard cert checks.

Step 6 — HA Certificate Symmetry
  In AES HA pair: both servers MUST have new cert at same time.
  Asymmetric expiry → "HA Far End is unreachable" while CTI looks healthy on each node.
  Per `1-23193638232`: cert expiry on one node breaks HA even if each node works alone.
```

---

## Certificate Cascade Across Products

Certificate expiry in one component can trigger failures across the entire stack.

### Cascade Paths

```
SMGR cert expires       → WebLM fails → ALL products lose license
Analytics cert expires  → Oceana REF connection fails → data pipeline down
                        → WFO Adherence loses data source
CA cert updated         → ALL products using that CA need truststore update
APC Oracle cert expires → APC services fail → dependent apps fail
```

### Key Rules

1. After cert change on ANY product: update truststore, restart app, clear browser cache.
2. In HA pairs: update BOTH servers simultaneously.
3. Verify SAN includes FQDN + hostname + IP for every new cert.
4. Test inter-product connections after each cert change (don't batch).

### Common Missed Steps

- Per-application keystores outside Tomcat (`find / -name '*.jks'`).
- Browser cache showing old cert state after fix.
- HA far-end cert not updated (causes "unreachable" despite healthy local services).

---

## Login / Authentication Failure

**Workflow 13: Login / Authentication Failure Troubleshooting** — when agents or administrators cannot log in to any Avaya product.

```
Step 1 — Identify the Failing Product
  - POM Agent login?     → POM service, EPM connectivity, agent mapping
  - WSfE / Workspace?    → Oceana/AES services, Kafka pods, certificates
  - WFO login (500)?     → WebLogic, DMSA account, SQL Server, LDAP/AD
  - AES web page login?  → Tomcat, license, certificate, database
  - AIC agent login?     → AIC services, certificate, cluster health
  - CMS/CCMS login?      → CMS service, database, ODBC connection

Step 2 — Universal Login Dependency Chain
  Service Running? → Cert Valid? → DB Connected? → LDAP/AD Reachable?
  → License Available? → User Mapping Correct?

Step 3 — Product-Specific Checks

  WFO Login 500 Error:
    - WebLogic logs: weblogic.log, SecureServer.log
    - Verify DMSA (Directory Mirror Service Account) valid and not locked
    - SQL Server connectivity (driver: SQLNCLI11 vs MSOLEDBSQL)
    - If after modifying DMSA: service may fail to start (per `1-23153206492`)
    - LDAP/AD connectivity if Azure AD integrated (per `SR 1-22707690032`)
    - Clear browser cache (mandatory after any WFO web-tier fix)

  WSfE / Workspace Login Failed to Activate:
    - "Unable to retrieve Voice resource" → AES JTAPI service, CTI link, DMCC
    - "No video channel" → SIP registration, SM connectivity (per `1-22797159182`)
    - "Asking for Account name" → AXP config, tenant mapping (per `INC6804313`)
    - Kafka pod eviction → `kubectl get pods -A | grep kafka` (per `1-22983941332`)
    - Fluentd pod eviction → same root cause, different pod

  POM Agent Login:
    - POM adaptor service status
    - Agent exists in POM campaign with valid extension mapping
    - EPM connectivity (monitor page blank after EPM patch: per `1-22931333623`)
    - After POM upgrade: agent mapping may need re-creation

  AES Web Page Cannot Log In:
    - Tomcat service status
    - License file includes AES features (per `1-22657234112`)
    - Certificate: expired cert prevents HTTPS login
    - Database: PostgreSQL/MySQL service running on AES

Step 4 — Check Kafka Pod Eviction (Critical for Oceana/AACC/Workspace)
  kubectl get pods -A | grep -i evict
  Evicted Kafka or Fluentd pods prevent the authentication pipeline.
  Fix:  kubectl delete pod <evicted-pod> -n <namespace>

Step 5 — Check Certificate Chain (login fails after cert changes)
  - New cert installed but app not restarted → in-memory keystore has old cert
  - Browser cache showing old cert → clear browser cache
  - Intermediate CA missing → verify full chain in truststore
  - SAN missing FQDN/hostname/IP → cert valid but app rejects it

Step 6 — Check SAML / Third-Party IDP (OKTA, Azure AD, Keycloak)
  - SAML metadata from IDP current (not expired)
  - Assertion consumer service URL matches product config
  - SAML assertion attributes match expected mapping (email, groups, roles)
  - IDP cert in product truststore matches IDP signing cert
  - Per `1-20000705804`: OKTA SAML with ACRA requires exact attribute mapping
  - Per `1-19914698372`: Workspace SAML authorization failure = group/role mismatch
```

---

## Outage / Total System Down

**Workflow 17: Outage / Total System Down Recovery** — when an Avaya system is completely down or unresponsive.

```
Step 1 — Triage Priority Order
  1. Infrastructure: VMs running? Network reachable? Storage available?
  2. Platform: EPM/SMGR responsive? Database running?
  3. Application: Product services started? Licenses valid?
  4. Integration: Cross-product connections established?

Step 2 — EPM Down and Not Recovering (per 1-23180610622)
  1. Check VM status in vSphere/VMware
  2. Check disk space: df -h (full disk prevents service start)
  3. Check database connectivity: EPM depends on PostgreSQL
  4. Check license: WebLM must be reachable
  5. Check certificate: expired cert prevents HTTPS access
  6. If VM won't boot: check virtual hardware, snapshot revert option

Step 3 — After Power Outage Recovery
  1. Power on in dependency order:
     Network → Storage → SMGR → EPM → MPP → Application
  2. Wait 5-10 min between layers for services to initialize
  3. AACC after power outage: verify CVLAN link to CM, check AACC database
     (per `1-22822437842`)
  4. Analytics after reboot: see Workflow 15 for full K8s recovery
  5. Recording after outage: verify recording service started, check un-archived files

Step 4 — Total Outage With Recording Loss
  Pattern: outage → recovery → recording not happening
  Check:
    1. Is recording service running? (ACRA WebLogic, RIS)
    2. Is AES DMCC link up after recovery?
    3. Were DMCC devices re-registered after AES came back?
    4. Is disk space available for new recordings?
    5. Per `1-22892285872`: patch was applied but recording service not restarted

Step 5 — High Traffic Voice Outage (per INC6553253)
  1. Check CM CPU/memory: list measurement, status health
  2. Check trunk utilization: list measurements trunk-groups
  3. Check DSP resources: list measurement dsp-resource
  4. Check for resource exhaustion: too many simultaneous calls
  5. Consider: call gapping, trunk group overflow, vector queue limits

Step 6 — Verify Cross-Product Connections After Recovery
  - CM ↔ AES: status essver, status cti-link
  - CM ↔ AACC: CVLAN link, vector test call
  - Oceana ↔ Analytics: REF connection, check abandoned call recording
  - AES ↔ Recording: DMCC registration status
  - EPM ↔ WebLM: license validation
```

---

## SMGR Troubleshooting

**Workflow 23: SMGR Troubleshooting** — when Avaya Aura System Manager issues affect the platform.

```
1. Data Replication Failures to Session Manager:
   - SMGR web → Session Manager → Replication Status
   - SM log: /var/log/Avaya/mgmt/replication/replication.log
   - SMGR log: JBoss logs for replication errors
   - Common: security password mismatch between SMGR and SM
   - Force sync: do_full_sync from SM CLI
   - Verify NTP sync (time drift breaks cert-based trust)

2. Trust Establishment Problems:
   - SMGR → Security → Certificates → check CA status and element certs
   - Verify certs not expired; trust chain intact
   - Regenerate cert on managed element; re-import into SMGR trust store
   - SMGR log: /var/log/Avaya/mgmt/smgr/Smgr.log

3. Software/Patch Deployment Failures:
   - Check deployment logs in SMGR web for step-by-step failure
   - Verify network connectivity on required ports
   - Check disk space on target: df -h (insufficient space = common cause)
   - Verify admin credentials stored in SMGR are correct for managed element
   - Fallback: download patch from support.avaya.com and install manually
```

---

## CMS Historical Report

**Workflow 24: CMS Historical Report Discrepancies**

```
Step 1 — Define: specific report, data points, time frame
Step 2 — Verify CMS-CM Link: status cdr-link → should be "connected"
Step 3 — Agent Trace: CM enable Agent Trace, CMS observe real-time
Step 4 — Cross-Reference CM: list history, display alarms
Step 5 — Check CMS Internal: ECS logs, data storage, archiving
```

---

## Login / Auth Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **WSfE login failed to activate** | Activation fails | AES JTAPI down, Kafka pod evicted, cert | Check AES JTAPI service, `kubectl get pods -A`, cert validity |
| **WFO login 500** | HTTP 500 | WebLogic, DMSA locked, SQL Server, LDAP | Check WebLogic logs, DMSA, SQL, LDAP (per `SWA-INC6468883`) |
| **POM agent cannot login** | Rejected at POM | POM adaptor down, EPM unreachable, agent not mapped | Check POM adaptor, EPM, mapping |
| **AES web cannot log in** | Page unreachable / rejects creds | Tomcat down, license missing, cert expired, DB down | Check Tomcat, license, cert, DB (per `1-22736492522`) |
| **CMSWEB access refused** | Page refuses connection | CMS service down, firewall, cert | Check service, firewall, cert |
| **Kafka pod eviction** | Agents suddenly cannot login | Disk pressure evicts Kafka/Fluentd pods | Delete evicted pods; fix disk pressure |
| **After upgrade login fails** | Worked before, fails after | Service not started, browser cache, config changed | Verify service; clear cache; check config migration |
| **SSH authentication error** | Cannot SSH with valid creds | Account locked, key mismatch, sshd config changed | Check user account, SSH key, `sshd_config` |

---

## Historical Cert / Login / SAML / Outage Patterns

Cross-FY patterns extracted from §4.10–§4.13. Restricted to certificate / WebLM / login / auth / outage / SMGR / EPM-down / SAML / IdP / power-outage scope.

### SAML / IdP / SSO

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **ACRA SAML/OKTA integration failure** | ACRA login fails with OKTA | SAML assertion mismatch or stale IDP metadata | Verify metadata from OKTA, check assertion attributes, refresh IDP metadata (per `1-20000705804`, `1-19914698372`) |
| **Workspace logout does not exit Azure AD session** | Workspace logout but Azure AD still active | Workspace SSO logout doesn't call Azure AD logout endpoint | Configure Workspace to call IdP logout endpoint on session termination (per `1-18666741782`) |
| **AACC CCMA SSO redirection loop** | CCMA login loops with SSO enabled | SSO/SAML config mismatch between CCMA and IdP | Verify SAML metadata, assertion URLs, IdP config (per `1-18704921472`) |

### WebLM / Licensing

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **AXP/EP license expired** | All calls hear `sysError.wav`, VPMS inaccessible | EP license file expired | Renew license, restart EPM (per `1-19810768322`, `1-20151243702`) |
| **WebLM Host ID changed** | All products enter grace mode simultaneously | VM migration / hardware / MAC change altered Host ID | Re-issue license file with new Host ID (per `1-18627666022`) |
| **WebLM Grace Mode** | Reduced functionality | WebLM unreachable: network, cert, or service | Check WebLM service, network, cert trust (per `1-18185450724`) |
| **GRHA in license error mode** | GRHA reports license error | License file not replicated to standby | Verify license file on standby GRHA; re-import (per `1-17834730001`) |
| **NDLOAM service not up after switchover** | License manager fails after EPM HA switchover | NDLOAM not starting on secondary EPM | Manually start NDLOAM; check service dependency on secondary (per `1-22144653762`) |

### Certificate Issues

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Email OAuth 2.0 cert failure** | Cannot send/receive Office365 email | OAuth 2.0 client cert expired or misconfigured | Renew OAuth cert, verify Azure AD app registration, check MSGraph permissions (per `1-19078183662`) |
| **AES license error mode after deleting default server cert** | License error mode, services degraded | Deleting default server cert breaks internal AES TLS | Do NOT delete default server cert; re-import or regenerate (per `1-19844950102`) |
| **AES DMCC weak cipher alarm** | Security scan reports weak ciphers | DMCC supports deprecated cipher suites | Apply cipher hardening per Avaya security advisory (per `1-20221132752`) |
| **AACC prompt manager fails to load** | AACC prompt mgmt page does not load | AAMS cert renewal broke prompt manager | Re-import new cert to AAMS; restart prompt manager (per `1-22199459912`) |
| **POM cert cannot be trusted in web** | POM web shows cert warning | Self-signed or expired POM cert | Renew POM cert; import CA to browser trust store (per `1-19150594372`) |
| **ACCASS PU Undeployed after CM/AES cert renewal** | PU undeployed after cert renewal | Cert change disrupted PU communication | Re-import certs to PU truststore; restart PU services (per `1-17973294431`) |
| **Softphone disconnect after AES/AEM upgrade** | All elite softphones disconnected | AES/AEM upgrade changed protocol or cert | Re-provision softphones; check cert trust after upgrade (per `1-19124609982`) |
| **ACR Oceana port 443 failure** | ACR can't send metadata to Oceana | Cert or firewall blocking HTTPS 443 to Oceana | Verify cert trust, firewall, and Oceana REST endpoint (per `1-17771923042`) |
| **SAL Gateway inaccessible** | Cannot reach SAL Gateway web GUI | SAL service down or cert issue | Restart SAL; check cert and network (per `1-17827595551`, `1-18825654652`) |
| **Oceanalytics GEO config failure in DR** | Cannot configure GEO replication for Analytics DR | Network or cert between primary and DR Analytics | Verify network path and certs between primary and DR Analytics clusters (per `1-17383834982`) |

### Login / Authentication / AD / LDAP

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **AES will not block user after 5 failed logins** | Lockout policy not enforced | AES user mgmt config bypassing lockout | Check AES user mgmt policy; verify lockout settings (per `1-22144812262`) |
| **AES User Management tab cannot display** | AES 10.1.3 User Mgmt page blank | Tomcat or DB issue after upgrade | Restart AES web console; verify DB migration completed (per `1-21998512072`) |
| **WSfE 3.8 intermittent login (3-4 attempts)** | Agents must retry login multiple times | WSfE session init race condition | Check WSfE service, Kafka pods, network latency (per `1-17797694932`) |
| **Oceana token expired** | Oceana REST API calls fail with token expiry | OAuth token TTL too short or refresh broken | Increase TTL; verify token refresh mechanism (per `1-17438238042`) |
| **AIC ORB service failed to start** | AIC services won't start, icadmin reports ORB failure | CORBA ORB init failure after migration or IP change | Reconfigure ORB with correct IP/hostname; restart AIC (per `1-22144546352`) |
| **CMS unable to install LDAP** | LDAP integration installation fails | LDAP client package dependency or config error | Check OS compatibility; verify LDAP server reachability (per `1-19567443342`) |
| **IC Poller-server failed to connect IMAP** | AIC cannot poll email server | IMAP connectivity, auth, or SSL/TLS mismatch | Verify IMAP reachability, credentials, TLS (per `1-17739428832`) |

### EPM / SMGR / Platform Outage

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **EPM services cannot start** | EPM fails after reboot or patch | Disk full, DB corruption, or license issue | Check disk space, PostgreSQL health, WebLM connectivity (per `1-19038422922`) |
| **EP backup not running** | EPM backup job not executing | Backup cron misconfigured or storage unreachable | Verify backup schedule and storage path (per `1-20156773112`) |
| **AAEP Web interface not responsive** | Web UI loads but doesn't respond | Tomcat resource exhaustion or session memory leak | Restart EPM Tomcat; check Java heap usage (per `1-19733243412`) |
| **AXP SMMC connection lost** | After ACCS reboot, no media connectivity | Service startup dependency order incorrect | Reboot in order SMMC → ACCS → verify (per `1-19555227082`) |
| **AES PostgreSQL stopped unexpectedly** | MAJ alarm, AES CTI down, getlogs unavailable | PG crash on AES: disk full, corrupt WAL, OOM | Check disk, restart PostgreSQL, verify DB integrity (per `1-17013543201`) |
| **AES connector outage** | All CTI connections drop simultaneously | AES platform-level failure (disk, memory, network) | Check AES infrastructure resources; restart AES in order (per `1-17951667070`) |
| **AES HA sync issue** | HA pair out of sync, failover fails | HA replication channel broken or DB divergence | Check HA sync; manually resync or rebuild standby (per `1-19910774792`) |
| **Security patch breaking services** | Avaya services fail after Log4j or OS patching | Patch incompatible with Avaya service version | Roll back patch; check Avaya compatibility matrix (per `1-18242801042`) |
| **Third-party security agent conflict** | RDC_service won't start after Qualys agent install | Security agent blocking Avaya service comms | Exclude Avaya processes/dirs from security agent scanning (per `1-18791421202`) |
| **NGINX config lost after reboot** | Custom NGINX config on Breeze reverts after reboot | Breeze startup overwrites custom NGINX | Place custom config in persistent override location (per `1-18936614672`) |
| **SNMP stops working suddenly** | NMS cannot poll SNMP MIBs | SNMP agent crashed or port blocked | Restart SNMP; check port conflicts or firewall (per `1-17130096288`) |


---

## Certificate Health Commands

### Certificate Expiry Detection (B1)

```bash
# Check a PEM/CRT file directly
CERT_FILE="/opt/avaya/certs/server.crt"
openssl x509 -in $CERT_FILE -noout -enddate -subject

# Check expiry with days-remaining (alert if <30 days)
openssl x509 -in $CERT_FILE -noout -checkend $((30*86400)) \
  && echo "OK: cert valid >30 days" \
  || echo "ALERT: cert expires within 30 days"

# Scan all Avaya certs and sort by days remaining
for cert in /opt/avaya/certs/*.crt /etc/pki/tls/certs/*.crt 2>/dev/null; do
  [ -f "$cert" ] || continue
  EXPIRY=$(openssl x509 -in "$cert" -noout -enddate 2>/dev/null | cut -d= -f2)
  DAYS=$(( ( $(date -d "$EXPIRY" +%s) - $(date +%s) ) / 86400 ))
  echo "$DAYS days | $cert"
done | sort -n | head -20

# Check live HTTPS endpoint (WebLM, EPM, SM, SMGR)
echo | openssl s_client -connect <weblm-host>:443 -servername <weblm-host> 2>/dev/null \
  | openssl x509 -noout -enddate -subject

echo | openssl s_client -connect <smgr-host>:443 2>/dev/null \
  | openssl x509 -noout -enddate -issuer
```

### Auto-Remediation: Certificate Near-Expiry Playbook (B2)

```
Alert keyword match: ["certificate", "expir", "cert", "ssl", "tls"]
Severity: high
Execution mode: approval  ← cert renewal ALWAYS requires human confirmation on Avaya
Cooldown: 86400 seconds (cert alerts fire repeatedly — suppress after first action)

Verification command:
  openssl x509 -in <cert> -noout -checkend 0

Remediation workflow:
  Step 1 (auto):    openssl x509 -in <cert> -noout -enddate -subject
                    → confirm which cert is expiring
  Step 2 (human):   Generate/import new cert via SMGR or Avaya cert wizard
  Step 3 (human):   Import into trust stores (JKS) per restart sequence below
  Step 4 (auto):    Verify: echo | openssl s_client -connect <host>:443 2>/dev/null
                             | openssl x509 -noout -enddate

Note: Mid-session cert expiry only affects calls when SDP renegotiation occurs
      (transfer, hold/resume). Schedule renewal in maintenance window.
```

### Post-Cert-Change Restart Sequence (B3)

```bash
# Step 0: backup trust store before any changes
cp /opt/avaya/truststore.jks /opt/avaya/truststore.jks.bak.$(date +%Y%m%d)

# Step 1: import new cert into Java trust store
keytool -import -trustcacerts \
  -alias avaya-new-cert \
  -file /tmp/new-cert.crt \
  -keystore /opt/avaya/truststore.jks \
  -storepass <password> -noprompt

# Step 2: restart in dependency order
# AES (csta-server)
systemctl restart avaya-aes || service avaya-aes restart

# Session Manager — via SMGR UI:
# Elements > Session Manager > select instance > Restart

# WebLM
# /opt/avaya/weblm/bin/shutdown.sh && sleep 15 && /opt/avaya/weblm/bin/startup.sh

# Step 3: clear browser cache on all operator workstations before declaring success
# (Ctrl+Shift+Delete in Chrome/Edge — otherwise stale TLS session resumed)

# Step 4: verify (wait 60s for services to stabilize)
sleep 60
echo | openssl s_client -connect <host>:443 2>/dev/null \
  | openssl x509 -noout -enddate
```

> **Invariant**: After any certificate change — inventory ALL JKS stores, restart ALL dependent services, clear browser cache on workstations. Missing any one of the three causes intermittent failures that are hard to reproduce.
