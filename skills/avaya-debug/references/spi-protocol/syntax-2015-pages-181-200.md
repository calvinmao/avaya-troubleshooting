---
title: "SPI-SYN24 - complete source pages 181-200"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 181-200

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-181"></a>

## PDF page 181

Source: SPI-SYN24; PDF page 181; extracted characters: 2476.

```text
       3.4.16       DABN22 and DABN24
The DABN message is sent by the switch when a facility abandons in processing, in queue, while ringing
or when a caller (agent or other party) drops from hold.

3.4.16.1                    DABN22 (New CM5.2)


                                                                Switch    Vect   Skill
                                               First Release    CM5.2     y/n    y/n
                                               Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        DABN22                                          seq num
                           seq num (cont)                                      tot siz              d              itn
              itn (cont)              pnumber                             pos (non-EAS) or p1-p15 (EAS)
        pos or p1-p15 (cont)        u       r           / / / /     /                            net_id
                                 seq                                                         timestamp
                          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             DABN22 = 252 (0xfc)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
d                  1 = agent dropped last conferenced party, 0 = doesn't apply
itn                internal trunk number used to identify trunk facilities, 1-32766
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                   packed decimal format, left-justified where 0 is null and hex a is digit 0, zero fill to a byte
                   boundary. The agent position is the identity of the agent who put the call on hold for the
                   held call dropped case.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
r                  reason field.
                     0      normal call abandoned
                     1      held call dropped
                     2-7    for future use
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-182"></a>

## PDF page 182

Source: SPI-SYN24; PDF page 182; extracted characters: 2446.

```text
3.4.16.2                   DABN24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                       DABN24                                          seq num
                           seq num (cont)                                     tot siz              d           / / / / / / /
                                 itn                                  / / /        pnumber              pos (non-EAS) or
                                                                                                          p1-p16 (EAS)
                        pos or p1-p16 (cont)                       u       r           / / / /     /            net_id
            net_id (cont)                                       seq                                         timestamp
                                         timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             DABN24 = 70 (0x46)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
d                  1 = agent dropped last conferenced party, 0 = doesn't apply
itn                internal trunk number used to identify trunk facilities, 1-65535
pnumber            number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16         agent position without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                   in packed decimal format, left-justified where 0 is null and hex a is digit 0, zero fill to
                   a byte boundary. The agent position is the identity of the agent who put the call on
                   hold for the held call dropped case.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
r                  reason field.
                    0       normal call abandoned
                    1       held call dropped
                    2-7     for future use
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-183"></a>

## PDF page 183

Source: SPI-SYN24; PDF page 183; extracted characters: 2438.

```text
       3.4.17       DADFWD20 and DADFWD24
The DADFWD20 message is sent by the switch when a facility is forwarded to an agent via direct agent
calling. This is a variable length message based on "pnumber" and "u".

3.4.17.1                    DADFWD20 (New CM3.1)


                                                                Switch   Vect    Skill
                                               First Release    CM3.1    y/n     y/n
                                               Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      DADFWD20                                         seq num
                           seq num (cont)                                      tot siz             a              itn
              itn (cont)            o                     skill                      pnumber               pos or p1-p15
                       pos (non-EAS) or p1-p15 (EAS) (cont)                             / / / /    u             net_id
            net_id (cont)                                       seq                                         timestamp
                                          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             DADFWD20 = 221 (0xdd)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
a                  ASAI adjunct routing; 1 = adjunct (re)routed call
itn                internal trunk number used to identify trunk facilities, 1-32766
o                  OCM call; 0 = no, 1 = call distributed by OCM
skill              skill number or split number call queued to, 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                   packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                   to a byte boundary
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-184"></a>

## PDF page 184

Source: SPI-SYN24; PDF page 184; extracted characters: 2159.

```text
3.4.17.2                   DADFWD24 (New CM7.0)


                                                               Switch   Vect    Skill
                                              First Release    CM7.0    y/n     y/n
                                              Last Release

    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0
              time_tag                     DADFWD24                                         seq num
                          seq num (cont)                                      tot siz             a           / / / / / / /
                                 itn                               o    / /                          skill
       / / /        pnumber                              pos (non-EAS) or p1-p16 (EAS)                                / / / /
    u                            net_id                                                        seq
                                                            timestamp



