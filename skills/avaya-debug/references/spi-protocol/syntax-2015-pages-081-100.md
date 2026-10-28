---
title: "SPI-SYN24 - complete source pages 81-100"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 81-100

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-081"></a>

## PDF page 81

Source: SPI-SYN24; PDF page 81; extracted characters: 1927.

```text
opcode             SKILLADD24 = 64 (0x40)
tag                message tag, 0-255 (it will be returned in the switch response message)
pnumber            number of digits in agent position, 1-16
p1-p16             agent position - EAS login ID in packed decimal format, left-justified where hex a is
                   digit 0 and 0 in this field is null, zero fill to a byte boundary.
ch                 agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so                 service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                   handling preference is skill level or greatest need.
da                 direct agent calls handled first: 0 = no, 1 = yes. This option is only used when agent call
                   handling preference is percent allocation.
e                  end bit, set when this is the last message of the set needed to satisfy the request
da_skill           agent's direct-agent skill (must be one of agent's 120 skills or zero which indicates no DA
                   skill)
percent1-60        Percent allocation to apply to this skill, (0-100).  Used only when the call handling
                   preference is percent allocation and the level is not reserve (r bit is not set for the skill).
r1-60              flag indicating if the level for this skill is reserve: 0 = not in reserve (regular agent), 1 =
                   reserve
level1-60          skill level (1-16) or reserve level (1-2)
skill1-60          skill number, 0-8000
ia1-60             field that indicates whether the corresponding skill is interruptible. This field is only valid
                   when the corresponding “rx” (reserve) field is 0.

                     0    not an interruptible skill
                     1    auto-in-interrupt
                     2    manual-in-interrupt
                     3    notify-interrupt
```

<a id="pdf-page-082"></a>

## PDF page 82

Source: SPI-SYN24; PDF page 82; extracted characters: 2765.

```text
       3.3.14       TGMOVE20 and TGMOVE23
The Trunk Group-Split Move message is sent by the switch whenever a trunk group is removed from
and/or added to another split. The move request will have originated from a switch administration
procedure. When a trunk group is removed from a split or added to an unmeasured split, the switch will
send a TGMOVE split=0 message. The reporting adjunct will update the split assignment for the specified
trunk group.

3.3.14.1                   TGMOVE20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM5.2

     7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                      TGMOVE20                                         seq num
                           seq num (cont)                                     tot siz                   / / / / /        skill
              skill (cont)               / / / / /                       tkgrp

time_tag     seconds past minute when event occurred, 0-59
opcode       TGMOVE20 = 195 (0xc3)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
skill        skill number, 0-999 (G3V8-G3V11), 0-2000 (MV2 and later)
             (0 indicates that the trunk group is not assigned to a skill or is assigned to an unmeasured
             skill)
tkgrp        trunk group number, 1-666 (G3V8-G3V10), 0-2000 (G3V11 and later)


3.3.14.2                   TGMOVE23 (New CM6.0)


                                                               Switch    Vect   Skill
                                               First Release   CM6.0     y/n    y/n
                                               Last Release

     7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                      TGMOVE23                                         seq num
                           seq num (cont)                                     tot siz                / / /           skill
              skill (cont)               / / / / /                       tkgrp

time_tag     seconds past minute when event occurred, 0-59
opcode       TGMOVE23 = 22 (0x16)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
skill        skill number, 0-8000 (CM6.0 and later)
             (0 indicates that the trunk group is not assigned to a skill or is assigned to an unmeasured
             skill)
tkgrp        trunk group number, 0-2000 (G3V11 and later)
```

<a id="pdf-page-083"></a>

## PDF page 83

Source: SPI-SYN24; PDF page 83; extracted characters: 1521.

