---
title: "SPI-SYN24 - complete source pages 61-80"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 61-80

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-061"></a>

## PDF page 61

Source: SPI-SYN24; PDF page 61; extracted characters: 1277.

```text
3.3.5.3                     ARSPLIT24 (New CM7.0


                                                                 Switch    Vect   Skill
                                                First Release    CM7.0     y/n    y/n
                                                Last Release



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                      ARSPLIT24                                         seq num
                           seq num (cont)                                       tot siz              r    / /           skill
              skill (cont)           /          slt-percent           / /                           slt-time
            / / / / / /                     tenant

time_tag          seconds past minute when message was formatted, 0-59
opcode            ARSPLIT24 = 52 (0x34)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
r                 remove; 0 = add; 1 = remove
skill             skill number  0-8000 (CM6.0 and later)
slt-percent       service level target percentage 1-99
slt-time          service level target time 1-9999 seconds
tenant            Split tenant number, 1-250
```

<a id="pdf-page-062"></a>

## PDF page 62

Source: SPI-SYN24; PDF page 62; extracted characters: 3079.

```text
       3.3.6        ARTKGRP20, ARTKGRP23 and ARTKGRP24
The Add/Remove Trunk Group-Split Translations message is sent by the switch when a trunk group is
added/removed as a measured trunk group and terminates on a skill. This allows for dynamic
administration without bringing down the reporting adjunct link. One of these messages is sent for each
measured trunk group. Typically ARTRUNK messages containing the trunk members follow an
ARTKGRP message. Measured trunks cannot be changed to unmeasured or added or removed using
switch administration with calls active.  This is blocked by the switch. If the trunk group is changed to
measured with calls active, the active calls will be treated as an unmeasured trunk group call.

3.3.6.1                    ARTKGRP20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y/n    y/n
                                              Last Release    CM5.2



    7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0
              time_tag                     ARTKGRP20                                       seq num
                          seq num (cont)                                     tot siz             r       / / / /       skill
             skill (cont)                / / / / /                      tkgrp

time_tag     seconds past minute when message was formatted, 0-59
opcode       ARTKGRP20 = 191 (0xbf)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
r            remove; 0 = add; 1 = remove
skill        skill on which trunk group terminates, 0-2000 (0 indicates that the trunk group does not
             terminate on a split or terminates on an unmeasured split)
tkgrp        trunk group number, 0-2000

      3.3.6.2              ARTKGRP23 (New CM6.0)


                                                              Switch    Vect   Skill
                                              First Release   CM6.0     y/n    y/n
                                              Last Release    CM6.3



    7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0
              time_tag                     ARTKGRP23                                       seq num
                          seq num (cont)                                     tot siz             r    / /          skill
             skill (cont)                / / / / /                      tkgrp

time_tag     seconds past minute when message was formatted, 0-59
opcode       ARTKGRP23 = 20 (0x14)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
r            remove; 0 = add; 1 = remove
skill        skill on which trunk group terminates, 0-8000 (CM6.0 and later)
             (0 indicates that the trunk group does not terminate on a split or terminates on an unmeasured
             split)
tkgrp        trunk group number, 0-2000
```

<a id="pdf-page-063"></a>

## PDF page 63

Source: SPI-SYN24; PDF page 63; extracted characters: 1324.

```text
3.3.6.3                     ARTKGRP24 (New CM7.0)


                                                                Switch    Vect   Skill
                                               First Release    CM7.0     y/n    y/n
                                               Last Release



     7   6   5  4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                      ARTKGRP24                                         seq num
                           seq num (cont)                                      tot siz              r    / /          skill
              skill (cont)                / / / / /                       tkgrp                            / / / / / /      ten
            tenant (cont)

time_tag      seconds past minute when message was formatted, 0-59
opcode        ARTKGRP24 = 53 (0x35)
seq num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
r             remove; 0 = add; 1 = remove
skill         skill on which trunk group terminates, 0-8000 (CM6.0 and later)
              (0 indicates that the trunk group does not terminate on a split or terminates on an unmeasured
              split)
tkgrp         trunk group number, 0-2000
tenant        Trunk Group tenant number, 1-250
```

<a id="pdf-page-064"></a>

## PDF page 64

Source: SPI-SYN24; PDF page 64; extracted characters: 2799.

