---
title: "SPI-SYN24 - complete source pages 41-60"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 41-60

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-041"></a>

## PDF page 41

Source: SPI-SYN24; PDF page 41; extracted characters: 2437.

```text
       3.2.9        XOPEN20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release

The Open Translation Block message is sent by the switch during the translation pumpup. It indicates
the start of a new block of translation data.

Following the XOPEN is a group of messages for that block type indication the members of that block.
For example, following the XOPEN for a trunk group (block type 2), an XTRUNK would be sent for each
member of the trunk group. It is up to the switch to ensure that a single XTRUNK is sent for each trunk
group member. If the reporting adjunct receives two XTRUNK messages for the same trunk group
member, two rows of data will be created for the same trunk group member with the possibility of
incorrect reporting for that trunk group member. This is true for all of the translations pumpup messages.
The switch will not send duplicates.

     7  6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0
              time_tag                       XOPEN20                                         seq num
                           seq num (cont)                                     tot siz                       parameter
          parameter (cont)              / / / /        block

 time_tag        seconds past minute when message was formatted, 0-59
 opcode          XOPEN20 = 178 (0xb2)
 seq mi,         sequence number, 1-0xffff ffff
 tot siz         total size of message in bytes, 1-255
 parameter       value (split or trunk group number) for items in the translation block.
 block           translation block:
                           0  open full translation block
                           1  open agent position translation block for split
                                     (parameter is split number 0-2000 (up to CM5.2), 0-8000 (CM6.0 and later)
                           2  open trunk translation block for trunk group
                                     (parameter is trunk group number 0-2000
                           3  open agent logon ID translation block
                           4  open VDN translation block
                           5  open logon/status block
                           6  open skill state block
```

<a id="pdf-page-042"></a>

## PDF page 42

Source: SPI-SYN24; PDF page 42; extracted characters: 2724.

```text
       3.2.10       XCLOSE20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release

The Close Translation Block message is sent by the switch during the translation pumpup. It indicates
the end of a block of translation data. The reporting adjunct will validate the count value with the actual
number of items received and if there is a discrepancy, the reporting adjunct Application connection will
not be established until the switch administrator resolves the problem.

An XOPEN/XCLOSE will be sent for each skill with a count of 0 agents.  Logged in agents will also be
sent at the end of the pumpup.

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      XCLOSE20                                         seq num
                           seq num (cont)                                      tot siz                         count
             count (cont)               / / / /        block

time_tag      seconds past minute when event occurred, 0-59
opcode        XCLOSE20 = 179 (0xb3)
seq num       sequence number, 1-0xffff ffff
tot siz       total size of message in bytes, 1-255
Count         number of items sent in this translation block,
                         agent positions        block 1, agents per split 0-1500
                         trunks                 block 2, trunks per trunk group 0-255 (< SPI language 24), 0-
                                                9999 (>= SPI language 24)
                         logid IDs              block 3, total login IDs currently logged in 0-5200 (w/ EAS), 0-
                                                10000 (non-EAS)
                         VDNs                   block 4, all VDNs 0-20000 (up to CM5.2), 1-30000 (CM6.0 and
                                                later)
                         Skill state            block 6, number measured skills 0-2000 (up to CM5.2), 0-8000
                                                (CM6.0 and later)
Block         translation block:
                        0  close full translation block (count field will be 0)
                        1  close agent position translation block
                        2  close trunk translation block
                        3  close agent logon ID translation block
                        4  close VDN translation block
                        5  open logon/status block (count field will be 0)
                        6  open skill state block
```

<a id="pdf-page-043"></a>

## PDF page 43

Source: SPI-SYN24; PDF page 43; extracted characters: 2981.

