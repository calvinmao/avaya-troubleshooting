---
title: "SPI-SYN24 - complete source pages 201-220"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 201-220

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-201"></a>

## PDF page 201

Source: SPI-SYN24; PDF page 201; extracted characters: 2156.

```text
3.4.25.3                    RECON24 (New CM7.0)


                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       RECON24                                         seq num
                           seq num (cont)                                      tot siz             u           / / / / / / /
                                 itn                                  / / /        pnumber               pos (non-EAS) or
                                                                                                           p1-p16 (EAS)
                pos or p1-p16 (cont)                    / / / /    s     / /                          skill
    /                            net_id                                                         seq
                                                             timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            RECON24 = 78 (0x4e)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-65535
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
s                 0 = no skill in message, 1 = skill in message
skill             skill matched 1-8000
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-202"></a>

## PDF page 202

Source: SPI-SYN24; PDF page 202; extracted characters: 3316.

```text
       3.4.26       COMP20 and COMP24
The COMP message is sent by the switch when a trunk's far end has answered (outbound call has been
completed).

3.4.26.1                   COMP20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                       COMP20                                          seq num
                           seq num (cont)                                     tot siz              o              itn
              itn (cont)            u                           net_id                                         seq
             seq (cont)                                                     timestamp
          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          COMP20 = 230 (0xe6)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           o               OCM call; 0 = no, 1 = call distributed by ocm
           itn             internal trunk number used to identify trunk facilities, 1-32766
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID

3.4.26.2                   COMP24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                       COMP24                                          seq num
                           seq num (cont)                                     tot siz              o           / / / / / / /
                                 itn                               u                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          COMP24 = 79 (0x4f)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           o               OCM call; 0 = no, 1 = call distributed by ocm
           itn             internal trunk number used to identify trunk facilities, 1-65535
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-203"></a>

## PDF page 203

Source: SPI-SYN24; PDF page 203; extracted characters: 3489.

```text
       3.4.27       LOOKAH20 and LOOKAH24
The LOOKAH message is sent by the switch when a facility attempts to lookahead interflow (LAI), BSR
poll (p bit is set for poll), BSR interflow or NCR (NCD or ENCT) is invoked.  This is followed by a DFWD if
the interflow (LAI or BSR) or NCR network redirection is successful.

3.4.27.1                    LOOKAH20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release

    7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                      LOOKAH20                                         seq num
                           seq num (cont)                                     tot siz              p              itn
              itn (cont)            u                            net_id                                        seq
             seq (cont)                                                     timestamp
          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          LOOKAH20 = 231 (0xe7)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           p               poll bit indicating lookahead is for BSR polling
           itn             internal trunk number used to identify trunk facilities, 1-32766
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID

3.4.27.2                    LOOKAH24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release

    7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                      LOOKAH24                                         seq num
                           seq num (cont)                                     tot siz              p           / / / / / / /
                                 itn                               u                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          LOOKAH24 = 80 (0x50)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           p               poll bit indicating lookahead is for BSR polling
           itn             internal trunk number used to identify trunk facilities, 1-65535
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-204"></a>

## PDF page 204

Source: SPI-SYN24; PDF page 204; extracted characters: 3154.

```text
       3.4.28       AROUTE20 and AROUTE24
The AROUTE20 message is sent by the switch when a facility requests adjunct routing.

3.4.28.1                   AROUTE20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                      AROUTE20                                         seq num
                           seq num (cont)                                     tot siz             u              itn
              itn (cont)            /                           net_id                                         seq
             seq (cont)                                                     timestamp
          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          AROUTE20 = 232 (0xe8)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-32766
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID

3.4.28.2                   AROUTE24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y      y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                      AROUTE24                                         seq num
                           seq num (cont)                                     tot siz             u           / / / / / / /
                                 itn                               /                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          AROUTE24 = 81 (0x51)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-65535
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-205"></a>

## PDF page 205

Source: SPI-SYN24; PDF page 205; extracted characters: 1864.

