# Network Infrastructure Troubleshooting Reference
<!--
scope: TCP/IP, DNS, routing, firewall, packet capture, QoS/DSCP, VLAN, MTU for Avaya deployments
last_reviewed: 2026-06-03
owner: avaya-debug skill
staleness_risks: iptables vs nftables syntax on newer RHEL, conntrack default limits per kernel version
related_docs: sip-voice-quality.md, cloud-infrastructure.md, lessons/network-infrastructure.md
-->



Diagnostic patterns for network layers affecting Avaya Aura deployments: TCP/IP
connectivity, DNS, routing, firewalls, packet capture, QoS, and VLAN segmentation.
All Avaya products are network-dependent; most "Avaya issues" have network root causes.

---

## Troubleshooting Methodology

Always work bottom-up: physical → datalink → network → transport → application.
Shortcutting to application (SIP/JTAPI) while a Layer 2/3 problem exists wastes time.

```
Layer 7 (App)     — SIP OPTIONS failure, JTAPI timeout, recording stall
Layer 4 (TCP/UDP) — nc -zv port check, ss -anp connection state, telnet test
Layer 3 (IP)      — ping, traceroute, routing table, MTU check
Layer 2 (Ethernet) — MAC table, VLAN membership, duplex/speed, CDP/LLDP
Layer 1 (Physical) — interface error counters, cable, transceiver
```

---

## Connectivity Verification (Layer 3 / Layer 4)

```bash
# Basic reachability (ICMP — may be blocked by firewall even when TCP works):
ping -c 10 <TARGET_IP>
# Check: packet loss %, RTT average, RTT variance (jitter)
# Jitter > 30ms = voice quality risk (see sip-voice-quality.md)

# TCP port reachability (no firewall ambiguity):
nc -zv <TARGET_IP> <PORT> -w 5
# Examples for Avaya:
nc -zv <SM_IP>  5060   # Session Manager SIP
nc -zv <AES_IP> 1099   # AES JTAPI
nc -zv <AES_IP> 4722   # AES DMCC TLS
nc -zv <EPM_IP> 8443   # EPM/WebLM HTTPS

# UDP port check (SIP commonly uses UDP 5060):
nc -zuv <TARGET_IP> 5060 -w 3

# Scan a range of ports quickly:
for PORT in 5060 5061 1099 4722 8443 8765 450; do
  RESULT=$(nc -zv -w 2 <TARGET_IP> "$PORT" 2>&1)
  echo "$PORT: $RESULT"
done

# HTTP/HTTPS endpoint check (GET and verify certificate):
curl -vso /dev/null https://<TARGET_IP>:8443/ 2>&1 | grep -E "TLS|SSL|Connected|expired|verify"

# traceroute — identify routing hops and where latency is introduced:
traceroute -T -p 5060 <SM_IP>   # TCP traceroute (bypasses ICMP-blocking firewalls)
# or (UDP default):
traceroute <SM_IP>
# MTR — continuous traceroute with packet loss per hop:
mtr --report --report-cycles 20 <SM_IP>
```

---

## DNS Resolution Debugging

DNS failures cause Session Manager registration failures, SMGR connectivity issues,
and cloud Avaya (AXP) endpoint resolution problems.

```bash
# Authoritative lookup (bypass local cache):
dig @8.8.8.8 <HOSTNAME> A
dig @<INTERNAL_DNS_IP> <HOSTNAME> A

# Reverse DNS lookup (check PTR record — some Avaya features require it):
dig -x <IP_ADDRESS>

# Check /etc/resolv.conf:
cat /etc/resolv.conf
# Avaya servers should have at least 2 nameservers; options timeout:2 attempts:3

# DNS cache flush:
systemd-resolve --flush-caches   # systemd-based
# or: nscd -i hosts               # nscd-based
# Verify: systemd-resolve --statistics | grep "Cache hits"

# Test DNS resolution time (should be <50ms for internal):
time dig @<DNS_IP> <HOSTNAME> +short

# Trace full DNS resolution chain:
dig +trace <HOSTNAME>

# Check hosts file overrides (may mask DNS problems):
grep -v "^#" /etc/hosts | grep -v "^$"

# Common DNS-related Avaya symptoms:
# - SM "unable to resolve peer" → FQDN in Entity Links not resolving
# - SMGR sync failure → DNS PTR record missing for AES/SM host
# - WebLM license float failure → license server hostname unreachable via DNS
```