```text
       3.3.15      VTGMOVE20 (New CM3.1)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y      y/n
                                             Last Release

The Trunk Group-VDN Move message is sent by the switch when Call Vectoring is enabled and a trunk
group is removed from and/or moved to a new VDN. The move request will have originated from a switch
administration procedure. When a trunk group is removed from a VDN or added to an unmeasured VDN,
the switch will send a VTGMOVE iln=0 message. The reporting adjunct will update the VDN assignment
for the specified trunk group.

    7   6   5   4   3  2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3  2   1   0   7   6  5   4   3   2   1   0
              time_tag                    VTGMOVE20                                       seq num
                          seq num (cont)                                    tot siz             /              iln
              iln (cont)                / / / / /                      tkgrp

time_tag     seconds past minute when event occurred, 0-59
opcode       VTGMOVE20 = 196 (0xc4)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
iln          internal line number, 0-32766 (0 indicates that the trunk group is not assigned to a VDN or is
             assigned to an unmeasured VDN)
tkgrp        trunk group number, 1-666 (G3V8-G3V10), 0-2000 (G3V11 and later)
```

<a id="pdf-page-084"></a>

## PDF page 84

Source: SPI-SYN24; PDF page 84; extracted characters: 2695.

```text
       3.3.16       VDNMOVE20, VDNMOVE23 and VDNMOVE24
A VDN-Vector Move message is sent by the switch when the administration information for a VDN is
changed. This information will always include the vector. Other information may include, depending on
switch type and feature set, the assigned vector, the VDN skill preferences (with EAS), and the BSR plan
number associated with the VDN. The move request may have originated from the reporting adjunct
(MVVDN or CHGVDNSK messages) or from a switch administration procedure.

VDNs are referenced by internal line numbers.

When a VDN is removed from a vector, the switch will send a VDNMOVE message.

This is a variable-length message based on the "s" bit. The first 7 bytes are always sent. If the "s" bit is
set then 5 additional bytes are sent for the "primary-skill", "secondary-skill" and "tertiary-skill".

3.3.16.1                   VDNMOVE20 (New CM3.1)


                                                              Switch    Vect    Skill
                                              First Release   CM3.1     y       y
                                              Last Release    CM5.2



    7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0
              time_tag                     VDNMOVE20                                        seq num
                          seq num (cont)                                      tot siz            s              iln
              iln (cont)            /                       vector                                      bsr plan
          / / / / /                   primary skill                /               secondary skill               /    ter skl
          tertiary skill (cont)

time_tag            seconds past minute when event occurred, 0-59
opcode              VDNMOVE20 = 197 (0xc5)
seq num             sequence number, 0-0xffff ffff
tot siz             total size in bytes, 1-255
s                   skill flag, 0 = no skills in message, 1 = skills in message
iln                 internal line number (1-32766)
vector              vector number, 1-999 (G3V8-CM2), 1-2000 (CM3 and later)
bsr plan            bsr application plan number, 1-255 (G3V8-G3V10), 1-512 (G3V11 and later)
primary skill       when s = 1, primary VDN agent skill 1-999 (G3V8-G3V11), 1-2000 (MV2 and later), 0 =
                    no skill used
secondary           when s = 1, secondary VDN agent skill 1-999 (G3V8-G3V11), 1-2000 (MV2 and later), 0
skill               = no skill used
tertiary skill      when s = 1, tertiary VDN agent skill 1-999 (G3V8-G3V11), 1-2000 (MV2 and later), 0 =
                    no skill used
```

<a id="pdf-page-085"></a>

## PDF page 85

Source: SPI-SYN24; PDF page 85; extracted characters: 3569.

```text
3.3.16.2                    VDNMOVE23 (New CM6.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM6.0     y       y
                                                Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                     VDNMOVE23                                          seq num
                           seq num (cont)                                       tot siz              s              iln
               iln (cont)            /                        vector                                       bsr plan
       / / /                       primary skill                        / / /                     secondary skill
       / / /                       tertiary skill

time_tag              seconds past minute when event occurred, 0-59
opcode                VDNMOVE23 = 24 (0x18)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
s                     skill flag, 0 = no skills in message, 1 = skills in message
iln                   internal line number (1-32766)
vector                vector number, 1-8000 (CM6.0 and later)
bsr plan              bsr application plan number, 1-255 (G3V8-G3V10), 1-512 (G3V11 and later)
primary skill         when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary skill       when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
tertiary skill        when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used


3.3.16.3                    VDNMOVE24 (New CM7.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM7.0     y       y
                                                Last Release



    7    6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                     VDNMOVE24                                          seq num
                           seq num (cont)                                       tot siz              s               iln
               iln (cont)            /                        vector                                        bsr plan
           / / / / / /                      tenant                      / / /                       primary skill
       / / /                      secondary skill                       / / /                       tertiary skill

time_tag              seconds past minute when event occurred, 0-59
opcode                VDNMOVE24 = 56 (0x38)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
s                     skill flag, 0 = no skills in message, 1 = skills in message
iln                   internal line number (1-32766)
vector                vector number, 1-8000 (CM6.0 and later)
bsr plan              bsr application plan number, 1-512
tenant                VDN tenant number, 1-250
primary skill         when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary skill       when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
tertiary skill        when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
```

