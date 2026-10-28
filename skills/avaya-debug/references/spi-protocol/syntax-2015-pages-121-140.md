---
title: "SPI-SYN24 - complete source pages 121-140"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 121-140

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-121"></a>

## PDF page 121

Source: SPI-SYN24; PDF page 121; extracted characters: 2856.

```text
ADMNAM20 (continued)

time_tag                seconds past minute when messages was formed, 0-59
opcode                  ADMNAM20 = 201 (0xc9)
seq num                 sequence number, 0-0xffff ffff
tot siz                 total size of message in bytes; 1-255
tag                     message tag, 0-255 from REQNAM20 message or 0 if admin change update
e                       end bit, set when this is the last message of the set needed to satisfy the request
r                       reason bit, 0 = response to sync request, 1 = admin change update
n1                      name-1 flag, 0 = name-1 NOT in message, 1 = name-1 IS in message
n2                      name-2 flag, 0 = name-2 NOT in message, 1 = name-2 IS in message
obj type                type of object which is listed:

                          obj type    entity
                          0           Vector Names
                          1           Trunk Group Names
                          2           Hunt Group Names
                          3           VDN (iln) Names
                          4           Agent Loginid Names

b                       Beginning bit, set when this is the first message of the set needed to satisfy the
                        request. This bit is only set for CM FP4 or later. (obj types 0-3 only)
obj id                  the identifying number for the object (obj types 0-3 only)

                          obj type    entity                      obj id values
                          0           Vector Names                1-2000 (CM3.1-CM5.2)
                                                                  1-8000 (CM6.0 and later)
                          1           Trunk Group Names           1-2000
                          2           Hunt Group Names            1-2000 (CM3.1-CM5.2)
                                                                  1-8000 (CM6.0 and later)
                          3           VDN (iln) Names             1-20000 (CM3.1-CM5.2)
                                                                  1-30000 (CM6.0 and later)
pnumber                 number of digits in agent position, 1-15 (obj type 4 only)
p1-p15                  agent position - with EAS login ID in packed decimal format, left-justified where hex a
                        is digit 0 and 0 in this field is null, zero fill position to a byte boundary (obj type 4 only)
name 1 len M            number of bytes of object data, (0-27)
name 1 byte X           object data bytes (ASCII encoded name1 data bytes)
name 2 len N            number of bytes of object data, (0-81)
name 2 script tag       UTF-8 script tag for name2 data bytes. The script tag represents a writing script. See
                        the following table for the actual values, 1-32.
name 2 byte X           object data bytes (UTF-8 encoded name2 data bytes)
```

<a id="pdf-page-122"></a>

## PDF page 122

Source: SPI-SYN24; PDF page 122; extracted characters: 1708.

```text
Script tag                                                Writing script
1             Basic Latin
2             Latin-1 Supplement
3             Latin Extended-A
4             Latin Extended-B
5             Greek and Coptic
6             Cyrillic and Cyrillic Supplementary
7             Armenian
8             Hebrew
9             Arabic
10            Devanagari
11            Bengali
12            Gurmukhi
13            Gujarati
14            Oriya
15            Tamil
16            Telugu
17            Kannada
18            Malayalam
19            Sinhala
20            Thai
21            Lao
22            Myanmar
23            Georgian
24            Tagalog
25            Khmer
26            Halfwidth and Fullwidth Forms
27            Hiragana, Katakana, Katakana Phonetic Extensions             CJKV Radicals Supplement
                                                                           Kangxi Radicals
28                                                                         CJKV Symbols and Punctuation
                                                                           Enclosed CJK Letters and Months
29            Bopomofo, Bopomofo Extended                                  CJKV Compatibility
30                                                                         CJKV Unified Ideographs Extension A
                                                                           JCKV Unified Ideographs
31                                                                         CJK Compatibility Ideographs
                                                                           CJK Compatibility Forms
32            Hangul Jamo, Hangul Compatibilty Jamo, Hangul Syllables
```

<a id="pdf-page-123"></a>

## PDF page 123

Source: SPI-SYN24; PDF page 123; extracted characters: 2225.

