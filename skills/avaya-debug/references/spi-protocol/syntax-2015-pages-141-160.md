---
title: "SPI-SYN24 - complete source pages 141-160"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 141-160

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-141"></a>

## PDF page 141

Source: SPI-SYN24; PDF page 141; extracted characters: 2374.

```text
3.4.2.2                    ALOGON23 (New CM6.0)


                                                              Switch   Vect    Skill
                                              First Release   CM6.0    y/n     y/n
                                              Last Release    CM6.3

3.4.2.2.1          ALOGON23, without EAS (New CM6.0)

The changes for ALOGON23 are for the EAS version of ALOGON only. Since both the non-EAS version
and the EAS version use the same opcode, the non-EAS version is also to use the new opcode for SPI
language 23.

    7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4   3  2   1   0
              time_tag                     ALOGON23                                        seq num
                          seq num (cont)                                     tot siz            p   x   f   s       / / / /
               loc_id                pnumber                                         pos
      dnumber            d1             d2             d3              d4             d5             d6              d7
         d8              d9

time_tag      seconds past minute when event occurred, 0-59
opcode        ALOGON23 = 5 (0x05)
seq_num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
p             change pending; 0 = no changes pending, 1 = a change is pending for this agent. (If pending
              is due to MVAGSTFD, the ALOGON23 message is not sent until the agent ends
              call/ACW/DAC.)
x             translation; 0 = normal logon, 1 = translation pump-up status (agent logged in or AAS agent
              released from maintenance busy) or DME change.
f             0 = agent successfully logged into split, 1 = login failed (used with MVAGSTFD, not login from
              phone)
s             0 = non-EAS, no skills in message.
loc_id        location id number, 0-44 (G3V8-G3V11), 0-250 (MV2 and later), 0 is default for no location id
pnumber       number of digits in "pos", will always be 5 for non-EAS
pos           agent position, 1-10000.
dnumber       number of digits in agent logon ID, 1-9
d1-d9         digits of the logon ID without EAS, packed decimal format, left-justified where 0 is null and hex
              a is digit 0, zero fill digits to a byte boundary, (for example logid 4000 will be 4aaa0).
```

<a id="pdf-page-142"></a>

## PDF page 142

Source: SPI-SYN24; PDF page 142; extracted characters: 2217.

```text
3.4.2.2.2             ALOGON23, with EAS (New CM6.0)

     7   6  5   4   3   2   1    0   7   6    5   4   3    2   1   0    7   6   5   4    3   2   1    0   7   6    5   4     3   2   1    0
              time_tag                        ALOGON23                                               seq num
                            seq num (cont)                                          tot siz               p   x           snumber
                loc_id                 pnumber              p1               p2               p3                p4                p5
         p6               p7               p8               p9              p10               p11               p12               p13
         p14             p15           dnumber              d1               d2               d3                d4                d5
         d6               d7               d8               d9              d10               d11               d12               d13
         d14             d15         d   s     ch     e     / /                            da_skl                            f   percent1
                                     a   o                                                                                   1
      percent1      r       level1        ia1                             skill1                           f            percent2
        (cont)      1                                                                                      2
     r      level2        ia2                            skill2                           f            percent3              r      . . .
     2                                                                                    3                                  3
                                                                     .  .  .
         . . .      f           percent59             r       level59       ia59                            skill59
                    5                                 5
                    9                                 9
     f          percent60             r     level60       ia60                             skill60
     6                               6
     0                               0
```

<a id="pdf-page-143"></a>

## PDF page 143

Source: SPI-SYN24; PDF page 143; extracted characters: 3152.