---

## Routing and IP Path Analysis

```bash
# Display routing table:
ip route show
# or legacy: route -n

# Find which interface/gateway a specific destination uses:
ip route get <TARGET_IP>
# Output example: <IP> via <GATEWAY> dev <IFACE> src <LOCAL_IP>

# Check for route asymmetry (outbound ≠ inbound path = SIP issues):
# From Avaya server:
traceroute -T -p 5060 <CARRIER_IP>
# From carrier (ask carrier to run):
# traceroute <SM_IP>
# If paths differ → NAT or policy routing issue → one-way audio risk

# Add a static route (temporary — persists until reboot):
ip route add <NETWORK>/24 via <GATEWAY_IP> dev <IFACE>
# Persistent route (RHEL/CentOS — in /etc/sysconfig/network-scripts/route-<IFACE>):
echo "<NETWORK>/24 via <GATEWAY_IP>" >> /etc/sysconfig/network-scripts/route-eth0

# ARP table (check for duplicate IPs / ARP conflicts):
arp -n
ip neigh show
# If same IP maps to multiple MACs → IP conflict → SIP registration instability

# Packet flow with policy routing (Avaya servers with multiple NICs):
ip rule show
# Multiple routing tables = possible asymmetric routing
```

---

## TCP Connection State Analysis

```bash
# Connection summary by state:
ss -s
# Focus: ESTABLISHED (normal), TIME_WAIT (normal if draining), CLOSE_WAIT (leak indicator)

# Active connections to/from Avaya ports:
ss -anp | grep -E ":5060|:5061|:1099|:4722|:8443"

# Connections per state count:
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn

# CLOSE_WAIT connections (connection teardown not completing — common in JTAPI):
ss -anp | grep CLOSE_WAIT | grep -iE "java|jtapi|dmcc"
# Many CLOSE_WAIT on AES JTAPI port → application not closing sockets properly
# Fix: check application code; may need AES restart if count grows unbounded

# TIME_WAIT accumulation (busy SIP server):
ss -ant | grep TIME_WAIT | wc -l
# > 10000 TIME_WAIT → enable net.ipv4.tcp_tw_reuse in sysctl

# Long-lived connection monitoring (identify stuck sessions > 1 hour):
ss -anp --timer | awk '$5 ~ /^timer:keepalive/ && $6 > 3600'

# Port exhaustion check (ephemeral port shortage = new SIP calls failing):
ss -s | grep "TCP:" 
cat /proc/sys/net/ipv4/ip_local_port_range  # Default: 32768 60999
# If nearly exhausted: widen range → sysctl -w net.ipv4.ip_local_port_range="10000 65535"
```

---

## Packet Capture (tcpdump / tshark)

```bash
# SIP signaling capture on Session Manager (save to file for Wireshark analysis):
tcpdump -i any -w /tmp/sip_capture_$(date +%Y%m%d_%H%M%S).pcap \
  'port 5060 or port 5061' -s 0 &
# Stop after 60 seconds or manually:
sleep 60 && kill %1

# Capture SIP to/from a specific carrier IP:
tcpdump -i eth0 -w /tmp/carrier_sip.pcap host <CARRIER_IP> and port 5060

# RTP media capture (for one-way audio diagnosis — port range varies):
tcpdump -i any -w /tmp/rtp_$(date +%H%M%S).pcap \
  'udp portrange 16384-32767' -s 0

# JTAPI/TSAPI capture (AES CTI traffic):
tcpdump -i any -w /tmp/jtapi_$(date +%H%M%S).pcap \
  'port 1099 or port 450 or port 4722'

# Quick SIP decode in terminal (no Wireshark needed):
tcpdump -i any -A -n 'port 5060' 2>/dev/null | grep -E "^(INVITE|BYE|OPTIONS|REGISTER|Via:|From:|To:|Call-ID:|Contact:)"

# tshark SIP call flow summary (requires tshark package):
tshark -r /tmp/sip_capture.pcap -Y sip -T fields \
  -e frame.time_relative -e ip.src -e ip.dst -e sip.Method -e sip.Status-Code \
  -E header=y -E separator=, > /tmp/sip_flow.csv

# DTMF capture (SIP INFO method or RFC 2833 telephone-event):
tshark -r /tmp/sip_capture.pcap -Y "sip.Method == \"INFO\" or rtp.p_type == 101"
```