<a id="pdf-page-086"></a>

## PDF page 86

Source: SPI-SYN24; PDF page 86; extracted characters: 2781.

```text
       3.3.17        MVVDN9 and MVVDN23
The Move VDN message is a variable-length message based on "number" sent by the reporting adjunct.
The first seven bytes are always sent.  It is a request to change the vector termination of one or more (up
to 32) VDNs. VDNs are referenced by internal line numbers. The switch will attempt to reassign each
VDN and report the results back to the reporting adjunct. For each VDN that is successfully moved, the
switch will send one VDNMOVE (or equivalent) message so that the reporting adjunct can update the
real-time database. Lastly, the switch sends a MVRCODE message that specifies which VDN(s) were
successfully moved and which were not.

3.3.17.1                   MVVDN9 (New CM3)


                                                              Switch    Vect   Skill
                                              First Release   CM3       y      y/n
                                              Last Release    CM5.2



    7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0
              MVVDN9                            tag                  / / /                        vector
      / /         number           /                             iln1                            /             iln2
             iln2 (cont)
                                                               .  .  .
     /                            ilnN

opcode      MVVDN9 = 47 (0x2f)
tag         message tag, 0-255 (it will be returned in the switch response message)
vector      vector number, 1-999 (G3V8-CM2), 1-2000 (CM3 and later)
number      number of VDNs (N) in move request, 1-32
iln1-N      list of N internal line numbers, 1-32766


3.3.17.2                   MVVDN23 (New CM6.0)


                                                              Switch    Vect   Skill
                                              First Release   CM6.0     y      y/n
                                              Last Release



    7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0
             MVVDN23                            tag                  / / /                        vector
      / /         number           /                             iln1                            /             iln2
             iln2 (cont)
                                                               .  .  .
     /                            ilnN

opcode      MVVDN23 = 60 (0x3c)
tag         message tag, 0-255 (it will be returned in the switch response message)
vector      vector number, 1-8000 (CM6.0 and later)
number      number of VDNs (N) in move request, 1-32
iln1-N      list of N internal line numbers, 1-32766
```

<a id="pdf-page-087"></a>

## PDF page 87

Source: SPI-SYN24; PDF page 87; extracted characters: 3230.

```text
       3.3.18       CHGVDNSK8 and CHGVDNSK23
The Change VDN's skills message is sent by the reporting adjunct to request a VDN's skills be changed
for up to 32 VDNs.  All three of the VDN's skills are always included, zero will indicate no skills are
assigned. The switch sends VDNMOVE (or equivalent) messages and then a MVRCODE message that
specifies which VDNs were successfully changed.

This is a variable length message based on the "number" of VDNs sent.

3.3.18.1                    CHGVDNSK8 (New MV2)


                                                                Switch    Vect    Skill
                                               First Release    MV2       y       y
                                               Last Release     CM5.2

     7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
            CHGVDNSK8                            tag                  / /          number                 / / / / /       1st skl
            1st skill (cont)        /                    2nd skill                  /                    3rd skill
     /                             iln1                             /                              iln2
                                                                 .  .  .
     /                            ilnN-1                            /                              ilnN

opcode              CHGVDNSK8 = 46 (0x2e)
tag                 message tag, 0-255 (it will be returned in the switch response message)
number              number of VDNs (N) in change request, (1-32)
1st, 2nd, 3rd       skill associated with the VDN skill, 1-999 (G3V8-G3V11), 1-2000 (MV2 and later),
skill               measured or unmeasured
iln1-N              list of N internal line number (1-32767)

3.3.18.2                    CHGVDNSK23 (New CM6.0)


                                                                Switch    Vect    Skill
                                               First Release    CM6.0     y       y
                                               Last Release

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
           CHGVDNSK23                            tag                  / /          number              / / /         1st skill
            1st skill (cont)           / / /                         2nd skill                         / / /         3rd skill
            3rd skill (cont)        /                              iln1                             /              iln2
              iln2 (cont)           /                              iln3                             /              iln4
                                                                 .  .  .
             ilnN-1 (cont)          /                              ilnN

opcode               CHGVDNSK23 = 58 (0x3a)
tag                  message tag, 0-255 (it will be returned in the switch response message)
number               number of VDNs (N) in change request, (1-32)
1st, 2nd, 3rd skill  skill associated with the VDN skill, 1-8000, measured or unmeasured
iln1-N               list of N internal line number (1-32767)
```

