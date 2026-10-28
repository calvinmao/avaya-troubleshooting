---
title: "SPI-SYN24 - complete source pages 221-240"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 221-240

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-221"></a>

## PDF page 221

Source: SPI-SYN24; PDF page 221; extracted characters: 2799.

```text
3.4.36.3                    AUDACD24 (New CM7.0)


                                                                Switch    Vect    Skill
                                               First Release    CM7.0     y/n     y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       AUDACD24                                         seq num
                           seq num (cont)                                       tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                 / / / /       d     u         / / / / /
                                                              skill-map
                                                           skill-map (cont)
                                                           skill-map (cont)
                                           skill-map (cont)                                         /             net_id
            net_id (cont)                                        seq                                          timestamp
                                          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDACD24 = 86 (0x56)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16         agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                   decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                   to a byte boundary
d                  direction of call
                   −    1 means call is outbound (ACDO)
                   −    2 means call is inbound (ACDI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map          one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                   the order of the skills in the ALOGON message.
                   −    1 means agent state applies for this skill
                   −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                        the reporting adjunct will report the agent activity for this skill as OTHER.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-222"></a>

## PDF page 222

Source: SPI-SYN24; PDF page 222; extracted characters: 3296.

```text
       3.4.37       AUDACW20, AUDACW23 and AUDACW24
This is a variable length message based on "pnumber" and whether or not EAS is active.  Prior to
AUDACW23, with EAS, this message will contain 7 additional bytes for the "skill-map" and without EAS
(since the d/u flag byte still exists) the first 4 bits of the "skill-map" are set to 0. Starting with AUDACD23
and the expansion to 120 skills, with EAS, this message will contain 15 additional bytes for the expanded
“skill-map”.

3.4.37.1                    AUDACW20 (New CM3.1)


                                                                Switch    Vect   Skill
                                               First Release    CM3.1     y/n    y/n
                                               Last Release     CM5.2



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0
              time_tag                      AUDACW20                                          seq num
                           seq num (cont)                                      tot siz                pnumber        pos or p1-
                                                                                                                        p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                  d      u   /     skill-map
                                                           skill-map (cont)
                                           skill-map (cont)                                         /            net_id
            net_id (cont)                                       seq                                          timestamp
                                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDACW20 = 241 (0xf1)
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
                  Note: this information is not available with AAUDIT.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map         one bit for each staffed skill. The skills are mapped left to right and correspond to the order
                  of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       the reporting adjunct will report the agent activity for this skill as OTHER.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-223"></a>

## PDF page 223

Source: SPI-SYN24; PDF page 223; extracted characters: 2973.

```text
3.4.37.2                    AUDACW23 (New CM6.0)


                                                                 Switch    Vect   Skill
                                                First Release    CM6.0     y/n    y/n
                                                Last Release     CM6.3



    7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                       AUDACW23                                          seq num
                           seq num (cont)                                       tot siz                pnumber         pos or p1-
                                                                                                                          p15
                                pos (non-EAS) or p1-p15 (EAS) (cont)                                   d     u         / / / / /
                                                               skill-map
                                                            skill-map (cont)
                                                            skill-map (cont)
                                           skill-map (cont)                                          /             net_id
            net_id (cont)                                        seq                                           timestamp
                                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDACW23 = 7 (0x07)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15        agent position - without EAS "pos" (1-10000), with EAS "p1-p15" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill to a byte
                  boundary
d                 direction of call
                  −    0 means no call (ACW)
                  −    1 means call is outbound (ACWO)
                  −    2 means call is inbound (ACWI)
                  Note: this information is not available with AAUDIT.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map         one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                  the order of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       the reporting adjunct will report the agent activity for this skill as OTHER.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-224"></a>

## PDF page 224

Source: SPI-SYN24; PDF page 224; extracted characters: 2819.

```text
3.4.37.3                    AUDACW24 (New CM7.0)


                                                                Switch    Vect   Skill
                                               First Release    CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDACW24                                          seq num
                           seq num (cont)                                      tot siz                 / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                 / / / /       d     u         / / / / /
                                                              skill-map
                                                           skill-map (cont)
                                                           skill-map (cont)
                                           skill-map (cont)                                         /            net_id
            net_id (cont)                                        seq                                         timestamp
                                          timestamp (cont)

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDACW24 = 87 (0x57)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16        agent position - without EAS "pos" (1-10000), with EAS "p1-p16" login ID in packed
                  decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                  to a byte boundary