```text
       3.4.29      SKSTATE20 and SKSTATE23
The Skill State message is sent by the switch when a skill changes state with respect to its Service Level
Supervisor threshold levels.  This message is also sent during a full translation pumpup and a
logon/status pumpup for any measured skills. Both forms of pumpup include this status information.

3.4.29.1                   SKSTATE20 (New CM3.1)


                                                              Switch   Vect    Skill
                                              First Release   CM3.1    y       y
                                              Last Release    CM5.2

    7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4   3   2  1   0
              time_tag                    SKSTATE20                                        seq num
                          seq num (cont)                                     tot siz                state       /     skill
             skill (cont)

                    time_tag     seconds past minute when message was formatted, 0-59
                    opcode       SKSTATE20 = 233 (0xe9)
                    seq num      sequence number, 0-0xffff ffff
                    tot siz      total size in bytes, 1-255
                    state        skill service level state (0 used by CMS to mean UNKNOWN)

                                   State    Meaning
                                   1        normal
                                   2        over threshold one (overload1)
                                   3        over threshold two (overload2)
                                   4        behind target percent (MV2 and later)
                                   5        auto reserving (MV2 and later)
                    skill        skill number 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
```

<a id="pdf-page-206"></a>

## PDF page 206

Source: SPI-SYN24; PDF page 206; extracted characters: 1506.

```text
3.4.29.2                   SKSTATE23 (New CM6.0)


                                                              Switch    Vect   Skill
                                              First Release   CM6.0     y      y
                                              Last Release

    7   6   5   4   3   2  1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                     SKSTATE23                                        seq num
                          seq num (cont)                                     tot siz                 state           / / / /
       / / /                          skill

                    time_tag      seconds past minute when message was formatted, 0-59
                    opcode        SKSTATE23 = 31 (0x1f)
                    seq num       sequence number, 0-0xffff ffff
                    tot siz       total size in bytes, 1-255
                    state         skill service level state (0 used by CMS to mean UNKNOWN)

                                   State     Meaning
                                   1         normal
                                   2         over threshold one (overload1)
                                   3         over threshold two (overload2)
                                   4         behind target percent (MV2 and later)
                                   5         auto reserving (MV2 and later)
                    skill         skill number 1-8000
```

<a id="pdf-page-207"></a>

## PDF page 207

Source: SPI-SYN24; PDF page 207; extracted characters: 2966.

```text
       3.4.30       ASA20 and ASA23
This message is sent by the switch whenever the average speed of answer value changes, and is used to
update the switch-based rolling average-speed-of-answer (ASA) status information that the reporting
adjunct stores for each split/skill and VDN.

3.4.30.1                    ASA20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release    CM5.2

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                         ASA20                                         seq num
                           seq num (cont)                                      tot siz             /              itn
              itn (cont)                                      vdn_asa                                    / / / / /        skill
             skill (cont)                                     skill_asa

time_tag     seconds past minute when event occurred, 0-59
opcode       ASA20 = 234 (0xea)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
iln          internal line number for VDN, 1-32766; 0 means no vdn_asa included
vdn_asa      average speed of answer for calls to the VDN, 0-65535 seconds
skill        skill number, 1-999 (G3V8-G3V11), 1-2000 (MV2 and later), 0 means no skill_asa value is set
skill_asa    average speed of answer for calls to the skill, 0-65535 seconds

3.4.30.2                    ASA23 (New CM6.0)


                                                               Switch    Vect    Skill
                                               First Release   CM6.0     y/n     y/n
                                               Last Release    CM6.3

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                         ASA23                                         seq num
                           seq num (cont)                                      tot siz             /              iln
              itn (cont)                                      vdn_asa                                 / / /           skill
             skill (cont)                                     skill_asa

time_tag     seconds past minute when event occurred, 0-59
opcode       ASA23 = 32 (0x20)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
iln          internal line number for VDN, 1-32766; 0 means no vdn_asa included
vdn_asa      average speed of answer for calls to the VDN, 0-65535 seconds
skill        skill number, 1-8000 (CM6.0 and later), 0 means no skill_asa value is set
skill_asa    average speed of answer for calls to the skill, 0-65535 seconds
```

<a id="pdf-page-208"></a>

## PDF page 208

Source: SPI-SYN24; PDF page 208; extracted characters: 3210.

