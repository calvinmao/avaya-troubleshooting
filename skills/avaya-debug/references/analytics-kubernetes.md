# Analytics / Oceanalytics / Kubernetes Troubleshooting Reference
<!--
scope: Oceanalytics, Kubernetes/bosh/CFCR, Kafka, MicroStrategy, PV alarms
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: Pod count expected per Analytics version, bosh director recovery steps, Kubernetes API versions
related_docs: diagnostic-principles.md, linux-server.md, lessons/analytics-kubernetes.md
-->



## Table of Contents
- [Platform Overview](#platform-overview)
- [Oceanalytics / Kubernetes Infrastructure](#oceanalytics--kubernetes-infrastructure)
- [Geo Redundancy / Disaster Recovery](#geo-redundancy--disaster-recovery)
- [Kubernetes Recovery (Workflow 15)](#kubernetes-recovery)
- [Analytics Fault Patterns](#analytics-fault-patterns)
- [Historical Analytics Fault Patterns (FY21–FY23)](#historical-analytics-fault-patterns-fy21fy23)
- [Kubernetes / Analytics Commands](#kubernetes--analytics-commands)

---

## Platform Overview

Avaya Analytics / Oceanalytics is a Cloud Foundry / Kubernetes appliance built on **bosh + cfcr** with **MicroStrategy (mstr)** as the BI front-end.

| Layer | Tool | Health Check |
|-------|------|--------------|
| Hypervisor | VMware vSphere | DRS **must be Fully Automatic** (PSN005633u). Manual DRS blocks bosh from re-creating master VMs and produces `Recommendations were detected, you may be running in Manual DRS mode. Aborting.` CPI errors. |
| bosh director | `cbosh vms`, `cbosh -d cfcr ...` | HTTP 500 from director usually = `/var/vcap/store` 100% full (move `director/tasks` aside to recover). |
| Kubernetes | `kubectl get nodes`, `kubectl get pods -A`, `ccm smoke-test` | Expected pod count is product-version-specific (e.g., 102 vs 104). A passing smoke-test with the wrong count is still a problem. |
| REF (Replication Framework) | `ccm` scale commands | Customers sometimes scale REF down to disconnect from Oceana; remember to scale back up. |
| ADW (Analytics Data Warehouse) | MySQL / MicroStrategy connection | After failover, browser cache and MicroStrategy ODBC may both need refresh (per `INC7091425`). |
| ODBC | `mysql-connector-odbc-8.0.28-1.el7.x86_64.rpm` (commonly bundled at `/home/cust/custom/mysql/`) | Reinstall + reconfigure on Linux side after node rebuild; no `mstr` restart needed. |
| PV alarms | `KubePersistentVolumeUsageCritical` | Real outage trigger; clear before they hit 100%. |
| Kafka | Message broker for data pipeline | Pod failures block the entire pipeline. |
| Geo Redundancy | Replication between primary and DR | Slow replication is common after initial config. |

**Browser cache invalidation is mandatory** after any Analytics web-tier fix; otherwise the UI keeps showing the broken state.

---

## Oceanalytics / Kubernetes Infrastructure

Operational details extending the overview.

| Layer | Component | Health Check |
|-------|-----------|-------------|
| **Kubernetes** | `kubectl get nodes`, `kubectl get pods -A` | Expected pod count is product-version-specific. A passing smoke-test with wrong count is still a problem. |
| **Kafka** | Message broker for Analytics↔Oceana data pipeline | Pod failures (`Kafka pod failed to start`) block the entire data pipeline (per `202506` Vinetian case). |
| **PV (Persistent Volume)** | `KubePersistentVolumeUsageCritical` alarm | Real outage trigger. Clear PV alarms before they hit 100% (per `INC6986565`). |
| **REF (Replication Framework)** | `ccm` scale commands | Customers scale REF down to disconnect from Oceana; remember to scale back up. |
| **ADW (Analytics Data Warehouse)** | MySQL + MicroStrategy connection | After failover/reboot, browser cache and MicroStrategy ODBC may both need refresh (per `INC7091425`). |
| **Geo Redundancy** | Replication between primary and DR Analytics clusters | Slow replication after Geo Redundancy configuration is a known pattern (per `202509` SCB case). |

---

## Geo Redundancy / Disaster Recovery

Analytics-specific DR considerations. (Certificate DR is covered in `certificates-login-outage.md`.)

| Component | Considerations |
|-----------|---------------|
| **Analytics DR** | Primary and DR cluster replication; slow replication is common after initial configuration. DR site may show minor alarms for pods that haven't fully synced. |
| **Oceana DR (relevant to Analytics)** | UCAStoreService backup/restore on new WSfE/Oceana nodes may fail if backup was from different version (per `202505` SCB case). Affects analytics pipeline if Oceana data source identity changes. |

Operational rules:
- Do not failover to the DR site until replication is confirmed healthy.
- Verify network bandwidth between primary and DR sites; slow replication is often bandwidth-bound.
- Monitor replication lag via `ccm` commands.

---

## Kubernetes Recovery

**Workflow 15: Analytics / Oceanalytics / Kubernetes Recovery**

When Analytics or Oceanalytics shows no data, pods are failing, or PV alarms fire:

```
Step 1 — Assess Kubernetes Cluster Health
  kubectl get nodes                          # All nodes Ready?
  kubectl get pods -A                        # All pods Running?
  kubectl get events --sort-by='.lastTimestamp' -A | tail -30

  Expected pod count is product-version-specific (e.g., 102 vs 104).
  A passing smoke-test with wrong count is still a problem.

Step 2 — Check Persistent Volume Alarms
  KubePersistentVolumeUsageCritical = real outage trigger
  Action: Clear PV before 100% — at 100% pods crash and may not recover
  Check: kubectl describe pv | grep -A5 "Capacity"
  Fix: Scale down non-critical pods, expand PV, or move director/tasks aside

Step 3 — Check REF (Replication Framework) Connection to Oceana
  ccm status                                 # REF status
  ccm scale ref                              # Check if REF was scaled down
  If customer scaled REF down to disconnect from Oceana → scale back up

Step 4 — Check ADW (Analytics Data Warehouse) / MicroStrategy
  After failover or reboot:
    1. Check MySQL connectivity from MSTR
    2. Clear browser cache (mandatory — stale cache shows old/broken UI)
    3. Reconfigure ODBC if node was rebuilt:
       rpm -qa | grep mysql-connector-odbc   # Verify installed
       # Reinstall from /home/cust/custom/mysql/ if missing
    4. No MSTR restart needed after ODBC reconfigure

Step 5 — Check Kafka Pipeline
  Kafka pod failed to start = entire data pipeline blocked
  Symptoms: no real-time data, no historical data, abandoned calls not recorded
  Fix: kubectl describe pod <kafka-pod> -n <namespace>
  Common causes: PV full, config drift after upgrade, ZooKeeper quorum loss

Step 6 — Check LDAP / Authentication
  Analytics login LDAP failure:
    - Verify LDAP bind DN and password
    - Check LDAP server reachability from Analytics nodes
    - Verify LDAP group mapping for Analytics roles
    - After LDAP changes: restart affected pods

Step 7 — Geo Redundancy Replication Issues
  After configuring Geo Redundancy:
    - Slow replication is common initially
    - Monitor replication lag via ccm commands
    - DR site may show minor alarms while syncing
    - Do not failover until replication is healthy
    - Verify network bandwidth between primary and DR sites

Step 8 — Post-Reboot Recovery (per INC7091425)
  After Analytics node reboot:
    1. Wait for all pods to reach Running state (may take 10-15 min)
    2. Verify no CrashLoopBackOff: kubectl get pods -A | grep -v Running
    3. Clear browser cache before checking UI
    4. If no real-time data: check REF connection to Oceana
    5. If no historical data: check MySQL/MSTR connectivity
    6. If both missing: check Kafka pipeline first (it feeds both)

Step 9 — Analytics Version Migration (per FY23 cases)
  When upgrading Analytics (e.g., 4.1.1 → 4.2.0 → 4.3):
    1. Verify the migration path is supported — version skipping is NOT supported
    2. Run pre-migration validation: check disk space, pod health, database integrity
    3. After migration: verify all database views and functions exist
       - Missing views/functions = migration script incomplete (per Analytics UBR case)
       - Run: `ccm smoke-test` to validate post-migration health
    4. Non-HA deployment failures: ensure VMs meet minimum resource requirements
       (per `1-19888441352`: insufficient resources cause bosh deployment to fail)
    5. After data migration: run report validation against known-good data to catch
       missing or corrupted data objects
```

---

## Analytics Fault Patterns

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Pods not running after reboot** | CrashLoopBackOff or pending pods post-reboot | K8s needs time to reschedule; resource contention | Wait 10-15 min; check `kubectl describe pod` for specific errors |
| **PV disk usage critical** | KubePersistentVolumeUsageCritical alarm | Log/data accumulation fills persistent volume | Clear PV before 100%; scale down non-critical pods; expand PV |
| **REF connection not coming up** | No data pipeline between Oceana and Analytics | Certificates, network, or REF scaled down by customer | Check certs, network, `ccm scale ref` (per `202412` SCB case) |
| **After-reboot no data** | No real-time or historical data after Analytics restart | Kafka pipeline, REF, or ADW not recovered | Check Kafka first → REF → ADW (per `INC7091425`) |
| **Geo Redundancy slow replication** | DR site lagging behind primary | Initial sync; insufficient bandwidth | Monitor replication lag; verify network bandwidth; be patient |
| **LDAP login failure** | Analytics web login fails with auth error | Bind DN, password, or group mapping issue | Verify LDAP bind credentials; check group mapping |
| **Abandoned call not in Analytics** | Oceana ED abandoned call not recorded in Analytics | Data pipeline broken between Oceana ED and Analytics | Check REF connection, Kafka pipeline, orca-ref-input-adaptor pods |
| **MSTR report error** | MicroStrategy reports fail to generate | ODBC driver mismatch or MySQL ADW down | Reinstall mysql-connector-odbc; verify MySQL connectivity |
| **bosh director HTTP 500** | bosh CLI returns 500 errors | `/var/vcap/store` 100% full | Move `director/tasks` aside to recover space, then retry |
| **Manual DRS blocks recovery** | bosh CPI error: `Recommendations were detected, you may be running in Manual DRS mode. Aborting.` | vSphere DRS not in Fully Automatic mode | Set DRS to Fully Automatic per PSN005633u |
| **Analytics migration failure** | Missing views/functions after upgrade | Migration script incomplete; version skipping unsupported | Verify migration path; run validation (per `1-20085562392`) |
| **Non-HA deployment failure** | Fresh install fails | Insufficient VM resources | Check VM resources, bosh director (per `1-19888441352`) |
| **GEO configuration failure in DR** | Cannot configure GEO replication for Analytics DR | Network or cert issue between sites | Verify network and certs (per `1-17383834982`) |
| **Realtime dashboard inaccurate** | "oldest call waiting duration" wrong | Data pipeline latency or calc bug | Check REF pipeline, Kafka and orca pods (per `1-18735357082`) |

---

## Historical Analytics Fault Patterns (FY21–FY23)

Analytics / Oceanalytics / Kubernetes / bosh / MSTR / REF / ADW related items pulled from the broader fault library.

### FY23

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Analytics data migration failure** | Missing database views/functions after version upgrade | Migration script incomplete or version skip unsupported | Verify migration path (no version skipping); run post-migration validation (per `1-20085562392`, Analytics UBR case) |
| **Analytics non-HA deployment failure** | Fresh Analytics install fails | Insufficient resources or config error during bosh deployment | Check VM resources, network config, bosh director health (per `1-19888441352`) |

### FY22

| Pattern | Symptoms | Root Cause | Resolution |
|---------|----------|------------|------------|
| **Oceanalytics GEO configuration failure in DR site** | Cannot configure GEO replication for Analytics DR | Network connectivity or certificate issue between primary and DR Analytics | Verify network path and certificates between primary and DR Analytics clusters (per `1-17383834982`) |
| **Oceanalytics agent performance report timeout** | Analytics agent performance report loads slowly or times out | Large data volume, insufficient ADW resources, or MSTR query optimization | Increase query timeout; optimize MSTR report; scale ADW resources (per `1-18221878452`) |
| **Realtime dashboard "oldest call waiting duration" inaccurate** | Analytics real-time dashboard shows incorrect wait time | Analytics data pipeline latency or calculation bug | Check REF pipeline latency; verify Kafka and orca pods healthy (per `1-18735357082`) |
| **WFM Pulse data not reflected, staffing adapter fails** | WFM shows no agent activity data, staffing adapter alarm | WFM staffing adapter cannot connect to data source (Analytics or AACC) | Check staffing adapter connectivity to Analytics/AACC; verify API credentials (per `1-18726856152`) |

---

## Kubernetes / Analytics Commands

```bash
# Bosh director status
cbosh vms                                    # List all VMs and their status
cbosh -d cfcr --                             # Check Kubernetes deployment

# Kubernetes diagnostics
kubectl get nodes                            # Node status
kubectl get pods -A                          # All pods across namespaces
kubectl get pods -A | grep -v Running        # Show only non-running pods
kubectl describe pod <pod> -n <namespace>    # Pod event details
kubectl get events --sort-by='.lastTimestamp' -A | tail -30
kubectl top nodes                            # Node resource usage
kubectl top pods -A                          # Pod resource usage

# Persistent Volume checks
kubectl get pv                               # PV status
kubectl describe pv <pv-name>                # PV capacity and usage

# CCM (Contact Center Manager) commands for Analytics
ccm status                                   # Overall status
ccm smoke-test                               # Connectivity test
ccm scale ref                                # REF scaling

# MySQL connectivity (ADW)
mysql -u <user> -p -h <adw-host> -e "SELECT 1"

# ODBC verification on Linux
rpm -qa | grep mysql-connector-odbc          # Check ODBC driver installed
ls /home/cust/custom/mysql/                  # Bundled driver location

# MSTR (MicroStrategy) diagnostics
# Access via web: https://<analytics-host>/MicroStrategy/servlet/mstrWeb
# Check ODBC connection from MSTR to MySQL ADW

# bosh director recovery (when HTTP 500 from director)
# /var/vcap/store full -> move director/tasks aside
df -h /var/vcap/store
```


---

## Prometheus Alert Rules — Kubernetes / kube-state-metrics

> Source: [samber/awesome-prometheus-alerts](https://github.com/samber/awesome-prometheus-alerts) (MIT License)
> Apply to Avaya Analytics (Oceanalytics on bosh/CFCR/K8s) deployments.

### Node Health

```yaml
# KubernetesNodeNotReady — node not in Ready state
- alert: KubernetesNodeNotReady
  expr: kube_node_status_condition{condition="Ready",status="true"} == 0
  for: 10m
  labels: { severity: critical }
  annotations:
    summary: "K8s node {{ $labels.node }} is not Ready for 10 min"

# KubernetesNodeMemoryPressure / DiskPressure
- alert: KubernetesNodeMemoryPressure
  expr: kube_node_status_condition{condition="MemoryPressure",status="true"} == 1
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Node {{ $labels.node }} under memory pressure — pods may be evicted"

- alert: KubernetesNodeDiskPressure
  expr: kube_node_status_condition{condition="DiskPressure",status="true"} == 1
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Node {{ $labels.node }} under disk pressure — check /var/vcap/store"
```

### Pod & Container Health

```yaml
# KubernetesPodCrashLooping — >3 restarts in 1 minute
- alert: KubernetesPodCrashLooping
  expr: increase(kube_pod_container_status_restarts_total[1m]) > 3
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash-looping"

# KubernetesPodNotHealthy — pod stuck in non-Running phase
- alert: KubernetesPodNotHealthy
  expr: |
    min_over_time(
      sum by(namespace, pod)(
        kube_pod_status_phase{phase=~"Pending|Unknown|Failed"}
      )[15m:1m]
    ) > 0
  labels: { severity: critical }
  annotations:
    summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} not healthy for 15 min"

# KubernetesContainerOomKiller — container OOM killed
- alert: KubernetesContainerOomKiller
  expr: |
    (kube_pod_container_status_restarts_total - kube_pod_container_status_restarts_total offset 10m >= 1)
    and ignoring(reason) min_over_time(kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}[10m]) >= 1
  for: 0m
  labels: { severity: warning }
  annotations:
    summary: "Container {{ $labels.container }} was OOM-killed — increase memory limit"

# KubernetesJobFailed — batch job failed
- alert: KubernetesJobFailed
  expr: kube_job_status_failed > 0
  for: 0m
  labels: { severity: warning }
  annotations:
    summary: "K8s job {{ $labels.namespace }}/{{ $labels.job_name }} has failed"
```

### Persistent Volume Health

```yaml
# KubernetesPersistentvolumeclaimPending
- alert: KubernetesPersistentvolumeclaimPending
  expr: kube_persistentvolumeclaim_status_phase{phase="Pending"} == 1
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "PVC {{ $labels.namespace }}/{{ $labels.persistentvolumeclaim }} stuck Pending"

# KubernetesVolumeOutOfDiskSpace — PV < 10% free
- alert: KubernetesVolumeOutOfDiskSpace
  expr: kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes * 100 < 10
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "PV on {{ $labels.namespace }}/{{ $labels.persistentvolumeclaim }} < 10% free"

# KubernetesVolumeFullInFourDays — linear fill projection
- alert: KubernetesVolumeFullInFourDays
  expr: |
    predict_linear(kubelet_volume_stats_available_bytes[6h:5m], 4 * 24 * 3600) < 0
  for: 0m
  labels: { severity: critical }
  annotations:
    summary: "PV {{ $labels.persistentvolumeclaim }} projected full in < 4 days"

# KubernetesPersistentvolumeError — PV in Failed/Pending state
- alert: KubernetesPersistentvolumeError
  expr: kube_persistentvolume_status_phase{phase=~"Failed|Pending"} > 0
  for: 0m
  labels: { severity: critical }
  annotations:
    summary: "PV {{ $labels.persistentvolume }} is in error state"
```

### Deployment & ReplicaSet

```yaml
# KubernetesDeploymentReplicasMismatch — desired != available
- alert: KubernetesDeploymentReplicasMismatch
  expr: |
    kube_deployment_spec_replicas
    != kube_deployment_status_replicas_available
  for: 10m
  labels: { severity: warning }
  annotations:
    summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replica mismatch"

# KubernetesStatefulsetReplicasMismatch
- alert: KubernetesStatefulsetReplicasMismatch
  expr: |
    kube_statefulset_status_replicas_ready
    != kube_statefulset_status_replicas
  for: 10m
  labels: { severity: warning }
  annotations:
    summary: "StatefulSet {{ $labels.namespace }}/{{ $labels.statefulset }} replica mismatch"

# KubernetesHpaScalingAbility — HPA maxed out (cannot scale further)
- alert: KubernetesHpaMaxedOut
  expr: |
    kube_horizontalpodautoscaler_status_current_replicas
    == kube_horizontalpodautoscaler_spec_max_replicas
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "HPA {{ $labels.namespace }}/{{ $labels.horizontalpodautoscaler }} at max replicas"
```

### API Server

```yaml
# KubernetesApiServerErrors — 5xx error rate > 3%
- alert: KubernetesApiServerErrors
  expr: |
    sum(rate(apiserver_request_total{job="apiserver",code=~"5.."}[1m]))
    / sum(rate(apiserver_request_total{job="apiserver"}[1m])) * 100 > 3
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "API server 5xx rate > 3% — bosh director and kubectl degraded"

# KubernetesApiClientErrors — client-side 5xx to API server
- alert: KubernetesApiClientErrors
  expr: |
    (sum(rate(rest_client_requests_total{code=~"5.."}[1m])) by (instance, job)
    / sum(rate(rest_client_requests_total[1m])) by (instance, job)) * 100 > 1
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Kubernetes API client reporting > 1% 5xx errors"
```

### Alert-to-Action Table (Avaya Analytics)

| Alert | Analytics Impact | First Action |
|-------|----------------|--------------|
| KubernetesNodeNotReady | Pod scheduling blocked; pipeline stalls | `kubectl describe node <node>`; check bosh vm status |
| KubernetesPodCrashLooping | Kafka, MicroStrategy, or REF pod cycling | `kubectl logs <pod> --previous`; look for OOM or DB conn error |
| KubernetesContainerOomKiller | Container memory limit too low | `kubectl top pod`; increase resource.limits.memory |
| KubernetesVolumeOutOfDiskSpace | `/var/vcap/store` pressure; pipeline write failures | `kubectl exec` into pod; `du -sh *`; rotate old data |
| KubernetesVolumeFullInFourDays | Pre-emptive warning for archive/Kafka volumes | Request customer storage expansion before outage |
| KubernetesApiServerErrors | bosh director commands fail; `ccm` unresponsive | Check etcd health; restart API server pod if needed |
| KubernetesDeploymentReplicasMismatch | Redundant pods missing — single point of failure | `kubectl rollout status`; describe failed pods |
| KubernetesHpaMaxedOut | Load exceeds capacity; consider increasing max replicas | Review CPU/memory limits; right-size pod resources |