<a id="pdf-page-088"></a>

## PDF page 88

Source: SPI-SYN24; PDF page 88; extracted characters: 1063.

```text
       3.3.19       VPARMS
The Request Vector Parameters message is sent by the reporting adjunct. It is a request for the vector
steps of the specified vector. The expected response is a VECTOR message.

For CM6.0 and later, if the requested vector contains a check step with a preference level other than “all-
levels” and the SPI language is prior to 23, the request will be denied (rcode=43).

                                                              Switch    Vect   Skill
                                              First Release   G3V1      y      y/n
                                              Last Release

    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0
              VPARMS                            tag                  / / /                        vector

opcode      VPARMS = 21 (0x15)
tag         message tag, 0-255 (it will be returned in the switch response message)
vector      vector number, 1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later)
```

<a id="pdf-page-089"></a>

## PDF page 89

Source: SPI-SYN24; PDF page 89; extracted characters: 431.

```text
       3.3.20      VECTOR20 and VECTOR24
The VECTOR message is sent by the switch in response to a VPARMS message.  This is a variable-
length message based on the "steps" field. The first 9 bytes are always sent and will be the same for all
messages sent for a single vector. Multiple messages will be sent for large vectors.

Vectors can have 99 steps per vector. The number of steps sent per message varies based on the
message.
```

<a id="pdf-page-090"></a>

## PDF page 90

Source: SPI-SYN24; PDF page 90; extracted characters: 4624.

```text
3.3.20.1                     VECTOR20 (New CM3.1)
Each vector step in VECTOR20 must be 24 bytes. The switch will send 9 steps per message, with up to
11 messages to send all 99 steps.

                                                                   Switch     Vect    Skill
                                                  First Release    CM3.1      y       y/n
                                                  Last Release     CM6.3

     7   6   5   4    3   2   1   0   7   6    5   4   3   2   1   0    7   6   5   4   3    2   1   0   7   6   5    4   3   2   1   0
               time_tag                        VECTOR20                                            seq num
                             seq num (cont)                                         tot siz                            tag
     m             steps
                                                                    .  .  .

          stype1          pri/c   c                    -                          cond                     threshold or table
                           ov
     s      sday or            shour                   smin             /     eday          ehour or type        emin or subtype
             comp
                                  dest                                            step-num                            var_t
      v_t                    var_c                                        -                                         -
              d1-d3 or s_num or type_val                    d4               d5               d6              d7               d8
          d9              d10              d11              d12             d13              d14              d15              d16
                                                                    .  .  .

          stypeN          pri/c   c                    -                          cond                     threshold or table
                           ov
     s      sday or            shour                   smin             /     eday          ehour or type        emin or subtype
             comp
                                  dest                                            step-num                            var_t
      v_t                    var_c                                        -                                         -
             d1-d3 or s_num or type_val                     d4               d5               d6              d7               d8
          d9              d10              d11             d12              d13              d14              d15             d16


time_tag        seconds past minute when event occurred, 0-59
opcode          VECTOR20 = 198 (0xc6)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
tag             message tag, 0-255 (it will be returned in the switch response message)
m               m=1, more steps for this vector will be sent in a subsequent vector, m=0, this is the last
                message for this vector
steps           number of steps (N) 0-9. This is the number of steps in this message.
stype1-N        step type for steps 1-N (see section 3.3.21)

                  stype    description                 stype      description                stype        description
                  1        queue-to                    11         collect digits             21           return (CM 3.0)
                  2        check                       12         route-to digits            22           set (CM3.0)
                  3        route-to number             13         messaging skill            23           unused
                  4        announcement                14         adjunct route              24           unused
                  5        wait                        15         converse-on split          25           unused
                  6        goto step (obsolete)        16         send digits (not           26           unused
                                                                  supported)
                  7        disconnect                  17         goto step                  27           unused
                  8        busy                        18         goto vector                28           unused
                  9        stop                        19         consider                   29           unused
                  10       goto vector (obsolete)      20         reply-best                 30           unused
                                                                                             31           unused
```

