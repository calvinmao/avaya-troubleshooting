---
title: "Cloud Infrastructure Troubleshooting Reference"
layer: L4
scope: "Avaya on AWS/Azure: EC2/VM, VPC/VNet, Security Groups/NSG, VPN, CloudWatch, EKS/AKS, AXP"
maturity: canonical
applicable_versions: [TBD]
last_reviewed: "2026-06-03"
owner: "avaya-debug skill"
staleness_risks:
  - "AWS/Azure CLI flag changes"
  - "CloudWatch metric names"
  - "AXP API versions"
  - "EKS/AKS K8s version support"
related_docs:
  - "network-infrastructure.md"
  - "analytics-kubernetes.md"
  - "lessons/cloud-infrastructure.md"
---

# Cloud Infrastructure Troubleshooting Reference


Diagnostic patterns for Avaya deployments on cloud platforms: AWS, Azure, and hybrid
on-premises/cloud architectures. Covers Avaya Experience Platform (AXP — cloud-native),
Avaya Aura on VMware/cloud VMs, and container-based components.

For Kubernetes-specific patterns (Oceanalytics, analytics pods) see `analytics-kubernetes.md`.

---

## Cloud Deployment Topology — Avaya

```
┌─────────────────────────────────────────────────────────────────┐
│  Cloud-Native (AXP / Avaya Experience Platform)                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ AXP Control  │  │ AXP Routing  │  │ Analytics / Reports │  │
│  │ (SaaS)       │  │ (SaaS)       │  │ (SaaS)              │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
│  Customer manages: SIP trunk credentials, user/skill config    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Hybrid: Aura on Cloud VMs + On-Prem Endpoints                 │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ Session Mgr  │  │ AES          │  │ EPM / WebLM         │  │
│  │ (Cloud VM)   │  │ (Cloud VM)   │  │ (Cloud VM)          │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
│         │                  │                                    │
│   Site-to-site VPN / Direct Connect / ExpressRoute             │
│         │                  │                                    │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ On-Prem CM   │  │ On-Prem AACC │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## AWS — EC2 and VPC Troubleshooting

### EC2 Instance Health

```bash
# From AWS CLI (run from admin workstation or CloudShell):
# Instance status checks (system check = AWS infra; instance check = guest OS):
aws ec2 describe-instance-status --instance-ids <INSTANCE_ID> \
  --output table --query 'InstanceStatuses[*].{InstanceStatus:InstanceStatus.Status,SystemStatus:SystemStatus.Status}'

# CPU / memory metrics via CloudWatch (last 1 hour, 5-min periods):
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<INSTANCE_ID> \
  --period 300 --statistics Average \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --output table

# Instance console output (last boot messages — useful when SSH unreachable):
aws ec2 get-console-output --instance-id <INSTANCE_ID> --output text | tail -100

# Check if instance is on a degraded host (planned retirement):
aws ec2 describe-instance-status --instance-id <INSTANCE_ID> \
  --query 'InstanceStatuses[*].Events'

# Reboot instance (non-destructive — persists EBS storage):
aws ec2 reboot-instances --instance-ids <INSTANCE_ID>
# Note: reboot AES/SM requires change-control approval (see linux-server.md safety matrix)
```

### VPC Networking and Security Groups

```bash
# List security group rules for an Avaya instance:
aws ec2 describe-security-groups --group-ids <SG_ID> \
  --query 'SecurityGroups[*].IpPermissions' --output table

# Check if SIP port is open in security group:
aws ec2 describe-security-groups --group-ids <SG_ID> \
  --query 'SecurityGroups[*].IpPermissions[?FromPort==`5060`]'

# Add SIP inbound rule to security group (change-control required):
aws ec2 authorize-security-group-ingress \
  --group-id <SG_ID> \
  --protocol tcp --port 5060 \
  --cidr <CARRIER_IP>/32

# VPC Flow Logs — check if traffic is being dropped:
# (Requires Flow Logs enabled on VPC/subnet)
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern '[version, account, eni, source, destination, srcport, destport="5060", protocol, packets, bytes, start, end, action="REJECT", status]' \
  --start-time $(date -d '1 hour ago' +%s)000

# Network ACL (stateless — must allow both inbound AND outbound for TCP):
aws ec2 describe-network-acls --filters Name=vpc-id,Values=<VPC_ID> \
  --query 'NetworkAcls[*].Entries' --output table
# Common mistake: NACL blocks ephemeral ports (1024-65535) for return traffic → SIP fails

# Check route table for correct path to on-prem (via VPN Gateway):
aws ec2 describe-route-tables --filters Name=vpc-id,Values=<VPC_ID> \
  --query 'RouteTables[*].Routes' --output table