```text
ALOGON23 (continued)

time_tag           seconds past minute when event occurred, 0-59
opcode             ALOGON23 = 5 (0x05)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
p                  change pending; 0 = no changes pending, 1 = a change is pending for this agent.
x                  translation; 0 = normal logon, 1 = translation pump-up status (agent logged in or AAS
                   agent released from maintenance busy) or DME change.
snumber            number of skills in the message (1-60)
loc_id             location id number, 0-44 (G3V8-G3V11), 0-250 (MV2 and later), 0 is default for no location
                   id
pnumber            number of digits in agent position, 1-15
p1-p15             agent position, with EAS login ID in packed decimal format, left-justified where 0 is null
                   and hex a is digit 0, zero fill to a byte boundary.
dnumber            number of digits in the physical extension, 1-15
d1-d15             the digits of the physical extension in packed decimal format, left-justified where 0 is null
                   and hex a is digit 0, zero fill to a byte boundary.
da                 flag indicating direct agent calls should be received first.  Valid only when call handling
                   preference is percent allocation.
so                 service objective flag: 0=not in use, 1=in use.  Valid only when call handling preference is
                   skill level or greatest need.
ch                 agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
e                  end bit, set when this is the last message of the set needed to satisfy the request
da_skill           agent's direct-agent skill (must be one of agent's 120 skills)
f 1-60             logon fail bits.  For non-zero skills, look at this bit to see whether login to pending skill has
                   failed. 0 = logon to pending skill succeeded, 1 = logon failed.  It is possible to send all
                   skills with fail bits set.  f1=skill1, f2=skill2, etc.
percent 1-60       percent allocation for this skill, 0-100.  Must be 0 when skill level is reserve (rN=1).  Must
                   be non-zero when call handling preference is percent allocation and skill level is not
                   reserve (rN=0).  Valid only when call handling preference is percent allocation.
r 1-60             flag indicating level is reserve level(r=1) rather than skill level(r=0).
level 1-60         skill level (0-15 representing levels 1-16) or reserve level (1-2).
ia 1-60            field that indicates whether the corresponding skill is interruptible. This field is only valid
                   when the corresponding “rx” (reserve) field is 0.
                     0    not an interruptible skill
                     1    auto-in-interrupt
                     2    manual-in-interrupt
                     3    notify-interrupt
skill 1-60         skills 1-8000 assigned to the agent in the order administered. Sending zero indicates no
                   skill administered (or skill not measured by CMS).
```

<a id="pdf-page-144"></a>

## PDF page 144

Source: SPI-SYN24; PDF page 144; extracted characters: 2529.

```text
3.4.2.3                    ALOGON24 (New CM7.0)


                                                              Switch    Vect   Skill
                                              First Release   CM7.0     y/n    y/n
                                              Last Release

3.4.2.3.1           ALOGON24, without EAS (New CM7.0)



    7   6   5   4   3   2  1   0   7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                     ALOGON24                                        seq num
                          seq num (cont)                                     tot siz             p   x   f  s       / / / /
              / / / / / / / /         / / /                        loc_id                           / / /       pnumber
         p1              p2             p3              p4             p5             / / / /       / / /       dnumber
         d1              d2             d3              d4             d5             d6              d7             d8
         d9             d10             d11            d12            d13             d14            d15             d16
           / / / / / /                                    tenant

time_tag      seconds past minute when event occurred, 0-59
opcode        ALOGON24 = 40 (0x28)
seq_num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
p             change pending; 0 = no changes pending, 1 = a change is pending for this agent. (If pending
              is due to MVAGSTFD, the ALOGON24 message is not sent until the agent ends
              call/ACW/DAC.)
x             translation; 0 = normal logon, 1 = translation pump-up status (agent logged in or AAS agent
              released from maintenance busy) or DME change.
f             0 = agent successfully logged into split, 1 = login failed (used with MVAGSTFD, not login
              from phone)
s             0 = non-EAS, no skills in message.
loc_id        location id number, 0-2000,  0 is default for no location id (13 bits for future expansion)
pnumber       number of digits in "pos", will always be 5 for non-EAS
pos           agent position, 1-10000.
dnumber       number of digits in agent logon ID, 1-16
d1-d16        digits of the logon ID without EAS, packed decimal format, left-justified where 0 is null
              and hex a is digit 0, zero fill digits to a byte boundary, (for example logid 4000 will be
              4aaa0).
tenant        Station tenant number, 1-250

-
```

<a id="pdf-page-145"></a>

## PDF page 145

Source: SPI-SYN24; PDF page 145; extracted characters: 3891.