<a id="pdf-page-091"></a>

## PDF page 91

Source: SPI-SYN24; PDF page 91; extracted characters: 4855.

```text
3.3.20.2                     VECTOR24 (New CM7.0)
Each vector step in VECTOR24 must be 28 bytes. The switch will send 8 steps per message, with up to
11 messages to send all 99 steps.


                                                                   Switch     Vect    Skill
                                                  First Release    CM7.0      y       y/n
                                                  Last Release

     7   6   5   4   3    2   1   0   7   6   5    4   3   2   1   0   7    6   5   4   3   2    1   0   7   6   5   4    3   2   1   0
               time_tag                        VECTOR24                                            seq num
                             seq num (cont)                                        tot siz                            tag
     m             steps
                                                                    .  .  .

          stype1          pri/c   c                    -                          cond                     threshold or table
                           ov
     s      sday or            shour                   smin             /     eday          ehour or type        emin or subtype
             comp
                                  dest                                            step-num                           var_t
      v_t                    var_c                                        -                                        -
              d1-d3 or s_num or type_val                    d4               d5               d6              d7               d8
          d9              d10              d11              d12             d13              d14              d15             d16
          d17             d18              d19              d20             d21              d22              d23             d24
                                                                    .  .  .

          stypeN          pri/c   c                    -                          cond                     threshold or table
                           ov
     s      sday or            shour                   smin             /     eday          ehour or type        emin or subtype
             comp
                                  dest                                            step-num                           var_t
      v_t                    var_c                                        -                                        -
              d1-d3 or s_num or type_val                    d4               d5               d6              d7               d8
          d9              d10              d11              d12             d13              d14              d15             d16
          d17             d18              d19              d20             d21              d22              d23             d24

time_tag        seconds past minute when event occurred, 0-59
opcode          VECTOR24 = 82 (0x52)
seq num         sequence number, 0-0xffff ffff
tot siz         total size in bytes, 1-255
tag             message tag, 0-255 (it will be returned in the switch response message)
m               m=1, more steps for this vector will be sent in a subsequent vector, m=0, this is the last
                message for this vector
steps           number of steps (N) 0-8. This is the number of steps in this message.
stype1-N        step type for steps 1-N (see section 3.3.21)

                  stype    description                 stype      description                stype       description
                  1        queue-to                    11         collect digits             21          return (CM 3.0)
                  2        check                       12         route-to digits            22          set (CM3.0)
                  3        route-to number             13         messaging skill            23          unused
                  4        announcement                14         adjunct route              24          unused
                  5        wait                        15         converse-on split          25          unused
                  6        goto step (obsolete)        16         send digits (not           26          unused
                                                                  supported)
                  7        disconnect                  17         goto step                  27          unused
                  8        busy                        18         goto vector                28          unused
                  9        stop                        19         consider                   29          unused
                  10       goto vector (obsolete)      20         reply-best                 30          unused
                                                                                             31          unused
```

<a id="pdf-page-092"></a>

## PDF page 92

Source: SPI-SYN24; PDF page 92; extracted characters: 1816.