```text
3.3.26.2                       ADMNAM24 (New CM7.0)


                                                                       Switch     Vect    Skill
                                                     First Release     CM7.0      y       y/n
                                                     Last Release



     7   6    5   4   3    2   1    0   7    6   5   4    3   2    1   0    7   6   5    4   3    2   1   0    7   6    5   4    3   2   1    0
                time_tag                         ADMNAM24                                               seq num
                              seq num (cont)                                            tot siz                              tag
     e   r    n   n      obj type
              1   2
                                                        for vector, trunk, hunt and VDN



     b            / / / / / / /         /                                obj_id                                        name 1 len M
             name 1 byte 1                      name 1 byte 2                      name 1 byte 3                             * * *
            name 1 byte M                        name 2 len N                     name 2 script tag                    name 2 byte 1
             name 2 byte 2                      name 2 byte 3                            * * *                         name 2 byte N


                                                                     for agent


     b           / / / / / /            pnumber                 p1               p2                p3                p4               p5
          p6                p7                p8                p9               p10              p11               p12               p13
          p14              p15               p16              / / / /               Name 1 len M                       Name 1 byte 1
            Name 1 bytes 2                      Name 1 byte 3                            * * *                        Name 1 byte M
             Name 2 len N                     Name 2 script tag                    Name 2 byte 1                       Name 2 byte 2
            Name 2 byte 3                             * * *                        Name 2 byte N
```

<a id="pdf-page-124"></a>

## PDF page 124

Source: SPI-SYN24; PDF page 124; extracted characters: 2832.

```text
ADMNAM24 (continued)

time_tag                seconds past minute when messages was formed, 0-59
opcode                  ADMNAM24 = 43 (0x2b)
seq num                 sequence number, 0-0xffff ffff
tot siz                 total size of message in bytes; 1-255
tag                     message tag, 0-255 from REQNAM20 message or 0 if admin change update
e                       end bit, set when this is the last message of the set needed to satisfy the request
r                       reason bit, 0 = response to sync request, 1 = admin change update
n1                      name-1 flag, 0 = name-1 NOT in message, 1 = name-1 IS in message
n2                      name-2 flag, 0 = name-2 NOT in message, 1 = name-2 IS in message
obj type                type of object which is listed:

                         obj type     entity
                         0            Vector Names
                         1            Trunk Group Names
                         2            Hunt Group Names
                         3            VDN (iln) Names
                         4            Agent Loginid Names

b                       Beginning bit, set when this is the first message of the set needed to satisfy the
                        request. (all object types)
obj id                  the identifying number for the object (obj types 0-3 only)

                         obj type     entity                     obj id values
                         0            Vector Names               1-2000 (CM3.1-CM5.2)
                                                                 1-8000 (CM6.0 and later)
                         1            Trunk Group Names          1-2000
                         2            Hunt Group Names           1-2000 (CM3.1-CM5.2)
                                                                 1-8000 (CM6.0 and later)
                         3            VDN (iln) Names            1-20000 (CM3.1-CM5.2)
                                                                 1-30000 (CM6.0 and later)
pnumber                 number of digits in agent position, 1-16 (obj type 4 only)
p1-p16                  agent position - with EAS login ID in packed decimal format, left-justified where
                        hex a is digit 0 and 0 in this field is null, zero fill position to a byte boundary
                        (obj type 4 only)
name 1 len M            number of bytes of object data, (0-27)
name 1 byte X           object data bytes (ASCII encoded name1 data bytes)
name 2 len N            number of bytes of object data, (0-81)
name 2 script tag       UTF-8 script tag for name2 data bytes. The script tag represents a writing script. See
                        the table under ADMNAM20 for the actual values, 1-32.
name 2 byte X           object data bytes (UTF-8 encoded name2 data bytes)
```

<a id="pdf-page-125"></a>

## PDF page 125

Source: SPI-SYN24; PDF page 125; extracted characters: 944.

```text
       3.3.27     RCODENAM20 (New CM3.1)


                                                          Switch   Vect   Skill
                                           First Release  CM3.1    y      y/n
                                           Last Release

The Return Code Name message is sent by the reporting adjunct to CM.

                   7  6   5  4   3   2  1   0  7   6   5  4   3   2  1   0  7   6   5  4   3  2   1   0
                        RCODENAM20                         tag                         rcode

                                       opcode     RCODENAM20 = 49 (0x31)
                                       tag        message tag, 1-255
                                       rcode        rcode    description
                                                    0        success
                                                    1        resend
                                                    2        skip
```

<a id="pdf-page-126"></a>

## PDF page 126

Source: SPI-SYN24; PDF page 126; extracted characters: 2213.