time_tag           seconds past minute when event occurred, 0-59
opcode             DADFWD24 = 42 (0x2a)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
a                  ASAI adjunct routing; 1 = adjunct (re)routed call
itn                internal trunk number used to identify trunk facilities, 1-65535
o                  OCM call; 0 = no, 1 = call distributed by OCM
skill              skill number or split number call queued to, 1-8000
pnumber            number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16         agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login
                   ID in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                   null, zero fill to a byte boundary
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-185"></a>

## PDF page 185

Source: SPI-SYN24; PDF page 185; extracted characters: 1900.

```text
       3.4.18       DFWD20, DFWD23 and DFWD24
The DFWD message is sent by the switch when a facility is forwarded internally. This is a variable length
message based on "dnumber" and the "e" and "u" bits. When the "e" bit is set the message will contain
two additional bytes for the "ewt" field. If "dnumber" is zero then there will be NO "dest"/"d1-d15" field in
message.

The message may optionally contain the expected wait time (EWT) for the split, which is based on the
history of calls that have queued to this split (ftype = 4).  EWT is calculated by the switch, and sent to
CMS. The message may optionally contain the UCID in CM3.1 and later.

When forwarded to an agent position (ftype = 6) the "dest" will contain the login ID packed decimal format,
left-justified with EAS.

3.4.18.1                    DFWD20 (New CM3.1)


                                                                 Switch    Vect    Skill
                                                First Release    CM3.1     y/n     y/n
                                                Last Release     CM5.2



    7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2    1   0
              time_tag                        DFWD20                                           seq num
                           seq num (cont)                                        tot siz             a               itn
              itn (cont)             o     ftype       dnumber                              dest or d1-d15
                dest or d1-d15 (cont)                    / / / /        / / /    u   c   e    plv                 ewt
              ewt (cont)             /                            net_id                                          seq
              seq (cont)                                                      timestamp
           timestamp (cont
```

<a id="pdf-page-186"></a>

## PDF page 186

Source: SPI-SYN24; PDF page 186; extracted characters: 2885.