```

### AWS VPN / Direct Connect Connectivity

```bash
# VPN connection status:
aws ec2 describe-vpn-connections --query \
  'VpnConnections[*].{State:State,Type:Type,VpnGatewayId:VpnGatewayId}' \
  --output table

# Check VPN tunnel status (both tunnels should be UP for redundancy):
aws ec2 describe-vpn-connections --vpn-connection-id <VPN_ID> \
  --query 'VpnConnections[*].VgwTelemetry' --output table

# Direct Connect virtual interface status:
aws directconnect describe-virtual-interfaces \
  --query 'virtualInterfaces[*].{Name:virtualInterfaceName,State:virtualInterfaceState,BGP:bgpPeers}' \
  --output table

# Verify on-prem route is propagated via VPN:
aws ec2 describe-route-tables --filters Name=route.origin,Values=EnableVgwRoutePropagation \
  --query 'RouteTables[*].Routes[?GatewayId!=`null`]' --output table
```

### CloudWatch Alarms for Avaya EC2

```bash
# List existing alarms for an Avaya instance:
aws cloudwatch describe-alarms \
  --alarm-name-prefix "Avaya-" \
  --output table \
  --query 'MetricAlarms[*].{Name:AlarmName,State:StateValue,Metric:MetricName}'

# Create CPU alarm for AES server (alert at 85%):
aws cloudwatch put-metric-alarm \
  --alarm-name "Avaya-AES-HighCPU" \
  --alarm-description "AES CPU exceeds 85% for 10 minutes" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --dimensions Name=InstanceId,Value=<AES_INSTANCE_ID> \
  --period 300 --evaluation-periods 2 \
  --threshold 85 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions <SNS_TOPIC_ARN>

# Create disk alarm using CloudWatch agent (requires CWAgent installed on instance):
aws cloudwatch put-metric-alarm \
  --alarm-name "Avaya-SM-DiskFull" \
  --metric-name disk_used_percent \
  --namespace CWAgent \
  --dimensions Name=InstanceId,Value=<SM_INSTANCE_ID> Name=path,Value=/ \
  --period 300 --evaluation-periods 1 \
  --threshold 85 --comparison-operator GreaterThanThreshold \
  --alarm-actions <SNS_TOPIC_ARN>
```

---

## Azure — VM and VNet Troubleshooting

### Azure VM Health

```bash
# Azure CLI — VM status (run from Azure Cloud Shell or az CLI):
az vm get-instance-view --name <VM_NAME> --resource-group <RG_NAME> \
  --query 'instanceView.statuses[*].{Code:code,DisplayStatus:displayStatus}' \
  --output table

# VM boot diagnostics (serial console log — useful when RDP/SSH unreachable):
az vm boot-diagnostics get-boot-log --name <VM_NAME> --resource-group <RG_NAME> | tail -100

# CPU metrics (last 1 hour):
az monitor metrics list \
  --resource "/subscriptions/<SUB_ID>/resourceGroups/<RG>/providers/Microsoft.Compute/virtualMachines/<VM>" \
  --metric "Percentage CPU" \
  --interval PT5M \
  --query 'value[*].timeseries[*].data[-12:]'

# Check if VM has scheduled maintenance:
az vm list-skus --location <REGION> | grep -i "AvailabilityZone"
az vm show -n <VM_NAME> -g <RG_NAME> --query 'instanceView.maintenanceRedeployStatus'

# Restart VM (non-destructive — persists managed disk):
az vm restart --name <VM_NAME> --resource-group <RG_NAME>
```

### Azure NSG (Network Security Group) Debugging

```bash
# List NSG rules affecting an Avaya VM:
az network nsg rule list --nsg-name <NSG_NAME> --resource-group <RG_NAME> \
  --query 'sort_by([*],&priority)[*].{Priority:priority,Name:name,Access:access,Protocol:protocol,Port:destinationPortRange}' \
  --output table

# Verify SIP port 5060 is allowed:
az network nsg rule list --nsg-name <NSG_NAME> --resource-group <RG_NAME> \
  --query '[?destinationPortRange==`5060`]'

# IP Flow Verify — test if NSG allows traffic on a specific port:
az network watcher test-ip-flow \
  --vm <VM_NAME> \
  --direction Inbound \
  --protocol TCP \
  --local <VM_PRIVATE_IP>:5060 \
  --remote <CARRIER_IP>:12345 \
  --resource-group <RG_NAME>
# Output: "Access: Allow" or "Access: Deny" + rule name causing deny

# NSG Flow Logs (requires Network Watcher + storage account):
az network watcher flow-log show \
  --nsg <NSG_NAME> \
  --resource-group <RG_NAME>

# Add SIP inbound NSG rule (change-control required):
az network nsg rule create \
  --nsg-name <NSG_NAME> --resource-group <RG_NAME> \
  --name Allow-SIP-Inbound \
  --priority 200 \
  --protocol Tcp --direction Inbound --access Allow \
  --destination-port-range 5060 5061 \
  --source-address-prefixes <CARRIER_IP_RANGE>