```text
3.4.2.3.2               ALOGON24, with EAS (New CM7.0)

     7    6   5    4   3    2    1   0    7    6    5   4    3    2    1   0    7    6    5    4   3    2    1    0    7    6   5    4    3    2    1    0
                 time_tag                           ALOGON24                                                    seq num
                                seq num (cont)                                                tot siz                  p    x           snumber
                / / / / / / / /              / / /                                loc_id                                  / / /           pnumber
           p1                p2                 p3                 p4                 p5                  p6                 p7                  p8
           p9               p10                p11                 p12                p13                p14                p15                 p16
        / / /          dnumber                  d1                 d2                 d3                  d4                 d5                  d6
           d7                d8                 d9                 d10                d11                d12                d13                 d14
          d15               d16                   / / / / / /                            tenant                        d    s     ch      e      / /     d
                                                                                                                       a    o                            a
                       da_skl (cont)                              / / / /           / / /          anumber                         attribute1
                attribute2                            attribute3                            attribute4                             attribute5
                attribute6                            attribute7                            attribute8                                . . .
               attribute15                           attribute16                           attribute17                            attribute18
               attribute 19                         attribute 20                     / / / /        f             percent1                r      level1
                                                                                                   1                                      1
     l     ia1                               skill1                              f             percent2                r        level2          ia2      s
     1                                                                           2                                     2                                 2
                         skill2 (cont)                        f             percent3                r        level3          ia3             skill3
                                                              3                                     3
               skill3 (cont)               f             percent4                r        level4          ia4                      skill4
                                           4                                     4
      skill4 (cont)     f             percent5                r        level5          ia5                               skill5
                        5                                     5
                                                                             .  .  .

          .  .  .      f             percent39               r       level39         ia39                               skill39
                       3                                     3
                       9                                     9
     f            percent40               r       level40         ia40                               skill40
     4                                    4
     0                                    0
```

<a id="pdf-page-146"></a>

## PDF page 146

Source: SPI-SYN24; PDF page 146; extracted characters: 3396.

```text
ALOGON24 (continued)

time_tag            seconds past minute when event occurred, 0-59
opcode              ALOGON24 = 40 (0x28)
seq num             sequence number, 0-0xffff ffff
tot siz             total size in bytes, 1-255
p                   change pending; 0 = no changes pending, 1 = a change is pending for this agent.
x                   translation; 0 = normal logon, 1 = translation pump-up status (agent logged in or AAS
                    agent released from maintenance busy) or DME change.
snumber             number of skills in the message (1-40)
loc_id              location id number, 0-2000,  0 is default for no location id (13 bits for future
                    expansion)
pnumber             number of digits in agent position, 1-16
p1-p16              agent position, with EAS login ID in packed decimal format, left-justified where 0 is
                    null and hex a is digit 0, zero fill to a byte boundary.
dnumber             number of digits in the physical extension, 1-16
d1-d16              the digits of the physical extension in packed decimal format, left-justified where 0
                    is null and hex a is digit 0, zero fill to a byte boundary.
da                  flag indicating direct agent calls should be received first.  Valid only when call handling
                    preference is percent allocation.
so                  service objective flag: 0=not in use, 1=in use.  Valid only when call handling preference is
                    skill level or greatest need.
ch                  agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
e                   end bit, set when this is the last message of the set needed to satisfy the request
da_skill            agent's direct-agent skill (must be one of agent's 120 skills)
tenant              Agent tenant number, 1-250
anumber             number of alphanumeric characters in attribute, 0-20
attribute1-20       Agent attribute, a 20 character alphanumeric string
f 1-40              logon fail bits.  For non-zero skills, look at this bit to see whether login to pending skill has
                    failed. 0 = logon to pending skill succeeded, 1 = logon failed.  It is possible to send all
                    skills with fail bits set.  f1=skill1, f2=skill2, etc.
percent 1-40        percent allocation for this skill, 0-100.  Must be 0 when skill level is reserve (rN=1).  Must
                    be non-zero when call handling preference is percent allocation and skill level is not
                    reserve (rN=0).  Valid only when call handling preference is percent allocation.
r 1-40              flag indicating level is reserve level(r=1) rather than skill level(r=0).
level 1-40          skill level (0-15 representing levels 1-16) or reserve level (1-2).
ia 1-40             field that indicates whether the corresponding skill is interruptible. This field is only valid
                    when the corresponding “rx” (reserve) field is 0.
                      0   not an interruptible skill
                      1   auto-in-interrupt
                      2   manual-in-interrupt
                      3   notify-interrupt
skill 1-40          skills 1-8000 assigned to the agent in the order administered. Sending zero indicates no
                    skill administered (or skill not measured by the reporting adjunct).
```

<a id="pdf-page-147"></a>

## PDF page 147

Source: SPI-SYN24; PDF page 147; extracted characters: 3327.