```text
       3.3.7       ARTGVDN20 and ARTGVDN24
The Add/Remove Trunk Group-VDN Translations message is sent by the switch when a trunk group
that terminates on a VDN is add/removed as a measured trunk group. This allows for dynamic
administration without bringing down the reporting adjunct link. One of these messages is sent for each
measured trunk group.

3.3.7.1                    ARTGVDN20 (New CM3.1)


                                                              Switch   Vect   Skill
                                              First Release   CM3.1    y      y/n
                                              Last Release    CM6.3

    7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0  7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0
              time_tag                    ARTGVDN20                                       seq num
                          seq num (cont)                                    tot siz             r              iln
              iln (cont)                / / / / /                      tkgrp

time_tag     seconds past minute when message was formatted, 0-59
opcode       ARTGVDN20 = 192 (0xc0)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
r            remove; 0 = add, 1 = remove
iln          internal line number of the VDN, 0-32766
             (0 indicates that the trunk group does not terminate on a VDN or terminates on an
             unmeasured VDN)
tkgrp        trunk group number, 0-666 (G3V8-G3V10), 0-2000 (G3V11 and later)


3.3.7.2                    ARTGVDN24 (New CM7.0)


                                                              Switch   Vect   Skill
                                              First Release   CM7.0    y      y/n
                                              Last Release

    7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0  7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0
              time_tag                    ARTGVDN24                                       seq num
                          seq num (cont)                                    tot siz             r              iln
              iln (cont)                / / / / /                      tkgrp                           / / / / / /      ten
            tenant (cont)

time_tag     seconds past minute when message was formatted, 0-59
opcode       ARTGVDN24 = 54 (0x36)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
r            remove; 0 = add, 1 = remove
iln          internal line number of the VDN, 0-32766
             (0 indicates that the trunk group does not terminate on a VDN or terminates on an
             unmeasured VDN)
tkgrp        trunk group number, 0-2000
tenant       Trunk group tenant number, 1-250
```

<a id="pdf-page-065"></a>

## PDF page 65

Source: SPI-SYN24; PDF page 65; extracted characters: 2338.

```text
       3.3.8        ARTRUNK20 and ARTRUNK24
The Add/Remove Trunk Translations message is sent by the switch when a trunk is added or removed
from a measured trunk group. This allows for dynamic administration without bringing down the reporting
adjunct link. One of these messages is sent for each trunk that is added/removed. Trunks are referenced
by internal trunk number (itn). For virtual IP/SIP trunk ports, the mapping into the cab, slot and circuit are
defined in the table in section 5.

Measured trunks cannot be changed to unmeasured or added or removed using switch administration
with calls active.  This is blocked by the switch. If the trunk group is changed to measured with calls
active, the active calls will be treated as an unmeasured trunk group call.

3.3.8.1                    ARTRUNK20 (New CM3.1)


                                                               Switch   Vect    Skill
                                              First Release    CM3.1    y/n     y/n
                                              Last Release     CM6.3



     7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                     ARTRUNK20                                        seq num
                           seq num (cont)                                     tot siz             r              itn
              itn (cont)                        cab                   car            slot                    circuit
     c      / / / /                      tkgrp                                loc_id

 time_tag      seconds past minute when message was formatted, 0-59
 opcode        ARTRUNK20 = 193 (0xc1)
 seq num       sequence number, 0-0xffff ffff
 tot siz       total size in bytes, 1-255
 r             remove; 0 = add; 1 = remove
 itn           internal trunk number, 1-32766
 cab           cabinet, 1-44 (G3V8-G3V11), 1-250 (MV2 and later)
 car           carrier, 1-5 representing letters A-E, 7 representing letter V (G3V11 and later)
 slot          slot, 1-25
 circuit       circuit, 1-256 (9 bits, continued in second byte)
 tkgrp         trunk group number, 0-666 (G3V8-G3V10), 0-2000 (G3V11 and later)
 loc id        location id number, 0-44 (G3V8-G3V11), 0-250 (MV2 and later), 0 is default for no location id
```

<a id="pdf-page-066"></a>

## PDF page 66

Source: SPI-SYN24; PDF page 66; extracted characters: 2439.