```text
       3.2.11       XVDN20, XVDN23 and XVDN24
The Vector Translations messages will be sent by the switch as part of a VDN translation block, if Call
Vectoring is enabled. One of these messages is sent for each measured VDN. The reporting adjunct will
record the extension and vector termination for each VDN in the database.  For messages which contain
additional information such as VDN skill preference or BSR plan, the reporting adjunct will also record this
information in the database. In subsequent messages the reporting adjunct and the switch will refer to the
VDNs by the internal line number (iln) specified in the message. Note that the extension is sent in packed
decimal format, where hex a is the digit 0 and 0 in the field is null.

This is a variable length message based on the "s" bit and "dnumber". If the "s" bit is set then 5 additional
bytes are sent for the "primary-skill", "secondary-skill" and "tertiary-skill".

3.2.11.1                    XVDN20 (New CM3.1)


                                                                 Switch    Vect   Skill
                                                First Release    CM3.1     y      y/n
                                                Last Release     CM5.2



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        XVDN20                                          seq num
                           seq num (cont)                                       tot siz              s              iln
               iln (cont)              / / /                          vector                          / /          bsr plan
      bsr (cont)      dnumber             d1              d2              d3              d4              d5              d6
          d7             / / / /          / / / / /                    primary skill                 /        secondary skill
      sec (cont)     /                 tertiary skill

time_tag           seconds past minute when message was formatted, 0-59
opcode             XVDN20 = 180 (0xb4)
seq num            sequence number, 1-0xffff ffff
tot siz            total size of message in bytes, 1-255
S                  skill flag, 0 = no skills in message, 1 = skills in message
Iln                internal line number, 1-32766
vector             vector on which this VDN terminates, 1-2000
bsr plan           bsr application plan number, 1-512
dnumber            number of digits in VDN extension, 1-15
d1-d15             digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in this field is
                   null, zero fill extension digits to a byte boundary)
primary skill      when s = 1, primary VDN agent skill 1-2000, 0 = no skill used
secondary          when s = 1, secondary VDN agent skill 1-2000, 0 = no skill used
skill
tertiary skill     when s = 1, tertiary VDN agent skill 1-2000, 0 = no skill used
```

<a id="pdf-page-044"></a>

## PDF page 44

Source: SPI-SYN24; PDF page 44; extracted characters: 2297.

```text
3.2.11.2                     XVDN23 (New CM6.0)


                                                                  Switch    Vect   Skill
                                                First Release     CM6.0     y      y/n
                                                Last Release      CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3    2   1   0   7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0
               time_tag                        XVDN23                                           seq num
                            seq num (cont)                                       tot siz              s               iln
               iln (cont)               / / /                          vector                           / /          bsr plan
      bsr (cont)       dnumber            d1               d2              d3              d4               d5              d6
          d7              d8              d9              d10             d11              d12             d13             d14
         d15             / / / /        / / /                       primary skill                        / / /         sec skill
            sec skill (cont)            / / /                       tertiary skill

time_tag            seconds past minute when message was formatted, 0-59
opcode              XVDN23 = 17 (0x11)
seq num             sequence number, 1-0xffff ffff
tot siz             total size of message in bytes, 1-255
s                   skill flag, 0 = no skills in message, 1 = skills in message
iln                 internal line number, 1-32766
vector              vector on which this VDN terminates, 1-8000 (CM6.0 and later)
bsr plan            bsr application plan number, 1-512
dnumber             number of digits in VDN extension, 1-15
d1-d15              digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in this field is
                    null, zero fill extension digits to a byte boundary)
primary skill       when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary           when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
skill
tertiary skill      when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
```

<a id="pdf-page-045"></a>

## PDF page 45

Source: SPI-SYN24; PDF page 45; extracted characters: 2371.

```text
3.2.11.3                    XVDN24 (New CM7.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM7.0     y      y/n
                                                Last Release



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        XVDN24                                          seq num
                           seq num (cont)                                       tot siz              s              iln
               iln (cont)               / / /                         vector                          / /          bsr plan
      bsr (cont)         / / / /        / / /        dnumber              d1              d2              d3              d4
          d5              d6              d7              d8              d9             d10             d11              d12
         d13             d14             d15             d16                / / / / / /                     tenant
       / / /                       primary skill                        / / /                     secondary skill
       / / /                       tertiary skill

time_tag           seconds past minute when message was formatted, 0-59
opcode             XVDN24 = 45 (0x2d)
seq num            sequence number, 1-0xffff ffff
tot siz            total size of message in bytes, 1-255
s                  skill flag, 0 = no skills in message, 1 = skills in message
iln                internal line number, 1-32766
vector             vector on which this VDN terminates, 1-8000 (CM6.0 and later)
bsr plan           bsr application plan number, 1-512
dnumber            number of digits in VDN extension, 1-16
d1-d16             digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in this
                   field is null, zero fill extension digits to a byte boundary).
tenant             VDN tenant number, 1-250
primary skill      when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary          when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
skill
tertiary skill     when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
```