---

## Firewall and ACL Debugging

```bash
# Check iptables rules (RHEL/CentOS without firewalld):
iptables -L -n -v --line-numbers
iptables -L INPUT -n -v | grep -E "DROP|REJECT"

# Check firewalld (RHEL 7+):
firewall-cmd --list-all
firewall-cmd --list-ports
# Add Avaya SIP port (temporary):
firewall-cmd --add-port=5060/tcp --add-port=5060/udp
# Persistent:
firewall-cmd --permanent --add-port=5060/tcp && firewall-cmd --reload

# Trace packet decision through iptables (requires iptables-legacy):
iptables -t raw -I PREROUTING -p tcp --dport 1099 -j TRACE
iptables -t raw -I OUTPUT -p tcp --sport 1099 -j TRACE
# Watch trace: dmesg | tail -f | grep "TRACE:"
# IMPORTANT: Remove TRACE rules after diagnosis (they generate heavy log volume)
iptables -t raw -D PREROUTING 1 && iptables -t raw -D OUTPUT 1

# conntrack table (stateful firewall state — can fill up and drop connections):
conntrack -L | wc -l
cat /proc/sys/net/netfilter/nf_conntrack_max
# If count approaches max → new SIP registrations dropped silently
# Increase: sysctl -w net.netfilter.nf_conntrack_max=524288

# Test if a specific path is allowed (from Avaya server to destination):
nc -zv <DEST_IP> <PORT> -w 5
# Blocked → run traceroute to identify which hop drops it → escalate to network/security team
```

---

## Network Performance Testing

```bash
# Bandwidth test between two Avaya servers (requires iperf3 on both):
# On the target (Session Manager, AES, etc.):
iperf3 -s -D  # Run as daemon

# From the source:
iperf3 -c <TARGET_IP> -t 30 -P 4
# Bandwidth < 100 Mbps on a Gig link → NIC, cable, or switch duplex issue
# High retransmit rate → packet loss on path

# Latency and jitter measurement (critical for voice quality):
ping -c 100 -i 0.1 <TARGET_IP> | tail -5
# RTT > 30ms average = marginal for voice
# RTT variance > 10ms (jitter) = likely voice quality complaints

# Large packet test (MTU/fragmentation detection):
ping -c 5 -M do -s 1400 <TARGET_IP>  # -M do = don't fragment
ping -c 5 -M do -s 1472 <TARGET_IP>  # Standard 1500-byte MTU path
# If 1472 fails but 1400 succeeds → MTU mismatch (common on VPN/MPLS paths)
# SIP/SDP in large packets will be silently dropped → call setup failure

# Detect MTU black hole:
tracepath <TARGET_IP>
# Shows PMTU discovery; "asymm" hops = MTU reduction point

# Network interface error counters:
ip -s link show <INTERFACE>
# rx_errors, tx_errors > 0 → physical layer problem (cable, SFP, duplex mismatch)
ethtool <INTERFACE> | grep -E "Speed|Duplex|Link"
# Half-duplex on Gig port = massive performance degradation
```

---

## QoS / DSCP Marking Verification

Avaya requires proper DSCP marking for voice traffic to meet QoS SLAs.