```text
       3.3.28         CHGNAM20 and CHGNAM24
The Change Name message is sent by the reporting adjunct to the switch to change the administered
name of an entity. Entities included in this protocol are: vectors, trunk groups, hunt groups, VDNs and
Agent LoginIDs. The expected response to each message is an RCODE20 [rcode = 0].

3.3.28.1                     CHGNAM20 (New CM3.1)


                                                                 Switch    Vect    Skill
                                                First Release    CM3.1     y       y/n
                                                Last Release     CM6.3

     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1    0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1    0
             CHGNAM20                             tag                 /   r   n   n     obj type
                                                                              1   2

                                                    for vector, trunk, hunt and VDN
     /                             obj id                                    name 1 len M                    name 1 byte 1
            name 1 byte 2                   name 1 byte 3                         * * *                      name 1 byte M
            name 2 len N                   name 2 script tag                 name 2 byte 1                   name 2 byte 2
            name 2 byte 3                         * * *                      name 2 byte N


                                                               for agent
      pnumber             p1              p2               p3              p4              p5              p6               p7
          p8              p9              p10             p11             p12             p13              p14             p15
            name 1 len M                    name 1 byte 1                    name 1 byte 2                   name 1 byte 3
                 * * *                      name 1 byte M                    name 2 len N                   name 2 script tag
            name 2 byte 1                   name 2 byte 2                    name 2 byte 3                         * * *
            name 2 byte N
```

<a id="pdf-page-127"></a>

## PDF page 127

Source: SPI-SYN24; PDF page 127; extracted characters: 2430.

```text
CHGNAM20 (continued)

opcode                   CHGNAM20 = 50 (0x32)
tag                      message tag, 0-255 (it will be returned in the switch response message RCODE20)
r                        reason bit, 0 = sync data, 1 = admin change update
n1                       name-1 flag, 0 = name-1 NOT in message, 1 = name-1 IS in message
n2                       name-2 flag, 0 = name-2 NOT in message, 1 = name-2 IS in message
obj type                 type of object which is listed:

                           obj type    entity
                           0           Vector Names
                           1           Trunk Group Names
                           2           Hunt Group Names
                           3           VDN (iln) Names
                           4           Agent Loginid Names

obj id                   the identifying number for the object

                           obj type    entity                      obj id values (obj types 0-3 only)
                           0           Vector Names                1-2000 (CM3.1-CM5.2)
                                                                   1-8000 (CM6.0 and later)
                           1           Trunk Group Names           1-2000
                           2           Hunt Group Names            1-2000 (CM3.1-CM5.2)
                                                                   1-8000 (CM6.0 and later)
                           3           VDN (iln) Names             1-20000 (CM3.1-CM5.2)
                                                                   1-30000 (CM6.0 and later)
pnumber                  number of digits in agent position, 1-15 (obj type 4 only)
p1-p15                   agent position - with EAS login ID in packed decimal format, left-justified where hex
                         a is digit 0 and 0 in this field is null, zero fill position to a byte boundary (obj type 4
                         only)
name 1 len M             number of bytes of object data, (0-27)
name 1 byte X            object data bytes (ASCII encoded name1 for obj type 0 thru 4)
name 2 len N             number of bytes of object data, (0-81)
name 2 script tag        UTF-8 script tag for name2 data bytes. The script tag represents a writing script.
                         See the table under ADMNAM20 for the actual values, 1-32.
name 2 byte X            object data bytes (UTF-8 encoded name2 for obj type 0 thru 4)
```

<a id="pdf-page-128"></a>

## PDF page 128

Source: SPI-SYN24; PDF page 128; extracted characters: 2125.

```text
3.3.28.2                        CHGNAM24 (New CM7.0)


                                                                       Switch     Vect    Skill
                                                    First Release      CM7.0      y       y/n
                                                    Last Release

     7   6   5    4   3    2   1    0   7    6   5   4    3   2    1   0   7    6   5    4   3   2    1   0    7   6    5   4   3    2   1    0
              CHGNAM24                                tag                   /   r   n    n      obj type
                                                                                    1    2


                                                        for vector, trunk, hunt and VDN


     b            / / / / / / /         /                                obj_id                                        name 1 len M
             name 1 byte 1                      name 1 byte 2                      name 1 byte 3                             * * *
            name 1 byte M                       name 2 len N                      name 2 script tag                    name 2 byte 1
             name 2 byte 2                      name 2 byte 3                            * * *                         name 2 byte N


                                                                     for agent


     b           / / / / / /            pnumber                p1                p2                p3               p4                p5
          p6                p7                p8               p9               p10               p11               p12               p13
          p14              p15               p16              / / / /              Name 1 len M                        Name 1 byte 1
            Name 1 bytes 2                      Name 1 byte 3                            * * *                        Name 1 byte M
             Name 2 len N                     Name 2 script tag                    Name 2 byte 1                       Name 2 byte 2
            Name 2 byte 3                             * * *                        Name 2 byte N
```