```text
       3.3.21      Vector Steps
The following steps are common to both VECTOR (section 3.3.20) and CHGVEC (section 3.3.22)
messages.

In all of the following descriptions, 28 bytes are shown.
For SPI language < 24, the last 4 bytes are NOT present.

3.3.21.1                   Queue to


   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0
        stype-1         pri   c                   -                          -
   s         -            dest_type                 -            -       -                -                      -
                               dest                                            -                              -
     -                       -                          -              -               -              -              -
                         -                              -              -               -              -              -
         -               -              -               -              -              -               -              -
         -               -              -               -              -              -               -              -

stype-1       queue-to
pri           0=low, 1=medium, 2=high, 3=top
c             1=this step is commented out
dest          destination

                dest_type      s      destination value
                0              0      1-999 (G3V8-G3V11), 1-2000 (MV2- CM5.2), 1-8000 (CM6.0 and later)
                0              1      VDN skill preference 1, 2, or 3 (valid only for EAS)
                1              N/A    N/A
s             0=specific skill (if dest_type=0), 1=VDN skill preference (valid only for EAS, and if
              dest_type=0).
dest_type     0=skill number or VDN skill preference, 1=best.
```

<a id="pdf-page-093"></a>

## PDF page 93

Source: SPI-SYN24; PDF page 93; extracted characters: 1153.

```text
3.3.21.2                        Check

     7    6   5    4   3    2   1    0   7    6   5    4   3    2   1    0   7    6   5    4   3    2   1    0   7    6    5   4    3   2    1   0
          stype-2            pri     c          -                   -                    cond                           threshold
     s         cmp              dest_type                     -              -                         slevel1                    slevel2
                                     dest                                           -                 -                 -                 -
                                       -                                            -                 -                 -                 -
            -                 -                 -                 -                 -                 -                 -                 -
           d9               d10               d11               d12                 -                 -                 -                 -
            -                 -                 -                 -                 -                 -                 -                 -
```

<a id="pdf-page-094"></a>

## PDF page 94

Source: SPI-SYN24; PDF page 94; extracted characters: 3058.

```text
stype-2                   check
pri                       0=low, 1=medium, 2=high, 3=top
c                         1=this step is commented out
slevel1                   the preferred level (for pref-level) or the start of the range (for pref-range). Only used
                          in Call Center 6.0 or later with SPI language 23 or greater.
                           Skill Level Preference        Skill Level 1 (slevel1)
                           all-levels                    0
                           pref-level                    1-16
                           pref-range                    1-16
slevel2                   the end of the range (for pref-range). Only used in Call Center 6.0 or later with SPI
                          language 23 or greater.
                           Skill Level Preference        Skill Level 2 (slevel2)
                           all-levels                    0
                           pref-level                    0
                           pref-range                    1-16
dest                      destination value.  split or skill 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000
                          (CM6.0 and later). For s=1, skill = 1, 2, or 3
                           dest_type      s      destination value
                           0              0      1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000 (CM6.0
                                                 and later)
                           0              1      N/A
                           1              N/A    N/A
cond/threshold,            Conditions               Comparato        Threshold
and cmp                                             r
                           0- unconditional         N/A              N/A
                           1- avail agents          1  >             0-998(G3V6,G3V7) [for G3V8+, see d9-d12]
                           3- staffed agents        1  >             0-998(G3V6,G3V7) [for G3V8+, see d9-d12]
                           6- calls queued          2  <             1-999
                           8- oldest call           2  <             1-999
                           11- ASA                  2  <             1-999
                           12- EWT                  2  <             [see d9-d12]
                           16- wait-improved        1  >             [see d9-d12]
s                         0=specific skill, 1=VDN skill preference (EAS only, and if dest_type=0)
cmp                        Comparator
                           s
                           1        >
                           2        <
dest_type                 0=split, 1=best.
d9-d12                     Condition               Threshold
                           1-avail agents          Agent threshold (0-1500) G3V8 and later
                           3-staffed agents        Agent threshold (0-1500) G3V8 and later
                           12-EWT                  Expected wait time, in seconds (1-9999)
                           16-wait-improved        Wait-improved (0-9999)
```

<a id="pdf-page-095"></a>

## PDF page 95

Source: SPI-SYN24; PDF page 95; extracted characters: 2490.