<a id="pdf-page-046"></a>

## PDF page 46

Source: SPI-SYN24; PDF page 46; extracted characters: 2565.

```text
       3.2.12       XSPLIT20 and XSPLIT24
The Split Translations messages is sent by the switch and is the first message of the agent position
translation block (XOPEN message block type 2).

3.2.12.1                   XSPLIT20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM6.3

     7  6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                       XSPLIT20                                       seq num
                           seq num (cont)                                     tot siz             /          slt-percent
      / /                         slt-time

                      time_tag        seconds past minute when message was formatted, 0-59
                      opcode          XSPLIT20 = 181 (0xb5)
                      seq num         sequence number, 0-4,294-967,295
                      tot siz         total size in bytes, 1-255
                      slt-percent     service level target percentage 1-99
                      slt-time        service level target time 1-9999 seconds

3.2.12.2                   XSPLIT24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release

     7  6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2  1   0
              time_tag                       XSPLIT24                                       seq num
                           seq num (cont)                                     tot siz             /          slt-percent
      / /                         slt-time                                / / / / / /                    tenant

                      time_tag        seconds past minute when message was formatted, 0-59
                      opcode          XSPLIT24 = 46 (0x2e)
                      seq num         sequence number, 0-4,294-967,295
                      tot siz         total size in bytes, 1-255
                      slt-percent     service level target percentage 1-99
                      slt-time        service level target time 1-9999 seconds
                      tenant          Split tenant number, 1-250
```

<a id="pdf-page-047"></a>

## PDF page 47

Source: SPI-SYN24; PDF page 47; extracted characters: 2419.

```text
       3.2.13       XAGENT20 and XAGENT24
This message is for non-EAS only.

The Agent Position Translations message is sent by the switch as part of a split translation block. One
of these messages is sent for each agent position assigned to the split. The reporting adjunct will record
the extension and split assignment for each agent position in the database. In subsequent messages the
reporting adjunct and the switch will refer to the agent positions by the terminal number (pos) specified in
the message. Note that the extension is sent in packed decimal format, where hex a is the digit 0 and 0 in
the field is null.

Without EAS, a single extension may be assigned to multiple splits.  In this case, the switch will send a
separate XAGENT message for each extension appearance in a split. In other words, each agent/split
pair has a unique terminal number and is tracked as a separate agent position by the reporting adjunct.
With EAS, only agents logged in are reported in translation pumpup therefore this message is not used.

3.2.13.1                   XAGENT20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    n
                                               Last Release    CM6.3

     7  6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1  0
              time_tag                      XAGENT20                                        seq num
                           seq num (cont)                                     tot siz                         pos
              pos (cont)             dnumber            d1              d2              d3             d4              d5
          d6             d7              d8             d9             d10             d11             d12            d13
         d14            d15

time_tag      seconds past minute when message was formatted, 0-59
opcode        XAGENT20 = 182 (0xb6)
seq num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
pos           agent position - without EAS (1-10,000),
dnumber       number of digits in agent extension, 1-15
d1-d15        digits of agent extension, packed decimal format, where hex a is digit 0 and 0 in this field is
              null, zero fill extension digits to a byte boundary
```

<a id="pdf-page-048"></a>

## PDF page 48

Source: SPI-SYN24; PDF page 48; extracted characters: 1387.

```text
3.2.13.2                   XAGENT24 (New CM7.0)


                                                              Switch   Vect    Skill
                                              First Release   CM7.0    y/n     n
                                              Last Release

    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3   2  1   0
              time_tag                     XAGENT24                                        seq num
                          seq num (cont)                                     tot siz                         pos
             pos (cont)               / / /       dnumber              d1             d2             d3              d4
         d5              d6             d7             d8              d9            d10             d11            d12
         d13            d14            d15             d16

time_tag      seconds past minute when message was formatted, 0-59
opcode        XAGENT24 = 47 (0x2f)
seq num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
pos           agent position - without EAS, 1-10,000
dnumber       number of digits in agent extension, 1-16
d1-d16        digits of agent extension, packed decimal format, where hex a is digit 0 and 0 in this
              field is null, zero fill extension digits to a byte boundary.
```

