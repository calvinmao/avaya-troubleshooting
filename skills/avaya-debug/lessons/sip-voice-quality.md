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
