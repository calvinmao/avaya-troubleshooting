---
title: "SPI-SYN24 - complete source pages 161-180"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 161-180

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-161"></a>

## PDF page 161

Source: SPI-SYN24; PDF page 161; extracted characters: 2386.

```text
DIGITS20 (continued)

time_tag              seconds past minute when event occurred, 0-59
opcode                DIGITS20 = 213 (0xd5)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
type                  type of digits

                       type     definition                                   parameter field contents
                       0        agent dialed digits (outbound call)          agent position
                       1        SID/ANI digits                               internal trunk number(ITN)
                       2        Collected digits                             internal trunk number(ITN)
                       3        Call work codes                              agent position
                       4        ISDN II-digits                               internal trunk number(ITN)
                       5        ASAI UUI (MV2 or later)                      internal trunk number (ITN)
pnumber               number of digits in "parameter"/"p1-p15", 1-15, agent position for outbound calls and
                      call work codes, will always be 5 for non-EAS and for "parameter" of internal trunk
                      number (ITN).
parameter/p1-         agent position for outbound calls and call work codes, without EAS "parameter" (1-
p15                   10000), with EAS "p1-p15" (0-9999999) login ID in packed decimal format, left-justified
                      where 0 is null and hex a is digit 0, zero fill to a byte boundary.
                      internal trunk number(ITN) "parameter" used to identify trunk facilities, 1-32766

dnumber               number of digits: 1-24 (type 0-4) and 1-96 (type 5)
d1-d24                for type=0-4, digits of destination number in packed decimal format, left-justified where 0
                      is null, hex a is digit 0, and hex c is # (for Collected digits).  When type = 4 (II-digits),
                      only d1-d2 will be populated, and leading zeros will be included.
d1-d96                for type=5, ASAI UUI (treated as binary data)
u                     flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id                network entity identifier, 1-32767
seq                   call sequence number, 0-65535
timestamp             unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-162"></a>

## PDF page 162

Source: SPI-SYN24; PDF page 162; extracted characters: 2575.

```text
3.4.9.2                        DIGITS24 (New CM7.0)


                                                                       Switch    Vect     Skill
                                                    First Release      CM7.0     y/n      y/n
                                                    Last Release



     7   6    5   4   3    2   1    0   7   6    5   4    3   2   1    0   7    6   5   4    3   2   1    0   7    6   5   4    3   2    1   0
                time_tag                          DIGITS24                                              seq num
                              seq num (cont)                                            tot siz                 type(0-4)            / / / /
        / / /         pnumber                                    parameter or p1-p16 (type 0,3)                                      / / / /
                dnumber                       d1               d2                d3               d4                d5                d6
           d7               d8                d9               d10              d11               d12              d13               d14
          d15              d16               d17               d18              d19               d20              d21               d22
          d23              d24          u                               net_id                                              seq
               seq (cont)                                                            timestamp
           timestamp (cont)



     7   6    5   4   3    2   1    0   7   6    5   4    3   2   1    0   7    6   5   4    3   2   1    0   7    6   5   4    3   2    1   0
                time_tag                          DIGITS24                                              seq num
                              seq num (cont)                                            tot siz                  type(5)             / / / /
        / / /         pnumber                                    parameter or p1-p16 (type 0,3)                                      / / / /
                dnumber                               d1                                  d2                                 d3
                                                                       .  .  .
                   d93                                d94                                d95                                d96
     u                               net_id                                                                seq
                                                                    timestamp
```

<a id="pdf-page-163"></a>

## PDF page 163

Source: SPI-SYN24; PDF page 163; extracted characters: 2349.

```text
DIGITS24 (continued)

time_tag             seconds past minute when event occurred, 0-59
opcode               DIGITS24 = 63 (0x3f)
seq num              sequence number, 0-0xffff ffff
tot siz              total size in bytes, 1-255
type                 type of digits

                      type     definition                                  parameter field contents
                      0        agent dialed digits (outbound call)         agent position
                      1        SID/ANI digits                              internal trunk number(ITN)
                      2        Collected digits                            internal trunk number(ITN)
                      3        Call work codes                             agent position
                      4        ISDN II-digits                              internal trunk number(ITN)
                      5        ASAI UUI (MV2 or later)                     internal trunk number (ITN)