```text
3.3.8.2                     ARTRUNK24 (New CM7.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM7.0     y/n    y/n
                                                Last Release



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                     ARTRUNK24                                          seq num
                           seq num (cont)                                       tot siz                           itn


                                                           traditional trunks
               itn (cont)                        cab                    car             slot                     circuit
     c   r   t    / /                      tkgrp                        / / /                          loc_id


                                                      or Virtual H.323/SIP trunks
               itn (cont)                                 Virtual trunk string                                 / / / / / / / /
     /   r   t    / /                      tkgrp                        / / /                          loc_id

time_tag                   seconds past minute when message was formatted, 0-59
opcode                     ARTRUNK24 = 38 (0x26)
seq num                    sequence number, 0-0xffff ffff
tot siz                    total size in bytes, 1-255
itn                        internal trunk number, 1-65535
cab                        cabinet, 1-44 (G3V8-G3V11), 1-250 (MV2 and later)
car                        carrier, 1-5 representing letters A-E, 7 representing letter V (G3V11 and later)
slot                       slot, 1-25
circuit                    circuit, 1-256 (9 bits, continued in second byte)
r                          remove; 0 = add; 1 = remove
Virtual trunk              The Txxxxx virtual H.323 or SIP trunk string, 1-24,000 (1-64,000 in the future)
string
t                          trunk location format. 0=use format with cab, car, slot, circuit
                           1=use format with Virtual trunk string
tkgrp                      trunk group number, 0-666 (G3V8-G3V10), 0-2000 (G3V11 and later)
loc_id                     location id number, 0-2000,  0 is default for no location id (13 bits for future
                           expansion)
```

<a id="pdf-page-067"></a>

## PDF page 67

Source: SPI-SYN24; PDF page 67; extracted characters: 1931.

```text
       3.3.9       AGMOVE20 (New CM3.1)


                                                              Switch   Vect    Skill
                                              First Release   CM3.1    y/n     n
                                              Last Release

The Agent Position Move message is sent by the switch when an agent position (extension) is removed
from and/or moved to a new split. When an agent position is removed from a split or added to an
unmeasured split, the switch will send an Agent Position Move message with split=0. When an agent
position is added to a measured split, the switch will send an Agent Position Move message with
appropriate split number. When an agent position is moved from one split to another split the switch may
send both the "remove" and "add" messages or simply the "add" ("move") message. The reporting
adjunct will update the split assignment for the specified agent position. The AGMOVE message is sent
by switch to the reporting adjunct in response to a MVAGSTFD from the reporting adjunct (only when
EAS is not optioned).

    7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4   3  2   1   0
              time_tag                     AGMOVE20                                        seq num
                          seq num (cont)                                     tot siz                        pos
                     pos (cont)                   /                     split

                     time_tag      seconds past minute when event occurred, 0-59
                     opcode        AGMOVE20 = 248 (0xF8)
                     seq num       sequence number, 0-0xffff ffff
                     tot siz       total size in bytes, 1-255
                     pos           agent position - 1-10000 (G3V8 and later)
                     split         split number, 1-999 (G3V8-G3V11), 1-2000 (MV2 and later)
```

<a id="pdf-page-068"></a>

## PDF page 68

Source: SPI-SYN24; PDF page 68; extracted characters: 1235.

```text
       3.3.10       MVAGSTFD21, MVAGSTFD23 and MVAGSTFD24
The Move Agent While Staffed message is a variable length message sent by the reporting adjunct to
the switch. In an EAS environment, the MVAGSTFD message is a request to add, remove, or change the
skill assignments for up to 32 agent positions (LoginID).

An agent with one skill cannot have that skill removed, and an agent with the maximum number of skills
cannot have a skill added. The remaining skills are not shifted when a skill is removed, so gaps can occur
in the administered positions for an agent. For example, if the first of four skills is removed, the agent will
have three remaining skills, in positions 2, 3, and 4. Skills are added in the first available position.

The expected response is one RCODE message or one CRCODE and up to 32 sets of messages to
effect the move. With EAS, this is ALOGON.

Starting with MVAGSTFD24, with the increased extension size, this request may not fit into a single
MVAGSTFD message. we are changing skills on more than 16 agents, a second message will be sent.
The 1st message in series covers agents 1-16 and the 2nd message covers agents 17-32, mapping to
pos1-pos16. The end bit is set for the last message in a series.
```

<a id="pdf-page-069"></a>

## PDF page 69

Source: SPI-SYN24; PDF page 69; extracted characters: 2824.