```text
       3.4.3         ALOGOFF20 and ALOGOFF24
An Agent Logoff message is sent by the switch whenever an agent logs off. The reporting adjunct will
update the status of the agent position to reflect that the position is no longer staffed.

3.4.3.1                     ALOGOFF20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0
              time_tag                     ALOGOFF20                                         seq num
                           seq num (cont)                                      tot siz               pnumber        pos or p1-
                                                                                                                       p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                    / / / /       reason

time_tag          seconds past minute when event occurred, 0-59
opcode            ALOGOFF20 = 207 (0xcf)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
reason            reason code (0-9); 0 is the default reason code.

3.4.3.2                     ALOGOFF24 (New CM7.0)


                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release

An Agent Logoff message is sent by the switch whenever an agent logs off. The reporting adjunct will
update the status of the agent position to reflect that the position is no longer staffed.

    7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                     ALOGOFF24                                         seq num
                           seq num (cont)                                      tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                / / / /         / / / /       reason

time_tag          seconds past minute when event occurred, 0-59
opcode            ALOGOFF24 = 57 (0x39)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                  in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                  null, zero fill to a byte boundary
reason            reason code (0-9); 0 is the default reason code.
```

<a id="pdf-page-148"></a>

## PDF page 148

Source: SPI-SYN24; PDF page 148; extracted characters: 2818.

```text
       3.4.4         AVAIL22, AVAIL23 and AVAIL24
The Agent State Change message is sent by the switch when an agent position changes state.  The
agent position will change states when the agent's work mode or call state changes.

This is a variable length message based on "pnumber" and whether or not EAS is active.  Prior to
AVAIL23, with EAS, this message will contain 8 additional bytes for the "skill-map". Starting with
AVAIL23 and the expansion to 120 skills, with EAS, this message will contain 16 additional bytes for the
expanded “skill-map”.

3.4.4.1                     AVAIL22 (New CM5.2)


                                                                 Switch   Vect    Skill
                                                First Release    CM5.2    y/n     y/n
                                                Last Release     CM5.2



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                       AVAIL22                                          seq num
                           seq num (cont)                                       tot siz                pnumber        pos or p1-
                                                                                                                         p15
                                pos (non-EAS) or p1-p15 (EAS) (cont)                                 m           / / / / / / /
         / / / /                                                       skill-map
                                                           skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AVAIL22 = 1 (0x01)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This flag
                  notifies IQ tracking that this astate change is not for a call release.
skill-map         one bit for each staffed skill. The skills are mapped left to right and correspond to the order
                  of the skills in the ALOGON message.
                  −    1 means agent is available for this skill
                  −    0 means agent is not available for this skill or the skill is not assigned/measured; The
                       reporting adjunct will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-149"></a>

## PDF page 149

Source: SPI-SYN24; PDF page 149; extracted characters: 2767.

```text
3.4.4.2                      AVAIL23 (New CM6.0)


                                                                  Switch    Vect    Skill
                                                 First Release    CM6.0     y/n     y/n
                                                 Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0
               time_tag                        AVAIL23                                           seq num
                            seq num (cont)                                        tot siz               pnumber         pos or p1-
                                                                                                                            p15
                                pos (non-EAS) or p1-p15 (EAS) (cont)                                   m    ia           / / / / /
                                                                skill-map
                                                            skill-map (cont)
                                                            skill-map (cont)
                                            skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AVAIL23 = 14 (0x0e)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This flag
                  notifies IQ tracking that this astate change is not for a call release.
ia                flag indicating agent became available due to being interrupted while in Aux with an
                  Interruptible Aux reason code.

                    0    N/A (agent was not interrupted while in Aux)
                    1    auto-in-interrupt
                    2    manual-in-interrupt
                    3    notify-interrupt

skill-map         one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                  the order of the skills in the ALOGON message.
                  −     1 means agent is available for this skill
                  −     0 means agent is not available for this skill or the skill is not assigned/measured; The
                        reporting adjunct will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-150"></a>

## PDF page 150

Source: SPI-SYN24; PDF page 150; extracted characters: 2610.