pnumber              number of digits in "parameter"/"p1-p16", 1-16, agent position for outbound calls
                     and call work codes, will always be 5 for non-EAS and for "parameter" of internal
                     trunk number (ITN).
parameter/           agent position for outbound calls and call work codes, without EAS "parameter"
p1-p16               (1-10000), with EAS "p1-p16" (0-9999999) login ID in packed decimal format, left-
                     justified where 0 is null and hex a is digit 0, zero fill to a byte boundary.
                     internal trunk number(ITN) "parameter" used to identify trunk facilities, 1-65535
dnumber              number of digits: 1-24 (type 0-4) and 1-96 (type 5)
d1-d24               for type=0-4, digits of destination number in packed decimal format, left-justified where 0
                     is null, hex a is digit 0, and hex c is # (for Collected digits).  When type = 4 (II-digits),
                     only d1-d2 will be populated, and leading zeros will be included.
d1-d96               for type=5, ASAI UUI (treated as binary data)
u                    flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id               network entity identifier, 1-32767
seq                  call sequence number, 0-65535
timestamp            unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-164"></a>

## PDF page 164

Source: SPI-SYN24; PDF page 164; extracted characters: 883.

```text
       3.4.10       AEVENT20 and AEVENT24
The Agent Event message is sent by the switch when an agent presses an event button or an event
related to the agent has occurred. This includes stroke count, malicious call, supervisor assist, audio
difficulty, RONA, ROIF, ROOF, "special" reason code buttons and agent notifications. The reporting
adjunct will generate an immediate exception for malicious call, audio difficulty, RONA, ROIF or ROOF.
The reporting adjunct will record the number of occurrences of supervisor assists and stroke counts on an
agent and split/skill basis.

Assist and stroke count will only be pegged in the reporting adjunct if the agent is on an ACD call
(split/skill or direct agent) or in ACW. Audio difficulty and MCT are pegged anytime the agent has any call.
If all calls are on hold, The reporting adjunct pegs the event for the last call put on hold.
```

<a id="pdf-page-165"></a>

## PDF page 165

Source: SPI-SYN24; PDF page 165; extracted characters: 3067.

```text
3.4.10.1                    AEVENT20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release    CM6.3

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AEVENT20                                         seq num
                           seq num (cont)                                      tot siz             /   u   t        button
      pnumber                                             pos (non-EAS) or p1-p15 (EAS)
     /                           net_id                                                      seq_num
                                                             timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            AEVENT20 = 214 (0xd6)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
t, button         type of button, button pressed
                   t=0    miscellaneous button type, button = 0-7 as follows:
                            0    supervisor assist or malicious call event completed (CLEAR)
                            1    malicious call started
                            2    supervisor assist call started
                            3    call redirected because no answer while ringing at agent position: RONA
                                 (Redirect On No Answer), or not delivered due to connectivity failure: ROIF
                                 (Redirect on IP Failure, CM2.1 or later) or ROOF (Redirect on Optim Failure,
                                 CM5.0 or later).
                            4    agent entered AUX reason code 0, *, # or timed out.
                            5    agent entered logout reason code 0, *, # or timed out.
                            6    agent has been notified for interruptible work while in AUX (CM6.0 and later).
                            7    agent has been cleared from interruptible work while in AUX (CM6.0 and
                                 later).
                   t=1    stroke count button type, button = 0-9 as follows: is a stroke button, 0-9
                            0    audio difficulty
                            N    stroke 1-9
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position, without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-166"></a>

## PDF page 166

Source: SPI-SYN24; PDF page 166; extracted characters: 3075.

```text
3.4.10.2                   AEVENT24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release

    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                      AEVENT24                                         seq num
                           seq num (cont)                                     tot siz              /  u   t        button
       / / /        pnumber                              pos (non-EAS) or p1-p16 (EAS)                                / / / /
    /                            net_id                                                        seq
                                                            timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            AEVENT24 = 64 (0x40)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