<a id="pdf-page-049"></a>

## PDF page 49

Source: SPI-SYN24; PDF page 49; extracted characters: 2591.

```text
       3.2.14       XTKGRP20 and XTKGRP24
The Trunk Group-Split Translations messages is sent by the switch and is the first message of a trunk
group translation block. One message is sent for each trunk group that does not terminate to a VDN. The
reporting adjunct records the split assignment for each trunk group in the database.

3.2.14.1                   XTKGRP20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1  0
              time_tag                      XTKGRP20                                        seq num
                           seq num (cont)                                     tot siz                / / /          split
             split (cont)

time_tag     seconds past minute when message was formatted, 0-59
opcode       XTKGRP20 =  183 (0xb7)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
split        split on which trunk group terminates, 0-2000 (up to CM5.2), 0-8000 (CM6.0 and later)
             (0 indicates that the trunk group does not terminate on a split or terminates on an unmeasured
             split)

3.2.14.2                   XTKGRP24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1  0
              time_tag                      XTKGRP24                                        seq num
                           seq num (cont)                                     tot siz                / / /          split
             split (cont)                 / / / / / /                     tenant

time_tag     seconds past minute when message was formatted, 0-59
opcode       XTKGRP24 =  48 (0x30)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
split        split on which trunk group terminates, 0-2000 (up to CM5.2), 0-8000 (CM6.0 and later)
             (0 indicates that the trunk group does not terminate on a split or terminates on an unmeasured
             split)
tenant       Trunk Group tenant number, 1-250.
```

<a id="pdf-page-050"></a>

## PDF page 50

Source: SPI-SYN24; PDF page 50; extracted characters: 2815.

```text
       3.2.15      XTGVDN20 and XTGVDN24
3.2.15.1                   XTGVDN20 (New CM3.1)


                                                              Switch   Vect    Skill
                                              First Release   CM3.1    y       y/n
                                              Last Release    CM6.3

The Trunk Group-VDN Translations message is sent by the switch and is the first message of a trunk
group translation block. It is used if Call Vectoring is enabled and/or the trunk group terminates on a VDN.
One message is sent for each measured trunk group. The reporting adjunct records the VDN termination
for each trunk group in the database.

    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                     XTGVDN20                                        seq num
                          seq num (cont)                                     tot siz             /             iln
              iln (cont)

time_tag     seconds past minute when message was formatted, 0-59
opcode       XTGVDN20 = 184 (0xb8)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
iln          internal line number, 0-32766 (0 indicates that the trunk group does not terminate on a VDN or
             terminates on an unmeasured VDN)

3.2.15.2                   XTGVDN24 (New CM7.0)


                                                              Switch   Vect    Skill
                                              First Release   CM7.0    y       y/n
                                              Last Release

The Trunk Group-VDN Translations message is sent by the switch and is the first message of a trunk
group translation block. It is used if Call Vectoring is enabled and/or the trunk group terminates on a VDN.
One message is sent for each measured trunk group. The reporting adjunct records the VDN termination
for each trunk group in the database.

    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                     XTGVDN24                                        seq num
                          seq num (cont)                                     tot siz             /             iln
              iln (cont)                  / / / / / /                    tenant

time_tag     seconds past minute when message was formatted, 0-59
opcode       XTGVDN24 = 49 (0x31)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
iln          internal line number, 0-32766 (0 indicates that the trunk group does not terminate on a VDN or
             terminates on an unmeasured VDN)
tenant       Trunk Group tenant number, 1-250
```

<a id="pdf-page-051"></a>

## PDF page 51

Source: SPI-SYN24; PDF page 51; extracted characters: 2588.