```text
3.3.21.3                    Route To Number

Variant 1:

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0
         stype-3         cov    c                   -                         cond                       threshold
    -        cmp               var                    -             -       -                -                       -
          -               -               -               -               -               -              -               -
          -               -               -               -               -               -              -               -
         d1              d2              d3              d4              d5              d6             d7              d8
         d9              d10            d11             d12             d13             d14             d15             d16
         d17             d18            d19             d20             d21             d22             d23             d24

Variant 2:

    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
         stype-3         cov    c                   -                                                    threshold
     -       cmp                -                     -             -       -                 -                      -
                                  -                                               -                            var_t
     v_t                      -                           -               -               -              -               -
          d1             d2              d3              d4              d5              d6              d7             d8
          d9             d10             d11            d12             d13             d14             d15             d16
         d17             d18             d19            d20             d21             d22             d23             d24


Variant 1 is used when the route to number:
    does not contain a variable (< SPI language 20)
    does contain a variable
               o    IF the route to number is ~r (< SPI language 20)

Variant 2 is used when:
    does not contain a variable (>= SPI language 20)
    does contain a variable (>= SPI language 23)
    does contain a variable (> SPI language 20 AND < SPI language 23) IF
               o    the route to number is ~r (>= SPI language 20)
```

<a id="pdf-page-096"></a>

## PDF page 96

Source: SPI-SYN24; PDF page 96; extracted characters: 2119.

```text
stype-3             route-to number
cov                 with coverage, 0=no, 1=yes
c                   1=this step is commented out
cond/threshold        Condition                 Threshold
                       0    unconditional       N/A
                      10    digits              0-9, hex c = #
                      17    interflow-qpos      1-9
cmp                 for condition 10 or 17

                      Comparator        Comparator
                      s                 s
                      1  >              4  <>
                      2  <              5  >=
                      3  =              6  <=
var                 Variable: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5
                    Used in message variant 1 (prior to SPI language 20).
var_t/v_t           Variable: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5, 34-37 for VDN
                    variables V6-V9, 101-776 for variables AA-ZZ
                    Used in message variant 2 (starting with SPI language 20).
d1-d16 (<           Digits to route to (encoded in hex).
language24)          (if have ~r in d1-d2 then may optionally have "var")

d1-d24 (>=          The hex 0, representing null, is used when digits = "none".
language24)
                      hex    char    hex     char
                      0      null    7       7
                      1      1       8       8
                      2      2       9       9
                      3      3       a       0
                      4      4       b       *
                      5      5       c       #
                      6      6

                      hex    char    meaning
                      e0     +       used with ~r to indicate E.164 phone number for SIP NCR
                      e1     ~p      pause 1.5 seconds
                      e2     ~w      wait for dial tone
                      e3     ~m      mark
                      e4     ~s      suppress display
                      e5     ~W      wait indefinitely
                      e6     ~r      redirection via NCR (allowed in d1,d2 only) [for G3V8.3 or later]
```

<a id="pdf-page-097"></a>

## PDF page 97

Source: SPI-SYN24; PDF page 97; extracted characters: 2987.

```text
3.3.21.4                   Announcement


    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0
         stype-4          -    c                   -                          -                            -
    -         -                -                var_annc          -       -                -                      -
          -               -              -              -               -              -               -              -
          -               -              -              -               -              -               -              -
         d1              d2             d3              d4             d5             d6              d7             d8
         d9             d10             d11            d12            d13             d14            d15             d16
          -               -              -              -               -              -               -              -

stype-4                          announcement
c                                1=this step is commented out
var_annc                         Variable announcement: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5
                                 (if "var" is set then d1-d15 must all be hex 0) (CM 3.0 and later)
d1-d15 (< language 24)           Announcement extension (packed decimal where 0= null and hex a is
                                 digit 0)
d1-d16 (>= language              If present then var must be 0.
24)

3.3.21.5                   Wait


    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0
         stype-5          -    c                   -                        cond                       seconds
    -         -                -                var_annc          -       -                -                      -
          -               -              -              -               -              -               -              -
          -               -              -              -               -              -               -              -
         d1              d2             d3              d4             d5             d6              d7             d8
         d9             d10             d11            d12            d13             d14            d15             d16
          -               -              -              -               -              -               -              -

stype-5                        wait
c                              1=this step is commented out
cond                           0=silence, 1=ringback, 2=music, 3=continue, 4=i-silent
seconds                        0-998 even numbers
var_annc                       Variable announcement: 1-26 for variable A-Z, 27-31 for VDN variable V1-V5
                               (CM 3.0 and later)
d1-d15 (< language             Audio/music source extension.
24)

d1-d16 (>= language
24)
```

<a id="pdf-page-098"></a>