```text
       3.4.31       DNEVENT20 and DNEVENT24
The VDN Event message is sent by the switch when a trunk is used to process a VDN call.  It reports the
association between the dialed VDN and the trunk that is carrying the call. For both measured and
unmeasured trunks, this message will be preceded by a SETUP. The next message expected for the
trunk will be a start vector processing message (VSTART).

This is a variable length message based on the "c", "n" and "u" bits. The first twelve bytes will always be
sent. The message may optionally contain the VDN call count, which represents the current number of
active calls that are associated with the VDN. The VDN call count is incremented and decremented by the
switch, but is stored and reported by the reporting adjunct. The message may optionally contain the time
spent by the call in VDN processing elsewhere in the network. The message may also optionally contain
the UCID.

The message may contain any one or more: call_count, net_time and UCID. Regardless of which of these
fields are present, they will always be in the following order: call_count, net_time, UCID.

3.4.31.1                   DNEVENT20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y      y/n
                                              Last Release    CM6.3



    7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0
              time_tag                     DNEVENT20                                        seq num
                          seq num (cont)                                     tot siz             r   c   n   u   p     / / /
    /                             itn                             /                              iln
                             call_count                           /                          net_time
    /                            net_id                                                       seq
                                                            timestamp

time_tag       seconds past minute when event occurred, 0-59
opcode         DNEVENT20 = 235 (0xeb)
seq num        sequence number, 0-0xffff ffff
tot siz        total size in bytes, 1-255
r              return to VDN, 1=yes, 0=no
c              call count flag - indicates active calls present for this VDN
n              net time flag - indicates call has been interflowed from another switch in the network
u              UCID flag - indicates that UCID fields (net_id, seq and timestamp) are present
p              POM (Proactive Outreach Manager) VDN flag, 1=yes, 0=no (CM6.2 and later)
itn            internal trunk number, 1-32766
iln            internal line number (VDN), 1-32766
call_count     active calls associated with this VDN, 0-7712
net_time       time spent in VDN processing at prior sending switch(es), 0-32766 (times greater than 32766
               seconds are truncated to 32766)
net_id         network entity identifier, 1-32767
seq            call sequence number, 0-65535
timestamp      unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-209"></a>

## PDF page 209

Source: SPI-SYN24; PDF page 209; extracted characters: 2096.

```text
3.4.31.2                   DNEVENT24 (New CM7.0)


                                                               Switch   Vect    Skill
                                              First Release    CM7.0    y       y/n
                                              Last Release

    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                     DNEVENT24                                        seq num
                          seq num (cont)                                      tot siz             r   c   n   u   p     / / /
                                 itn                               /                             iln
                             call_count                            /                          net_time
    /                            net_id                                                        seq
                                                            timestamp

time_tag        seconds past minute when event occurred, 0-59
opcode          DNEVENT24 = 83 (0x53)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
r               return to VDN, 1=yes, 0=no
c               call count flag - indicates active calls present for this VDN
n               net time flag - indicates call has been interflowed from another switch in the network
u               UCID flag - indicates that UCID fields (net_id, seq and timestamp) are present
p               POM (Proactive Outreach Manager) VDN flag, 1=yes, 0=no (CM6.2 and later)
itn             internal trunk number, 1-65535
iln             internal line number (VDN), 1-32766
call_count      active calls associated with this VDN, 0-7712
net_time        time spent in VDN processing at prior sending switch(es), 0-32766 (times greater than 32766
                seconds are truncated to 32766)
net_id          network entity identifier, 1-32767
seq             call sequence number, 0-65535
timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-210"></a>

## PDF page 210

Source: SPI-SYN24; PDF page 210; extracted characters: 1979.

```text
       3.4.32      MODEVENT20 (New CM3.1)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y      y/n
                                             Last Release

The Modification Event message is sent by the switch when an entity on the switch has had its
administration changed and its modification number incremented.  Entities included in this protocol are
measured VDNs, vectors, and BSR application plans.

The modification number for a measured VDN is incremented and the MODEVENT20 message is sent
whenever the assigned vector or the assigned skills change.

The modification number for a vector is incremented and the MODEVENT20 message is sent whenever
the vector is modified.  If a vector is modified, this means that something in one or more steps has
changed. This includes a successful submission of the vector form on the SAT, and a successful
processing of the CHGVEC message from the reporting adjunct.

    7   6   5   4  3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1  0
              time_tag                   MODEVENT20                                       seq num
                          seq num (cont)                                    tot siz                 / / / /      obj type
                mod                /                           obj id

 time_tag     seconds past minute when event occurred, 0-59
 opcode       MODEVENT20 = 236 (0xec)
 seq num      sequence number, 0-0xffff ffff
 tot siz      total size in bytes, 1-255
 obj type     type of object which changed: 0=vector, 1=VDN
 mod          modification tag number, 0-255
 obj id       identifier for object

                obj type    entity        obj id values
                0           vector        1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
                1           VDN (iln)     1-32767
```