```text
3.4.4.3                     AVAIL24 (New CM7.0)


                                                                 Switch    Vect    Skill
                                                First Release    CM7.0     y/n     y/n
                                                Last Release



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        AVAIL24                                         seq num
                           seq num (cont)                                       tot siz                 / / /        pnumber
                           pos (non-EAS) or p1-p16 (EAS)                                 / / / /     m     ia          / / / / /
                                                               skill-map
                                                            skill-map (cont)
                                                            skill-map (cont)
                                           skill-map (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AVAIL24 = 58 (0x3a)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
m                 flag to indicate the agent returned to available because of Multiple Call Handling.  This flag
                  notifies IQ tracking that this astate change is not for a call release.
ia                flag indicating agent became available due to being interrupted while in Aux with an
                  Interruptible Aux reason code.

                    0   N/A (agent was not interrupted while in Aux)
                    1   auto-in-interrupt
                    2   manual-in-interrupt
                    3   notify-interrupt

skill-map         (EAS) one bit for each staffed skill (1-120). The skills are mapped left to right and
                  correspond to the order of the skills in the ALOGON message.
                  −    1 means agent is available for this skill
                  −    0 means agent is not available for this skill or the skill is not assigned/measured; The
                       reporting adjunct will report the agent activity for this skill as OTHER.
```

<a id="pdf-page-151"></a>

## PDF page 151

Source: SPI-SYN24; PDF page 151; extracted characters: 2222.

```text
       3.4.5         ACD20 and ACD24
This is a variable length message based on "pnumber" and "u".

3.4.5.1                     ACD20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                        ACD20                                          seq num
                           seq num (cont)                                      tot siz               pnumber        pos or p1-
                                                                                                                       p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                  d     r   u       / / / /
     /                           net_id                                                         seq
                                                             timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            ACD20 = 209 (0xd1)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call
                  1 means call is outbound (ACDO)
                  2 means call is inbound (ACD, ACDI)
r                 reconnect; 1 means the ACD call is being reconnected after being on hold.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-152"></a>

## PDF page 152

Source: SPI-SYN24; PDF page 152; extracted characters: 1957.

```text
3.4.5.2                    ACD24 (New CM7.0)


                                                               Switch   Vect    Skill
                                              First Release    CM7.0    y/n     y/n
                                              Last Release



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4  3   2   1   0
              time_tag                        ACD24                                         seq num
                           seq num (cont)                                     tot siz                / / /       pnumber
                          pos (non-EAS) or p1-p16 (EAS)                               / / / /       d     r   u       / / / /
     /                           net_id                                                        seq
                                                            timestamp

time_tag         seconds past minute when event occurred, 0-59
opcode           ACD24 = 59 (0x3b)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
pnumber          number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16       agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                 in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                 null, zero fill to a byte boundary
d                direction of call
                 1 means call is outbound (ACDO)
                 2 means call is inbound (ACD, ACDI)
r                reconnect; 1 means the ACD call is being reconnected after being on hold.
u                flag indicating that the UCID fields (net_id, seq and timestamp) are present
net_id           network entity identifier, 1-32767
seq              call sequence number, 0-65535
timestamp        unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-153"></a>

## PDF page 153

Source: SPI-SYN24; PDF page 153; extracted characters: 2967.

```text
       3.4.6         ACW22 and ACW24
This is a variable length message based on "pnumber" and "u".

3.4.6.1                     ACW22 (New CM5.2)


                                                                Switch    Vect   Skill
                                               First Release    CM5.2     y/n    y/n
                                               Last Release     CM6.3



     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                         ACW22                                          seq num
                           seq num (cont)                                      tot siz                pnumber        pos or p1-
                                                                                                                        p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                   d     r   k   e   u   h   w
     m           / / / / / / /      /                            net_id                                         seq
              seq (cont)                                                     timestamp
          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            ACW22 = 255 (0xff)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call
                  −    0 means no call (ACW)
                  −    1 means call is outbound (ACWO)
                  −    2 means call is inbound (ACWI)
r                 reconnect; 1 means the ACWO/ACWI call is being reconnected after being on hold.
k                 keyboard dialed; 1 means the ACWO call was placed by an adjunct on behalf of the agent.
e                 external call; 1 = external off-premises call dialed by agent or on behalf of agent. DCS calls
                  are considered off-premises.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
h                 flag to indicate the agent has just put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
m                 flag to indicate the agent called a measured internal destination. This flag will only be set if
                  the "e" flag is not set, that is, the call is not external.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-154"></a>

## PDF page 154

Source: SPI-SYN24; PDF page 154; extracted characters: 2724.

```text
3.4.6.2                      ACW24 (New CM7.0)


                                                                Switch   Vect    Skill
                                               First Release    CM7.0    y/n     y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                        ACW24                                          seq num
                           seq num (cont)                                      tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                 / / / /      d     r   k   e   u   h   w
    m            / / / / / / /      /                            net_id                                         seq
              seq (cont)                                                     timestamp
          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            ACW24 = 60 (0x3c)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                  in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                  null, zero fill to a byte boundary