```text
DFWD20 (continued)

time_tag           seconds past minute when event occurred, 0-59
opcode             DFWD20 = 222 (0xde)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
a                  ASAI adjunct routing; 1 = adjunct (re)routed call
itn                internal trunk number used to identify trunk facilities, 1-32766
o                  OCM call; 0 = no, 1 = call distributed by OCM
ftype              forwarding type

                     0    redirected (intraflow) to a VDN
                     1    interflow
                     2    lookahead interflow, BSR interflow, or Network Call Redirection
                     3    unknown destination
                     4    redirected (intraflow) to a split
                     5    not used
                     6    redirected (intraflow) to an extension
                     7    redirected (intraflow) to an attendant position
dnumber            number of digits in "dest"/"d1-d15", 5 for ftype=0 and 5 for ftype=4 and 1-15 for
                   ftype=6(EAS)
                   0=call was forwarded to an unmeasured endpoint. In this case, no destination is sent.
dest/d1-d15        destination: with EAS "d1-d15" (0-9999999) login ID in packed decimal format, left-justified
                   where hex a is digit 0 and 0 in this field is null, zero fill to a byte boundary. If "dnumber" is
                   zero then there will be NO "dest"/"d1-d15" field in message.

                                 ftype                 dest field represents
                     0 (intraflow to VDN)              vector number
                     4 (intraflow to split)            split
                     6 (intraflow to extension)        agent position
c                  call deflection flag, valid only when ftype=2.  When this bit is set it indicates that the BSR
                   or route-to number interflow was successful by means of call redirection through the public
                   network.
e                  ewt flag (If set, last two bytes are part of the message, only if ftype is 4. If not set, EWT is
                   understood by CMS to be null)
plv                priority (with vectoring):  If ftype is 4, and the call is directed to a split via a messaging
                   split, route to number, or adjunct routing, priorities pegged are: 1 = medium (no priority
                   was sent), 2 = high (a priority was sent).
ewt                expected wait time for the priority level specified in the plv field, 0-32767 seconds (with
                   vectoring)
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-187"></a>

## PDF page 187

Source: SPI-SYN24; PDF page 187; extracted characters: 1291.

```text
3.4.18.2                       DFWD23 (New CM6.0)


                                                                       Switch     Vect     Skill
                                                     First Release     CM6.0      y/n      y/n
                                                     Last Release      CM6.3



     7   6    5   4    3   2   1    0   7    6   5    4   3    2   1   0    7   6    5   4    3   2    1   0   7    6   5    4   3    2   1    0
                time_tag                           DFWD23                                                seq num
                              seq num (cont)                                             tot siz               a                itn
                itn (cont)              o      ftype        dnumber                                   dest or d1-d15
                  dest or d1-d15 (cont)                        / / / /        ptype      u    c   e     plv                 ewt/tp
              ewt/tp (cont)                 / / /                              prt                              /             net_id
              net_id (cont)                                             seq                                               timestamp
                                               timestamp (cont)
```

<a id="pdf-page-188"></a>

## PDF page 188

Source: SPI-SYN24; PDF page 188; extracted characters: 3726.

```text
DFWD23 (continued)

time_tag           seconds past minute when event occurred, 0-59
opcode             DFWD23 = 12 (0x0c)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
a                  ASAI adjunct routing; 1 = adjunct (re)routed call
itn                internal trunk number used to identify trunk facilities, 1-32766
o                  OCM call; 0 = no, 1 = call distributed by OCM
ftype              forwarding type

                     0    redirected (intraflow) to a VDN
                     1    interflow
                     2    lookahead interflow, BSR interflow, or Network Call Redirection
                     3    unknown destination
                     4    redirected (intraflow) to a split
                     5    redirected to another VDN by a Policy Routing Table (PRT) – the iln of the VDN the
                          call is routed to included in the dest field
                     6    redirected (intraflow) to an extension
                     7    redirected (intraflow) to an attendant position
dnumber            number of digits in "dest"/"d1-d15", 5 for ftype=0 and 5 for ftype=4 and 1-15 for
                   ftype=6(EAS)
                   0=call was forwarded to an unmeasured endpoint. In this case, no destination is sent.
dest/d1-d15        destination: with EAS "d1-d15" in packed decimal format, left-justified where hex a is digit
                   0 and 0 in this field is null, zero fill to a byte boundary. If "dnumber" is zero then there will
                   be NO "dest"/"d1-d15" field in message.

                                 ftype                             dest field represents
                     0 (intraflow to VDN)              vector number or zero if routing to PRT
                     4 (intraflow to split)            split
                     5 (PRT)                           VDN we are routing to
                     6 (intraflow to extension)        agent position
ptype                0      No PRT number included (i.e., ftype is not 5)
                     1      Percentage Allocation type PRT
                     2-7    Reserved for future use
c                  call deflection flag, valid only when ftype=2.  When this bit is set it indicates that the BSR
                   or route-to number interflow was successful by means of call redirection through the public
                   network.
e                  ewt/tp flag If set, ewt/tp two byte field is part of the message. If set when the ftype = 4. the
                   field contains ewt. If set when the ftype = 5, the field contains the target percentage (tp).
plv                priority (with vectoring):  If ftype is 4, and the call is directed to a split via a messaging
                   split, route to number, or adjunct routing, priorities pegged are: 1 = medium (no priority
                   was sent), 2 = high (a priority was sent).