```text
3.3.10.1                     MVAGSTFD21 (New CM4)


                                                                  Switch    Vect    Skill
                                                 First Release    CM4       y/n     y/n
                                                 Last Release     CM5.2

The first 14 bytes are always sent.
This message is specific to the 13 Digit Dial Plan Expansion enhancement.

     7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0
            MVAGSTFD21                            tag                 s    action     r         level                  count
     /                    to_skill                    /                   from_skill                               pos1
                                                               pos1 (cont)
                      pos1 (cont)                                                         pos2
                                                               pos2 (cont)
                                                                  pos3
                                      pos3 (cont)
                                                                  .  .  .
                                                                  posN
                                      posN (cont)

opcode           MVAGSTFD21 = 53 (0x35)
tag              message tag, 0-255 (it will be returned in the switch response message(s))
s                skills, 1=skills are used in this message, 0=skills not used. If s=0, the only valid operation is
                 the "move" action.
action           1 = add to_skill to agent (from_skill is unused).
                 2 = remove from_skill from agent (to_skill is unused).
                 3 = move agents between splits/skills
r                flag indicating level is reserved, 0=skill level, 1=reserve level.
level            skill level (1-16) for to_skill (used only if s = 1).  Reserve level (1-2) if r = 1.  0 = level is
                 unspecified (no change requested).
count            the number of agent positions included in the message (1-32).
to_skill,        skill or split number, 0-999 (G3V8-G3V11), 0-2000 (MV2 and later), measured (EAS or non-
from_skill       EAS) or unmeasured (EAS only). The "from_skill" is not used for `add' (action = 1);
                 therefore it will contain "0". The "to_skill is not used for `delete' (action = 2); therefore it will
                 contain "0". When action = 3, to_skill is the 'to' split or skill and from_skill is the 'from' split or
                 skill.
pos1 –           agent position - without EAS (1-10000), with EAS (0-9999999999999) login ID in BCD
pos32            format, left-justified where hex a is digit 0 and 0 in this field is null
```

<a id="pdf-page-070"></a>

## PDF page 70

Source: SPI-SYN24; PDF page 70; extracted characters: 3306.

```text
3.3.10.2                     MVAGSTFD23 (New CM6.0)


                                                                  Switch     Vect    Skill
                                                 First Release    CM6.0      y/n     y/n
                                                 Last Release     CM6.3

The first 15 bytes are always sent.
This message is specific to the 13 Digit Dial Plan Expansion enhancement.
If the dial plan is expanded beyond 13 digits, a new protocol message would be needed.

     7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0
            MVAGSTFD23                             tag                 s    action     r     ia           level             count
      cnt    /                         to_skill                          / / /                         from_skill
                                                                   pos1
                                      pos1 (cont)                                                           pos2
                                                               pos2 (cont)
              pos2 (cont)                                                          pos3
                                                       pos3 (cont)                                                           . . .
                                                                   .  .  .
                                                                  posN
                                      posN (cont)

opcode            MVAGSTFD23 = 56 (0x38)
tag               message tag, 0-255 (it will be returned in the switch response message(s))
s                 skills, 1=skills are used in this message, 0=skills not used. If s=0, the only valid operation is
                  the "move" action.
action            1 = add to_skill to agent (from_skill is unused).
                  2 = remove from_skill from agent (to_skill is unused).
                  3 = move agents between splits/skills
r                 flag indicating level is reserved, 0=skill level, 1=reserve level.
ia                field that indicates whether the skill is interruptible. This field is only valid when the “r”
                  (reserve) field is 0.

                   0    not an interruptible skill
                   1    auto-in-interrupt
                   2    manual-in-interrupt
                   3    notify-interrupt

level             skill level (1-16) for to_skill (used only if s = 1).  Reserve level (1-2) if r = 1.  0 = level is
                  unspecified (no change requested).
count             the number of agent positions included in the message (1-32).
to_skill,         skill or split number, 0-8000 measured (EAS or non-EAS) or unmeasured (EAS only). The
from_skill        "from_skill" is not used for `add' (action = 1); therefore it will contain "0". The "to_skill is not
                  used for `delete' (action = 2); therefore it will contain "0". When action = 3, to_skill is the 'to'
                  split or skill and from_skill is the 'from' split or skill.
pos1 –            agent position - without EAS (1-10000), with EAS login ID in BCD format, left-justified where
pos32             hex a is digit 0 and 0 in this field is null
```

<a id="pdf-page-071"></a>

## PDF page 71

Source: SPI-SYN24; PDF page 71; extracted characters: 3065.

```text
3.3.10.3                     MVAGSTFD24 (New CM7.0)


                                                                  Switch    Vect    Skill
                                                 First Release    CM7.0     y/n     y/n
                                                 Last Release

The first 20 bytes are always sent.

     7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0   7   6    5   4   3   2   1   0
            MVAGSTFD24                            tag                 s    action     r     ia           level            count
      cnt    e                        to_skill                           / / /                        from_skill
                                                                  pos1
                                                              pos1 (cont)
                                                                  pos2
                                                              pos2 (cont)
                                                                  .  .  .

                                                                  posN
                                                              posN (cont)

opcode            MVAGSTFD24 = 62 (0x3e)
tag               message tag, 0-255 (it will be returned in the switch response message(s))
s                 skills, 1=skills are used in this message, 0=skills not used. If s=0, the only valid operation is
                  the "move" action.
