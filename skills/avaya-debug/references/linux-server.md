# Linux Server Troubleshooting Reference
<!--
scope: Linux OS health on Avaya servers (AES, SM, AACC, ACRA, EPM), systemd, kernel, sysctl, OOM, SELinux
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: RHEL/CentOS version-specific sysctl keys, systemd unit names per product version, Prometheus node-exporter metric names
related_docs: log-collection.md, network-infrastructure.md, lessons/linux-server.md
-->



Diagnostic patterns for Linux-based Avaya servers (AES, Session Manager, AACC, ACRA,
EPM, SMGR, POM, CCMM). All Avaya Aura components run on RHEL/CentOS 7/8/9 unless
otherwise noted. Patterns are directly applicable without modification.

---

## System Vitals — First-Response Snapshot

Run these first on any Linux Avaya server exhibiting symptoms. They give a complete
health picture in under 60 seconds.

```bash
# One-liner: collect everything relevant in a single pass
echo "=== $(date) ===" && \
echo "--- LOAD / CPU ---" && uptime && mpstat 1 3 && \
echo "--- MEMORY ---" && free -h && \
echo "--- DISK ---" && df -hT && \
echo "--- SWAP ---" && swapon --show && \
echo "--- TOP 10 PROCESSES (CPU) ---" && ps -eo pid,pcpu,pmem,comm,args --sort=-pcpu | head -11 && \
echo "--- TOP 10 PROCESSES (MEM) ---" && ps -eo pid,pcpu,pmem,comm,args --sort=-pmem | head -11 && \
echo "--- NETWORK CONNECTIONS ---" && ss -s && \
echo "--- FAILED SERVICES ---" && systemctl --failed --no-legend

# Save full snapshot to file for SR attachment:
SNAP=/tmp/linux_snapshot_$(hostname)_$(date +%Y%m%d_%H%M%S).txt
{ uptime; free -h; df -hT; ss -s; systemctl --failed; } > "$SNAP"
echo "Snapshot saved: $SNAP"
```

---

## CPU Analysis

### Load Average Interpretation

```
load average: 1.23, 0.87, 0.65
              │     │     └── 15-min average
              │     └──────── 5-min average
              └────────────── 1-min average
```

Rule of thumb: load ≤ number of vCPUs = healthy; load > 2× vCPUs = investigate.

```bash
# Number of logical CPUs on this host:
nproc
# or:
grep -c ^processor /proc/cpuinfo

# Per-CPU utilisation (1-second samples, 5 iterations):
mpstat -P ALL 1 5

# Which processes are causing high CPU?
ps -eo pid,pcpu,comm,args --sort=-pcpu | head -20

# Extended CPU profiling (10-second window):
sar -u 1 10

# CPU runqueue and context switches (look for high %steal in VM environments):
vmstat 1 10
# %st (steal) > 5% = hypervisor is overcommitting — escalate to VMware/cloud team
```

**Avaya-specific**: AES JTAPI and DMCC are Java services — high CPU often means GC
pressure. Always cross-check with `jstat -gcutil <PID> 1000 5` (see `aes-cti-jtapi.md`).

---

## Memory Analysis

```bash
# Overall memory picture:
free -h
# "available" column (not "free") = usable memory for new processes
# available < 10% of total RAM → investigate OOM risk

# Detailed breakdown:
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty"

# OOM killer history (was anything killed recently?):
dmesg | grep -iE "oom|killed process|out of memory" | tail -20
journalctl -k | grep -iE "oom|killed" | tail -20

# Per-process memory usage (RSS = actual physical RAM used):
ps -eo pid,rss,vsz,comm --sort=-rss | head -20 | \
  awk 'NR==1{print} NR>1{printf "%s %sMB %sMB %s\n", $1, int($2/1024), int($3/1024), $4}'

# Slab cache (kernel memory objects — can grow on busy servers):
slabtop -o | head -20

# Swap usage detail:
for f in /proc/*/status; do
  awk -v pid="${f%/status}" '/VmSwap/{if($2>0) print pid, $2"kB"}' "$f" 2>/dev/null
done | sort -k2 -rn | head -10
```