t, button         type of button, button pressed
                   t=0    miscellaneous button type, button = 0-7 as follows:
                            0   supervisor assist or malicious call event completed (CLEAR)
                            1   malicious call started
                            2   supervisor assist call started
                            3   call redirected because no answer while ringing at agent position: RONA
                                (Redirect On No Answer), or not delivered due to connectivity failure: ROIF
                                (Redirect on IP Failure, CM2.1 or later) or ROOF (Redirect on Optim Failure,
                                CM5.0 or later).
                            4   agent entered AUX reason code 0, *, # or timed out.
                            5   agent entered logout reason code 0, *, # or timed out.
                            6   agent has been notified for interruptible work while in AUX (CM6.0 and later).
                            7   agent has been cleared from interruptible work while in AUX (CM6.0 and
                                later).
                   t=1    stroke count button type, button = 0-9 as follows: is a stroke button, 0-9
                            0    audio difficulty
                            N    stroke 1-9
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position, without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                  in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                  null, zero fill to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-167"></a>

## PDF page 167

Source: SPI-SYN24; PDF page 167; extracted characters: 1623.

```text
       3.4.11       IDLE20, IDLE23 and IDLE24
The IDLE message is sent by the switch when a facility goes idle.

3.4.11.1                    IDLE20 (New CM3.1)


                                                                Switch   Vect    Skill
                                               First Release    CM3.1    y/n     y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                         IDLE20                                         seq num
                           seq num (cont)                                      tot siz             u               itn
              itn (cont)            /                            net_id                                         seq
              seq (cont)                                                     timestamp
          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          IDLE20 = 215 (0xd7)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-32766
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-168"></a>

## PDF page 168

Source: SPI-SYN24; PDF page 168; extracted characters: 2438.

```text
3.4.11.2                    IDLE23 (New CM6.0)


                                                                Switch   Vect    Skill
                                               First Release    CM6.0    y/n     y/n
                                               Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        IDLE23                                         seq num
                           seq num (cont)                                      tot siz             u              itn
              itn (cont)               r_abort          / / / /     /                            net_id
                                 seq                                                        timestamp
                          timestamp (cont)

time_tag        seconds past minute when event occurred, 0-59
opcode          IDLE23 = 27 (0x1b)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn             internal trunk number used to identify trunk facilities, 1-32766
r_abort         Reason for why call was aborted and may be requeued later with same ucid.
                 0    Default – call was not aborted for later requeue
                 1    Call could not be delivered because media or other resources were not available when
                      agent was selected
                 2    Wait time increased drastically
                 3    Call was aborted after being delivered to the agent because the call was still receiving
                      uninterruptible wait treatment
                 4    Recovering from a network failure - e.g., Call was cancelled because 182 Queued
                      message was not received from CM within configured timeout
                 5    Recovering from a Voice Portal failure - Call was cancelled due to a VP application
                      failure
                 6    Cancelled due to caller interaction - Caller has subsequently indicated a change to the
                      disposition via a prompt from ICR
net_id          network entity identifier, 1-32767
seq             call sequence number, 0-65535
timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-169"></a>

## PDF page 169

Source: SPI-SYN24; PDF page 169; extracted characters: 2431.

```text
3.4.11.3                    IDLE24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                        IDLE24                                         seq num
                           seq num (cont)                                     tot siz             u      / / /       r_abort
                                 itn                               /                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

time_tag        seconds past minute when event occurred, 0-59
opcode          IDLE24 = 65 (0x41)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
r_abort         Reason for why call was aborted and may be requeued later with same ucid.
                 0    Default – call was not aborted for later requeue
                 1    Call could not be delivered because media or other resources were not available when
                      agent was selected
                 2    Wait time increased drastically
                 3    Call was aborted after being delivered to the agent because the call was still receiving
                      uninterruptible wait treatment
                 4    Recovering from a network failure - e.g., Call was cancelled because 182 Queued
                      message was not received from CM within configured timeout
                 5    Recovering from a Voice Portal failure - Call was cancelled due to a VP application
                      failure
                 6    Cancelled due to caller interaction - Caller has subsequently indicated a change to the
                      disposition via a prompt from ICR
itn             internal trunk number used to identify trunk facilities, 1-65535
net_id          network entity identifier, 1-32767
seq             call sequence number, 0-65535
timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-170"></a>

## PDF page 170

Source: SPI-SYN24; PDF page 170; extracted characters: 3447.

```text
       3.4.12        SETUP22 and SETUP24