action            1 = add to_skill to agent (from_skill is unused).
                  2 = remove from_skill from agent (to_skill is unused).
                  3 = move agents between splits/skills
r                 flag indicating level is reserved, 0=skill level, 1=reserve level.
ia                field that indicates whether the skill is interruptible. This field is only valid when the “r”
                  (reserve) field is 0.

                   0    not an interruptible skill
                   1    auto-in-interrupt
                   2    manual-in-interrupt
                   3    notify-interrupt
level             skill level (1-16) for to_skill (used only if s = 1).  Reserve level (1-2) if r = 1.  0 = level is
                  unspecified (no change requested).
count             the number of agent positions included in the message (1-16).
e                 end bit, set when this is the last message of the set needed to satisfy the request
to_skill,         skill or split number, 0-8000 measured (EAS or non-EAS) or unmeasured (EAS only). The
from_skill        "from_skill" is not used for `add' (action = 1); therefore it will contain "0". The "to_skill is not
                  used for `delete' (action = 2); therefore it will contain "0". When action = 3, to_skill is the 'to'
                  split or skill and from_skill is the 'from' split or skill.
pos1 –            agent position - without EAS (1-10000), with EAS login ID in BCD format, left-justified
pos16             where hex a is digit 0 and 0 in this field is null
```

<a id="pdf-page-072"></a>

## PDF page 72

Source: SPI-SYN24; PDF page 72; extracted characters: 2482.

```text
       3.3.11      APARMS7 and APARMS24

The Agent Parameters message is sent by the reporting adjunct to the switch to request the skills for an
agent.  The expected response is an AGENTSK with the agent's skills or an RCODE 1 or 31.This
message is only used in EAS configurations.

3.3.11.1                   APARMS7 (New G3V11)


                                                             Switch    Vect   Skill
                                             First Release   G3V11     y      y
                                             Last Release    CM6.3

    7   6   5   4   3  2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0
             APARMS7                           tag                 pnumber            p1             p2             p3
         p4             p5              p6             p7             p8              p9            p10             p11
         p12            p13            p14            p15

opcode       APARMS7 = 40 (0x28)
tag          message tag, 0-255 (it will be returned in the switch response message)
pnumber      number of digits in agent position, 1-15
p1 – p15     agent position - with EAS (0-9999999) login ID in packed decimal format, left-justified where
             hex a is digit 0 and 0 in this field is null, zero fill position to a byte boundary

3.3.11.2                   APARMS24 (New CM7.0)


                                                             Switch    Vect   Skill
                                             First Release   CM7.0     y      y
                                             Last Release

    7   6   5   4   3  2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3  2   1   0   7   6   5  4   3   2   1   0
            APARMS24                           tag                  / / /        pnumber             p1             p2
         p3             p4              p5             p6             p7              p8             p9             p10
         p11            p12            p13            p14             p15            p16

opcode         APARMS24 = 63 (0x3f)
tag            message tag, 0-255 (it will be returned in the switch response message)
pnumber        number of digits in agent position, 1-16
p1 – p16       agent position - with EAS (0-9999999) login ID in packed decimal format, left-justified
               where hex a is digit 0 and 0 in this field is null, zero fill position to a byte boundary.
```

<a id="pdf-page-073"></a>

## PDF page 73

Source: SPI-SYN24; PDF page 73; extracted characters: 3387.

```text
       3.3.12       AGENTSK20, AGENTSK23, AGENTSK24
The Agent Skills message is sent by switch to the reporting adjunct in response to an APARMS
message to indicate the agent's skills. Blanks (or holes) in the administration will be represented by
skill=0, level=0, reserve=0, percent=0.

3.3.12.1                    AGENTSK20 (New CM3.1)


                                                                 Switch    Vect   Skill
                                                First Release    CM3.1     y      y
                                                Last Release     CM5.2



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                     AGENTSK20                                          seq num
                           seq num (cont)                                       tot siz                           tag
       pnumber            p1              p2              p3              p4              p5              p6              p7
          p8              p9             p10             p11             p12             p13             p14             p15
      ch     s   d   /                    da_skl                             percent1            r        level1           skill1
             o   a                                                                               1
             skill1 (cont)                   percent2            r        level2                           skill2
                                                                 2
                                                                 .  .  .
            percent60            r       level60                          skill60
                                 6
                                 0

time_tag         seconds past minute when message was formed, 0-59
opcode           AGENTSK20 = 194 (0xc2)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
tag              message tag, 0-255 (it will be returned in the switch response message).
pnumber          number of digits in agent position, 1-15
p1 - p15         agent position - (0-9999999) login ID in packed decimal format, left-justified where hex a is
                 digit 0 and 0 in this field is null, zero fill to a byte boundary