d                 direction of call
                  −    0 means no call (ACW)
                  −    1 means call is outbound (ACWO)
                  −    2 means call is inbound (ACWI)
                  Note: this information is not available with AAUDIT.
u                 flag indicating that the UCID fields (net_id, seq and timestamp) are present
skill-map         one bit for each staffed skill (1-120). The skills are mapped left to right and correspond to
                  the order of the skills in the ALOGON message.
                  −    1 means agent state applies for this skill
                  −    0 means agent state does not apply for this skill or the skill is not assigned/measured;
                       the reporting adjunct will report the agent activity for this skill as OTHER.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-225"></a>

## PDF page 225

Source: SPI-SYN24; PDF page 225; extracted characters: 2402.

```text
       3.4.38       AUDAUX20, AUDAUX23 and AUDAUX24
This is a variable length message based on "pnumber".

3.4.38.1                   AUDAUX20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y/n    y/n
                                               Last Release    CM5.2



    7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                      AUDAUX20                                         seq num
                           seq num (cont)                                     tot siz                pnumber        pos or p1-
                                                                                                                       p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                 d     u         / / / / /
    /            reason             /                           net_id                                         seq
             seq (cont)                                                     timestamp
          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDAUX20 = 242 (0xf2)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position - witout EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                   packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                   to a byte boundary
d                  direction of call
                   −    0 means no call (AUX)
                   −    1 means call is outbound (AUXO)
                   −    2 means call is inbound (AUXI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
reason             reason code (0-99); 0 is the default reason code.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-226"></a>

## PDF page 226

Source: SPI-SYN24; PDF page 226; extracted characters: 2587.

```text
3.4.38.2                    AUDAUX23 (New CM6.0)


                                                                Switch    Vect   Skill
                                               First Release    CM6.0     y/n    y/n
                                               Last Release     CM6.3



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDAUX23                                          seq num
                           seq num (cont)                                      tot siz                pnumber        pos or p1-
                                                                                                                        p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                   d     u   i       / / / /
    /            reason             /                            net_id                                         seq
             seq (cont)                                                      timestamp
          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDAUX23 = 16 (0x10)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15         agent position - witout EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                   packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                   to a byte boundary