The SETUP message is sent by the switch when a trunk is seized or as the first message of a call
entering the reporting adjunct measured domain.  The universal call id (UCID) associated with a call must
be sent at the beginning of the call (or when it enters the measured domain).

3.4.12.1                    SETUP22 (New CM5.2)


                                                               Switch    Vect   Skill
                                               First Release   CM5.2     y/n    y/n
                                               Last Release    CM6.3

This is a variable length message based on the "u1" and "u2" bits. The first ten bytes are always sent.

    7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                       SETUP22                                         seq num
                           seq num (cont)                                     tot siz              u              itn
                                                                                                   1
              itn (cont)            d   o   i   c  u   r   m   /   /                           net_id1
                                                   2
                                seq1                                                       timestamp1
                         timestamp1 (cont)                         /                           net_id2
                                seq2                                                       timestamp2
                         timestamp2 (cont)

time_tag         seconds past minute when event occurred, 0-59
opcode           SETUP22 = 254 (0xfe)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
u1               flag indicating that the UCID fields (net_id1, seq1, and timestamp1) are present.
itn              internal trunk number used to identify trunk facilities, 1-32766
d                direction; 0 = outbound, 1 = inbound
o                OCM call; 0 = no, 1 = call distributed by OCM
i                ignore messsage indication for ProActive Contact support; 0 = accept, 1 = ignore
c                converse flag indicating SETUP sent because call being routed to a converse-on skill port.
u2               flag indicating that the UCID fields (net_id2, seq2, and time_stamp2) are present. This is
                 the parent held call UCID provided with a call transferred from one CM to another.
r                re-sent call with the same UCID of a call that was aborted while still active and has
                 returned. Default is 0.
m                media-added - The itn for the call has changed because media was added by a SIP INVITE
                 with replaces for ICR support.  This SETUP will be immediately followed by an XFER
                 (rename) and an IDLE for the first itn.  The UCID included in all the messages will be the
                 same as the original SETUP.  Default is 0.
net_id1          network entity identifier; 1-32767
seq1             call sequence number; 0-65535
timestamp1       unix style (seconds since 1/1/70) time call assigned a UCID
net_id2          network entity identifier; 1-32767
seq2             call sequence number; 0-6553.
timestamp2       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-171"></a>

## PDF page 171

Source: SPI-SYN24; PDF page 171; extracted characters: 3603.

```text
3.4.12.2                   SETUP24 (New CM7.0)


                                                              Switch    Vect    Skill
                                              First Release   CM7.0     y/n     y/n
                                              Last Release

This is a variable length message based on the "u1" and "u2" bits. The first ten bytes are always sent.

    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                      SETUP24                                         seq num
                          seq num (cont)                                      tot siz             u     / / /       reason
                                                                                                  1
                                 itn                              d   o   i   c   u   r   m   /   /           net_id1
                                                                                  2
           net_id1 (cont)                                      seq1                                       timestamp1
                                        timestamp1 (cont)                                         /           net_id2
           net_id2 (cont)                                      seq2                                       timestamp2
                                        timestamp2 (cont)

time_tag         seconds past minute when event occurred, 0-59
opcode           SETUP24 = 66 (0x42)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
u1               flag indicating that the UCID fields (net_id1, seq1, and timestamp1) are present.
reason           reason the setup was sent:

                   0   New contact – the first message for a contact
                   1   The SETUP is part of a RENAME
                   2   Adding a trunk – an example is outflow
                   3   LAR redirect of the call
                   4   Converse command connection to the IVR port
                   5   CTI phantom call
itn              internal trunk number used to identify trunk facilities, 1-65535
d                direction; 0 = outbound, 1 = inbound
o                OCM call; 0 = no, 1 = call distributed by OCM
i                ignore messsage indication for ProActive Contact support; 0 = accept, 1 = ignore
c                converse flag indicating SETUP sent because call being routed to a converse-on skill port.
u2               flag indicating that the UCID fields (net_id2, seq2, and time_stamp2) are present. This is
                 the parent held call UCID provided with a call transferred from one CM to another.
r                re-sent call with the same UCID of a call that was aborted while still active and has
                 returned. Default is 0.
m                media-added - The itn for the call has changed because media was added by a SIP INVITE
                 with replaces for ICR support.  This SETUP will be immediately followed by an XFER
                 (rename) and an IDLE for the first itn.  The UCID included in all the messages will be the
                 same as the original SETUP.  Default is 0.
net_id1          network entity identifier; 1-32767
seq1             call sequence number; 0-65535
timestamp1       unix style (seconds since 1/1/70) time call assigned a UCID
net_id2          network entity identifier; 1-32767
seq2             call sequence number; 0-6553.
timestamp2       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-172"></a>

## PDF page 172

Source: SPI-SYN24; PDF page 172; extracted characters: 2813.

```text
       3.4.13       QUEUED20, QUEUED23 and QUEUED24