ch               agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so               service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                 handling preference is skill level or greatest need.
da               direct agent calls handled first: 0 = no, 1 = yes.  This option is only used when agent call
                 handling preference is percent allocation
da_skill         agent's direct-agent skill (must be one of agent's 60 skills or 0 if no direct agent skill is
                 assigned)
percent1-        target percent of calls(0-100) handled by this agent which are for this skill. Used only when
60               call handling preference is percent allocation.
r1-60            flag indicating if level for this skill is reserve: 0 = not in reserve (regular agent), 1 = reserve
level1-60        skill level (1-16) or reserve level (1-2)
skill1-60        skill number, 0-999 (G3V8-G3V11), 0-2000 (MV2-CM5.2)
```

<a id="pdf-page-074"></a>

## PDF page 74

Source: SPI-SYN24; PDF page 74; extracted characters: 2471.

```text
3.3.12.2                     AGENTSK23 (New CM6.0)


                                                                   Switch    Vect    Skill
                                                 First Release     CM6.0     y       y
                                                 Last Release      CM6.3

With expansion to 120 skills this request may not fit into a single AGENTSK23 message.  If the agent has
more than 60 skills, a second message will be sent. The 1st message in the series covers skills 1 through
60 and the 2nd message covers skills 61 through 120, mapping to skills 1-60. The end bit is set for the last
message in a series.

    7   6    5   4   3   2   1    0   7   6   5   4    3   2   1   0   7   6    5   4   3   2   1   0   7    6   5   4   3   2   1    0
               time_tag                       AGENTSK23                                           seq num
                            seq num (cont)                                         tot siz                            tag
      pnumber             p1               p2               p3               p4              p5               p6               p7
          p8              p9               p10             p11              p12              p13             p14              p15
      ch     s   d   e     / /                          da_skl                                  percent1             r       level1
             o   a                                                                                                   1
     l    ia1                           skill1                                  percent2            r         level2          ia2     s
    1                                                                                               2                                 2
                      skill2 (cont)                            percent3             r        level3           ia3          skill3
                                                                                    3
                                                                    . . .
          . . .              percent59            r         level59         ia59                          skill59
                                                  5
                                                  9
            percent60             r        level60         ia60                          skill60
                                  6
                                  0
```

<a id="pdf-page-075"></a>

## PDF page 75

Source: SPI-SYN24; PDF page 75; extracted characters: 1999.

```text
AGENTSK23 (continued)

time_tag         seconds past minute when message was formed, 0-59
opcode           AGENTSK23 = 4 (0x04)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
tag              message tag, 0-255 (it will be returned in the switch response message).
pnumber          number of digits in agent position, 1-15
p1 - p15         agent position - EAS login ID in packed decimal format, left-justified where hex a is digit 0
                 and 0 in this field is null, zero fill to a byte boundary
ch               agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so               service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                 handling preference is skill level or greatest need.
da               direct agent calls handled first: 0 = no, 1 = yes.  This option is only used when agent call
                 handling preference is percent allocation
e                end bit, set when this is the last message of the set needed to satisfy the request
da_skl           agent's direct-agent skill (must be one of agent's 120 skills or 0 if no direct agent skill is
                 assigned)
percent1-        target percent of calls(0-100) handled by this agent which are for this skill. Used only when
60               call handling preference is percent allocation.
r1-60            flag indicating if level for this skill is reserve: 0 = not in reserve (regular agent), 1 = reserve
level1-60        skill level (1-16) or reserve level (1-2)
ia1-60           field that indicates whether the corresponding skill is interruptible. This field is only valid
                 when the corresponding “rx” (reserve) field is 0.

                  0    not an interruptible skill
                  1    auto-in-interrupt
                  2    manual-in-interrupt
                  3    notify-interrupt

skill1-60        skill number, 0-8000
```

<a id="pdf-page-076"></a>

## PDF page 76

Source: SPI-SYN24; PDF page 76; extracted characters: 2616.

```text
3.3.12.3                      AGENTSK24 (New CM7.0)


                                                                    Switch    Vect     Skill
                                                  First Release     CM7.0     y        y
                                                  Last Release