**Thresholds**:
| Metric | Warning | Critical |
|--------|---------|----------|
| Available memory | <20% total | <10% total |
| Swap used | >0 (investigate) | >25% swap |
| OOM kills in dmesg | Any | — |

**Avaya note**: Avaya Java services pre-allocate heap (`-Xmx`). If `free -h` shows
"available" < `-Xmx` value of the JVM, the OS may start paging — causes GC pauses
and recording timer drift (see `recording-wfo.md L-001`).

---

## Disk & Filesystem Analysis

```bash
# Filesystem usage:
df -hT
# Alert: Use% > 85% on /var (logs), /opt (Avaya install), /tmp

# Inode exhaustion (a full filesystem with df showing <100% — inode problem):
df -i
# If IUse% = 100% while Use% is low → too many small files (log fragments, temp files)

# Find disk hogs:
du -sh /var/log/avaya/* 2>/dev/null | sort -rh | head -20
du -sh /opt/avaya/* 2>/dev/null | sort -rh | head -10

# Find files >100MB in Avaya directories:
find /var/log/avaya /opt/avaya -size +100M -ls 2>/dev/null

# Disk I/O performance (check await > 20ms = I/O bottleneck):
iostat -xz 1 5
# Columns: r/s (reads/sec), w/s (writes/sec), await (ms latency), %util

# Identify which process is causing disk I/O:
iotop -bo -n 5 -d 2
# (requires iotop package: yum install iotop)

# Log rotation status check:
ls -lh /var/log/avaya/*.log | head -20
# If log files >500MB and not rotated → logrotate config broken

# Emergency log cleanup (safe — compresses old rotated logs):
find /var/log/avaya -name "*.log.[0-9]*" -mtime +7 ! -name "*.gz" -exec gzip {} \;
find /var/log/avaya -name "*.gz" -mtime +30 -delete
```

**Auto-remediation (disk full)**:
```bash
#!/bin/bash
# Run as cron: 0 */2 * * * /opt/avaya/scripts/disk_cleanup.sh
THRESHOLD=85
USED=$(df /var/log | awk 'NR==2{gsub(/%/,"",$5); print $5}')
if [ "$USED" -gt "$THRESHOLD" ]; then
  find /var/log/avaya -name "*.log.[0-9]*" -mtime +3 -exec gzip {} \;
  find /var/log/avaya -name "*.gz" -mtime +14 -delete
  logger "avaya disk_cleanup: /var/log at ${USED}% — rotated and compressed old logs"
fi
```

---

## Process & Service Management

```bash
# List all Avaya-related processes:
ps -eo pid,ppid,pcpu,pmem,stat,comm,args | grep -iE "avaya|jtapi|dmcc|cstam|oceana|pom|aacc|acra|weblogic" | grep -v grep

# Process tree for a service:
pstree -p $(pgrep -f jtapi | head -1)

# Open file handles for a process (useful for "too many open files" errors):
ls /proc/<PID>/fd | wc -l
# or:
lsof -p <PID> | wc -l
# Alert: > 50000 open FDs approaching ulimit

# Check ulimits for Avaya services:
cat /proc/<PID>/limits
# Look for: Max open files — should be >= 65536 for Avaya Java services

# Set ulimits persistently (in /etc/security/limits.conf or /etc/limits.d/avaya.conf):
# avaya soft nofile 65536
# avaya hard nofile 65536

# Strace a process briefly (diagnose syscall hangs — non-disruptive for 10 sec):
strace -p <PID> -f -e trace=network,file -c -T -- sleep 10 2>&1

# Core dump configuration check:
cat /proc/sys/kernel/core_pattern
ulimit -c   # Should be "unlimited" for Avaya services that generate cores
```

---

## Systemd Service Management