The QUEUED message is sent by the switch when a facility queues to a skill hunt group.

This is a variable length message based on the "e" bit and "u" bit. The message may optionally contain
the expected wait time (EWT) for the split. EWT is calculated by the switch, but stored and reported by
the reporting adjunct. The message may optionally contain the UCID in CM3.1 and later.

3.4.13.1                    QUEUED20 (New CM3.1)


                                                                Switch    Vect    Skill
                                               First Release    CM3.1     y/n     y/n
                                               Last Release     CM5.2

Twelve bytes (the first 11 bytes + the first byte of the UCID for the “u” flag) will always be sent.

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      QUEUED20                                          seq num
                           seq num (cont)                                      tot siz              o              itn
              itn (cont)                              dest                      p   e    plv    b                ewt
              ewt (cont)            u                            net_id                                          seq
              seq (cont)                                                     timestamp
          timestamp (cont)

time_tag        seconds past minute when event occurred, 0-59
opcode          QUEUED20 = 217 (0xd9)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
o               OCM call; 0 = no, 1 = call distributed by OCM
itn             internal trunk number used to identify trunk facilities, 1-32766
dest            destination: split/skill number, 1-2000 (MV2 and later)
p               priority call (w/o vectoring enabled) 0 = none, 1 = priority
e               ewt flag indicating that ewt field is present If not, EWT for that priority is understood by the
                reporting adjunct to be null)
plv             priority level (with vectoring enabled); 0 = low, 1 = medium, 2 = high, 3 = top  (Send 1 or 2 if
                vectoring active but non-vector controlled split.)
b               backup split/skill; 0 = main, 1 = backup
ewt             expected wait time for the priority level specified in the plv field, 1-32767 seconds (vectoring
                only)
u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id          network entity identifier, 1-32767
seq             call sequence number, 0-65535
timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-173"></a>

## PDF page 173

Source: SPI-SYN24; PDF page 173; extracted characters: 2784.