```bash
# Capture and verify DSCP markings on SIP/RTP:
tcpdump -i eth0 -n 'port 5060 or udp portrange 16384-32767' -v 2>/dev/null | \
  grep -E "tos|dscp"
# Voice (RTP) should be: EF (DSCP 46 / tos 0xb8)
# SIP signaling should be: CS3 (DSCP 24 / tos 0x60)
# If unmarked: check QoS policy on Avaya server and upstream switch

# Check DSCP policy on Linux (tc — traffic control):
tc qdisc show dev eth0
tc filter show dev eth0

# Switch QoS trust verification (from switch CLI — Cisco example):
# show mls qos interface <PORT> statistics
# show run interface <PORT> | include trust dscp

# QoS impact: RTP without EF marking in a congested network:
# - Jitter spikes → one-way audio, choppy voice
# - Packet drops → clicks, silence gaps
# Refer to sip-voice-quality.md for threshold detail
```

---

## VLAN and Network Segmentation

```bash
# Check VLAN membership on Avaya server interface:
ip link show
# VLAN interfaces appear as: eth0.100 (VLAN 100 on eth0)

# Create VLAN interface (if Avaya server requires separate voice VLAN):
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add <IP>/<PREFIX> dev eth0.100
ip link set eth0.100 up

# Verify Avaya traffic on correct VLAN (VLAN tagging in capture):
tcpdump -i eth0 -e -n 'vlan' | head -20
# "vlan X" in output = 802.1Q tagged traffic present

# Common VLAN issue: Avaya server on data VLAN, phones on voice VLAN, no routing between
# Symptom: phones register, softphones (PC-based) cannot
# Fix: add inter-VLAN routing rule on Layer 3 switch for voice ↔ data VLANs
```

---

## Common Network Failure Patterns

| Symptom | Layer | Most Likely Cause | Diagnostic Command |
|---------|-------|-------------------|--------------------|
| SIP trunk "in service" but calls fail | L4/L7 | Firewall blocking OPTIONS | `nc -zv <CARRIER_IP> 5060` |
| Calls drop at exactly 90 sec | L7 (SIP) | OPTIONS timeout (see L-001) | `tcpdump port 5060`, `traceroute -T` |
| One-way audio | L3 (IP) | Asymmetric routing / NAT | `traceroute` both directions |
| Intermittent call drops | L3 (IP) | Packet loss / jitter | `mtr --report <TARGET>` |
| JTAPI timeout errors | L4 (TCP) | CLOSE_WAIT accumulation | `ss -anp | grep 1099` |
| Registration flood | L7/DNS | DNS timeout or cert issue | `dig <SM_FQDN>`, `openssl s_client` |
| Voice quality complaints | L3/QoS | DSCP not marked / congestion | `tcpdump -v port 5060 | grep tos` |
| MTU fragmentation | L3 (IP) | VPN / MPLS reduces MTU | `ping -M do -s 1472 <TARGET>` |
| ARP conflict | L2 | Duplicate IP assigned | `arp -n; ip neigh show` |
| Port exhaustion | L4 | Too many TIME_WAIT | `ss -s; cat /proc/sys/net/ipv4/ip_local_port_range` |

---

## Avaya-Specific Port Reference

| Source | Destination | Port | Protocol | Service |
|--------|-------------|------|----------|---------|
| SIP clients | Session Manager | 5060 | TCP/UDP | SIP unencrypted |
| SIP clients | Session Manager | 5061 | TLS | SIP encrypted |
| SM | CM | 5060 | TCP | SIP trunk |
| JTAPI app | AES | 1099 | TCP | JTAPI/TSAPI |
| DMCC app | AES | 450 | TCP | DMCC unencrypted |
| DMCC app | AES | 4722 | TLS | DMCC encrypted |
| Admin browser | AES / EPM | 8443 | HTTPS | Web console |
| Admin browser | SMGR | 443 | HTTPS | System Manager |
| ACRA | CM/phone | 16384-32767 | UDP | RTP recording |
| POM | AACC | 8443 | HTTPS | Campaign API |
| SM | DNS server | 53 | TCP/UDP | FQDN resolution |