<a id="pdf-page-211"></a>

## PDF page 211

Source: SPI-SYN24; PDF page 211; extracted characters: 2484.

```text
       3.4.33       RAUDIT and RAUDIT24
Whenever the reporting adjunct receives a progress mark or state change (FSTATE) for an unmeasured
trunk, it sets an AT4 timer (5 minutes).  If this timer expires, the reporting adjunct will send an RAUDIT
message to the switch and reset the AT4 timer. The expected response from the switch is an
AUDIT/TAUDIT message for the requested trunk facility (internal trunk number).

Whenever the reporting adjunct receives a DNEVENT message with a VDN count, it sets an AT6 timer
(default 2 minutes) for the VDN.  If this timer expires, the reporting adjunct will send an RAUDIT message
to the switch and reset the timer. The expected response from the switch is a VAUDIT message for the
requested VDN (internal line number).

The reporting adjunct checks the EWT status of a split/skill based on an AT5 (default 2 minute) timer.  If
any non-NULL EWT values for that split/skill have not been updated by a QUEUED or DFWD-to-split
message since the timer was last reset and the EWT values cannot be inferred, then an RAUDIT
message with t=1 is sent to the switch.  The reporting adjunct will expect an EWTAUDIT message with
the updated expected wait times for the requested split/skill.

The EWT for a particular skill will be updated via an EWTAUDIT to the reporting adjunct when a call
comes out of queue (calculated using the top position, CM5.2.1 and later) or when the last agent logs out
of the skill (CM6.2 and later).

3.4.33.1                   RAUDIT


                                                               Switch   Vect    Skill
                                              First Release    G3V1     y/n     y/n
                                              Last Release     CM6.3



    7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0
              RAUDIT                            tag                /                            facility
      t            / / / / / /                 NOP

opcode      RAUDIT = 8 (0x08)
tag         message tag, 0-255 (it will be returned in the switch response message)
facility     t=1    split/skill number
             t=2    internal trunk number, 1-32766
             t=3    internal line number, 1-32766
t           audit type

             1    EWT (Expected Wait Time) (facility = split/skill)
             2    unmeasured trunk facility (facility = itn)
             3    VDN counted calls (facility = iln)
```

<a id="pdf-page-212"></a>

## PDF page 212

Source: SPI-SYN24; PDF page 212; extracted characters: 1044.

```text
3.4.33.2                    RAUDIT24 (New CM7.0)


                                                                Switch    Vect    Skill
                                                First Release   CM7.0     y/n     y/n
                                                Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
             RAUDIT24                            tag                                            facility
      t            / / / / / /                  NOP

opcode      RAUDIT24 = 66 (0x42)
tag         message tag, 0-255 (it will be returned in the switch response message)
facility      t=1    split/skill number
              t=2    internal trunk number, 1-65535
              t=3    internal line number, 1-32766
t           audit type

              1   EWT (Expected Wait Time) (facility = split/skill)
              2   unmeasured trunk facility (facility = itn)
              3   VDN counted calls (facility = iln)
```

<a id="pdf-page-213"></a>

## PDF page 213

Source: SPI-SYN24; PDF page 213; extracted characters: 1468.

```text
       3.4.34       TAUDIT20 and TAUDIT24
          (Replacements for AAUDIT, EWTAUDIT and VAUDIT)

          NOTE: IQ can receive an EWTAUDIT or VAUDIT.  These items will be used to update the
          database for expected wait time or VDN calls-counted (active calls). IQ does not currently
          process any other audit messages.

An Audit message is sent by the switch as part of a periodic task or at the request of the reporting
adjunct.  The audit is designed to ensure that the reporting adjunct database reflects the current status of
the switch database.

The switch audits the measured agents and facilities every 10 minutes and sends AAUDIT equivalent or
TAUDIT messages.

When the reporting adjunct receives an AAUDIT equivalent or TAUDIT message, it compares the status
of the agent or facility with that in the reporting adjunct real-time database.  If a discrepancy is found, the
reporting adjunct will log an error, abort call recording, initialize the agent position or trunk associated with
the call, and then wait for the next initializing event before continuing to track the agent or facility.

If the reporting adjunct receives an audit message inconsistent with the current state of the trunk or agent,
the reporting adjunct changes the state to OTHER for agent inconsistencies and UNKNOWN for trunk
inconsistencies.  When the state changes or another audit is received, the reporting adjunct updates the
agent/trunk to the switch state.
```