```text
3.4.13.2                     QUEUED23 (New CM6.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM6.0     y/n     y/n
                                                Last Release     CM6.3

Sixteen bytes (the first 15 bytes plus the first byte of UCID for the “u” flag) will always be sent.

    7   6   5   4    3   2   1   0   7   6   5   4   3    2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3    2   1   0
               time_tag                      QUEUED23                                           seq num
                            seq num (cont)                                       tot siz              o               itn
               itn (cont)               / / /                           dest                          p   e   b      plv        / /
      / /               queued_calls                                   oldest_call                                 ewt
              ewt (cont)             u                             net_id                                          seq
              seq (cont)                                                       timestamp
          timestamp (cont)

time_tag            seconds past minute when event occurred, 0-59
opcode              QUEUED23 = 28 (0x1c)
seq num             sequence number, 0-0xffff ffff
tot siz             total size in bytes, 1-255
o                   OCM call; 0 = no, 1 = call distributed by OCM
itn                 internal trunk number used to identify trunk facilities, 1-32766
dest                destination: split/skill number, 1-8000
p                   priority call (w/o vectoring enabled) 0 = none, 1 = priority
e                   ewt flag indicating that ewt field is present If not, EWT for that priority is understood by the
                    reporting adjunct to be null)
b                   backup split/skill; 0 = main, 1 = backup
plv                 priority level (with vectoring enabled); 0 = low, 1 = medium, 2 = high, 3 = top, 4 = redirect
                    (Send 1 or 2 if vectoring active but non-vector controlled split.)
queued_calls        number of calls in queue including this added one, 0-999 (Over 999 will be sent as 0x3ff)
oldest_call         times in secs of the oldest call in queue, 0-999 secs
ewt                 expected wait time for the priority level specified in the plv field, 1-32767 seconds
                    (vectoring only).
u                   flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id              network entity identifier, 1-32767
seq                 call sequence number, 0-65535
timestamp           unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-174"></a>

## PDF page 174

Source: SPI-SYN24; PDF page 174; extracted characters: 2773.

```text
3.4.13.3                    QUEUED24 (New CM7.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM7.0     y/n     y/n
                                                Last Release

Seventeen bytes (the first 16 bytes plus the first byte of UCID for the “u” flag) will always be sent.

    7   6   5   4   3   2    1   0   7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                      QUEUED24                                           seq num
                           seq num (cont)                                        tot siz              o           / / / / / / /
                                  itn                                   / / /                           dest
    p   e   b      plv        / /     / /                queued_calls                                  oldest_call
                                 ewt                                 u                             net_id
                                 seq                                                           timestamp
                           timestamp (cont)

time_tag            seconds past minute when event occurred, 0-59
opcode              QUEUED24 = 67 (0x43)
seq num             sequence number, 0-0xffff ffff
tot siz             total size in bytes, 1-255
o                   OCM call; 0 = no, 1 = call distributed by OCM
itn                 internal trunk number used to identify trunk facilities, 1-65535
dest                destination: split/skill number, 1-8000
p                   priority call (w/o vectoring enabled) 0 = none, 1 = priority
e                   ewt flag indicating that ewt field is present If not, EWT for that priority is understood by the
                    reporting adjunct to be null)
b                   backup split/skill; 0 = main, 1 = backup
plv                 priority level (with vectoring enabled); 0 = low, 1 = medium, 2 = high, 3 = top, 4 = redirect
                    (Send 1 or 2 if vectoring active but non-vector controlled split.)
queued_calls        number of calls in queue including this added one, 0-999 (Over 999 will be sent as 0x3ff)
oldest_call         times in secs of the oldest call in queue, 0-999 secs
ewt                 expected wait time for the priority level specified in the plv field, 1-32767 seconds
                    (vectoring only).
u                   flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id              network entity identifier, 1-32767
seq                 call sequence number, 0-65535
timestamp           unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-175"></a>

## PDF page 175

Source: SPI-SYN24; PDF page 175; extracted characters: 2544.

```text
       3.4.14       DAQUEUED20, DAQUEUED23 and DAQUEUED24
The DAQUEUED message is sent by the switch when a facility is extended to an agent (direct agent call).
DAQUEUED is sent independent of the call actually queuing.

This is a variable length message based on "pnumber" and "u".

3.4.14.1                   DAQUEUED20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM5.2



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                    DAQUEUED20                                        seq num
                           seq num (cont)                                     tot siz             u              itn
              itn (cont)            o                    split                      pnumber             pos(non-EAS) or
                                                                                                          p1-p15(EAS)
                       pos (non-EAS) or p1-p15 (EAS) (cont)                            / / / /    /            net_id
            net_id (cont)                                       seq                                        timestamp
                                         timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            DAQUEUED20 = 218 (0xda)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-32766
o                 OCM call; 0 = no, 1 = call distributed by OCM
split             split or skill, 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-5200 for G3V2-G3V4 or 1-10000 G3V5 and later),
                  with EAS "p1-p15" (0-9999999) login ID in packed decimal format, left-justified where hex a
                  is digit 0 and 0 in this field is null, zero fill to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-176"></a>

## PDF page 176

Source: SPI-SYN24; PDF page 176; extracted characters: 2083.

```text
3.4.14.2                    DAQUEUED23 (New CM6.0)


                                                                 Switch   Vect    Skill
                                                First Release    CM6.0    y/n     y/n
                                                Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                     DAQUEUED23                                          seq num
                           seq num (cont)                                       tot siz              u              itn
              itn (cont)            o     / /                          split                             / / / /       pnumber
                                           pos (non-EAS) or p1-p15 (EAS)                                                 / / / /
     /                            net_id                                                         seq
                                                              timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            DAQUEUED23= 29 (0x1d)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-32766