If the agent has more than 60 skills, a second message will be sent. The 1st message in the series covers
skills 1 through 60 and the 2nd message covers skills 61 through 120, mapping to skills 1-60. The end bit
is set for the last message in a series.

     7   6   5   4   3   2    1   0    7   6   5   4    3   2   1   0    7   6   5   4   3    2   1   0   7    6   5   4   3    2   1   0
               time_tag                        AGENTSK24                                            seq num
                             seq num (cont)                                          tot siz                            tag
        / / /        pnumber                p1               p2               p3               p4               p5               p6
          p7               p8               p9              p10              p11              p12              p13              p14
         p15              p16           ch     s   d    e    / /                           da_skl                            percent1
                                               o   a
        p1       r         level1           ia1                           skill1                                   percent2             r
      (cont)     1                                                                                                                      2
          level2           ia2                            skill2                                  percent3             r       level3
                                                                                                                       3
     l    ia3                            skill3                                  percent4             r         level4          ia4     …
     3                                                                                                4
                                                                     . . .

          . . .              percent59             r         level59         ia59                           skill59
                                                   5
                                                   9
            percent60             r         level60         ia60                           skill60
                                  6
                                  0
```

<a id="pdf-page-077"></a>

## PDF page 77

Source: SPI-SYN24; PDF page 77; extracted characters: 2001.

```text
AGENTSK24 (continued)

time_tag         seconds past minute when message was formed, 0-59
opcode           AGENTSK24 = 55 (0x37)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
tag              message tag, 0-255 (it will be returned in the switch response message).
pnumber          number of digits in agent position, 1-16
p1 – p16         agent position - EAS login ID in packed decimal format, left-justified where hex a is
                 digit 0 and 0 in this field is null, zero fill to a byte boundary.
ch               agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so               service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                 handling preference is skill level or greatest need.
da               direct agent calls handled first: 0 = no, 1 = yes.  This option is only used when agent call
                 handling preference is percent allocation
e                end bit, set when this is the last message of the set needed to satisfy the request
da_skl           agent's direct-agent skill (must be one of agent's 120 skills or 0 if no direct agent skill is
                 assigned)
percent1-        target percent of calls(0-100) handled by this agent which are for this skill. Used only when
60               call handling preference is percent allocation.
r1-60            flag indicating if level for this skill is reserve: 0 = not in reserve (regular agent), 1 = reserve
level1-60        skill level (1-16) or reserve level (1-2)
ia1-60           field that indicates whether the corresponding skill is interruptible. This field is only valid
                 when the corresponding “rx” (reserve) field is 0.

                  0    not an interruptible skill
                  1    auto-in-interrupt
                  2    manual-in-interrupt
                  3    notify-interrupt

skill1-60        skill number, 0-8000
```

<a id="pdf-page-078"></a>

## PDF page 78

Source: SPI-SYN24; PDF page 78; extracted characters: 3710.

```text
       3.3.13       SKILLADD8, SKILLADD23 and SKILLADD24
The Skill Add message is sent by the reporting adjunct to the switch. It is a request to change the skill
assignments for an agent position (LoginID).  At least one skill must be present.  All skills will be replaced.
Blanks (or holes) in the administration will be represented by skill=0. The expected response is an
RCODE  0, 1, 38, 45, 31 or 60 message.  The expected response also includes RCODE  62 and 63
messages.  An agent's skill assignment changes can take place while the agent is staffed.

If the agent is using the percent allocation call handling preference, the administration change for a
logged in agent means that accumulated metrics for the percent allocation on the switch will be zeroed
out and restarted with the new login.

3.3.13.1                    SKILLADD8 (New MV2)


                                                                 Switch    Vect   Skill
                                                First Release    MV2       y      y
                                                Last Release     CM5.2



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
             SKILLADD8                            tag                  pnumber            p1              p2              p3
          p4              p5              p6              p7              p8              p9              p10             p11
         p12             p13             p14             p15          ch     s   d   /                    da_skill
                                                                             o   a
             percent1            r        level1                           skill1                            percent2            r
                                 1                                                                                               2
          level2                           skill2
                                                                 .  .  .
            percent60            r        level60                         skill60
                                 6
                                 0

opcode             SKILLADD8 = 45 (0x2d)
tag                message tag, 0-255 (it will be returned in the switch response message)
pnumber            number of digits in agent position, 1-15
p1-p15             agent position - (0-9999999) login ID in packed decimal format, left-justified where hex a is
                   digit 0 and 0 in this field is null, zero fill to a byte boundary
ch                 agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so                 service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                   handling preference is skill level or greatest need.
da                 direct agent calls handled first: 0 = no, 1 = yes. This option is only used when agent call
                   handling preference is percent allocation.
da_skill           agent's direct-agent skill (must be one of agent's 60 skills or zero which indicates no DA
                   skill)
percent1-60        Percent allocation to apply to this skill, (0-100).  Used only when the call handling
                   preference is percent allocation and the level is not reserve (r bit is not set for the skill).