<a id="pdf-page-214"></a>

## PDF page 214

Source: SPI-SYN24; PDF page 214; extracted characters: 1929.

```text
3.4.34.1                   TAUDIT20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y/n    y/n
                                              Last Release    CM6.3

    7   6   5   4   3  2   1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                      TAUDIT20                                       seq num
                          seq num (cont)                                     tot siz              / /           state
    u                             itn                             /                           net_id
                                seq                                                       timestamp
                            timestamp

time_tag       seconds past minute when event occurred, 0-59
opcode         TAUDIT20 = 238 (0xee)
seq num        sequence number, 0-0xffff ffff
tot siz        total size in bytes, 1-255
state          current state

                 0     IDLE           trunk is available for calls (in idle pool)
                 2     QUEUED         trunk is queued to a split
                 3     DCON           trunk is connected to an agent position
                 6     MBUSY          trunk is maintenance-busy
                 9     OTHER          trunk is SEIZED, DABN, DFWD, FBUSY or FDISC actual state can be
                                      sent, but OTHER is acceptable
                 15    HOLD           trunk is on-hold at an agent position
u              flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn            internal trunk number, 1-32766
net_id         network entity identifier, 1-32767
seq            call sequence number, 0-65535
timestamp      unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-215"></a>

## PDF page 215

Source: SPI-SYN24; PDF page 215; extracted characters: 1971.

```text
3.4.34.2                   TAUDIT24 (New CM7.0)


                                                              Switch    Vect   Skill
                                              First Release   CM7.0     y/n    y/n
                                              Last Release

    7   6   5   4   3   2  1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                      TAUDIT24                                        seq num
                          seq num (cont)                                      tot siz              / /           state
    u           / / / / / / /                                   itn                               /            net_id
               net_id                                          seq                                        timestamp
                                            timestamp

time_tag       seconds past minute when event occurred, 0-59
opcode         TAUDIT24 = 84 (0x54)
seq num        sequence number, 0-0xffff ffff
tot siz        total size in bytes, 1-255
state          current state

                 0     IDLE           trunk is available for calls (in idle pool)
                 2     QUEUED         trunk is queued to a split
                 3     DCON           trunk is connected to an agent position
                 6     MBUSY          trunk is maintenance-busy
                 9     OTHER          trunk is SEIZED, DABN, DFWD, FBUSY or FDISC actual state can be
                                      sent, but OTHER is acceptable
                 15    HOLD           trunk is on-hold at an agent position
u              flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn            internal trunk number, 1-65535
net_id         network entity identifier, 1-32767
seq            call sequence number, 0-65535
timestamp      unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-216"></a>

## PDF page 216

Source: SPI-SYN24; PDF page 216; extracted characters: 2610.