o                 OCM call; 0 = no, 1 = call distributed by OCM
split             split or skill, 1-8000
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-177"></a>

## PDF page 177

Source: SPI-SYN24; PDF page 177; extracted characters: 2041.

```text
3.4.14.3                   DAQUEUED24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                    DAQUEUED24                                         seq num
                           seq num (cont)                                     tot siz              u           / / / / / / /
                                 itn                               o    / /                          split
       / / /        pnumber                               pos (non-EAS) or p1-p16 (EAS)                               / / / /
    /                            net_id                                                        seq
                                                            timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            DAQUEUED24 = 68 (0x44)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-65535
o                 OCM call; 0 = no, 1 = call distributed by OCM
split             split or skill, 1-8000
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-178"></a>

## PDF page 178

Source: SPI-SYN24; PDF page 178; extracted characters: 3454.

```text
       3.4.15        DCON22, DCON23 and DCON24
The DCON message is sent by the switch when a facility dequeues and connects to an agent. DCON is
also sent to indicate someone such as a service observer has bridged on to the call ("b" bit is set). This is
a variable length message based on "pnumber" and the "s" and "u" bits. The "s" bit is only set for EAS
and only when ringing an agent with a call for a measured skill. The message may optionally contain the
UCID in CM5.2 and later.  When the "s" bit is set, the message will contain 2 additional bytes for the "skill"
field.

3.4.15.1                    DCON22 (New CM5.2)


                                                                Switch    Vect   Skill
                                               First Release    CM5.2     y/n    y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                        DCON22                                          seq num
                           seq num (cont)                                      tot siz              d              itn
              itn (cont)              pnumber                             pos (non-EAS) or p1-p15 (EAS)
        pos or p1-p15 (cont)        e   b   s   u   n     o            / / / / / /                        skill
    /                            net_id                                                         seq
                                                             timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            DCON22 = 253 (0xfd)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
d                 direction; 0=outbound, 1=inbound
itn               internal trunk number used to identify trunk facilities, 1-32766
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
                  0=an unmeasured endpoint received the call. In this case, no position is sent.
pos/p1-p15        agent position without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where 0 is null and hex a is digit 0, zero fill to a byte
                  boundary
e                 call to extension; 0=no (ACD or direct agent), 1=extension call (Note: a call to the login ID
                  with EAS that does not have the direct agent COR will be considered an extension call)
b                 bridging; 0 = not bridging on to a call, 1 = bridging on to a call
s                 0 = no skill in message, 1 = skill in message (ACD or Direct Agent call)
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
n                 flag indicating that call was dequeued after multiple split queueing
o                 type of observing when "b" bit is set due to service observing. Field for IQ 5.0 support
                  starting with CM 5.2.
                   0    none (bridging case)
                   1    agent
                   2    VDN
skill             skill matched 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-179"></a>

## PDF page 179

Source: SPI-SYN24; PDF page 179; extracted characters: 3817.