ewt/tp             With ftype = 4, contains the expected wait time for the priority level specified in the plv
                   field, 0-32767 seconds. With ftype = 5, contains the tp (target percentage) 1-100 assigned
                   in the PRT table (in prt field) to the VDN in the dest field, R6 and later.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
prt                The number of the Policy Routing Table used to route the call to this subsequent VDN
                   range 1-8000 – set to all 0’s if no PRT number included
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-189"></a>

## PDF page 189

Source: SPI-SYN24; PDF page 189; extracted characters: 1316.

```text
3.4.18.3                        DFWD24 (New CM7.0)


                                                                        Switch     Vect     Skill
                                                      First Release     CM7.0      y/n      y/n
                                                      Last Release



     7   6    5   4    3   2    1   0    7   6    5   4    3   2    1   0    7    6   5    4   3    2   1    0   7    6   5    4   3    2   1    0
                time_tag                            DFWD24                                                seq num
                               seq num (cont)                                             tot siz                a             / / / / / / /
                                      itn                                    o      ftype           / / / /         / / /          dnumber
                                        dest or d1-d16                                              / / / /        ptype       u   c    e    plv
                                    ewt/tp                                      / / /                                prt
     /                                net_id                                                                 seq
                                                                     timestamp
```

<a id="pdf-page-190"></a>

## PDF page 190

Source: SPI-SYN24; PDF page 190; extracted characters: 3716.

```text
DFWD24 (continued)

time_tag           seconds past minute when event occurred, 0-59
opcode             DFWD24 = 71 (0x47)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
a                  ASAI adjunct routing; 1 = adjunct (re)routed call
itn                internal trunk number used to identify trunk facilities, 1-65535
o                  OCM call; 0 = no, 1 = call distributed by OCM
ftype              forwarding type

                    0    redirected (intraflow) to a VDN
                    1    interflow
                    2    lookahead interflow, BSR interflow, or Network Call Redirection
                    3    unknown destination
                    4    redirected (intraflow) to a split
                    5    redirected to another VDN by a Policy Routing Table (PRT) – the iln of the VDN the
                         call is routed to included in the dest field
                    6    redirected (intraflow) to an extension
                    7    redirected (intraflow) to an attendant position
dnumber            number of digits in "dest"/"d1-d16", 5 for ftype=0 and 5 for ftype=4 and 1-24 for
                   ftype=6(EAS)
                   0=call was forwarded to an unmeasured endpoint. In this case, no destination is sent.
dest/d1-d16        destination: with EAS "d1-d16" in packed decimal format, left-justified where hex a is
                   digit 0 and 0 in this field is null, zero fill to a byte boundary. If "dnumber" is zero then
                   there will be NO "dest"/"d1-d16" field in message.

                                 ftype                            dest field represents
                    0 (intraflow to VDN)               vector number or zero if routing to PRT
                    4 (intraflow to split)             split
                    5 (PRT)                            VDN we are routing to
                    6 (intraflow to extension)         agent position
ptype               0       No PRT number included (i.e., ftype is not 5)
                    1       Percentage Allocation type PRT
                    2-7     Reserved for future use
c                  call deflection flag, valid only when ftype=2.  When this bit is set it indicates that the BSR or
                   route-to number interflow was successful by means of call redirection through the public
                   network.
e                  ewt/tp flag If set, ewt/tp two byte field is part of the message. If set when the ftype = 4. the
                   field contains ewt. If set when the ftype = 5, the field contains the target percentage (tp).
plv                priority (with vectoring):  If ftype is 4, and the call is directed to a split via a messaging split,
                   route to number, or adjunct routing, priorities pegged are: 1 = medium (no priority was sent),
                   2 = high (a priority was sent).
ewt/tp             With ftype = 4, contains the expected wait time for the priority level specified in the plv field,
                   0-32767 seconds. With ftype = 5, contains the tp (target percentage) 1-100 assigned in the
                   PRT table (in prt field) to the VDN in the dest field, R6 and later.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
prt                The number of the Policy Routing Table used to route the call to this subsequent VDN
                   range 1-8000 – set to all 0’s if no PRT number included
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-191"></a>

## PDF page 191

Source: SPI-SYN24; PDF page 191; extracted characters: 2114.

```text
       3.4.19       MBUSY20 and MBUSY24