```

### Azure VNet Connectivity

```bash
# Check VNet peering status (used for multi-region Avaya deployments):
az network vnet peering list \
  --vnet-name <VNET_NAME> --resource-group <RG_NAME> \
  --query '[*].{Name:name,State:peeringState,RemoteVNet:remoteVirtualNetwork.id}' \
  --output table
# "Connected" = healthy; "Disconnected" = routing broken between VNets

# VPN Gateway connection status:
az network vpn-connection show \
  --name <CONNECTION_NAME> --resource-group <RG_NAME> \
  --query 'connectionStatus'
# Expected: "Connected"; "Unknown" or "NotConnected" = tunnel down

# ExpressRoute circuit status (used for on-prem to Azure Avaya hybrid):
az network express-route show \
  --name <CIRCUIT_NAME> --resource-group <RG_NAME> \
  --query '{ServiceState:serviceProviderProvisioningState,CircuitState:circuitProvisioningState}'

# Connection Troubleshoot — point-to-point connectivity check via Network Watcher:
az network watcher run-configuration-diagnostic \
  --resource <VM_RESOURCE_ID> \
  --queries '[{protocol: "TCP", destination: "<TARGET_IP>", destinationPort: "5060", direction: "Outbound"}]'
```

### Azure Monitor Alerts for Avaya VMs

```bash
# Create action group (alert notification channel):
az monitor action-group create \
  --name "AvayaOpsTeam" --resource-group <RG_NAME> \
  --short-name "AvayaOps" \
  --email avaya-ops@yourcompany.com

# Create CPU alert for Session Manager VM:
az monitor metrics alert create \
  --name "Avaya-SM-HighCPU" \
  --resource-group <RG_NAME> \
  --scopes "/subscriptions/<SUB>/resourceGroups/<RG>/providers/Microsoft.Compute/virtualMachines/<SM_VM>" \
  --condition "avg Percentage CPU > 85" \
  --window-size 5m --evaluation-frequency 1m \
  --action "AvayaOpsTeam" \
  --description "Session Manager CPU > 85% for 5 min"
```

---

## Hybrid Connectivity: On-Prem ↔ Cloud

```bash
# Test latency from on-prem to cloud-hosted Avaya component:
ping -c 50 <CLOUD_AES_IP>
# RTT < 50ms required for JTAPI (higher latency = JTAPI event ordering issues)
# RTT < 30ms recommended for SIP (voice quality threshold)

# Verify VPN/DX throughput (run iperf3 across the tunnel):
# On cloud SM: iperf3 -s -D
# On-prem: iperf3 -c <CLOUD_SM_IP> -t 30 -P 2
# Bandwidth < 10 Mbps on VPN = congestion → check VPN gateway SKU / DX capacity

# Identify split-DNS issues (on-prem resolves to internal IP, cloud resolves to public):
# On-prem: dig <SM_FQDN>         → should return private IP via on-prem DNS
# Cloud VM: dig <SM_FQDN>         → should return cloud private IP
# If cloud VM resolves to on-prem IP → routing asymmetry → one-way audio / JTAPI timeout

# MTU on VPN tunnel (often 1400 bytes, not 1500):
ping -c 5 -M do -s 1350 <CLOUD_IP>   # Should succeed
ping -c 5 -M do -s 1472 <CLOUD_IP>   # May fail through VPN
# If 1472 fails: set MTU on Avaya VM NIC: ip link set eth0 mtu 1400

# Check BGP route propagation for Direct Connect / ExpressRoute:
# (Run on cloud router/VGW via cloud console)
# AWS: aws ec2 describe-route-tables --filters Name=route.origin,Values=EnableVgwRoutePropagation
# Azure: az network vnet-gateway list-advertised-routes --name <GATEWAY_NAME> -g <RG>
```

---

## Cloud Storage Troubleshooting

```bash
# AWS S3 — check Avaya backup/recording archive bucket:
aws s3 ls s3://<AVAYA_BUCKET>/ --human-readable --summarize
# Verify recording archives are landing:
aws s3 ls s3://<AVAYA_BUCKET>/recordings/ --recursive | grep $(date +%Y-%m-%d) | wc -l

# S3 bucket policy (check ACRA/WFO archive service has write access):
aws s3api get-bucket-policy --bucket <AVAYA_BUCKET> | jq .
# If no policy or wrong policy → recordings silently fail to archive

# Azure Blob Storage — check WFO/ACRA archive container:
az storage blob list \
  --container-name avaya-recordings \
  --account-name <STORAGE_ACCOUNT> \
  --query '[?properties.lastModified > `<YESTERDAY_DATE>`].name' \
  --output table

