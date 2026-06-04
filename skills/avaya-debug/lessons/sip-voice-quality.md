# Lessons — SIP / Voice Quality

Field-captured findings for SIP signaling, one-way audio, codec negotiation, QoS, SBC, and RTP/jitter issues. Mirrors `../references/sip-voice-quality.md`. See `./README.md` for the entry template, ID convention, and promotion rule.

---

## L-001 — OPTIONS Keep-Alive Timeout on Carrier Blocking

- **Symptom**: SIP trunk shows "in service" in CM, but outbound calls drop after exactly 90 seconds. Pattern repeats on all calls regardless of destination or time-of-day.
- **Evidence**: traceSM shows `OPTIONS timeout` after 3 consecutive failures (at 30 sec, 60 sec, 90 sec marks). Carrier firewall ACL only allows outbound REGISTER; inbound OPTIONS response blocked. Wireshark capture shows SIP OPTIONS sent from Session Manager but no 200 OK response returned. CM status command: `display sip-entity <entity>` shows "in service" but OPTIONS health check = FAILED.
- **Root cause**: Session Manager sends OPTIONS keep-alive every 30 sec per SIP RFC 3261. Carrier firewall blocks inbound OPTIONS (asymmetric firewall rule: allows outbound REGISTER/INVITE but not inbound OPTIONS). After 3 timeouts (90 sec), SM marks registration as failed and removes trunk from service, dropping active calls.
- **Fix**: Disable OPTIONS keep-alive on SIP Entity configuration in CM. In CM Administration: Telephony > SIP Trunks > select entity > disable "OPTIONS enable" (or set OPTIONS Interval to 0). Switch to REGISTER refresh only (default REGISTER interval 300 sec). Verify with carrier that inbound SIP REGISTER responses are allowed; if not, escalate to carrier network team to open firewall ACL.
- **Provenance**: SR 1-23156789012 | 2025-01-22
- **Promotion**: pending (awaiting second carrier verification)

## L-002 — CSeq Distribution Per Call-ID Is the Smoking Gun for B2BUA Replaces Propagation Defects

- **Symptom**: One-way audio after SIP Replaces / blind transfer / agent merge. Need to determine whether the B2BUA correctly issued the downstream re-INVITE (which it should generate to redirect media on the other leg).
- **Evidence**: Method to apply — for the target dialog's Call-ID, count CSeq occurrences across ALL pcap files + SM syslog stream by method name. Normal Replaces-driven call: `1 INVITE × N, 1 ACK × M, 2 INVITE × K, 2 ACK × K, 3 BYE × P`. Failed propagation: `1 INVITE × N, 1 ACK × M, 2 BYE × P` (CSeq jumps from 1 INVITE directly to 2 BYE; no CSeq:2 INVITE in any direction throughout dialog lifetime). Reference: SR 1-23647477802 BC1 Call-ID `d6c229d25d5641f180920505695906f` showed CSeq:2 INVITE = 0; same-window normal call `de723eec5d5641f184c90505695906f` showed expected CSeq:2 INVITE at 10:12:02.945 (118ms after ACK).
- **Root cause**: When B2BUA fails to issue re-INVITE on one leg after processing inbound Replaces, the CSeq sequence on the un-updated leg jumps from CSeq:1 INVITE (initial dialog) to CSeq:2 BYE (final teardown). The absence of intermediate CSeq:2 INVITE is structurally observable and definitive.
- **Fix / workaround**: Always run this CSeq distribution test BEFORE concluding a re-INVITE was sent or hypothesizing other failure modes. Test is cheap (single grep + count) and rules out / confirms the B2BUA defect class quickly.
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: promoted to references/sip-voice-quality.md#post-bridging-one-way-audio-invariants-sip-replaces--b2bua on 2026-06-04

## L-003 — Same-Window Normal-Call Control Method Discriminates Per-Call Defects From Configuration

- **Symptom**: Intermittent defect (e.g. ~2% incidence) is hard to escalate without proving it's per-call rather than systemic (which would point to configuration, not engineering).
- **Evidence**: For SR 1-23647477802, in the same 2-minute pcap window as failing BC1, found normal call `de723eec5d5641f184c90505695906f` that did exhibit the textbook CM B2BUA pattern (CSeq:1 INVITE → CSeq:2 INVITE 118ms after ACK → CSeq:3 BYE). Both calls used same CM (172.17.61.2), same SM (172.17.61.13), same B5000 (172.17.61.24), same campaign. Sole difference: which specific calls hit the defect.
- **Root cause**: Demonstrates the system IS capable of correct behavior — so configuration is correct and the failure must be a per-call race condition or edge case in the B2BUA logic. Eliminates entire class of "system misconfigured" hypotheses.
- **Fix / workaround**: Required step in any intermittent-defect investigation. Find a normal call in the same captured time window exhibiting the expected behavior. Use it as control evidence in PEA submission — separates "intermittent code defect" from "configuration drift" for the engineering team.
- **Provenance**: SR 1-23647477802 | 2026-06-04
- **Promotion**: promoted to references/sip-voice-quality.md#post-bridging-one-way-audio-invariants-sip-replaces--b2bua on 2026-06-04