```text
       3.2.16       XTRUNK20 and XTRUNK24
The Trunk Translations messages are sent by the switch as part of a trunk group translation block. One
message is sent for each trunk that is a member of the opened trunk group. The reporting adjunct will
record the equipment location, trunk group assignment and location-id for each trunk in the database. In
subsequent messages the reporting adjunct and the switch will refer to the trunk by the internal trunk
number (itn) specified in the message.

SPI pumpup supports sending up to 24,000 XTRUNK20 messages.
SPI pumpup supports sending up to 24,000 XTRUNK24 messages (64,000 future), with 9,999 per
trunk group. (Currently only sending up to 999 per trunk group.)

For XTRUNK20 and non-H.323/SIP trunks in XTRUNK24, the mapping into the cab, carrier and slot are
defined in the table in section 5.

For XTRUNK24, H.323/SIP trunks set the “t” flag to indicate that the cabinet, carrier and slot fields contain
the binary number for a virtual IP or SIP trunk number (range 00001 to 64,000).

3.2.16.1                   XTRUNK20 (New CM3.1)


                                                              Switch    Vect    Skill
                                              First Release   CM3.1     y/n     y/n
                                              Last Release    CM6.3



    7   6   5   4   3   2  1    0  7   6   5   4   3   2   1  0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1  0
              time_tag                      XTRUNK20                                        seq num
                          seq num (cont)                                     tot siz             /              itn
              itn (cont)                        cab                  Car            slot                    circuit
    c           / / / / / / /                 loc_id

                      time_tag     seconds past minute when message was formatted, 0-59
                      opcode       XTRUNK20 = 185 (0xb9)
                      seq num      sequence number, 0-0xffff ffff
                      tot siz      total size in bytes, 1-255
                      itn          internal trunk number, 1-32766
                      cab          cabinet, 1-44 (G3V8-G3V11), 1-250 (MV2 and later)
                      car          carrier, 1-5 representing letters A-E, 7 representing letter V
                      slot         slot, 1-25
                      circuit      circuit, 1-256 (9 bits, continued in second byte)
                      loc_id       location id number, 0-250, 0 is default for no location id
```

<a id="pdf-page-052"></a>

## PDF page 52

Source: SPI-SYN24; PDF page 52; extracted characters: 2239.

```text
3.2.16.2                    XTRUNK24 (New CM7.0)


                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release

     7  6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                      XTRUNK24                                         seq num
                           seq num (cont)                                     tot siz                           itn

                                                          traditional trunks
              itn (cont)                        cab                   car             slot                    circuit
     c   t  /                        loc_id

                                                     or virtual H.323/SIP trunks
              itn (cont)                                 Virtual trunk string                               / / / / / / / /
     /   t  /                        loc_id

 time_tag           seconds past minute when message was formatted, 0-59
 opcode             XTRUNK24 = 37 (0x25)
 seq num            sequence number, 0-0xffff ffff
 tot siz            total size in bytes, 1-255
 itn                internal trunk number, 1-65,535
 cab                cabinet, 1-250
 car                carrier, 1-5 representing letters A-E, 7 representing letter V
 slot               slot, 1-25
 circuit            circuit, 1-256 (9 bits, continued in second byte)
 Virtual            The Txxxxx virtual H.323 or SIP trunk string, 1-24,000 (1-64,000 in the future)
 trunk string
 t                  trunk location format. 0=use format with cab, car, slot, circuit
                    1=use format with Virtual trunk string
 loc_id             location id number, 0-2000.  0 is default for no location id (13 bits for future
                    expansion)


       3.2.17       SKSTATE20 and SKSTATE23
Refer to SKSTATE in Call Processing (section 3.4.29) for the layout.


       3.2.18       ALOGON20, ALOGON23 and ALOGON24
Refer to ALOGON in the Call Processing (section 3.4.2) for message layout.
```

<a id="pdf-page-053"></a>

## PDF page 53

Source: SPI-SYN24; PDF page 53; extracted characters: 958.

```text
3.3       Switch Administration
Switch Administration request messages will only be sent by the reporting adjunct to the switch when the
reporting adjunct Session is in the DATA TRANSFER mode. The switch response messages will be
intermixed with the Call Processing messages and will be time-stamped and sent (or buffered) in the
order that they were processed.

Every request message that is sent by the reporting adjunct will be tagged (tag) and the switch will return
this tag, unchanged, in each response message that is associated with that particular request. The
reporting adjunct uses the tag to correlate the switch response with the reporting adjunct switch
Administration process that sent the request.

If the switch does not recognize a request message, or can not interpret one or more of the message
parameters, the switch will return the RCODE message with rcode=1 (illegal request). Otherwise the
normal response message(s) will be returned.
```