```text
       3.4.35        AUDAVAIL22, AUDAVAIL23 and AUDAVAIL24

This is a variable length message based on "pnumber" and whether or not EAS is active.  Prior to
AUDAVAIL23, with EAS, this message will contain 8 additional bytes for the "skill-map". Starting with
AUDAVAIL23 and the expansion to 120 skills, with EAS, this message will contain 16 additional bytes for
the expanded “skill-map”.


3.4.35.1                    AUDAVAIL22 (New CM5.2)


                                                                Switch    Vect    Skill
                                               First Release    CM5.2     y/n     y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDAVAIL22                                        seq num
                           seq num (cont)                                       tot siz               pnumber         pos or p1-
                                                                                                                         p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                 m            / / / / / / /
        / / / /                                                       skill-map
                                                           skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDAVAIL22 = 2 (0x02)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This is
                  for IQ 5.0 support starting with CM 5.2.
skill-map         one bit for each staffed skill. The skills are mapped left to right and correspond to the order
                  of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       CMS will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-217"></a>

## PDF page 217

Source: SPI-SYN24; PDF page 217; extracted characters: 2713.

```text
3.4.35.2                    AUDAVAIL23 (New CM6.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM6.0     y/n     y/n
                                                Last Release     CM6.3



    7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0   7   6    5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDAVAIL23                                          seq num
                           seq num (cont)                                        tot siz                pnumber         pos or p1-
                                                                                                                           p15
                                pos (non-EAS) or p1-p15 (EAS) (cont)                                  m     ia          / / / / /
                                                               skill-map
                                                            skill-map (cont)
                                                            skill-map (cont)
                                            skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDAVAIL23 = 8 (0x08)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This is
                  for IQ 5.0 support starting with CM 5.2.
ia                flag indicating agent became available due to being interrupted while in Aux with an
                  Interruptible Aux reason code.

                    0    N/A (agent was not interrupted while in Aux)
                    1    auto-in-interrupt
                    2    manual-in-interrupt
                    3    notify-interrupt
skill-map         one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                  the order of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       CMS will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-218"></a>

## PDF page 218

Source: SPI-SYN24; PDF page 218; extracted characters: 2557.

```text
3.4.35.3                    AUDAVAIL24 (New CM7.0)


                                                                Switch    Vect    Skill
                                                First Release   CM7.0     y/n     y/n
                                                Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDAVAIL24                                         seq num
                           seq num (cont)                                       tot siz                / / /         pnumber
                           pos (non-EAS) or p1-p16 (EAS)                                 / / / /     m    ia          / / / / /
                                                              skill-map
                                                           skill-map (cont)
                                                           skill-map (cont)
                                           skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDAVAIL24 = 85 (0x55)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This is
                  for IQ 5.0 support starting with CM 5.2.
ia                flag indicating agent became available due to being interrupted while in Aux with an
                  Interruptible Aux reason code.

                   0    N/A (agent was not interrupted while in Aux)
                   1    auto-in-interrupt
                   2    manual-in-interrupt
                   3    notify-interrupt
skill-map         one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                  the order of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       CMS will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-219"></a>

## PDF page 219

Source: SPI-SYN24; PDF page 219; extracted characters: 3273.

```text
       3.4.36       AUDACD20, AUDACD23 and AUDACD24
This is a variable length message based on "pnumber" and whether or not EAS is active.  Prior to
AUDACD23, with EAS, this message will contain 7 additional bytes for the "skill-map" and without EAS
since the d/u flag byte still exists, the first 4 bits of the "skill-map" are set to 0. Starting with AUDACD23
and the expansion to 120 skills, with EAS, this message will contain 15 additional bytes for the expanded
“skill-map”.

3.4.36.1                    AUDACD20 (New CM3.1)


                                                                Switch    Vect   Skill
                                               First Release    CM3.1     y/n    y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDACD20                                          seq num
                           seq num (cont)                                       tot siz               pnumber        pos or p1-
                                                                                                                         p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                   d     u   /     skill-map
                                                           skill-map (cont)
                                           skill-map (cont)                                         /            net_id
            net_id (cont)                                        seq                                         timestamp
                                          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDACD20 = 240 (0xf0)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                   packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                   to a byte boundary
d                  direction of call
                   −    1 means call is outbound (ACDO)
                   −    2 means call is inbound (ACDI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map          one bit for each staffed skill. The skills are mapped left to right and correspond to the
                   order of the skills in the ALOGON message.
                   −    1 means agent state applies for this skill
                   −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                        the reporting adjunct will report the agent activity for this skill as OTHER.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-220"></a>

## PDF page 220

Source: SPI-SYN24; PDF page 220; extracted characters: 2961.

```text
3.4.36.2                    AUDACD23 (New CM6.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM6.0     y/n     y/n
                                                Last Release     CM6.3



    7   6   5   4   3   2    1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0
              time_tag                       AUDACD23                                           seq num
                           seq num (cont)                                        tot siz                pnumber        pos or p1-
                                                                                                                           p15
                                pos (non-EAS) or p1-p15 (EAS) (cont)                                   d      u         / / / / /
                                                               skill-map
                                                            skill-map (cont)
                                                            skill-map (cont)
                                           skill-map (cont)                                           /            net_id
            net_id (cont)                                         seq                                          timestamp
                                           timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDACD23 = 6 (0x06)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                   decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a
                   byte boundary
d                  direction of call
                   −     1 means call is outbound (ACDO)
                   −     2 means call is inbound (ACDI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map          one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                   the order of the skills in the ALOGON message.
                   −     1 means agent state applies for this skill
                   −     0 means agent state does not apply for this skill or the skill is not assigned/measured;
                         the reporting adjunct will report the agent activity for this skill as OTHER.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```
