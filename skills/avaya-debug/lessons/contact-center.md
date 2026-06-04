# Lessons — Contact Center (AACC / Oceana / POM / CMS)

Field-captured findings for contact-center routing, agents, vectors, campaigns, and reporting. Mirrors `../references/contact-center.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---

## L-001 — Edify Socket Service State Divergence on LDAP Sync Lag

- **Symptom**: Agent logged out from CM, but visible in AACC OAM "Ready" state for 25 seconds. Other agents see the phantom agent in skill queue, cause routing delays and skill misalignment.
- **Evidence**: CM `display agent <ID>` shows logged-out. AACC logs show `SocketServer EXCEPTION: Connection reset by peer` at 10:23:45 during LDAP sync. Agent state in AACC database query shows "UNKNOWN" status instead of "Offline". LDAP access log shows ldap_sync operation took 42 seconds (threshold default: 30 sec). Phantom agent visible in supervisor dashboard for 25 sec, then transitions to Offline.
- **Root cause**: Edify Socket Service cached agent state during LDAP sync lag. When LDAP took >30 sec to confirm logout, AACC served stale agent state from cache. Socket connection error caused state to remain hung until cache timeout (25 sec) or manual refresh.
- **Fix**: (1) Restart Edify Socket Server service on AACC: `systemctl restart avaya-edify-socket-service`. (2) Reduce LDAP sync timeout from default 30 sec to 5 sec in AACC config (check AACC Administration > Directory Services > LDAP > Sync Timeout). (3) Monitor LDAP server latency; escalate to Directory Services team if consistent >5 sec.
- **Provenance**: SR 1-23156782912 | 2025-01-18
- **Promotion**: pending (awaiting verification on second customer site)

## L-002 — POM Predictive Agent Bridging Mechanism Is SIP Replaces, Not Pure AMS Mixing

- **Symptom**: POM Predictive one-way audio cases analyzed under wrong architectural model (assumed AMS-only RTP mixing) lead to misdirected root-cause hypotheses and wasted customer data-collection cycles.
- **Evidence**: `POM simple call flow.docx` (Zhao Jun, Aug 2026) Chapter 4 Step ⑲ explicitly: "Use same CXI agent nail-up call session to initiate a new SIP INVITE with Replace header to replace the previous call leg to customer." Confirmed in MPP `SessionManager.log.6` at 2026-06-01 10:11:58.314 JST for BC1: `SND ^INVITE ... Replaces: e2b0c485c45bf11d64e0011ac2b3e;from-tag=...;to-tag=...`. Three concurrent SIP dialogs exist during bridging — A (nail-up to agent), B (original customer / CCA probe), C (post-Replaces customer).
- **Root cause**: Predictive (Rhythm type = "Automatic control") uses three-dialog SIP Replaces flow. Progressive may use different mechanism — verify per POM version. Misinterpreting Predictive as Progressive-style AMS-only bridging discards SIP-plane evidence chain.
- **Fix / workaround**: Always check Campaign Detail Report column "Rhythm type" first. If "Automatic control" (Predictive), apply Replaces-based diagnostic workflow. Three dialogs to track: A (nail-up Call-ID), B (customer-leg Call-ID, replaced after bridging), C (new Call-ID from Replaces INVITE, MPP port distinct from B).
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: promoted to references/contact-center.md#pom-predictive-agent-bridging-invariants on 2026-06-04

## L-003 — Campaign Detail Report "Duration of the whistle" Confirms Phase D Replaces Triggered

- **Symptom**: Need high-precision time anchor to locate Replaces INVITE in MPP `SessionManager.log` (which can contain hundreds of INVITEs per minute under campaign load).
- **Evidence**: Campaign Detail Report column C74 "Duration of the whistle" and C76 "Proxy connection time" are populated only when Phase D agent-merge executed. For BC1: whistle = 10:11:58.332, proxy connection = 10:11:58.352. MPP log shows `SND ^INVITE ... Replaces:` at 10:11:58.314 — whistle is 18ms after Replaces. For BC2: whistle = 10:14:28.500, CXI `hints.sip.replaces` at 10:14:28.481 — whistle is 19ms after. Per `POM simple call flow.docx` Step ⑲: "CXI will also play a beep tone to agent call leg to notify this call merge" in parallel with Replaces INVITE.
- **Root cause**: The whistle is the in-band beep CXI plays to agent at the same moment it instructs SessionManager to emit the Replaces INVITE. Latency between CXI event and on-the-wire SIP send is consistently ~18–20ms.
- **Fix / workaround**: Use whistle timestamp ± 50ms window when searching MPP `SessionManager.log` for the matching `SND ^INVITE` with `Replaces:` header. If whistle field is empty in Campaign Report, Phase D did NOT execute — the failure is upstream of bridging (no Answer_Human, no agent available, etc.), NOT a Replaces propagation defect.
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: promoted to references/contact-center.md#pom-predictive-agent-bridging-invariants on 2026-06-04

## L-004 — CM B2BUA Intermittent Failure to Propagate Replaces as re-INVITE to PSTN-facing Dialog

- **Symptom**: ~2% of POM Predictive outbound calls have one-way audio after agent bridges in. Agent cannot hear customer; customer can hear agent. SIP signaling at CM↔SBC boundary completes normally; call duration is typical. Intermittent — same campaign, same CM, same SBC, only specific calls hit it.
- **Evidence**: For affected calls (BC1 `d6c229d25d5641f180920505695906f`, BC2 `342f17ec5d5741f1a58a0505695906f`): full search across 5 pcap files + SM `PVCLIPBASM0031H` syslog stream shows CSeq method distribution on B5000-facing Call-ID = `1 INVITE × 20, 1 ACK × 5, 2 INVITE × 0, 2 BYE × 6` (CSeq jumps from 1 INVITE directly to 2 BYE — no re-INVITE ever generated). Same-window normal call `de723eec5d5641f184c90505695906f` shows expected `1 INVITE → CSeq:2 INVITE (at 10:12:02.945, 118ms after ACK, target URI 172.17.61.24) → CSeq:3 BYE`. MPP log confirms Replaces INVITE WAS sent for the failing calls (BC1 SessionManager.log.6 at 10:11:58.314; BC2 CXI `hints.sip.replaces` at 10:14:28.481).
- **Root cause**: CM R020x.02.0.229.0 acting as B2BUA processes Phase D Replaces sub-step (a) correctly on MPP-facing side (200 OK on Dialog C + BYE on Dialog B) but intermittently skips sub-step (b) — fails to issue re-INVITE on PSTN-facing dialog to redirect SBC media from pre-Replaces AMS port to post-Replaces port. SBC continues sending customer RTP to orphaned AMS endpoint; customer→agent direction silent.
- **Fix / workaround**: No signaling-level workaround. Switching campaign from Predictive to Progressive MAY bypass if Progressive doesn't use Replaces in that POM version (verify first). PEA escalation to CM Backend Engineering (BBE). Patch will require CM-side fix.
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: pending — awaiting BBE PEA confirmation + 2nd customer case