<a id="pdf-page-054"></a>

## PDF page 54

Source: SPI-SYN24; PDF page 54; extracted characters: 3140.

```text
       3.3.1        BUSYOUT20 (New CM3.1)


                                                               Switch   Vect    Skill
                                              First Release    CM3.1    y/n     y/n
                                              Last Release

The Busy-Out Link message is sent by the switch when the reporting adjunct Session is busied-out for
administration purposes. This is usually done by the switch administrator when making changes that will
affect the reporting adjunct database configuration (e.g., adding another extension to a measured split or
administering another trunk group as measured). These changes will typically result in the "translations
changed" flag being set so that when the reporting adjunct reinitiates the session (RTCS) the switch will
report that translations changed (XSTAT20 c=1) and the reporting adjunct will request full translations
(RFTB) in order to update the real-time database to reflect the changes that were made. This message is
also sent in response to an RTCS if the reporting adjunct Session is busied-out at the time of the request.

The reporting adjunct will mark the reporting adjunct Session BUSIED-OUT, initialize all measured agent
positions and trunks, and wait for another reporting adjunct Session to be established.

The switch supports busying out the link, but this does not need to be done for database configuration
changes.

     7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                     BUSYOUT20                                        seq num
                           seq num (cont)                                     tot siz

                            time_tag      seconds past minute when event occurred, 0-59
                            opcode        BUSYOUT20 = 186 (0xba)
                            seq num       sequence number, 0-0xffff ffff
                            tot siz       total size in bytes, 1-255


       3.3.2        RELBUSY20 (New CM3.1)


                                                               Switch   Vect    Skill
                                              First Release    CM3.1    y/n     y/n
                                              Last Release

The Release Busy Link message is sent by the switch when the reporting adjunct session is released
from busy-out. The reporting adjunct will attempt to initiate another reporting adjunct session by sending
the RTCS message.

     7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                     RELBUSY20                                        seq num
                           seq num (cont)                                     tot siz

                            time_tag      seconds past minute when event occurred, 0-59
                            opcode        RELBUSY20 = 187 (0xbb)
                            seq num       sequence number, 0-0xffff ffff
                            tot siz       total size in bytes, 1-255
```

<a id="pdf-page-055"></a>

## PDF page 55

Source: SPI-SYN24; PDF page 55; extracted characters: 3019.

```text
       3.3.3        ARVDN20, ARVDN23 and ARVDN24
The Add/Remove Vector Translations message is sent by the switch when a VDN is added/removed as
a measured VDN if Call Vectoring is enabled. This allows for dynamic administration without bringing
down the reporting adjunct link. One of these messages is sent for each measured VDN. VDNs are
referenced by internal line number (iln).

VDNs can be made measured or unmeasured or removed using switch administration while calls are in
progress.  VDN statistics will not be accumulated for these calls in progress (i.e, calls in progress will look
like calls to an unmeasured VDN).

This is a variable length message based on the "s" bit and "dnumber". If the "s" bit is set then 5 additional
bytes are sent for the "primary-skill", "secondary-skill" and "tertiary-skill".

3.3.3.1                     ARVDN20 (New CM3.1)


                                                                Switch   Vect    Skill
                                               First Release    CM3.1    y       y/n
                                               Last Release     CM5.2



     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       ARVDN20                                         seq num
                           seq num (cont)                                      tot siz             r              iln
              iln (cont)            s                        vector                                       bsr plan
      dnumber            d1              d2              d3              d4              d5             d6              d7
          d8             d9              d10            d11             d12             d13             d14             d15
          / / / / /                   primary skill                 /               secondary skill                /    ter skl
          tertiary skill (cont)

time_tag              seconds past minute when message was formed, 0-59
opcode                ARVDN20 = 188 (0xbc)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
r                     remove, 0 = add, 1 = remove
iln                   internal line number, 1-32766
s                     skill flag, 0 = no skills in message, 1 = skills in message
vector                vector on which this VDN terminates, 1-2000
bsr plan              bsr application plan number, 1-512
dnumber               number of digits in VDN extension, 1-15
d1-d15                digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in this field
                      is null, zero fill extension digits to a byte boundary)
primary skill         when s = 1, primary VDN agent skill 1-2000, 0 = no skill used
secondary skill       when s = 1, secondary VDN agent skill 1-2000, 0 = no skill used
tertiary skill        when s = 1, tertiary VDN agent skill 1-2000, 0 = no skill used
```