<a id="pdf-page-129"></a>

## PDF page 129

Source: SPI-SYN24; PDF page 129; extracted characters: 2422.

```text
CHGNAM24 (continued)

opcode                   CHGNAM24 = 65 (0x41)
tag                      message tag, 0-255 (it will be returned in the switch response message RCODE20)
r                        reason bit, 0 = sync data, 1 = admin change update
n1                       name-1 flag, 0 = name-1 NOT in message, 1 = name-1 IS in message
n2                       name-2 flag, 0 = name-2 NOT in message, 1 = name-2 IS in message
obj type                 type of object which is listed:

                          obj type     entity
                          0            Vector Names
                          1            Trunk Group Names
                          2            Hunt Group Names
                          3            VDN (iln) Names
                          4            Agent Loginid Names

obj id                   the identifying number for the object

                          obj type     entity                     obj id values (obj types 0-3 only)
                          0            Vector Names               1-2000 (CM3.1-CM5.2)
                                                                  1-8000 (CM6.0 and later)
                          1            Trunk Group Names          1-2000
                          2            Hunt Group Names           1-2000 (CM3.1-CM5.2)
                                                                  1-8000 (CM6.0 and later)
                          3            VDN (iln) Names            1-20000 (CM3.1-CM5.2)
                                                                  1-30000 (CM6.0 and later)
pnumber                  number of digits in agent position, 1-16 (obj type 4 only)
p1-p16                   agent position - with EAS login ID in packed decimal format, left-justified
                         where hex a is digit 0 and 0 in this field is null, zero fill position to a byte
                         boundary (obj type 4 only)
name 1 len M             number of bytes of object data, (0-27)
name 1 byte X            object data bytes (ASCII encoded name1 for obj type 0 thru 4)
name 2 len N             number of bytes of object data, (0-81)
name 2 script tag        UTF-8 script tag for name2 data bytes. The script tag represents a writing script.
                         See the table under ADMNAM20 for the actual values, 1-32.
name 2 byte X            object data bytes (UTF-8 encoded name2 for obj type 0 thru 4)
```

<a id="pdf-page-130"></a>

## PDF page 130

Source: SPI-SYN24; PDF page 130; extracted characters: 1944.

```text
       3.3.29       MVRCODE20 (New CM3.1)


                                                               Switch   Vect    Skill
                                              First Release    CM3.1    y/n     y/n
                                              Last Release

The Return Code from Move Request message is sent by the switch in response to a move request:
CHGVDNSK or MVVDN. A bit map is used to indicate the status of each (up to 32) move requests. The
bit map is divided into four bytes, and the bytes are used from left to right. Within each byte, the bits are
used from right to left. For example, if two extensions were moved, bits 0 and 1 of the first byte
(success1) will be used and bit 0 will represent the status of the first item in the move request message
and bit 1 will represent the status of the second item in the message.

     7  6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3  2   1   0
              time_tag                     MVRCODE20                                        seq num
                           seq num (cont)                                     tot siz                          tag
     /           number                      success1                       success2                       success3
              success4

time_tag         seconds past minute when message was formatted, 0-59
opcode           MVRCODE20 = 202 (0xca)
seq_num          sequence number, 0-0xffff ffff
tot_siz          total size in bytes, 1-255
tag              message tag, 0-255 (it will be returned in the switch response message)
number           number of items in the request, 1-32
success1-4       one bit for each item in the move request, 0 = failure, 1 = success. The bits are right-
                 justified within each byte, i.e., success1 represents the success of items 8-1, success2
                 represents items 16-9, and so on.
```

<a id="pdf-page-131"></a>

## PDF page 131

Source: SPI-SYN24; PDF page 131; extracted characters: 1476.

```text
       3.3.30       RCODE20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y/n    y/n
                                              Last Release

The Return Code from Request message is sent by the switch in response to a request from the
reporting adjunct.  In general, it is used whenever the switch does not completely understand a request
message (rcode=1) and specifically, to indicate the result of the following requests: VPARMS, CHGVEC
and SKILLADD.

    7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                      RCODE20                                        seq num
                          seq num (cont)                                     tot siz                         tag
                rcode                                                      parameter
          parameter (cont)

            time_tag        seconds past minute when event occurred, 0-59
            opcode          RCODE20 = 203 (0xcb)
            seq num         sequence number, 0-0xffff ffff
            tot siz         total size in bytes, 1-255
            tag             message tag, 0-255 (it will be returned in the switch response message)
            rcode           return code
            parameter       value of item that error occurred on
```