The MBUSY message is sent by the switch when a trunk is busied out.

3.4.19.1                   MBUSY20 (New CM3.1)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y/n    y/n
                                             Last Release    CM6.3



    7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                      MBUSY20                                         seq num
                          seq num (cont)                                      tot siz             /             itn
              itn (cont)

                    time_tag      seconds past minute when event occurred, 0-59
                    opcode        MBUSY20 = 223 (0xdf)
                    seq num       sequence number, 0-0xffff ffff
                    tot siz       total size in bytes, 1-255
                    itn           internal trunk number used to identify trunk facilities, 1-32766

3.4.19.2                   MBUSY24 (New CM7.0)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y/n    y/n
                                             Last Release



    7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                      MBUSY24                                         seq num
                          seq num (cont)                                      tot siz                          itn
              itn (cont)

                 time_tag      seconds past minute when event occurred, 0-59
                 opcode        MBUSY24 = 72 (0x48)
                 seq num       sequence number, 0-0xffff ffff
                 tot siz       total size in bytes, 1-255
                 itn           internal trunk number used to identify trunk facilities, 1-65535
```

<a id="pdf-page-192"></a>

## PDF page 192

Source: SPI-SYN24; PDF page 192; extracted characters: 3148.

```text
       3.4.20       FBUSY20 and FBUSY24
The FBUSY message is sent by the switch when a facility receives forced busy.