<a id="pdf-page-056"></a>

## PDF page 56

Source: SPI-SYN24; PDF page 56; extracted characters: 2286.

```text
3.3.3.2                     ARVDN23 (New CM6.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM6.0     y      y/n
                                                Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                       ARVDN23                                          seq num
                           seq num (cont)                                       tot siz              r              iln
               iln (cont)            s                        vector                                       bsr plan
      dnumber             d1              d2              d3              d4              d5              d6              d7
          d8              d9             d10             d11             d12             d13             d14             d15
       / / /                       primary skill                        / / /                     secondary skill
       / / /                       tertiary skill

time_tag              seconds past minute when message was formed, 0-59
opcode                ARVDN23 = 18 (0x12)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
r                     remove, 0 = add, 1 = remove
iln                   internal line number, 1-32766
s                     skill flag, 0 = no skills in message, 1 = skills in message
vector                vector on which this VDN terminates, 1-8000 (CM6.0 and later)
bsr plan              bsr application plan number, 1-512
dnumber               number of digits in VDN extension, 1-15
d1-d15                digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in this field
                      is null, zero fill extension digits to a byte boundary)
primary skill         when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary skill       when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
tertiary skill        when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
```

<a id="pdf-page-057"></a>

## PDF page 57

Source: SPI-SYN24; PDF page 57; extracted characters: 2452.

```text
3.3.3.3                     ARVDN24 (New CM7.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM7.0     y      y/n
                                                Last Release



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                       ARVDN24                                          seq num
                           seq num (cont)                                       tot siz              r              iln
               iln (cont)            s                        vector                                       bsr plan
       / / /        dnumber               d1              d2              d3              d4              d5              d6
          d7              d8              d9             d10             d11             d12             d13             d14
         d15             d16                / / / / / /                     tenant                      / / /      primary skill
          primary skill (cont)         / / /                      secondary skill                       / / /       tertiary skill
          tertiary skill (cont)

time_tag              seconds past minute when message was formed, 0-59
opcode                ARVDN24 = 50 (0x32)
seq num               sequence number, 0-0xffff ffff
tot siz               total size in bytes, 1-255
r                     remove, 0 = add, 1 = remove
iln                   internal line number, 1-32766
s                     skill flag, 0 = no skills in message, 1 = skills in message
vector                vector on which this VDN terminates, 1-8000 (CM6.0 and later)
bsr plan              bsr application plan number, 1-512
dnumber               number of digits in VDN extension, 1-16
d1-d16                digits of VDN extension (packed decimal format, where hex a is digit 0 and 0 in
                      this field is null, zero fill extension digits to a byte boundary).
tenant                VDN tenant number, 1-250
primary skill         when s = 1, primary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
secondary skill       when s = 1, secondary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
tertiary skill        when s = 1, tertiary VDN agent skill 1-8000 (CM6.0 and later), 0 = no skill used
```

<a id="pdf-page-058"></a>

## PDF page 58

Source: SPI-SYN24; PDF page 58; extracted characters: 2393.