<a id="pdf-page-132"></a>

## PDF page 132

Source: SPI-SYN24; PDF page 132; extracted characters: 4951.

```text
RCODE20 (continued)

Rcode     Description                                                             Parameter      In Response To
0         request successfully completed                                                         CHGVEC,SKILLADD
1         illegal request                                                                        any
20        vector number out of range                                              vector no.     CHGVEC,VPARMS,
                                                                                                 MVVDN
21        field in vector step out of range                                       step no.       CHGVEC
22        bad vector 'goto' destination                                           step no.       CHGVEC
24        split/skill number out of range                                                        MVAGSTFD
25        bad step type in vector specification                                   step no.       CHGVEC
26        undefined split number in CVP request                                   step no.       CHGVEC
27        vector 'goto' cannot go to same vector                                  step no.       CHGVEC
28        too many steps                                                                         CHGVEC
29        invalid step type                                                       step no.       CHGVEC
31        extension not assigned                                                  step no.       CHGVEC
                                                                                  none           APARMS
                                                                                  none           SKILLADD
32        extension not a BRI extension                                           step no.       CHGVEC
33        announcement not assigned                                               step no.       CHGVEC
34        illegal packed decimal digit                                            step no.       CHGVEC
35        invalid i condition                                                     step no.       CHGVEC
36        invalid wait condition                                                  step no.       CHGVEC
37        split is not vector controlled                                          step no.       CHGVEC
38        request pending until agent logs out                                                   SKILLADD
39        switch run tape in progress, try later                                                 NOT USED
42        split not messaging type split                                          step no.       CHGVEC
43        unsupported step type for this CMS release                              step no.       VPARMS
44        cannot move to unmeasured split                                                        NMVAGENT
45        request pending until agent is in AUX or AVAIL state                                   SKILLADD
46        specified split/skill not assigned to agent                                            (used in CRCODE)
47        specified split/skill already assigned to agent                                        (used in CRCODE)
48        agent already assigned to maximum split/skill pairs                                    (used in CRCODE)
49        agent cannot be assigned to both AUDIX and non-AUDIX                                   (used in CRCODE)
          splits/skills
50        maximum agents active in this split/skill                                              (used in CRCODE)
51        maximum agents assigned in system                                                      (used in CRCODE)
52        cannot remove only skill for an agent                                                  (used in CRCODE)
53        request denied - a change is currently pending for this                                (used in CRCODE)
          agent
54        agent cannot be assigned to both AAS and non-AAS                                       (used in CRCODE)
          splits/skills
55        agent is adjunct controlled                                                            (used in CRCODE)
56        skill type must be specified                                                           MVAGSTFD
57        maximum number of agents allowed by B/CMS already                                      (used in CRCODE)
          administered
58        agent must have at least one administered skill                                        SKILLADD
59        feature not enabled on switch                                                          CHGVEC
60        administration contention. Try again later                                             any
61        cannot remove direct agent skill                                                       (used in CRCODE)
62        cannot add/remove standard skill                                                       (used in CRCODE)
```

<a id="pdf-page-133"></a>

## PDF page 133

Source: SPI-SYN24; PDF page 133; extracted characters: 433.

```text
63        direct agent skill cannot be a reserve skill                                          SKILLADD
64        cannot change reserve skill to standard or vice versa                                 (used in CRCODE)
65        entity locked on switch                                                               CHGVEC, VPARMS
66        Skill tenant number doesn’t match agent tenant number                                 SKILLADD
```

<a id="pdf-page-134"></a>

## PDF page 134

Source: SPI-SYN24; PDF page 134; extracted characters: 4146.