d                 direction of call
                  −    0 means no call (ACW)
                  −    1 means call is outbound (ACWO)
                  −    2 means call is inbound (ACWI)
r                 reconnect; 1 means the ACWO/ACWI call is being reconnected after being on hold.
k                 keyboard dialed; 1 means the ACWO call was placed by an adjunct on behalf of the agent.
e                 external call; 1 = external off-premises call dialed by agent or on behalf of agent. DCS calls
                  are considered off-premises.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
h                 flag to indicate the agent has just put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
m                 flag to indicate the agent called a measured internal destination. This flag will only be set if
                  the "e" flag is not set, that is, the call is not external.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-155"></a>

## PDF page 155

Source: SPI-SYN24; PDF page 155; extracted characters: 3039.

```text
       3.4.7         AUX22, AUX23 and AUX24
This is a variable length message based on "pnumber" and "u".

3.4.7.1                     AUX22 (New CM5.2)


                                                                Switch    Vect    Skill
                                               First Release    CM5.2     y/n     y/n
                                               Last Release     CM5.2



     7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        AUX22                                          seq num
                           seq num (cont)                                       tot siz               pnumber        pos or p1-
                                                                                                                         p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                   d     r   k   e   u   h   w
     m           / / / / / / /                 reason               /                             net_id
                                 seq                                                         timestamp
                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUX22 = 3 (0x03)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call:
                   0    no call (AUX)
                   1    call is outbound (AUXO)
                   2    call is inbound (AUXI)
r                 reconnect; 1 means the AUXO/AUXI call is being reconnected after being on hold.
k                 keyboard dialed; 1 means the AUXO call was placed by an adjunct on behalf of the agent.
e                 external call; 1 = external off-premises call dialed by agent or on behalf of agent. DCS calls
                  are considered off-premises.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
h                 flag to indicate the agent has put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
m                 flag to indicate the agent called a measured internal destination. This flag will only be set if
                  the "e" flag is not set, that is, the call is not external.
reason            reason code (0-99); 0 is the default reason code.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-156"></a>

## PDF page 156

Source: SPI-SYN24; PDF page 156; extracted characters: 3202.

```text
3.4.7.2                     AUX23 (New CM6.0)


                                                                Switch    Vect    Skill
                                                First Release   CM6.0     y/n     y/n
                                                Last Release    CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        AUX23                                           seq num
                           seq num (cont)                                       tot siz                pnumber        pos or p1-
                                                                                                                         p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                   d      r   k   e   u   h   w
     m   i           / / / / / / /                reason             /                            net_id
                                 seq                                                          timestamp
                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUX23 = 15 (0x0F)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
d                 direction of call:
                    0   no call (AUX)
                    1   call is outbound (AUXO)
                    2   call is inbound (AUXI)
r                 reconnect; 1 means the AUXO/AUXI call is being reconnected after being on hold.
k                 keyboard dialed; 1 means the AUXO call was placed by an adjunct on behalf of the agent.
e                 external call; 1 = external off-premises call dialed by agent or on behalf of agent. DCS calls
                  are considered off-premises.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
h                 flag to indicate the agent has put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
m                 flag to indicate the agent called a measured internal destination. This flag will only be set if
                  the "e" flag is not set, that is, the call is not external.
i                 flag that indicates that the AUX reason code entered is interruptible. The flag is to be set to
                  1 when the agent used an AUX reason code that has the Aux Work/Interruptible field on
                  the Reason Code Names screen set to “y”.
reason            reason code (0-99); 0 is the default reason code.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-157"></a>

## PDF page 157

Source: SPI-SYN24; PDF page 157; extracted characters: 3053.