```text
3.4.15.2                    DCON23 (New CM6.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM6.0     y/n    y/n
                                                Last Release     CM6.3



    7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        DCON23                                           seq num
                           seq num (cont)                                       tot siz              d              itn
              itn (cont)              pnumber                              pos (non-EAS) or p1-p15 (EAS)
        pos or p1-p15 (cont)         e   b   s   u   n    o           slevel           p       a        / / /           skill
              skill (cont)           /                            net_id                                          seq
              seq (cont)                                                      timestamp
          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            DCON23 = 11 (0x0b)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
d                 direction; 0=outbound, 1=inbound
itn               internal trunk number used to identify trunk facilities, 1-32766
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
                  0=an unmeasured endpoint received the call. In this case, no position is sent.
pos/p1-p15        agent position without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed decimal
                  format, left-justified where 0 is null and hex a is digit 0, zero fill to a byte boundary
e                 call to extension; 0=no (ACD or direct agent), 1=extension call (Note: a call to the login ID
                  with EAS that does not have the direct agent COR will be considered an extension call)
b                 bridging; 0 = not bridging on to a call, 1 = bridging on to a call
s                 0 = no skill in message, 1 = skill in message (ACD or Direct Agent call)
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
n                 flag indicating that call was dequeued after multiple split queueing
o                 type of observing when "b" bit is set due to service observing.
                  −    0 none (bridging case)
                  −    1 agent
                  −    2 VDN

slevel            Level assigned to the agent for the skill that the call was delivered for, 0 (default) or level 1-
                  16.
p                   0   Call was not delivered via the preferred skill level check vector command or no skill
                        preference was specified (default)
                    1   Agent’s level for the skill does not match the level specified in the check vector
                        command (either this was the only eligible agent or none of the eligible agent’s
                        assigned level for the skill matched)
                    2   Agent’s level for the skill matches the preferred skill level (or range) specified by the
                        check vector command.
a                   0   for the not applicable case (default)
                    1   ACD call was routed to the agent after being queued (call surplus)
                    2   ACD call was routed to the agent without being queued (agent surplus)
skill             skill matched 1-8000
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-180"></a>

## PDF page 180

Source: SPI-SYN24; PDF page 180; extracted characters: 3981.

```text
3.4.15.3                    DCON24 (New CM7.0)


                                                                Switch    Vect   Skill
                                               First Release    CM7.0     y/n    y/n
                                               Last Release

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        DCON24                                          seq num
                           seq num (cont)                                      tot siz              d           / / / / / / /
                                 itn                                   / / /        pnumber              pos (non-EAS) or
                                                                                                           p1-p16 (EAS)
                pos or p1-p16 (cont)                    / / / /     e   b   s   u   n     o          slevel           p       a
       / / /                           skill                        /                            net_id
                                 seq                                                         timestamp
                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            DCON24 = 69 (0x45)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
d                 direction; 0=outbound, 1=inbound
itn               internal trunk number used to identify trunk facilities, 1-65535
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
                  0=an unmeasured endpoint received the call. In this case, no pos/p1-p16 is sent.
pos/p1-p16        agent position without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where 0 is null and hex a is digit 0, zero fill to a byte
                  boundary
e                 call to extension; 0=no (ACD or direct agent), 1=extension call (Note: a call to the login ID
                  with EAS that does not have the direct agent COR will be considered an extension call)
b                 bridging; 0 = not bridging on to a call, 1 = bridging on to a call
s                 0 = no skill in message, 1 = skill in message (ACD or Direct Agent call)
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
n                 flag indicating that call was dequeued after multiple split queueing
o                 type of observing when "b" bit is set due to service observing.
                  −    0 none (bridging case)
                  −    1 agent
                  −    2 VDN
slevel            Level assigned to the agent for the skill that the call was delivered for, 0 (default) or level 1-
                  16.
p                  0    Call was not delivered via the preferred skill level check vector command or no skill
                        preference was specified (default)
                   1    Agent’s level for the skill does not match the level specified in the check vector
                        command (either this was the only eligible agent or none of the eligible agent’s
                        assigned level for the skill matched)
                   2    Agent’s level for the skill matches the preferred skill level (or range) specified by the
                        check vector command.
a                  0    for the not applicable case (default)
                   1    ACD call was routed to the agent after being queued (call surplus)
                   2    ACD call was routed to the agent without being queued (agent surplus)
skill             skill matched 1-8000
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```