```text
       3.3.31      CRCODE20 (New CM3.1)


                                                            Switch   Vect   Skill
                                            First Release   CM3.1    y/n    y/n
                                            Last Release

This is a variable length message sent by the switch in response to a MVAGSTFD message.  It contains
up to 32 individual RCODEs, one for each agent position specified in the MVAGSTFD message. The
number of RCODEs contained in the message is indicated by the "count" field.  This message must be
sent within 2 minutes of the time of the MVAGSTFD message.

    7   6   5  4   3   2  1   0   7   6  5   4   3  2   1   0   7  6   5   4  3   2   1   0  7   6   5  4   3   2   1  0
             time_tag                    CRCODE20                                       seq num
                         seq num (cont)                                   tot siz                        tag
      / /          count                    rcode1                        rcode2                       rcode3
              rcode4
                                                            .  .  .
              rcodeN

time_tag       seconds past minute when event occurred, 0-59
opcode         CRCODE20 = 204 (0xcc)
seq num        sequence number, 0-0xffff ffff
tot siz        total size in bytes, 1-255
tag            message tag, 0-255, set to the tag value of the IQ message that generated the CRCODE20
count          the number of RCODES, 1-32, included in the message
rcode 1-N      return code for specific request.  (See table below for valid codes.)

   Rcode      Description                                                              In Response To
   0          request successfully completed                                           MVAGSTFD
   1          illegal request                                                          MVAGSTFD
   20         vector number out of range                                               (used in RCODE)
   21         field in vector step out of range                                        (used in RCODE)
   22         bad vector 'goto' destination                                            (used in RCODE)
   24         split/skill number out of range                                          MVAGSTFD
   25         bad step type in vector specification                                    (used in RCODE)
   26         undefined split number in CVP request                                    (used in RCODE)
   27         vector 'goto' cannot go to same vector                                   (used in RCODE)
   28         too many steps                                                           (used in RCODE)
   29         invalid step type                                                        (used in RCODE)
   31         extension not assigned                                                   (used in RCODE)
   32         extension not a BRI extension                                            (used in RCODE)
   33         announcement not assigned                                                (used in RCODE)
   34         illegal packed decimal digit                                             (used in RCODE)
   35         invalid if condition                                                     (used in RCODE)
   36         invalid wait condition                                                   (used in RCODE)
   37         split is not vector controlled                                           (used in RCODE)
   38         request pending until agent logs out                                     (used in RCODE)
   39         switch run tape in progress, try later                                   NOT USED
   42         split not messaging type split                                           (used in RCODE)
   43         unsupported step type for this CMS release                               (used in RCODE)
   44         cannot move to unmeasured split                                          NMVAGENT,MVAGSTFD
   45         request pending until agent is in AUX or AVAIL state                     MVAGSTFD
```

<a id="pdf-page-135"></a>

## PDF page 135

Source: SPI-SYN24; PDF page 135; extracted characters: 1781.

```text
46        specified split/skill not assigned to agent                           MVAGSTFD
47        specified split/skill already assigned to agent                       MVAGSTFD
48        agent already assigned to maximum skills                              MVAGSTFD
49        agent cannot be in both AUDIX and non-AUDIX skills                    MVAGSTFD
50        maximum agents active in this skill                                   MVAGSTFD
51        maximum agents logged into system                                     MVAGSTFD
52        cannot remove only skill for an agent                                 MVAGSTFD
53        request denied - change currently pending for agent                   MVAGSTFD
54        agent cannot be in both AAS and non-AAS skills                        MVAGSTFD
55        adjunct controlled agents limited to one skill                        MVAGSTFD
56        skill type must be specified                                          MVAGSTFD
57        max agents allowed by B/CMS already administered                      MVAGSTFD
58        agent must have at least one administered skill                       MVAGSTFD
60        switch administration contention                                      any
61        cannot remove direct agent skill                                      MVAGSTFD
62        cannot add/remove standard skill                                      MVAGSTFD
63        direct agent skill cannot be a reserve skill                          MVAGSTFD
64        cannot change reserve skill to standard or vice versa                 MVAGSTFD
65        entity locked on switch                                               (used in RCODE)
66        Skill tenant number doesn’t match agent tenant number                 MVAGSTFD
```

<a id="pdf-page-136"></a>

## PDF page 136

Source: SPI-SYN24; PDF page 136; extracted characters: 1635.

```text
       3.3.32      USERID21 (New CM4)


                                                              Switch   Vect    Skill
                                              First Release   CM4      y/n     y/n
                                              Last Release

The user Identity 21 format is to be an ASCII string of up to 32 characters.  The population of user
identity changes made by the reporting adjunct will be supported by the reporting adjunct only.

This is a variable length message based on the "id-length" field.

The first five bytes are always sent.

This message is to follow an ACD admin change message (MVAGSTFD, SKILLADD, MVVDN,
CHGVDNSK or CHGNAM). The expected response is one RCODE20 message.

    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0
             USERID21                          tag                       admin-opcode                     admin-tag
              id-length                     id_byte-1                      id-byte-2                      id-byte-3
                                                              .  .  .
              id-byte-N

opcode                USERID21 = 54 (0x36)
tag                   message tag, 0-255 (it will be returned in the switch response message(s))
admin-opcode          opcode of the admin message identity applies to
admin-tag             tag of the admin message identity applies to
id-length             number of bytes in id (0-32)
id-byte-N             object data bytes ASCII encoded - user identity for admin change (N ranges from 1 to
                      32)
```