# Check storage account connectivity from Avaya VM:
nc -zv <STORAGE_ACCOUNT>.blob.core.windows.net 443 -w 5
# If blocked → check NSG outbound rules; Storage service endpoint may be needed
```

---

## IAM / Permissions Troubleshooting

```bash
# AWS — check what an Avaya service role can do:
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<ACCOUNT>:role/AvayaServiceRole \
  --action-names s3:PutObject ec2:DescribeInstances cloudwatch:PutMetricData \
  --query 'EvaluationResults[*].{Action:EvalActionName,Decision:EvalDecision}'

# AWS — find who/what assumed a role (for audit):
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole \
  --start-time $(date -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
  --query 'Events[*].{Time:EventTime,User:Username,Resource:Resources[0].ResourceName}'

# Azure — check role assignments for Avaya service principal:
az role assignment list \
  --assignee <SERVICE_PRINCIPAL_ID> \
  --output table \
  --query '[*].{Role:roleDefinitionName,Scope:scope}'

# Common Avaya cloud IAM failures:
# - ACRA cannot write recordings to S3/Blob → missing s3:PutObject / Storage Blob Data Contributor
# - CloudWatch agent cannot push metrics → missing cloudwatch:PutMetricData
# - Auto-scaling fails for AXP workers → missing ec2:RunInstances / Microsoft.Compute/virtualMachines/write
```

---

## Container & Kubernetes (Cloud-Hosted)

For detailed Kubernetes diagnostics see `analytics-kubernetes.md`. Cloud-specific
additions:

```bash
# AWS EKS — cluster status:
aws eks describe-cluster --name <CLUSTER_NAME> \
  --query 'cluster.{Status:status,Version:version,Endpoint:endpoint}'

# EKS node health:
kubectl get nodes -o wide
kubectl describe node <NODE_NAME> | grep -E "Condition|Pressure|Ready"

# Azure AKS — cluster status:
az aks show --name <CLUSTER_NAME> --resource-group <RG_NAME> \
  --query '{State:provisioningState,Version:kubernetesVersion,Fqdn:fqdn}'

# AKS node pool health:
az aks nodepool list --cluster-name <CLUSTER_NAME> --resource-group <RG_NAME> \
  --query '[*].{Name:name,State:provisioningState,Count:count,VMSize:vmSize}'

# Check Oceanalytics/Analytics pods in cloud K8s:
kubectl get pods -n avaya-analytics -o wide
kubectl logs <POD_NAME> -n avaya-analytics --tail=100
kubectl describe pod <POD_NAME> -n avaya-analytics | grep -A5 "Events:"

# Persistent volume binding (cloud PV issues — EBS stuck in "Terminating"):
kubectl get pv,pvc -n avaya-analytics
aws ec2 describe-volumes --filters Name=tag:kubernetes.io/created-for/pvc/name,Values=<PVC_NAME>
```

---

## Cloud Cost and Right-Sizing (Avaya VMs)

```bash
# AWS — check if Avaya EC2 instances are right-sized (CPU < 10% avg = over-provisioned):
aws ce get-right-sizing-recommendation \
  --service "AmazonEC2" \
  --configuration '{"RecommendationTarget":"SAME_INSTANCE_FAMILY","BenefitsConsidered":true}'

# Identify idle Avaya instances (< 5% CPU for 7 days):
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<INSTANCE_ID> \
  --period 86400 --statistics Average \
  --start-time $(date -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S)

# Azure — Advisor recommendations for Avaya VMs:
az advisor recommendation list \
  --category Cost \
  --query '[?resourceMetadata.resourceType==`Microsoft.Compute/virtualMachines`].[shortDescription.solution,resourceMetadata.resourceId]' \
  --output table
```

---

## Cloud Troubleshooting Quick Reference

| Symptom | Likely Cause | First Check |
|---------|-------------|-------------|
| Cloud Avaya VM unreachable via SSH | NSG/SG blocking port 22 | `az network watcher test-ip-flow` / VPC flow logs |
| SIP trunk fails to cloud SM | NSG missing port 5060 | `aws ec2 describe-security-groups` |
| JTAPI timeout to cloud AES | VPN tunnel down | VPN connection status; RTT > 50ms |
| Recording archive missing | S3/Blob IAM or NSG | `nc -zv blob.core.windows.net 443` |
| Analytics pod crash-loop | PV not bound / EBS stuck | `kubectl describe pv`; AWS volume state |
| Cloud-to-on-prem call fails | Split DNS / MTU | `dig` from cloud VM; `ping -M do -s 1400` |
| License checkout fails (WebLM) | Cloud WebLM unreachable from on-prem | `curl -vso /dev/null https://<WEBLM_IP>:52233` |
| AXP agent login fails | AXP SaaS outage or user config | AXP admin console; Avaya status page |