3.4.20.1                    FBUSY20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0
              time_tag                       FBUSY20                                         seq num
                           seq num (cont)                                      tot siz             u              itn
              itn (cont)            /                            net_id                                        seq
             seq (cont)                                                     timestamp
          timestamp (cont

           time_tag        seconds past minute when event occurred, 0-59
           opcode          FBUSY20 = 224 (0xe0)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-32766
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID

3.4.20.2                    FBUSY24 (New CM7.0)


                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0
              time_tag                       FBUSY24                                         seq num
                           seq num (cont)                                      tot siz             u           / / / / / / /
                                 itn                               /                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          FBUSY24 = 73 (0x49)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-65535
           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-193"></a>

## PDF page 193

Source: SPI-SYN24; PDF page 193; extracted characters: 3336.

```text
       3.4.21       VSTART20 and VSTART24
The VSTART message is sent by the switch when a facility starts vector processing.

3.4.21.1                   VSTART20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0
              time_tag                      VSTART20                                         seq num
                           seq num (cont)                                     tot siz             u              itn
              itn (cont)              / / /                         vector                        /            net_id
            net_id (cont)                                       seq                                        timestamp
                                         timestamp (cont)

     time_tag        seconds past minute when event occurred, 0-59
     opcode          VSTART20 = 225 (0xe1)
     seq             sequence number, 0-0xffff ffff
     tot siz         total size in bytes, 1-255
     u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
     itn             internal trunk number used to identify trunk facilities, 1-32766
     vector          vector number, 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
     net_id          network entity identifier, 1-32767
     seq             call sequence number, 0-65535
     timestamp       unix style (seconds since 1/1/70) time call assigned a UCID


3.4.21.2                   VSTART24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y      y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                      VSTART24                                         seq num
                           seq num (cont)                                     tot siz             u           / / / / / / /
                                 itn                                  / / /                         vector
    /                            net_id                                                        seq
                                                            timestamp

     time_tag        seconds past minute when event occurred, 0-59
     opcode          VSTART24 = 74 (0x4a)
     seq             sequence number, 0-0xffff ffff
     tot siz         total size in bytes, 1-255
     u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
     itn             internal trunk number used to identify trunk facilities, 1-65535
     vector          vector number, 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
     net_id          network entity identifier, 1-32767
     seq             call sequence number, 0-65535
     timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-194"></a>

## PDF page 194

Source: SPI-SYN24; PDF page 194; extracted characters: 3324.

```text
       3.4.22       VSTOP20 and VSTOP24
The VSTOP message is sent by the switch when a facility stops vector processing.

3.4.22.1                   VSTOP20 (New CM3.1)


                                                               Switch   Vect    Skill
                                              First Release    CM3.1    y       y/n
                                              Last Release     CM6.3



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       VSTOP20                                        seq num
                           seq num (cont)                                     tot siz             u              itn
              itn (cont)              / / /                         vector                        /            net_id
            net_id (cont)                                       seq                                        timestamp
                                         timestamp (cont)

     time_tag        seconds past minute when event occurred, 0-59
     opcode          VSTOP20 = 226 (0xe2)
     seq_num         sequence number, 0-0xffff ffff
     tot siz         total size in bytes, 1-255
     u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
     itn             internal trunk number used to identify trunk facilities, 1-32766
     vector          vector number, 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
     net_id          network entity identifier, 1-32767
     seq             call sequence number, 0-65535
     timestamp       unix style (seconds since 1/1/70) time call assigned a UCID

3.4.22.2                   VSTOP24 (New CM7.0)


                                                               Switch   Vect    Skill
                                              First Release    CM7.0    y       y/n
                                              Last Release



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0
              time_tag                       VSTOP24                                        seq num
                           seq num (cont)                                     tot siz             u           / / / / / / /
                                 itn                                  / / /                         vector
    /                            net_id                                                        seq
                                                            timestamp

     time_tag        seconds past minute when event occurred, 0-59
     opcode          VSTOP24 = 75 (0x4b)
     seq_num         sequence number, 0-0xffff ffff
     tot siz         total size in bytes, 1-255
     u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
     itn             internal trunk number used to identify trunk facilities, 1-65535
     vector          vector number, 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
     net_id          network entity identifier, 1-32767
     seq             call sequence number, 0-65535
     timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-195"></a>

## PDF page 195

Source: SPI-SYN24; PDF page 195; extracted characters: 2156.

```text
       3.4.23       FDISC20 and FDISC24
The FDISC20 message is sent by the switch when a facility receives a forced disconnect. Forced
disconnects may happen as a result of a "fdisc" vector step, a vector timeout event, or a "reply best"
vector step. This message provides the reporting adjunct the ability to associate a vector, VDN, and trunk
by the itn in this message and the DNEVENT and VSTART messages.

3.4.23.1                   FDISC20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release    CM6.3

    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                       FDISC20                                         seq num
                           seq num (cont)                                     tot siz             u              itn
              itn (cont)                / / / /        dtype       /                            net_id
                                seq                                                         timestamp
                          timestamp (cont)

           time_tag        seconds past minute when event occurred, 0-59
           opcode          FDISC20 = 227 (0xe3)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-32766
           dtype           type of disconnect

                            0    disconnect vector step executed
                            1    vector timeout
                            2    reply best vector step executed

           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-196"></a>

## PDF page 196

Source: SPI-SYN24; PDF page 196; extracted characters: 1799.

```text
3.4.23.2                    FDISC24 (New CM7.0)


                                                                Switch    Vect   Skill
                                               First Release    CM7.0     y      y/n
                                               Last Release

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        FDISC24                                         seq num
                           seq num (cont)                                      tot siz              u           / / / / / / /
                                 itn                                    / / / /         dtype       /            net_id
            net_id (cont)                                        seq                                         timestamp
                                             timestamp

           time_tag        seconds past minute when event occurred, 0-59
           opcode          FDISC24 = 76 (0x4c)
           seq num         sequence number, 0-0xffff ffff
           tot siz         total size in bytes, 1-255
           u               flag indicating that the UCID fields (net_id, seq and timestamp) are present
           itn             internal trunk number used to identify trunk facilities, 1-65535
           dtype           type of disconnect

                             0    disconnect vector step executed
                             1    vector timeout
                             2    reply best vector step executed

           net_id          network entity identifier, 1-32767
           seq             call sequence number, 0-65535
           timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-197"></a>

## PDF page 197

Source: SPI-SYN24; PDF page 197; extracted characters: 2061.

```text
       3.4.24       HOLD20 and HOLD24
The HOLD message is sent by the switch when a facility is put on "hold" by an agent. This is a variable
length message based on "pnumber".

3.4.24.1                    HOLD20 (New CM3.1)


                                                                Switch    Vect   Skill
                                               First Release    CM3.1     y/n    y/n
                                               Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                        HOLD20                                          seq num
                           seq num (cont)                                      tot siz              u              itn
              itn (cont)              pnumber                              pos (non-EAS) or p1-p15 (EAS
        pos or p1-p15 (cont)        /                            net_id                                         seq
              seq (cont)                                                     timestamp
          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            HOLD20 = 228 (0xe4)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-32766
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-198"></a>

## PDF page 198

Source: SPI-SYN24; PDF page 198; extracted characters: 2032.

```text
3.4.24.2                    HOLD24 (New CM7.0)



                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        HOLD24                                         seq num
                           seq num (cont)                                      tot siz             u           / / / / / / /
                                 itn                                  / / /        pnumber               pos (non-EAS) or
                                                                                                          p1-p16 (EAS)
                pos or p1-p16 (cont)                    / / / /     /                           net_id
                                seq                                                         timestamp
                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            HOLD24 = 77 (0x4d)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-65535
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                  in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                  null, zero fill to a byte boundary
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-199"></a>

## PDF page 199

Source: SPI-SYN24; PDF page 199; extracted characters: 2632.

```text
       3.4.25       RECON20, RECON23 and RECON24
The RECON message is sent by the switch when a facility is reconnected after being put on "hold" by an
agent. This is a variable length message based on "pnumber" and the "s" and "u" bits. The "s" bit is only
set for EAS and only when reconnecting to a call for a CMS measured skill. When the "s" bit is set, the
message will contain one additional byte for the "skill" field.  Without EAS the first 2 bits of the "skill" field
are set to 0. The message may optionally contain the UCID.

3.4.25.1                    RECON20 (New CM3.1)


                                                                Switch    Vect    Skill
                                               First Release    CM3.1     y/n     y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       RECON20                                          seq num
                           seq num (cont)                                       tot siz             u              itn
              itn (cont)              pnumber                              pos (non-EAS) or p1-p15 (EAS
        pos or p1-p15 (cont)        s       / / / /                        skill                    /            net_id
            net_id (cont)                                        seq                                         timestamp
                                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            RECON20 = 229 (0xe5)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-32766
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
s                 0 = no skill in message, 1 = skill in message
skill             skill matched 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-200"></a>

## PDF page 200

Source: SPI-SYN24; PDF page 200; extracted characters: 2058.

```text
3.4.25.2                    RECON23 (New CM6.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM6.0     y/n     y/n
                                                Last Release     CM6.3



    7   6   5   4   3    2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        RECON23                                          seq num
                           seq num (cont)                                       tot siz              u               itn
              itn (cont)               pnumber                              pos (non-EAS) or p1-p15 (EAS
        pos or p1-p15 (cont)         s    / /                          skill                         /             net_id
            net_id (cont)                                         seq                                          timestamp
                                           timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            RECON23 = 30 (0x1e)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
itn               internal trunk number used to identify trunk facilities, 1-32766
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
s                 0 = no skill in message, 1 = skill in message
skill             skill matched 1-8000
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```