```bash
# Check all Avaya service unit files:
systemctl list-units 'avaya*' --all
systemctl list-units '*jtapi*' '*dmcc*' '*oceana*' '*pom*' --all

# Service status with recent log context:
systemctl status avaya-jtapi --lines=50 -l

# Structured log for a specific service (last 2 hours):
journalctl -u avaya-jtapi --since "2 hours ago" --no-pager | tail -100

# Find services that have failed and auto-restarted:
journalctl -p err -b | grep -iE "avaya|jtapi|dmcc|acra|oceana" | tail -50

# Service dependency tree (understand what must be running first):
systemctl list-dependencies avaya-jtapi --all

# Override service parameters without editing vendor unit file:
systemctl edit avaya-jtapi
# Creates /etc/systemd/system/avaya-jtapi.d/override.conf
# Example override to increase Java heap for AES JTAPI:
# [Service]
# Environment="JAVA_OPTS=-Xmx4g -XX:MaxGCPauseMillis=200 -XX:+UseG1GC"

# Force immediate restart with startup log capture:
systemctl restart avaya-jtapi && journalctl -u avaya-jtapi -f --no-pager &
# (Ctrl-C after startup completes)

# Check for services in a restart loop (StartLimitHit):
journalctl -u avaya-jtapi | grep -E "start-limit|too many start requests"
# If hit: systemctl reset-failed avaya-jtapi  then investigate root cause before restart
```

**Avaya service restart safety matrix**:
| Service | Auto-restart OK? | Notes |
|---------|-----------------|-------|
| `avaya-jtapi` | Yes (non-peak) | Drops active JTAPI sessions |
| `avaya-dmcc` | Yes (non-peak) | Drops DMCC device registrations |
| `avaya-acra` | Yes | Interrupts active recordings |
| `avaya-oceana` | **Approval required** | Drops all active engagements |
| `avaya-aes` (full) | **Approval required** | CM/SMGR-level impact |
| `avaya-smgr` | **Change control** | Loss of call routing |
| `avaya-weblm` | **Change control** | Product-wide license loss |

---

## Kernel Parameters for Avaya Servers

These sysctl settings are recommended for Avaya Linux servers handling high-volume
SIP signaling and JTAPI connections:

```bash
# View current values:
sysctl net.core.somaxconn net.ipv4.tcp_keepalive_time net.ipv4.tcp_keepalive_intvl \
       net.ipv4.tcp_keepalive_probes net.ipv4.tcp_tw_reuse net.ipv4.ip_local_port_range \
       vm.swappiness fs.file-max

# Recommended values for AES / Session Manager:
cat > /etc/sysctl.d/avaya-tuning.conf << 'EOF'
# TCP keepalive (detect dead connections faster — AES JTAPI relies on this)
net.ipv4.tcp_keepalive_time = 60
net.ipv4.tcp_keepalive_intvl = 10
net.ipv4.tcp_keepalive_probes = 6

# Allow reuse of TIME_WAIT connections (SIP trunk high-call-rate environments)
net.ipv4.tcp_tw_reuse = 1

# Increase connection backlog for SIP (Session Manager handles burst registrations)
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 4096

# Ephemeral port range (increase for high SIP call rates)
net.ipv4.ip_local_port_range = 10000 65535

# Reduce swap aggressiveness (Java heaps should stay in RAM)
vm.swappiness = 10

# File descriptor limit (Java services open many sockets)
fs.file-max = 2097152
EOF
sysctl -p /etc/sysctl.d/avaya-tuning.conf
```

---

## Log Analysis Quick Patterns

```bash
# Scan Avaya logs for recent errors (last 30 min):
find /var/log/avaya -name "*.log" -newer /tmp/30_min_ref -exec \
  grep -l "ERROR\|FATAL\|Exception\|OutOfMemory" {} \; 2>/dev/null

# Count error frequency by type:
grep -h "ERROR\|FATAL" /var/log/avaya/**/*.log 2>/dev/null | \
  awk '{print $(NF-0)}' | sort | uniq -c | sort -rn | head -20

# Follow multiple logs simultaneously:
tail -f /var/log/avaya/jtapi/spi.log /var/log/avaya/dmcc/acr.log &

# Extract timestamps from Java stack traces (find stacks near a known event time):
awk '/14:23:/{found=1} found{print; if(/^$/) {count++; if(count>3) exit}}' \
  /var/log/avaya/jtapi/spi.log

# Journal rate-limiting (if journald is dropping messages under load):
grep -c "Missed" /run/log/journal/*/system.journal 2>/dev/null || true
# Fix: in /etc/systemd/journald.conf → RateLimitBurst=0 → systemctl restart systemd-journald
```

---

## Security & Audit Patterns