<a id="pdf-page-137"></a>

## PDF page 137

Source: SPI-SYN24; PDF page 137; extracted characters: 3087.

```text
3.4       Call Processing
Call Processing messages are sent continuously while the reporting adjunct Session is in the DATA
TRANSFER mode. Each message will be time-stamped and sent (or buffered) in the order they are
processed.
       3.4.1        TIME20 (New CM3.1)


                                                               Switch    Vect    Skill
                                               First Release   CM3.1     y/n     y/n
                                               Last Release

The Time of Day message is the first Call Processing message sent by the switch after the translation
pumpup is completed. Thereafter, it is sent every minute, on the minute. the reporting adjunct uses this
message to reset the reporting adjunct clock. In addition, every message sent by the switch to the
reporting adjunct is time-stamped (time_tag) with the seconds past the minute when the event happened.
The reporting adjunct sets the seconds of the clock with every message, therefore it is important that all
messages between TIME20 messages are sent in the order created so that time (time_tag) never goes
backwards.

Since a TIME20 message is required every minute, the reporting adjunct will set the AT2 timer (2
minutes) and reset this timer every time a TIME20 message is received. If the timer expires (i.e., data
transfer timeout) the reporting adjunct will initiate another reporting adjunct Session.

For the time zone offset fields (s, hr offset & min offset), the switch and the reporting adjunct use different
formats. The switch uses Linux format and the reporting adjunct uses Java format. Therefore, the
reporting adjunct will need to convert the time zone offset received into Java format before using it.  For
example, Java expects the Mountain Standard Time Zone to be GMT -7, but Linux configures it as GMT
+7. So the s field in the TIME20 would be zero. The reporting adjunct needs to convert the s field to 1
prior to using it.

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0
              time_tag                        TIME20                                         seq num
                           seq num (cont)                                      tot siz                         year
                hour                                           yday                                d            minute
     s           hr offset                   min offset

time_tag        seconds past minute, 0-59
opcode          TIME20 = 205 (0xcd)
seq num         sequence number, 0-0xffff ffff
tot siz         total size of message in bytes, 1-255
year            current year on switch, 0-99
hour            current hour on switch, 0-23
yday            current day of the year on switch, 1-366
d               daylight savings time flag; 0 = standard time, 1 = daylight savings time
minute          current minute on switch, 0-59
s               time zone offset flag; 0 = +, 1 = -
hr offset       time zone offset hours, 0-23
min offset      time zone offset minutes, 0-59
```

<a id="pdf-page-138"></a>

## PDF page 138

Source: SPI-SYN24; PDF page 138; extracted characters: 2288.

```text
       3.4.2        ALOGON20, ALOGON23 and ALOGON24
An Agent Logon message is sent by the switch during the translation pumpup and whenever an agent
staffs a position. When sent as part of an agent logon translation block, one of these messages is sent for
each extension that is staffed. The reporting adjunct will update the status of the agent position (record
who is logged on) in the database. Note that the logid is sent in packed decimal format, where hex a is
the digit 0 and 0 in the field is null.

With EAS, a single agent has one "agent position" independent of how may skills that agent has.

The switch will require at least one login digit if the reporting adjunct is optioned.
This is a variable length message sent from the switch to the reporting adjunct. The length is based on
the "snumber", "pnumber" and "dnumber" fields. For the EAS version, field "f1" always starts on a byte
boundary. Four bits will be zero filled for a digit if needed.

The skills are in administered order with any administered blanks eliminated (however, blanks may exist
because a skill is not measured by the reporting adjunct, i.e., skill=0, level=0). The order and position of
the skills in the message must correspond to the bit-map in the AVAIL and AUDAVAIL messages.

The ALOGON message is sent when an agent logs in, when an agent performs add/remove skills from a
phone, and at pumpup.  The ALOGON is also sent in response to the MVAGSTFD or SKILLADD
message when a move is completed.

If the entire login attempt fails, no ALOGON message is sent; an exception to this rule is with the
MVAGSTFD message where the ALOGON message may be sent with all fail bits set.

Starting with ALOGON23, the expansion to 120 skills this request may not fit into a single ALOGON
message.  If the agent has more than 60 skills, a second message will be sent. The 1st message in the
series covers skills 1 through 60 and the 2nd message covers skills 61 through 120, mapping to skills 1-
60. The end bit is set for the last message in a series.

Starting with ALOGON24, with the increases to number of digits and additional fields, 60 skills may not fit
into one ALOGON message. Instead of splitting ALOGON into 2 messages that each send 60 skills, it will
now be 3 messages that each send 40 skills.
```