## PDF page 98

Source: SPI-SYN24; PDF page 98; extracted characters: 2002.

```text
3.3.21.6                  Goto Step and Goto Vector
For the Go To Step, the field names depend on the value in the "cond" field (the condition of the goto).
The possible conditions are as follows:

Conditions                               Thresholds                                Format
0-unconditional                          N/A                                       A
1-avail agents                           0-999 (obsolete)                          A
3-staffed agents                         0-999 (obsolete)                          A
6-calls queued                           0-999                                     A
8-oldest call                            0-999                                     A
9-TOD                                    none                                      B
10-digits                                none                                      C
11-ASA                                   0-999                                     D or E
12-EWT                                   1-9999                                    E
13-ANI                                   none                                      D or E
14-counted-calls                         0-999                                     D or E
15-ii-digits                             none                                      F
16-wait-improved                         0-999                                     E
17-interflow-qpos                        1-9                                       A
18-holiday                               1-99                                      G
19-A-Z (variable)                        none                                      C
20-pn                                    none                                      C
21-mg                                    none                                      C
22-server                                none                                      C
23-svhour                                1-99                                      G
```

<a id="pdf-page-099"></a>

## PDF page 99

Source: SPI-SYN24; PDF page 99; extracted characters: 2569.

```text
Format A:

For conditions 0, 1, 3, 6, 8, and 17 the message will contain the following fields.

    7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
       stype17 or        pri    c                   -                        cond                       threshold
        stype-18
    s        cmp                -                     -            v       -                 -                      -
                                dest                                         step-num                         var_t
     v_t                      -                                      -                                       -
                               s_num                                     -               -               -              -
          d9             d10            d11             d12              -               -               -              -
          -               -               -              -               -               -               -              -

stype-17 or             goto step or goto vector
stype-18
pri                     0=low, 1=medium, 2=high, 3=top, for conditions 6 and 8
c                       1=this step is commented out
dest                    Step number to go to (1-32) if stype-17.
                        Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                        stype-18
threshold               see ranges for thresholds above (paired with conditions) and "v" is zero
s                       0=specific split/skill in s_num, 1=VDN skill preference in s_num (EAS only)
cmp                      Comparator
                         s
                         1       >
                         2       <
                         3       =
                         4       <>
                         5       >=
                         6       <=
var_t                   Variable threshold: 1-26 for variable A-Z (MV2 and later), 27-31 for VDN variable V1-
                        V5 (CM 3.0 and later)
v                       Variable threshold flag: 0=no variable in var_t, 1=variable is in var_t (MV2 and later)
s_num                   Number of the split/skill: 1-999 (G3V8-G3V11), 1-2000 (MV2-CM5.2), 1-8000 (CM6.0
                        and later), or VDN skill preference (1-3),
step_num                Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
d9-d12                  Agent threshold (0-1500), for conditions 1 and 3 and "v" is 0, (G3V8 and later)
```

<a id="pdf-page-100"></a>

## PDF page 100

Source: SPI-SYN24; PDF page 100; extracted characters: 1788.

```text
Format B:

For condition 9 (Time Of Day), the following fields are contained in the message.

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
        stype17 or        -     c                   -                         cond                           -
        stype-18
     -      sday              shour                 smin            -     eday             ehour                   emin
                                dest                                         step-num                            -
       -                      -                                       -                                      -
           -              -               -               -               -               -              -               -
           -              -               -               -               -               -              -               -
           -              -               -               -               -               -              -               -

stype-17         goto step or goto vector
or
stype-18
c                1=this step is commented out
dest             Step number to go to (1-32) if stype-17.
                 Vector to go to (1-999 (G3V8-CM2), 1-2000 (CM3-CM5.2), 1-8000 (CM6.0 and later) if
                 stype-18
sday             start day for TOD condition; 0-7, 0 = all, 1 = Mon, ...
shour            start hour for TOD condition; 0-23
smin             start minutes for TOD condition; 0-59
eday             end day for TOD condition; 0-7, 0 = all, 1 = Mon, ...
ehour            end hour for TOD condition; 0-23
emin             end minutes for TOD condition; 0-59
step_num         Vector Step number to go to: 0-31 (stype-18 only CM 3.0 and later)
```