```bash
# Recent login activity (failed logins indicate brute-force):
last | head -20
lastb | head -20   # Failed logins (requires root)
grep "Failed password\|Accepted password\|Invalid user" /var/log/secure | tail -30

# Privilege escalation audit:
grep "sudo:" /var/log/secure | tail -20

# File permission audit on Avaya config dirs:
find /opt/avaya/config -type f -perm /o+w 2>/dev/null
# World-writable config files = security risk

# SELinux status (common cause of Avaya service startup failures on RHEL):
getenforce
sestatus
# If Enforcing and service fails to start:
ausearch -c 'avaya-jtapi' | audit2why   # Explains SELinux denial reason
# Temporary: setenforce 0 (for diagnosis only — resets on reboot)
# Permanent fix: generate policy → audit2allow -a -M avaya_jtapi; semodule -i avaya_jtapi.pp

# Check for unexpected cron jobs:
crontab -l -u avaya 2>/dev/null
ls -la /etc/cron.d/ /etc/cron.hourly/ /etc/cron.daily/
```

---

## Performance Baseline Commands

```bash
# Collect 10-minute performance baseline (save to file for SR):
sar -A 60 10 > /tmp/sar_baseline_$(hostname)_$(date +%Y%m%d_%H%M).txt &

# Network interface statistics (check for errors/drops):
ip -s link show
# rx_errors or tx_drops > 0 → NIC or switch problem; escalate to network team

# Interrupt distribution (are all CPUs handling network interrupts?):
cat /proc/interrupts | grep -E "CPU|eth|ens|eno|bond"
# If all interrupts on CPU0 → IRQ affinity misconfigured; check /proc/irq/*/smp_affinity

# NUMA topology (important for multi-socket Avaya servers):
numactl --hardware
# Java services should be pinned to a single NUMA node to avoid cross-socket latency
```


---

## Prometheus Alert Rules — Node Exporter (Linux Servers)