```text
3.4.7.3                     AUX24 (New CM7.0)



                                                                Switch    Vect   Skill
                                               First Release    CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0
              time_tag                         AUX24                                          seq num
                           seq num (cont)                                      tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                 / / / /      d      r  k   e   u   h   w
    m    i         / / / / / /                 reason               /                            net_id
                                 seq                                                         timestamp
                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUX24 = 61 (0x3d)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call:
                   0    no call (AUX)
                   1    call is outbound (AUXO)
                   2    call is inbound (AUXI)
r                 reconnect; 1 means the AUXO/AUXI call is being reconnected after being on hold.
k                 keyboard dialed; 1 means the AUXO call was placed by an adjunct on behalf of the agent.
e                 external call; 1 = external off-premises call dialed by agent or on behalf of agent. DCS calls
                  are considered off-premises.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
h                 flag to indicate the agent has put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
m                 flag to indicate the agent called a measured internal destination. This flag will only be set if
                  the "e" flag is not set, that is, the call is not external.
i                 flag that indicates that the AUX reason code entered is interruptible. The flag is to be set to
                  1 when the agent used an AUX reason code that has the Aux Work/Interruptible field on
                  the Reason Code Names screen set to “y”.
reason            reason code (0-99); 0 is the default reason code.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-158"></a>

## PDF page 158

Source: SPI-SYN24; PDF page 158; extracted characters: 2321.

```text
       3.4.8        OTHER22 and OTHER24
This is a variable length message based on "pnumber".

3.4.8.1                     OTHER22 (New CM5.2)


                                                               Switch    Vect    Skill
                                               First Release   CM5.2     y/n     y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0  7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       OTHER22                                         seq num
                           seq num (cont)                                      tot siz               pnumber        pos or p1-
                                                                                                                       p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                  d        / / /    u   h   w
     /                           net_id                                                      seq_num
                                                             timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            OTHER22 = 250 (0xfa)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                  packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call
                  −    0 means no call
                  −    1 means call is outbound
                  −    2 means call is inbound
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present.
h                 flag to indicate the agent has put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-159"></a>

## PDF page 159

Source: SPI-SYN24; PDF page 159; extracted characters: 2079.

```text
3.4.8.2                    OTHER24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
              time_tag                       OTHER24                                         seq num
                           seq num (cont)                                     tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                / / / /      d        / / /    u   h   w
    /                            net_id                                                        seq
                                                            timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            OTHER24 = 62 (0x3e)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                  in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                  null, zero fill to a byte boundary
d                 direction of call
                  −    0 means no call
                  −    1 means call is outbound
                  −    2 means call is inbound
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present.
h                 flag to indicate the agent has put a call on hold.
w                 flag to indicate the observer is waiting for another call to observe.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-160"></a>

## PDF page 160

Source: SPI-SYN24; PDF page 160; extracted characters: 2911.

```text
       3.4.9          DIGITS20 and DIGITS24
The Digits Dialed message is sent by the switch for outbound calls to tell the reporting adjunct what
digits the agent dialed (trunk/feature access codes and authorization/account codes not included).  This
sends ISDN SID/ANI for inbound calls.

Call Work Codes are only sent when the agent is talking on an ACD call or is in ACW for a call.

These are variable-length messages based on the length field. The first twelve bytes will always be sent.

3.4.9.1                      DIGITS20 (New CM3.1)


                                                                  Switch    Vect    Skill
                                                 First Release    CM3.1     y/n     y/n
                                                 Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3    2   1   0   7   6   5   4   3   2   1   0
               time_tag                        DIGITS20                                          seq num
                            seq num (cont)                                        tot siz                type(0-4)       pnumber
                                            parameter or p1-p15 (type 0,3)                                                  / / / /
               dnumber                     d1              d2              d3               d4              d5               d6
          d7              d8               d9             d10              d11             d12             d13              d14
         d15              d16             d17             d18              d19             d20             d21              d22
         d23              d24        u                             net_id                                           seq
              seq (cont)                                                       timestamp
           timestamp (cont)



     7   6   5   4   3   2   1   0   7   6   5    4   3   2   1   0   7   6   5   4   3   2    1   0   7   6   5   4   3   2   1   0
               time_tag                        DIGITS20                                          seq num
                            seq num (cont)                                        tot siz                 type(5)        pnumber
                                            parameter or p1-p15 (type 0,3)                                                  / / / /
               dnumber                             d1                               d2                              d3
                                                                  .  .  .
                 d93                              d94                              d95                              d96
     u                             net_id                                                          seq
                                                               timestamp
```