r1-60              flag indicating if the level for this skill is reserve: 0 = not in reserve (regular agent), 1 =
                   reserve
level1-60          skill level (1-16) or reserve level (1-2)
skill1-60          skill number, 0-999 (G3V8-G3V11), 0-2000 (MV2-CM5.2)
```

<a id="pdf-page-079"></a>

## PDF page 79

Source: SPI-SYN24; PDF page 79; extracted characters: 3999.

```text
3.3.13.2                     SKILLADD23 (New CM6.0)


                                                                  Switch    Vect    Skill
                                                 First Release    CM6.0     y       y
                                                 Last Release     CM6.3

With expansion to 120 skills this request may not fit into a single SKILLADD23 message.  If the agent has
more than 60 skills, a second message will be sent. The 1st message in the series covers skills 1 through
60 and the 2nd message covers skills 61 through 120, mapping to skills 1-60. The end bit is set for the last
message in a series.

    7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4    3   2   1   0   7   6    5   4    3   2   1   0
            SKILLADD23                           tag                   pnumber             p1               p2               p3
         p4              p5               p6              p7              p8               p9              p10              p11
         p12             p13             p14             p15          ch     s   d    e    / /                  da_skill
                                                                             o   a
      da_skill              percent1             r         level1         ia1                            skill1
       (cont)                                    1
             percent2            r         level2          ia2                           skill2                              . . .
                                 2
                                                                   .  .  .
         . . .             percent59             r        level59         ia5                           skill59
                                                 5                         9
                                                 9
            percent60            r        level60         ia60                          skill60
                                 6
                                 0


opcode              SKILLADD23 = 57(0x39)
tag                 message tag, 0-255 (it will be returned in the switch response message)
pnumber             number of digits in agent position, 1-15
p1-p15              agent position - EAS login ID in packed decimal format, left-justified where hex a is digit 0
                    and 0 in this field is null, zero fill to a byte boundary
ch                  agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
so                  service objective flag: 0 = not in use, 1 = in use.  This option is only used when agent call
                    handling preference is skill level or greatest need.
da                  direct agent calls handled first: 0 = no, 1 = yes. This option is only used when agent call
                    handling preference is percent allocation.
e                   end bit, set when this is the last message of the set needed to satisfy the request
da_skill            agent's direct-agent skill (must be one of agent's 120 skills or zero which indicates no DA
                    skill)
percent1-60         Percent allocation to apply to this skill, (0-100).  Used only when the call handling
                    preference is percent allocation and the level is not reserve (r bit is not set for the skill).
r1-60               flag indicating if the level for this skill is reserve: 0 = not in reserve (regular agent), 1 =
                    reserve
level1-60           skill level (1-16) or reserve level (1-2)
skill1-60           skill number, 0-8000
ia1-60              field that indicates whether the corresponding skill is interruptible. This field is only valid
                    when the corresponding “rx” (reserve) field is 0.

                     0    not an interruptible skill
                     1    auto-in-interrupt
                     2    manual-in-interrupt
                     3    notify-interrupt
```

<a id="pdf-page-080"></a>

## PDF page 80

Source: SPI-SYN24; PDF page 80; extracted characters: 2345.

```text
3.3.13.3                      SKILLADD24 (New CM7.0)


                                                                    Switch    Vect    Skill
                                                  First Release     CM7.0     y       y
                                                  Last Release

With expansion to 120 skills this request may not fit into a single SKILLADD23 message.  If the agent has
more than 60 skills, a second message will be sent. The 1st message in the series covers skills 1 through
60 and the 2nd message covers skills 61 through 120, mapping to skills 1-60. The end bit is set for the last
message in a series.

     7   6   5   4   3   2   1    0   7   6   5   4    3   2   1   0    7   6   5   4    3   2   1    0   7   6   5    4   3   2   1   0
            SKILLADD24                             tag                     / / /         pnumber               p1               p2
          p3              p4               p5               p6               p7               p8               p9               p10
         p11              p12              p13              p14              p15              p16          ch     s    d   e     / /   d
                                                                                                                  o    a
                    da_skill (cont)                            percent1              r         level1          ia1           skill1
                                                                                    1
             skill1 (cont)                    percent2              r         level2          ia2                   skill2
                                                                   2
     skill2 (cont)           percent3              r         level3          ia3                            skill3
                                                   3
                                                                    .  .  .
          . . .              percent59             r        level59          ia59                          skill59
                                                   5
                                                   9
            percent60             r        level60          ia60                          skill60
                                  6
                                  0
```