d                  direction of call
                   −    0 means no call (AUX)
                   −    1 means call is outbound (AUXO)
                   −    2 means call is inbound (AUXI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
reason             reason code (0-99); 0 is the default reason code.
i                  flag that indicates that the AUX reason code entered is interruptible. The flag is to be set
                   to 1 when the agent used and AUX reason code that has the Aux Work/Interruptible field
                   on the Reason Code Names screen set to “y”.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-227"></a>

## PDF page 227

Source: SPI-SYN24; PDF page 227; extracted characters: 2437.

```text
3.4.38.3                   AUDAUX24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
              time_tag                      AUDAUX24                                         seq num
                          seq num (cont)                                      tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                / / / /      d     u   i       / / / /
    /            reason             /                           net_id                                         seq
             seq (cont)                                                     timestamp
          timestamp (cont)

time_tag           seconds past minute when event occurred, 0-59
opcode             AUDAUX24 = 88 (0x58)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
pnumber            number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16         agent position - witout EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                   in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                   null, zero fill to a byte boundary
d                  direction of call
                   −    0 means no call (AUX)
                   −    1 means call is outbound (AUXO)
                   −    2 means call is inbound (AUXI)
                   Note: this information is not available with AAUDIT.
u                  flag indicating that the UCID fields (net_id, seq and timestamp) are present
reason             reason code (0-99); 0 is the default reason code.
i                  flag that indicates that the AUX reason code entered is interruptible. The flag is to be set
                   to 1 when the agent used and AUX reason code that has the Aux Work/Interruptible field
                   on the Reason Code Names screen set to “y”.
net_id             network entity identifier, 1-32767
seq                call sequence number, 0-65535
timestamp          unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-228"></a>

## PDF page 228

Source: SPI-SYN24; PDF page 228; extracted characters: 2330.

```text
       3.4.39        AUDOTHER22 and AUDOTHER24
This is a variable length message based on "pnumber".

3.4.39.1                   AUDOTHER22 (New CM5.2)


                                                               Switch    Vect   Skill
                                               First Release   CM5.2     y/n    y/n
                                               Last Release    CM6.3



    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6  5   4   3   2   1   0
              time_tag                    AUDOTHER22                                         seq num
                          seq num (cont)                                      tot siz               pnumber         pos or p1-
                                                                                                                       p15
                               pos (non-EAS) or p1-p15 (EAS) (cont)                                 d        / / /    u   h   w
    /                            net_id                                                        seq
                                                            timestamp

time_tag          seconds past minute when event occurred, 0-59
opcode            AUDOTHER22 = 251 (0xfb)
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
h                 flag to indicate the agent has just put a call on hold.
w                 flag to indicate the observer is waiting fo another call to observe.
net_id            network entity identifier, 1-32767
seq               call sequence number, 0-65535
timestamp         unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-229"></a>

## PDF page 229

Source: SPI-SYN24; PDF page 229; extracted characters: 2072.

```text
3.4.39.2                   AUDOTHER24 (New CM7.0)


                                                               Switch   Vect    Skill
                                              First Release    CM7.0    y/n     y/n
                                              Last Release



    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                    AUDOTHER24                                        seq num
                          seq num (cont)                                      tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                                / / / /      d        / / /    u   h   w
    /                            net_id                                                        seq
                                                            timestamp

time_tag         seconds past minute when event occurred, 0-59
opcode           AUDOTHER24 = 89 (0x59)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
pnumber          number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16       agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                 in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                 null, zero fill to a byte boundary
d                direction of call
                 −     0 means no call
                 −     1 means call is outbound
                 −     2 means call is inbound
u                flag indicating that the UCID fields (net_id, seq and timestamp) are present.
h                flag to indicate the agent has just put a call on hold.
w                flag to indicate the observer is waiting fo another call to observe.
net_id           network entity identifier, 1-32767
seq              call sequence number, 0-65535
timestamp        unix style (seconds since 1/1/70) time call assigned a UCID
```

<a id="pdf-page-230"></a>

## PDF page 230

Source: SPI-SYN24; PDF page 230; extracted characters: 2773.

```text
       3.4.40       AUDUNSTF20 and AUDUNSTF24
This message is non-EAS only.

This is a variable length message based on "pnumber".

3.4.40.1                   AUDUNSTF20 (New CM3.1)


                                                              Switch    Vect   Skill
                                              First Release   CM3.1     y/n    y/n
                                              Last Release    CM6.3



    7   6   5   4   3  2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1  0
              time_tag                    AUDUNSTF20                                        seq num
                          seq num (cont)                                     tot siz               pnumber        pos or p1-
                                                                                                                     p15
                              pos (non-EAS) or p1-p15 (EAS) (cont)

time_tag         seconds past minute when event occurred, 0-59
opcode           AUDUNSTF20 = 244 (0xf4)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
pnumber          number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15       agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                 packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                 to a byte boundary

3.4.40.2                   AUDUNSTF24 (New CM7.0)


                                                              Switch    Vect   Skill
                                              First Release   CM7.0     y/n    y/n
                                              Last Release



    7   6   5   4   3  2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1  0
              time_tag                    AUDUNSTF24                                        seq num
                          seq num (cont)                                     tot siz                / / /        pnumber
                          pos (non-EAS) or p1-p16 (EAS)                               / / / /

time_tag         seconds past minute when event occurred, 0-59
opcode           AUDUNSTF24 = 90 (0x5a)
seq num          sequence number, 0-0xffff ffff
tot siz          total size in bytes, 1-255
pnumber          number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16       agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login ID
                 in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                 null, zero fill to a byte boundary
```

<a id="pdf-page-231"></a>

## PDF page 231

Source: SPI-SYN24; PDF page 231; extracted characters: 2650.

```text
       3.4.41       EWTAUDIT20 and EWTAUDIT23
The EWTAUDIT message is sent by the switch when it receives an RAUDIT message from the reporting
adjunct, indicating that it has not received a QUEUED or DFWD message for a particular split/skill within
the expected timeframe.

The EWTAUDIT will contain the updated Expected Wait Times for all four priorities for a split/skill.

3.4.41.1                   EWTAUDIT20 (New CM3.1)


                                                               Switch    Vect   Skill
                                              First Release    CM3.1     y      y/n
                                              Last Release     CM5.2



    7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1   0
              time_tag                    EWTAUDIT20                                         seq num
                          seq num (cont)                                      tot siz             e   e   e   e   /     split
                                                                                                  t   h   m   l
             split (cont)                                      ewt_t                                          ewt_h
            ewt_h (cont)                                      ewt_m                                           ewt_l
            ewt_l (cont)

time_tag     seconds past minute when event occurred, 0-59
opcode       EWTAUDIT20 = 245 (0xf5)
seq num      sequence number, 0-0xffff ffff
tot siz      total size in bytes, 1-255
et           flag indicating whether ewt_t contains an EWT (when 0, ewt_t is null; when 1, ewt_t will
             contain a numeric value in seconds)
eh           flag indicating whether ewt_h contains an EWT (when 0, ewt_h is null; when 1, ewt_h will
             contain a numeric value in seconds)
em           flag indicating whether ewt_m contains an EWT (when 0, ewt_m is null; when 1, ewt_m will
             contain a numeric value in seconds)
el           flag indicating whether ewt_l contains an EWT (when 0, ewt_l is null; when 1, ewt_l will contain
             a numeric value in seconds)
split        split or skill number for which CMS needs an update for expected wait time. 1-999 (G3V8-
             G3V11), 1-2000 (MV2 and later)
ewt_t        expected wait time for split/skill at top priority, 0-9999 seconds
ewt_h        expected wait time for split/skill at high priority, 0-9999 seconds
ewt_m        expected wait time for split/skill at medium priority, 0-9999 seconds
ewt_l        expected wait time for split/skill at low priority, 0-9999 seconds
```

<a id="pdf-page-232"></a>

## PDF page 232

Source: SPI-SYN24; PDF page 232; extracted characters: 2222.

```text
3.4.41.2                    EWTAUDIT23 (New CM6.0)


                                                                Switch   Vect    Skill
                                               First Release    CM6.0    y       y/n
                                               Last Release



    7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0   7   6   5   4   3   2   1   0
              time_tag                     EWTAUDIT23                                         seq num
                           seq num (cont)                                      tot siz             e   e   e   e        / / / /
                                                                                                    t  h   m    l
       / / /                          split                                                    ewt_t
                               ewt_h                                                           ewt_m
                                ewt_l

time_tag      seconds past minute when event occurred, 0-59
opcode        EWTAUDIT23 = 34 (0x22)
seq num       sequence number, 0-0xffff ffff
tot siz       total size in bytes, 1-255
et            flag indicating whether ewt_t contains an EWT (when 0, ewt_t is null; when 1, ewt_t will
              contain a numeric value in seconds)
eh            flag indicating whether ewt_h contains an EWT (when 0, ewt_h is null; when 1, ewt_h will
              contain a numeric value in seconds)
em            flag indicating whether ewt_m contains an EWT (when 0, ewt_m is null; when 1, ewt_m will
              contain a numeric value in seconds)
el            flag indicating whether ewt_l contains an EWT (when 0, ewt_l is null; when 1, ewt_l will contain
              a numeric value in seconds)
split         split or skill number for which CMS needs an update for expected wait time. 1-8000
ewt_t         expected wait time for split/skill at top priority, 0-9999 seconds
ewt_h         expected wait time for split/skill at high priority, 0-9999 seconds
ewt_m         expected wait time for split/skill at medium priority, 0-9999 seconds
ewt_l         expected wait time for split/skill at low priority, 0-9999 seconds
```

<a id="pdf-page-233"></a>

## PDF page 233

Source: SPI-SYN24; PDF page 233; extracted characters: 1410.

```text
       3.4.42       VAUDIT20 (New CM3.1)


                                                               Switch    Vect   Skill
                                               First Release   CM3.1     y      y/n
                                               Last Release

This message is sent by the switch to the reporting adjunct in response to an RAUDIT.  It is used by the
reporting adjunct to update the VDN call count for a VDN that has not had any new calls arrive and thus
no recent DNEVENT messages have been received.

    7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4  3   2   1   0
              time_tag                      VAUDIT20                                         seq num
                          seq num (cont)                                      tot siz              /              iln
              iln (cont)                                    call_count

                            time_tag       seconds past minute when event occurred, 0-59
                            opcode         VAUDIT20 = 246 (0xf6)
                            seq num        sequence number, 0-0xffff ffff
                            tot siz        total size in bytes, 1-255
                            iln            internal line number, 1-32766
                            call_count     active calls associated with this VDN, 0-7712
```

<a id="pdf-page-234"></a>

## PDF page 234

Source: SPI-SYN24; PDF page 234; extracted characters: 2792.

```text
       3.4.43        XFER20 and XFER24
The Transfer message is sent by the switch when a call is merged, conferenced, transferred or path
replacement done to another destination. It is an instruction to the reporting adjunct to copy the status of
the transfer trunk (xfer) to the destination trunk (dest) and then track the call as if it arrived on the dest
trunk. If the conference field (c) is set, the reporting adjunct will track both the xfer and dest trunks until
one or both of the call drops from the conference.

Any of the trunks involved may be measured or unmeasured, currently being tracked or not (either the
trunk or agent must be measured).From a reporting adjunct perspective, internal calls use internal
unmeasured trunks.In all of these cases, the reporting adjunct will copy the status of the xfer trunk to the
dest trunk and attempt to track the call(s).

For example, an internal call placed to the split and connected to a position will use an unmeasured trunk
(the reporting adjunct will be tracking this trunk). If the agent transfers the call to another destination, the
second call will also involve an unmeasured trunk (which may or may not be tracked by the reporting
adjunct) and the XFER20 message will instruct the reporting adjunct to transfer the status of the second
call (if not being tracked the status is SEIZED) to the original call.

3.4.43.1                     XFER20 (New CM3.1)


                                                                 Switch     Vect   Skill
                                                First Release    CM3.1      y/n    y/n
                                                Last Release     CM6.3



    7   6   5   4   3    2   1   0   7   6   5   4   3   2   1   0    7   6   5   4   3   2   1   0   7    6   5   4   3   2   1   0
              time_tag                         XFER20                                           seq num
                           seq num (cont)                                        tot siz              u              xfer
                                                                                                      x
              xfer (cont)            u                              dest                               /     type        pnumber
                                     d
                                           pos (non-EAS) or p1-p15 (EAS)                                                   / / / /
    /                            x_net_id                                                         x_seq
                                                              x_timestamp
    /                            d_net_id                                                         d_seq
                                                             d_timestamp
```

<a id="pdf-page-235"></a>

## PDF page 235

Source: SPI-SYN24; PDF page 235; extracted characters: 1918.

```text
XFER20 (continued)

time_tag           seconds past minute when event occurred, 0-59
opcode             XFER20 = 247 (0xf7)
seq num            sequence number, 0-0xffff ffff
tot siz            total size in bytes, 1-255
ux                 flag indicating that the UCID fields (net_id, seq and timestamp) are present for xfer itn
xfer               internal trunk number of transfer trunk, 1-32677
ud                 flag indicating that the UCID fields (net_id, seq and timestamp) are present for dest itn
dest               internal trunk number of destination trunk, 1-32677
type               0=transfer, 1=conference, 2=special link (G2), 3=rename, 4=path replacement (G3V10
                   and later) Special link is used for transfers that involve two physical trunks and neither of
                   the trunks drops. Rename is used when two or more facilities drop when a transfer occurs,
                   the call continues on the "dest" facility.
pnumber            number of digits in agent position, 1-15, will always be 5 for non-EAS
                   0=an unmeasured endpoint transferred the call. In this case, no position is sent.
pos-p1-p15         agent position that initiates the transfer/conference, without EAS "pos" (1-10000), with
                   EAS "p1-p15" (0-9999999) login ID in packed decimal format, left-justified where hex a is
                   digit 0 and 0 in this field is null, zero fill to a byte boundary
                   flag indicating that the UCID fields (net_id, seq and timestamp) are present

x_net_id           network entity identifier, 1-32767
x_seq              call sequence number, 0-65535
x_timestamp        unix style (seconds since 1/1/70) time call assigned a UCID
d_net_id           network entity identifier, 1-32767
d_seq              call sequence number, 0-65535
d_timestam         unix style (seconds since 1/1/70) time call assigned a UCID
p
```

<a id="pdf-page-236"></a>

## PDF page 236

Source: SPI-SYN24; PDF page 236; extracted characters: 1433.

```text
3.4.43.2                      XFER24 (New CM7.0)


                                                                      Switch    Vect     Skill
                                                   First Release      CM7.0     y/n      y/n
                                                   Last Release



    7    6   5   4    3   2   1    0   7    6   5   4    3   2   1    0   7   6    5   4    3   2   1    0   7   6    5   4   3    2   1   0
               time_tag                           XFER24                                               seq num
                             seq num (cont)                                            tot siz               u   u           / / / / / /
                                                                                                             x   d
                                   xfer                                                                  dest
       type           pnumber                                   pos (non-EAS) or p1-p16 (EAS)                                      / / / /
    /                              x_net_id                                                             x_seq
                                                                 x_timestamp
    /                              d_net_id                                                             d_seq
                                                                 d_timestamp
```

<a id="pdf-page-237"></a>

## PDF page 237

Source: SPI-SYN24; PDF page 237; extracted characters: 1893.

```text
XFER24 (continued)

time_tag          seconds past minute when event occurred, 0-59
opcode            XFER24 = 91 (0x5b)
seq num           sequence number, 0-0xffff ffff
tot siz           total size in bytes, 1-255
ux                flag indicating that the UCID fields (net_id, seq and timestamp) are present for xfer itn
xfer              internal trunk number of transfer trunk, 1-65535
ud                flag indicating that the UCID fields (net_id, seq and timestamp) are present for dest itn
dest              internal trunk number of destination trunk, 1-65535
type              0=transfer, 1=conference, 2=special link (G2), 3=rename, 4=path replacement (G3V10
                  and later) Special link is used for transfers that involve two physical trunks and neither of
                  the trunks drops. Rename is used when two or more facilities drop when a transfer occurs,
                  the call continues on the "dest" facility.
pnumber           number of digits in agent position, 1-16, will always be 5 for non-EAS
                  0=an unmeasured endpoint transferred the call. In this case, no position is sent.
pos-p1-p16        agent position that initiates the transfer/conference, without EAS "pos" (1-10000),
                  with EAS "p1-p16" (0-9999999) login ID in packed decimal format, left-justified
                  where hex a is digit 0 and 0 in this field is null, zero fill to a byte boundary
                  flag indicating that the UCID fields (net_id, seq and timestamp) are present

x_net_id          network entity identifier, 1-32767
x_seq             call sequence number, 0-65535
x_timestamp       unix style (seconds since 1/1/70) time call assigned a UCID
d_net_id          network entity identifier, 1-32767
d_seq             call sequence number, 0-65535
d_timestam        unix style (seconds since 1/1/70) time call assigned a UCID
p
```

<a id="pdf-page-238"></a>

## PDF page 238

Source: SPI-SYN24; PDF page 238; extracted characters: 2587.

```text
       3.4.44        CPERROR7 and CPERROR24
The Call Processing Error message will be sent by the reporting adjunct to the switch when it detects a
protocol violation in call processing messaging. This is a variable length message based on "pnumber".

3.4.44.1                   CPERROR7


                                                              Switch    Vect   Skill
                                              First Release   G3V11     y/n    y/n
                                              Last Release    CM6.3

    7   6   5   4  3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1  0
            CPERROR7                       err_opcode             /                              itn
      pnumber                                            pos (non-EAS) or p1-p15 (EAS)

opcode           CPERROR7 = 42 (0x2a)
err_opcode       opcode of the message from the switch that violates the protocol
itn              internal trunk number used to identify trunk facilities, 1-32766
pnumber          number of digits in agent position, 1-15, will always be 5 for non-EAS
pos/p1-p15       agent position - without EAS "pos" (1-10000), with EAS "p1-p15" (0-9999999) login ID in
                 packed decimal format, left-justified where hex a is digit 0 and 0 in this field is null, zero fill
                 to a byte boundary

3.4.44.2                   CPERROR24 (New CM7.0)


                                                              Switch    Vect   Skill
                                              First Release   CM7.0     y/n    y/n
                                              Last Release

    7   6   5  4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2  1   0   7   6   5   4   3   2   1   0
           CPERROR24                       err_opcode                                          itn
       / / /       pnumber                               pos (non-EAS) or p1-p16 (EAS)                               / / / /

opcode             CPERROR24 = 67 (0x43)
err_opcode         opcode of the message from the switch that violates the protocol
itn                internal trunk number used to identify trunk facilities, 1-65535
pnumber            number of digits in agent position, 1-16, will always be 5 for non-EAS
pos/p1-p16         agent position - without EAS "pos" (1-10000), with EAS "p1-p16" (0-9999999) login
                   ID in packed decimal format, left-justified where hex a is digit 0 and 0 in this field is
                   null, zero fill to a byte boundary
```

<a id="pdf-page-239"></a>

## PDF page 239

Source: SPI-SYN24; PDF page 239; extracted characters: 744.

```text
3.5      Miscellaneous
       3.5.1       NOP


                                                             Switch   Vect   Skill
                                             First Release   G3V1     y/n    y/n
                                             Last Release

The No Operation message may be sent by the reporting adjunct and ignored by the switch. Starting with
R3V2, CMS will send this as a two-byte message.

                                  7   6   5   4  3   2   1   0  7   6   5   4   3  2   1   0
                                             NOP                            NOP

                                        opcode      NOP = 11 (0xb)
                                        opcode      NOP = 11 (0xb) (sent twice)
```

<a id="pdf-page-240"></a>

## PDF page 240

Source: SPI-SYN24; PDF page 240; extracted characters: 2352.

```text
4.      Message Index

4.1     Alphabetical List

                 Table 1 Reporting Adjunct to Switch Messages – Alphabetical List

                                  Message           Code    Section In
                                  APARMS7            x28     3.3.11.1
                                  APARMS24           x3f     3.3.11.2
                                  CHGNAM20           x32     3.3.28.1
                                  CHGNAM24           x41     3.3.28.2
                                  CHGVDNSK8          x2e     3.3.18.1
                                  CHGVDNSK23         x3a     3.3.18.2
                                  CHGVEC20           x33     3.3.22.1
                                  CHGVEC24           x44     3.3.22.2
                                  CPERROR7           x2a     3.4.44.1
                                  CPERROR24          x43     3.4.44.2
                                  MVAGSTFD21         x35     3.3.10.1
                                  MVAGSTFD23         x38     3.3.10.2
                                  MVAGSTFD24         x3e     3.3.10.3
                                  MVVDN9             x2f     3.3.17.1
                                  MVVDN23            x3c     3.3.17.2
                                  NOP                x0b     3.5.1
                                  RAUDIT             x08     3.4.33.1
                                  RAUDIT24           x42     3.4.33.2
                                  RCODENAM20         x31     3.3.27
                                  REQLIST5           x23     3.3.23
                                  REQNAM20           x30     3.3.25
                                  RFTB               x06     3.2.7
                                  RLTB               x0c     3.2.8
                                  RTCS21             x34     3.2.1.1
                                  RTCS23             x37     3.2.1.2
                                  RTCS24             x3d     3.2.1.3
                                  SKILLADD8          x2d     3.3.13.1
                                  SKILLADD23         x39     3.3.13.2
                                  SKILLADD24         x40     3.3.13.3
                                  USERID21           x36     3.3.32
                                  VPARMS             x15     3.3.19
```