```text
       3.3.4       ARAGENT20 and ARAGENT24
This message is for non-EAS only.

The Add/Remove Agent Position Translations message is sent by the switch when an agent is
added/removed from a measured split. This allows for dynamic administration without bringing down the
-adjunct reporting link. One of these messages is sent for each measured agent position that belongs to
the measured split. With EAS, only agents logged in are reported in translation pumpup therefore there is
no need to add/remove agents with this message.

When a split is added, the ARSPLIT message is sent first followed by the ARAGENT messages.  When a
split is removed, the ARAGENT messages are sent before the ARSPLIT message.

The agent cannot be changed to measured or unmeasured or removed while the agent is active on a call.
The request to change the "measured" field on the switch hunt group form will be blocked by the switch.


3.3.4.1                    ARAGENT20 (New CM3.1)


                                                             Switch    Vect   Skill
                                             First Release   CM3.1     y/n    n
                                             Last Release    CM6.3



    7   6   5   4   3  2   1   0   7   6  5   4   3   2   1  0   7   6   5   4   3  2   1   0   7   6  5   4   3   2   1  0
              time_tag                    ARAGENT20                                       seq num
                          seq num (cont)                                    tot siz                         pos
             pos (cont)              dnumber           d1             d2             d3              d4             d5
         d6             d7              d8             d9             d10            d11            d12            d13
         d14            d15        r   / /                          split

time_tag     seconds past minute when message was formatted, 0-59
opcode       ARAGENT20 = 189 (0xbd)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
pos          agent position - 1-10000
dnumber      number of digits in agent extension, 1-15,
d1-d15       digits of agent extension, packed decimal format, where hex a is digit 0 and 0 in this field is
             null, zero fill extension digits to a byte boundary
r            remove; 0 = add, 1 = remove
split        split number  0-8000 (CM6.0 and later)
```

<a id="pdf-page-059"></a>

## PDF page 59

Source: SPI-SYN24; PDF page 59; extracted characters: 1520.

```text
3.3.4.2                    ARAGENT24 (New CM7.0)


                                                              Switch    Vect   Skill
                                              First Release   CM7.0     y/n    n
                                              Last Release



    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                    ARAGENT24                                        seq num
                          seq num (cont)                                     tot siz                         pos
             pos (cont)               / / /       dnumber              d1             d2              d3             d4
         d5              d6             d7              d8             d9             d10            d11             d12
         d13            d14             d15            d16        r    / /                         split

time_tag      seconds past minute when message was formatted, 0-59
opcode        ARAGENT24 = 51 (0x33)
seq num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
pos           agent position - 1-10000
dnumber       number of digits in agent extension, 1-16
d1-d16        digits of agent extension, packed decimal format, where hex a is digit 0 and 0 in this
              field is null, zero fill extension digits to a byte boundary.
r             remove; 0 = add, 1 = remove
split         split number  0-8000 (CM6.0 and later)
```

<a id="pdf-page-060"></a>

## PDF page 60

Source: SPI-SYN24; PDF page 60; extracted characters: 2948.

```text
       3.3.5        ARSPLIT20, ARSPLIT23 and ARSPLIT24
The Add/Remove Split Translations message is sent by the switch when a skill is added/removed as a
measured skill. A skill can not be removed if agents are logged in to that skill.  With EAS, after the
ARSPLIT message is sent, the SKSTATE message will follow.

This allows for dynamic administration without bringing down the reporting adjunct link. One of these
messages is sent for each measured skill.

If calls are active in the skill, a request to change the "measured" field on the switch hunt group form will
be blocked by the switch.

3.3.5.1                     ARSPLIT20 (New CM3.1)


                                                                Switch   Vect    Skill
                                               First Release    CM3.1    y/n     y/n
                                               Last Release     CM5.2



     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      ARSPLIT20                                        seq num
                           seq num (cont)                                      tot siz             r       / / / /       skill
              skill (cont)          /          slt-percent           / /                          slt-time

time_tag          seconds past minute when message was formatted, 0-59
opcode            ARSPLIT20 = 190 (0xbe)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
r                 remove; 0 = add; 1 = remove
skill             skill number 0-2000
slt-percent       service level target percentage 1-99
slt-time          service level target time 1-9999 seconds

      3.3.5.2               ARSPLIT23 (New CM6.0)


                                                                Switch   Vect    Skill
                                               First Release    CM6.0    y/n     y/n
                                               Last Release     CM6.3



     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      ARSPLIT23                                        seq num
                           seq num (cont)                                      tot siz             r     / /          skill
              skill (cont)          /          slt-percent           / /                          slt-time

time_tag          seconds past minute when message was formatted, 0-59
opcode            ARSPLIT23 = 19 (0x13)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
r                 remove; 0 = add; 1 = remove
skill             skill number  0-8000 (CM6.0 and later)
slt-percent       service level target percentage 1-99
slt-time          service level target time 1-9999 seconds
```