> Source: [samber/awesome-prometheus-alerts](https://github.com/samber/awesome-prometheus-alerts) (MIT License)
> Apply to all Avaya Linux servers (AES, SM, AACC, ACRA, EPM, CCMM) running `node_exporter`.

### Memory & Swap

```yaml
# HostOutOfMemory — available RAM < 10%
- alert: HostOutOfMemory
  expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes < 0.10
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "Host out of memory (< 10% left)"

# HostSwapIsFillingUp — swap > 80% used
- alert: HostSwapIsFillingUp
  expr: (1 - (node_memory_SwapFree_bytes / node_memory_SwapTotal_bytes)) * 100 > 80
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "Swap space filling up (> 80%)"

# HostOomKillDetected — OOM killer fired in last 30 min
- alert: HostOomKillDetected
  expr: increase(node_vmstat_oom_kill[30m]) > 0
  labels: { severity: critical }
  annotations:
    summary: "OOM kill detected — Java heap or DB buffer likely cause"
```

### CPU & I/O

```yaml
# HostHighCpuLoad — sustained CPU > 80%
- alert: HostHighCpuLoad
  expr: 1 - (avg without(cpu)(rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 0.80
  for: 5m
  labels: { severity: warning }
  annotations:
    summary: "CPU load > 80% for 5 minutes"

# HostCpuStealNoisyNeighbor — steal time > 10% (hypervisor contention)
- alert: HostCpuStealNoisyNeighbor
  expr: avg by(instance)(rate(node_cpu_seconds_total{mode="steal"}[5m])) * 100 > 10
  for: 5m
  labels: { severity: warning }
  annotations:
    summary: "CPU steal > 10% — hypervisor overloaded or noisy neighbor VM"

# HostCpuHighIowait — I/O wait > 10% (storage bottleneck)
- alert: HostCpuHighIowait
  expr: avg by(instance)(rate(node_cpu_seconds_total{mode="iowait"}[5m])) * 100 > 10
  for: 5m
  labels: { severity: warning }
  annotations:
    summary: "I/O wait > 10% — disk or NFS may be bottleneck"
```

### Disk & Filesystem

```yaml
# HostOutOfDiskSpace — < 10% free on non-tmpfs
- alert: HostOutOfDiskSpace
  expr: |
    node_filesystem_avail_bytes{fstype!~"^(fuse.*|tmpfs|cifs|nfs)"}
    / node_filesystem_size_bytes < 0.10
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Disk < 10% free on {{ $labels.mountpoint }}"

# HostDiskMayFillIn24Hours — linear projection fills disk in < 24h
- alert: HostDiskMayFillIn24Hours
  expr: |
    predict_linear(node_filesystem_avail_bytes{fstype!~"^(fuse.*|tmpfs|cifs|nfs)"}[3h], 86400) <= 0
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "Disk {{ $labels.mountpoint }} projected to fill within 24 hours"

# HostOutOfInodes — < 10% inodes free
- alert: HostOutOfInodes
  expr: |
    node_filesystem_files_free{fstype!~"^(fuse.*|tmpfs|cifs|nfs)"}
    / node_filesystem_files < 0.10
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Inode exhaustion < 10% free — log spam or small-file accumulation"
```

### Network

```yaml
# HostNetworkReceiveErrors — persistent RX errors
- alert: HostNetworkReceiveErrors
  expr: rate(node_network_receive_errs_total[2m]) / rate(node_network_receive_packets_total[2m]) > 0.01
  for: 2m
  labels: { severity: warning }
  annotations:
    summary: "NIC receive errors > 1% — check cable or switch port"

# HostNetworkBondDegraded — bond member down
- alert: HostNetworkBondDegraded
  expr: (node_bonding_active{master!=""}) < node_bonding_slaves{master!=""}
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Bond {{ $labels.master }} is degraded — a member NIC is down"

# HostConntrackLimit — conntrack table > 80% full
- alert: HostConntrackLimit
  expr: node_nf_conntrack_entries / node_nf_conntrack_entries_limit > 0.80
  for: 5m
  labels: { severity: critical }
  annotations:
    summary: "Conntrack table > 80% — SIP NAT/ALG or high call volume at risk"
```

### System Services & Time

```yaml
# HostSystemdServiceCrashed — any unit in failed state
- alert: HostSystemdServiceCrashed
  expr: node_systemd_unit_state{state="failed"} == 1
  for: 0m
  labels: { severity: warning }
  annotations:
    summary: "systemd unit {{ $labels.name }} is in failed state"

# HostClockSkew — NTP drift > 50 ms (affects SIP and CDR timestamps)
- alert: HostClockSkew
  expr: abs(node_timex_offset_seconds) > 0.05
  for: 10m
  labels: { severity: warning }
  annotations:
    summary: "Clock skew > 50 ms — check NTP; affects SIP timers and CDR correlation"

# HostClockNotSynchronising — NTP sync lost
- alert: HostClockNotSynchronising
  expr: min_over_time(node_timex_sync_status[1m]) == 0
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "NTP sync lost — certificate validity and SIP call setup may fail"
```

### Alert Routing for Avaya Servers

| Alert | Avaya Impact | First Action |
|-------|-------------|--------------|
| HostOutOfMemory | AES/JTAPI connection drops; WFO insert failures | `free -h`; check Java heap (`jstat -gcutil`) |
| HostOomKillDetected | Service crash without clean shutdown log | `dmesg | grep -i oom`; identify victim process |
| HostHighCpuLoad | SIP processing delays; JTAPI event queue backup | `top -H`; identify thread consuming CPU |
| HostOutOfDiskSpace | Log loss; PostgreSQL write failures; recording gaps | `du -sh /var/log/*`; rotate logs immediately |
| HostDiskMayFillIn24Hours | Pre-emptive — correlates with heavy recording or logging | Schedule log rotation; alert customer |
| HostOutOfInodes | Identical symptom to disk full but `df -h` shows space | `df -i`; find directory with millions of small files |
| HostNetworkBondDegraded | Potential single-point of failure for voice traffic | `cat /proc/net/bonding/bond0`; notify network team |
| HostConntrackLimit | SIP calls fail with no SBC-side error | `sysctl net.netfilter.nf_conntrack_max`; increase limit |
| HostSystemdServiceCrashed | Named service down — check which unit | `journalctl -u <name> -n 100` |
| HostClockSkew | TLS cert validation errors; SIP 401/407 TOTP drift | `chronyc tracking`; `chronyc sources -v` |