<a id="pdf-page-139"></a>

## PDF page 139

Source: SPI-SYN24; PDF page 139; extracted characters: 2170.

```text
3.4.2.1                    ALOGON20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y/n    y/n
                                              Last Release    CM5.2

3.4.2.1.1           ALOGON20, without EAS (New CM3.1)


    7   6   5   4   3   2   1  0   7   6   5   4   3   2  1   0   7   6   5   4   3  2   1   0   7   6   5   4  3   2   1   0
              time_tag                     ALOGON20                                        seq num
                          seq num (cont)                                     tot siz             p   x   f   s       / / / /
               loc_id                pnumber                                          pos
      dnumber            d1             d2              d3             d4              d5             d6             d7
         d8              d9

time_tag      seconds past minute when event occurred, 0-59
opcode        ALOGON20 = 206 (0xce)
seq_num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
p             change pending; 0 = no changes pending, 1 = a change is pending for this agent. (If pending
              is due to MVAGSTFD, the ALOGON message is not sent until the agent ends
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

<a id="pdf-page-140"></a>

## PDF page 140

Source: SPI-SYN24; PDF page 140; extracted characters: 4331.

```text
3.4.2.1.2            ALOGON20, with EAS (New CM3.1)

    7    6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                      ALOGON20                                           seq num
                            seq num (cont)                                       tot siz              p   x         snumber
                loc_id                 pnumber            p1               p2              p3              p4              p5
          p6              p7              p8              p9              p10             p11             p12              p13
         p14             p15           dnumber            d1               d2              d3              d4              d5
          d6              d7              d8              d9              d10             d11             d12              d13
         d14             d15         d   s    ch     /                    da_skill                    f           percent1
                                     a   o                                                            1
     r      level1                         skill1                    f           percent2             r      level2         skill2
    1                                                                2                                2
             skill2 (cont)
                                                                  .  .  .
     f          percentN             r      levelN                         skillN
    N                                N

time_tag           seconds past minute when event occurred, 0-59
opcode             ALOGON20 = 206 (0xce)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
p                  change pending; 0 = no changes pending, 1 = a change is pending for this agent.
x                  translation; 0 = normal logon, 1 = translation pump-up status (agent logged in or AAS
                   agent released from maintenance busy) or DME change.
snumber            number of skills in the message (1-60)
loc_id             location id number, 0-44 (G3V8-G3V11), 0-250 (MV2 and later), 0 is default for no location
                   id
pnumber            number of digits in agent position, 1-15
p1-p15             agent position, with EAS (0-9999999) login ID in packed decimal format, left-justified
                   where 0 is null and hex a is digit 0, zero fill to a byte boundary.
dnumber            number of digits in the physical extension, 1-15
d1-d15             the digits of the physical extension in packed decimal format, left-justified where 0 is null
                   and hex a is digit 0, zero fill to a byte boundary.
da                 flag indicating direct agent calls should be received first.  Valid only when call handling
                   preference is percent allocation.
so                 service objective flag: 0=not in use, 1=in use.  Valid only when call handling preference is
                   skill level or greatest need.
ch                 agent's call handling preference, 0 = skill level, 1 = greatest need, 2 = percent allocation
da_skill           agent's direct-agent skill (must be one of agent's 60 skills)
f 1-60             logon fail bits.  For non-zero skills, look at this bit to see whether login to pending skill has
                   failed. 0 = logon to pending skill succeeded, 1 = logon failed.  It is possible to send all
                   skills with fail bits set.  f1=skill1, f2=skill2, etc.
percent 1-60       percent allocation for this skill, 0-100.  Must be 0 when skill level is reserve (rN=1).  Must
                   be non-zero when call handling preference is percent allocation and skill level is not
                   reserve (rN=0).  Valid only when call handling preference is percent allocation.
r 1-60             flag indicating level is reserve level(r=1) rather than skill level(r=0).
level 1-60         skill level (0-15 representing levels 1-16) or reserve level (1-2).
skill 1-60         skills 1-999 (G3V8-G3V11), 1-2000 (MV2 and later), assigned to the agent in the order
                   administered. Sending zero indicates no skill administered (or skill not measured by
                   CMS).
```
