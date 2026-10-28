---
title: "SPI-SYN24 - complete source pages 1-20"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 1-20

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-001"></a>

## PDF page 1

Source: SPI-SYN24; PDF page 1; extracted characters: 3185.

```text
Subject:Call Center Protocol Specification                                       Date:  May 19, 2015
        for Switch / Reporting Adjunct Interface -
        Overview and Syntax of SPI Messages                                      From:  Raechel Greschler
        Issue: 0.7                                                                      DR 2Y229
        COMPAS ID: 160965                                                               +1.303.538.5607
                                                                                        greschler@avaya.com
                                                                                        Issue 1.0


                                                       ABSTRACT

Ancestor versions of this document are:
    •    COMPAS ID 4585DR (SPI languages 1-7)
    •    COMPAS ID 96484 (SPI languages 8-9)
    •    COMPAS ID 109193 (SPI languages 20-23)

This document contains an overview of the protocol specification for the switch interface to Call Center
reporting adjuncts starting with SPI language 24. Reporting adjuncts are management information
systems that reside on an adjunct processor. They track ACD activity and collect data provided by the
switch, and use this data to generate various real-time and historical reports. The data collected includes
information about agents, splits, trunks, trunk groups, VDNs, and vectors. Reporting adjuncts also have
some limited switch administration capabilities.

The entire definition of the protocol specification has been split in three documents. This document
contains an overview of the communications protocol and the layout and rules for each message. The
syntax for messages to the reporting adjuncts is covered. The semantics to the protocol (call trees) can
be found in COMPAS ID 21003. The semantics document gives message sequences for various call
scenarios. The database definitions for the R3V8 database can be found in COMPAS ID 19974.

This document is written using generic product terms as much as possible. “Switch” can refer to releases
of G3, DEFINITY®, MultiVantage® or Communication Manager®. “Reporting Adjunct” can refer to
releases of CMS®, R3Vx, IQ®, WAE (Work Assignment Engine), etc. All SPI messages apply to all
reporting adjunct products with the following exceptions:
    •    When the switch receives CHGVDNSK, MVAGSTFD, MVVDN, SKILLADD or CHGNAM from IQ
         (SPI language 21+) and WAE, it will wait for USERID message
    •    The switch will only accept REQNAM, RCODENAM, CHGNAM or USERID from IQ (SPI
         language 21+) and WAE
    •    If the switch receives RLTB from IQ (SPI language 21+) or WAE, it will abort an ADMNAM
    •     download in progress
    •    WAE does not do pumpup
    •    The only audits that the switch sends to IQ are EWTAUDIT or VAUDIT.
    •    IQ only supports an EAS environment. Any non-EAS messages are not sent to IQ.
    •    IQ does not support vector admin (VECTOR, CHGVEC).











Issue 1.0                                        Avaya, Inc. – Proprietary                                    Page 1 of 253
                                          Use pursuant to Company Instructions
```

<a id="pdf-page-002"></a>

## PDF page 2

Source: SPI-SYN24; PDF page 2; extracted characters: 3527.

```text
Issue 1.0 has the following changes from COMPAS ID 109193:

    −    “Quick Links to SPI Messages” was added.
    −    The Cross-reference table in section 3.1 was updated
    −    COMPAS MRs (79738, 80260) from the prior version of this document (COMPAS ID 109193)
         were resolved
    −    References to specific reporting products were minimized
    −    General cleanup and minor reorganization. Obsolete information was removed (see ancestor
         documents for this information).
    −    Add SPI language 24 (based on SRAD Compas ID 166079), including,

sorted by requirements:

    •    Overhead for new SPI L24 language
             o    New XSTAT24 for support of SPI language 24 (CMS R3V18) and Release 3 (CM7.0)
    •    Support increased agent-skill pairs
             o    New RTCS24 and XFAIL24 for support of 360,000 agent/skill pairs
    •    Support CM increased locations to 2000
             o    New XTRUNK24, ARTRUNK24 and ALOGON24 for support of 2,000 location IDs
    •    Send quantity of licensed logged in agents allowed
             o    New XSTAT24 to send quantity of licensed logged in agents allowed
    •    Expand DADFWD24 for support of 8000 skills
             o    New DADFWD24 for support of 8000 skills (outage from SPI language 23)
    •    Add specific RCODE for tenant number mismatch for Match Agent Skills feature
    •    Add “b” beginning bit to ADMNAM24 for agent object type along with spare bits
             o    Noted partial support of the “b” (beginning) bit in ADMNAM20 starting with FP4
             o    New ADMNAM24 for full support of “b” (beginning) bit
    •    Support increased extension size (to 16 digits)
                          support increased dnumber (from 4 to 5 bits) AND increase digits from d1-d15 to
                           d1-d16: XVDN24, XAGENT24, ARVDN24, ARAGENT24, MVAGSTFD24,
                           APARMS24, AGENTSK24, SKILLADD24, VECTOR24, CHGVEC24,
                           ALOGON24, DFWD24
                          support increased pnumber (from 4 to 5 bits) AND increase digits from p1-p15 to
                           p1-p16: ADMNAM24, CHGNAM24, ALOGON24, ALOGOFF24, AVAIL24,
                           ACD24, ACW24, AUX24, OTHER24, DIGITS24, AEVENT24, DAQUEUED24,
                           DCON24, DABN24, DADFWD24, HOLD24, RECON24, AUDAVAIL24,
                           AUDACD24, AUDACW24, AUDAUX24, AUDOTHER24, AUDUNSTF24,
                           XFER24, CPERROR24
    •    Support increased trunk capacity
             o    support of 24,000 measured trunks (64,000 future): RTCS24, XFAIL24
             o    allow sending 64,000 trunk messages: XTRUNK24
             o    allow sending 9999 XTRUNK messages per trunk group: XCLOSE20
             o    Increase ITN from 15 to 16 bits: XTRUNK24, ARTRUNK24, DIGITS24, IDLE24,
                  SETUP24, QUEUED24, DAQUEUED24, DCON24, DABN24, DADFWD24, DFWD24,
                  MBUSY24, FBUSY24, VSTART24, VSTOP24, FDISC24, HOLD24, RECON24,
                  COMP24, LOOKAH24, AROUTE24, DNEVENT24, RAUDIT24, TAUDIT24, XFER24,
                  CPERROR24
    •    Support Tenant related info to reporting adjunct
             o    send Tenant Number: XVDN24, XSPLIT24, XTKGRP24, XTGVDN24, ARVDN24,
                  ARSPLIT24, ARTKGRP24, ARTGVDN24, VDNMOVE24, ALOGON24
Issue 1.0                                     Avaya, Inc. – Proprietary                                Page 2 of 253
                                       Use pursuant to Company Instructions
```

<a id="pdf-page-003"></a>

## PDF page 3

Source: SPI-SYN24; PDF page 3; extracted characters: 2781.

```text
    •    Add why sent info to SETUP
              o    Add a 4 bit reason code to SETUP24 indicating why the SETUP was sent
    •    Change trunk eqloc format to match virtual trunk locations
              o    Use a spare bit  to indicate the location fields are for virtual IP/SIP trunk number:
                   XTRUNK24, ARTRUNK24
              o    Allow the location fields to be a virtual IP/SIP trunk number (range 0001-64,000):
                   XTRUNK24, ARTRUNK24
    •    Send Attribute reporting attribute in ALOGON message

sorted by message:

    •    RTCS
              o    support of 360,000 agent/skill pairs
              o    support of 24,000 measured trunks (64,000 future)
    •    XFAIL
              o    support of 360,000 agent/skill pairs
              o    support of 24,000 measured trunks (64,000 future)
    •    XSTAT
              o    support of SPI language 24 (CMS R3V18) and Release 3 (CM7.0)
              o    send quantity of licensed logged in agents allowed
    •    XCLOSE
              o    allow sending 9999 XTRUNK messages per trunk group
    •    XVDN
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
              o    send tenant number (new field, 10 bits)
    •    XSPLIT
              o    send tenant number (new field, 10 bits)
    •    XAGENT
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
    •    XTKGRP
              o    send tenant number (new field, 10 bits)
    •    XTGVDN
              o    send tenant number (new field, 10 bits)
    •    XTRUNK
              o    Support CM increased locations to 2000
              o    Increase ITN from 15 to 16 bits
              o    Use a spare bit to indicate the location fields are for virtual IP/SIP trunk number
              o    Allow the location fields to be a virtual IP/SIP trunk number (range 00001-64,000)
              o    allow sending 24,000 trunk messages (64,000 future)
    •    ARVDN
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
              o    send tenant number (new field, 10 bits)
    •    ARAGENT
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
    •    ARSPLIT
              o    send tenant number (new field, 10 bits)
    •    ARTKGRP
              o    send tenant number (new field, 10 bits)
    •    ARTGVDN
              o    send tenant number (new field, 10 bits)
    •    ARTRUNK

Issue 1.0                                        Avaya, Inc. – Proprietary                                     Page 3 of 253
                                          Use pursuant to Company Instructions
```

<a id="pdf-page-004"></a>

## PDF page 4

Source: SPI-SYN24; PDF page 4; extracted characters: 3195.

```text
              o    Support CM increased locations to 2000
              o    Move “r” bit to make room for ITN increase.
              o    Increase ITN from 15 to 16 bits
              o    Use a spare bit to indicate the location fields are for virtual IP/SIP trunk number
              o    Allow the location fields to be a virtual IP/SIP trunk number (range 00001-64,000)
    •    MVAGSTFD
              o    support increased extension size (pos from 13 nybles to 16 nybles)
              o    receive up to 2 messages instead of 1. Add an end bit.
    •    APARMS
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AGENTSK
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    SKILLADD
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    VDNMOVE
              o    send tenant number (new field, 10 bits)
    •    VECTOR/CHGVEC
              o    support increased ANI
                            Goto format D (ANI), new condition 24 supports 24 digits in ANI
                            Route-to number
              o    support increased extension size (go to d1-d16)
                            announcement step
                            wait step
                            goto step (format D)
                            disconnect step
                            collect step
                            messaging step
    •    ADMNAM
              o    Add “b” beginning bit to ADMNAM24 for agent object type along with spare bits
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    CHGNAM
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    RCODE20
              o    Add specific RCODE for tenant number mismatch for Match Agent Skills feature
    •    ALOGON
              o    Support CM increased locations to 2000
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
              o    send tenant number (new field, 10 bits)
              o    Send Attribute reporting attribute in ALOGON message
              o    Send up to 3 messages instead of 2.
    •    ALOGOFF
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AVAIL
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    ACD
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    ACW
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUX

Issue 1.0                                         Avaya, Inc. – Proprietary                                     Page 4 of 253
                                          Use pursuant to Company Instructions
```

<a id="pdf-page-005"></a>

## PDF page 5

Source: SPI-SYN24; PDF page 5; extracted characters: 2793.

```text
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    OTHER
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    DIGITS
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
                            used to hold both agent position and ITN
    •    AEVENT
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    IDLE
              o    Increase ITN from 15 to 16 bits
    •    SETUP
              o    Increase ITN from 15 to 16 bits
              o    Add a 4 bit reason code to SETUP24 indicating why the SETUP was sent
    •    QUEUED
              o    Increase ITN from 15 to 16 bits
    •    DAQUEUED
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    DCON
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    DABN
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    DADFWD
              o    Expand DADFWD24 for support of 8000 skills
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    DFWD
              o    support increased extension size (dnumber from 4 to 5 bits, digits from d1-d15 to d1-d16)
              o    Increase ITN from 15 to 16 bits
    •    MBUSY
              o    Increase ITN from 15 to 16 bits
    •    FBUSY
              o    Increase ITN from 15 to 16 bits
    •    VSTART
              o    Increase ITN from 15 to 16 bits
    •    VSTOP
              o    Increase ITN from 15 to 16 bits
    •    FDISC
              o    Increase ITN from 15 to 16 bits
    •    HOLD
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    RECON
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    COMP
              o    Increase ITN from 15 to 16 bits
    •    LOOKAH
              o    Increase ITN from 15 to 16 bits

Issue 1.0                                         Avaya, Inc. – Proprietary                                    Page 5 of 253
                                          Use pursuant to Company Instructions
```

<a id="pdf-page-006"></a>

## PDF page 6

Source: SPI-SYN24; PDF page 6; extracted characters: 1676.

```text
    •    AROUTE
              o    Increase ITN from 15 to 16 bits
    •    ASA
              o    Increase ITN from 15 to 16 bits
    •    DNEVENT
              o    Increase ITN from 15 to 16 bits
    •    RAUDIT
              o    Increase ITN from 15 to 16 bits
    •    TAUDIT
              o    Increase ITN from 15 to 16 bits
    •    AUDAVAIL
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUDACD
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUDACW
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUDAUX
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUDOTHER
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    AUDUNSTF
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
    •    XFER
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits
    •    CPERROR
              o    support increased extension size (pnumber from 4 to 5 bits, digits from p1-p15 to p1-p16)
              o    Increase ITN from 15 to 16 bits

































Issue 1.0                                         Avaya, Inc. – Proprietary                                    Page 6 of 253
                                          Use pursuant to Company Instructions
```

<a id="pdf-page-007"></a>

## PDF page 7

Source: SPI-SYN24; PDF page 7; extracted characters: 3374.

```text
LINKS TO SPI MESSAGE DESIGNS

   •   ACD 3.4.5                                          •   FDISC 3.4.23
   •   ACW 3.4.6                                          •   HOLD 3.4.24
   •   ADMLIST 3.3.24                                     •   IDLE 3.4.11
   •   ADMNAM 3.3.26                                      •   LOOKAH 3.4.27
   •   AEVENT 3.4.10                                      •   MBUSY 3.4.19
   •   AGENTSK 3.3.12                                     •   MODEVENT 3.4.32
   •   AGMOVE 3.3.9                                       •   MVAGSTFD 3.3.10
   •   ALOGOFF 3.4.3                                      •   MVRCODE 3.3.29
   •   ALOGON 3.4.2                                       •   MVVDN 3.3.17
   •   APARMS 3.3.11                                      •   NOP 3.5.1
   •   ARAGENT 3.3.4                                      •   OTHER 3.4.8
   •   AROUTE 3.4.28                                      •   QUEUED 3.4.13
   •   ARSPLIT 3.3.5                                      •   RAUDIT 3.4.33
   •   ARTGVDN 3.3.7                                      •   RCODE 3.3.30
   •   ARTKGRP 3.3.6                                      •   RCODENAM 3.3.27
   •   ARTRUNK 3.3.8                                      •   RECON 3.4.25
   •   ARVDN 3.3.3                                        •   RELBUSY 3.3.2
   •   ASA 3.4.30                                         •   REQLIST 3.3.23
   •   AUDACD 3.4.36                                      •   REQNAM 3.3.25
   •   AUDACW 3.4.37                                      •   RFTB 3.2.7
   •   AUDAUX 3.4.38                                      •   RLTB 3.2.8
   •   AUDAVAIL 3.4.35                                    •   RTCS 3.2.1
   •   AUDOTHER 3.4.39                                    •   SETUP 3.4.12
   •   AUDUNSTF 3.4.40                                    •   SKILLADD 3.3.13
   •   AUX 3.4.7                                          •   SKSTATE 3.4.29
   •   AVAIL 3.4.4                                        •   TAUDIT 3.4.34
   •   BUSYOUT 3.3.1                                      •   TGMOVE 3.3.14
   •   CHGNAM 3.3.28                                      •   TIME 3.4.1
   •   CHGVDNSK 3.3.18                                    •   USERID 3.3.32
   •   CHGVEC 3.3.22                                      •   VAUDIT 3.4.42
   •   COMP 3.4.26                                        •   VDNMOVE 3.3.16
   •   CPERROR 3.4.44                                     •   VECTOR 3.3.20
   •   CRCODE 3.3.31                                      •   VPARMS 3.3.19
   •   DABN 3.4.16                                        •   VSTART 3.4.21
   •   DADFWD 3.4.17                                      •   VSTOP 3.4.22
   •   DAQUEUED 3.4.14                                    •   VTGMOVE 3.3.15
   •   DCON 3.4.15                                        •   XAGENT 3.2.13
   •   DFWD 3.4.18                                        •   XCLOSE 3.2.10
   •   DIGITS 3.4.9                                       •   XFAIL 3.2.3
   •   DNEVENT 3.4.31                                     •   XFER 3.4.43
   •   EWTAUDIT 3.4.41                                    •   XOPEN 3.2.9
   •   FBUSY 3.4.20                                       •   XSPLIT 3.2.12

Issue 1.0                               Avaya, Inc. – Proprietary                        Page 7 of 253
                                  Use pursuant to Company Instructions
```

<a id="pdf-page-008"></a>

## PDF page 8

Source: SPI-SYN24; PDF page 8; extracted characters: 457.

```text
    •    XSTAT 3.2.5                                                •    XTRUNK 3.2.16
    •    XTGVDN 3.2.15                                              •    XVDN 3.2.11
    •    XTKGRP 3.2.14



































































Issue 1.0                                      Avaya, Inc. – Proprietary                                 Page 8 of 253
                                        Use pursuant to Company Instructions
```

<a id="pdf-page-009"></a>

## PDF page 9

Source: SPI-SYN24; PDF page 9; extracted characters: 5346.

```text
                                                  TABLE OF CONTENTS

1. Introduction..................................................................................................................18
   1.1 Purpose...................................................................................................................18
   1.2 Overview.................................................................................................................18
      1.2.1 OSI Reference Model.......................................................................................18
         1.2.1.1 Physical Layer............................................................................................19
         1.2.1.2 Data Link Layer...........................................................................................19
         1.2.1.3 Network Layer.............................................................................................19
         1.2.1.4 Transport Layer..........................................................................................19
         1.2.1.5 Session Layer.............................................................................................19
         1.2.1.6 Presentation Layer......................................................................................19
         1.2.1.7 Application Layer........................................................................................19
      1.2.2 X.25 Protocol....................................................................................................20
      1.2.3 BX.25 Protocol..................................................................................................20
      1.2.4 TCP/IP Protocol................................................................................................20
      1.2.5 Reporting Adjunct Protocol...............................................................................20
   1.3 Terminology............................................................................................................21
2. PROTOCOL SPECIFICATION....................................................................................24
3. PROTOCOL SYNTAX.................................................................................................26
   3.1 Compatibility...........................................................................................................26
   3.2 Translation Pumpup................................................................................................31
      3.2.1 RTCS21, RTCS23 and RTCS24...................................................................31
         3.2.1.1 RTCS21 (New CM4)...............................................................................32
         3.2.1.2 RTCS23 (New CM6.0)............................................................................32
         3.2.1.3 RTCS24 (New CM7.0)............................................................................33
      3.2.2 RCODE20.....................................................................................................34
      3.2.3 XFAIL21, XFAIL23 and XFAIL24..................................................................34
         3.2.3.1 XFAIL21 (New CM4)...............................................................................34
         3.2.3.2 XFAIL23 (New CM6.0)............................................................................35
         3.2.3.3 XFAIL24 (New CM7.0)............................................................................35
      3.2.4 BUSYOUT20 (New CM3.1)..........................................................................35
      3.2.5 XSTAT20 and XSTAT24...............................................................................36
         3.2.5.1 XSTAT20 (New CM3.1)..........................................................................36
         3.2.5.2 XSTAT24 (New CM7.0)..........................................................................38
      3.2.6 TIME20 (New CM3.1)...................................................................................39
      3.2.7 RFTB.............................................................................................................40
      3.2.8 RLTB.............................................................................................................40
      3.2.9 XOPEN20 (New CM3.1)...............................................................................41
      3.2.10 XCLOSE20 (New CM3.1)...........................................................................42
      3.2.11 XVDN20, XVDN23 and XVDN24................................................................43
         3.2.11.1 XVDN20 (New CM3.1)..........................................................................43
         3.2.11.2 XVDN23 (New CM6.0)..........................................................................44
         3.2.11.3 XVDN24 (New CM7.0)..........................................................................45


Issue 1.0                                                 Avaya, Inc. – Proprietary                                              Page 9 of 253
                                                 Use pursuant to Company Instructions
```

<a id="pdf-page-010"></a>

## PDF page 10

Source: SPI-SYN24; PDF page 10; extracted characters: 4752.

```text
   3.2.12 XSPLIT20 and XSPLIT24...........................................................................46
      3.2.12.1 XSPLIT20 (New CM3.1).......................................................................46
      3.2.12.2 XSPLIT24 (New CM7.0).......................................................................46
   3.2.13 XAGENT20 and XAGENT24......................................................................47
      3.2.13.1 XAGENT20 (New CM3.1).....................................................................47
      3.2.13.2 XAGENT24 (New CM7.0).....................................................................48
   3.2.14 XTKGRP20 and XTKGRP24......................................................................49
      3.2.14.1 XTKGRP20 (New CM3.1).....................................................................49
      3.2.14.2 XTKGRP24 (New CM7.0).....................................................................49
   3.2.15 XTGVDN20 and XTGVDN24......................................................................50
      3.2.15.1 XTGVDN20 (New CM3.1).....................................................................50
      3.2.15.2 XTGVDN24 (New CM7.0).....................................................................50
   3.2.16 XTRUNK20 and XTRUNK24......................................................................51
      3.2.16.1 XTRUNK20 (New CM3.1).....................................................................51
      3.2.16.2 XTRUNK24 (New CM7.0).....................................................................52
   3.2.17 SKSTATE20 and SKSTATE23...................................................................52
   3.2.18 ALOGON20, ALOGON23 and ALOGON24................................................52
3.3 Switch Administration.............................................................................................53
   3.3.1 BUSYOUT20 (New CM3.1)..........................................................................54
   3.3.2 RELBUSY20 (New CM3.1)...........................................................................54
   3.3.3 ARVDN20, ARVDN23 and ARVDN24..........................................................55
      3.3.3.1 ARVDN20 (New CM3.1).........................................................................55
      3.3.3.2 ARVDN23 (New CM6.0).........................................................................56
      3.3.3.3 ARVDN24 (New CM7.0).........................................................................57
   3.3.4 ARAGENT20 and ARAGENT24...................................................................58
      3.3.4.1 ARAGENT20 (New CM3.1)....................................................................58
      3.3.4.2 ARAGENT24 (New CM7.0)....................................................................59
   3.3.5 ARSPLIT20, ARSPLIT23 and ARSPLIT24...................................................60
      3.3.5.1 ARSPLIT20 (New CM3.1).......................................................................60
      3.3.5.2 ARSPLIT23 (New CM6.0).......................................................................60
      3.3.5.3 ARSPLIT24 (New CM7.0........................................................................61
   3.3.6 ARTKGRP20, ARTKGRP23 and ARTKGRP24............................................62
      3.3.6.1 ARTKGRP20 (New CM3.1)....................................................................62
      3.3.6.2 ARTKGRP23 (New CM6.0)....................................................................62
      3.3.6.3 ARTKGRP24 (New CM7.0)....................................................................63
   3.3.7 ARTGVDN20 and ARTGVDN24...................................................................64
      3.3.7.1 ARTGVDN20 (New CM3.1)....................................................................64
      3.3.7.2 ARTGVDN24 (New CM7.0)....................................................................64
   3.3.8 ARTRUNK20 and ARTRUNK24...................................................................65
      3.3.8.1 ARTRUNK20 (New CM3.1)....................................................................65
      3.3.8.2 ARTRUNK24 (New CM7.0)....................................................................66
   3.3.9 AGMOVE20 (New CM3.1)............................................................................67

Issue 1.0                                           Avaya, Inc. – Proprietary                                        Page 10 of
                                                              253
                                           Use pursuant to Company Instructions
```

<a id="pdf-page-011"></a>

## PDF page 11

Source: SPI-SYN24; PDF page 11; extracted characters: 4981.

```text
   3.3.10  MVAGSTFD21, MVAGSTFD23 and MVAGSTFD24.................................68
      3.3.10.1 MVAGSTFD21 (New CM4)...................................................................69
      3.3.10.2 MVAGSTFD23 (New CM6.0)................................................................70
      3.3.10.3 MVAGSTFD24 (New CM7.0)................................................................71
   3.3.11 APARMS7 and APARMS24........................................................................72
      3.3.11.1 APARMS7 (New G3V11)......................................................................72
      3.3.11.2 APARMS24 (New CM7.0).....................................................................72
   3.3.12 AGENTSK20, AGENTSK23, AGENTSK24................................................73
      3.3.12.1 AGENTSK20 (New CM3.1)...................................................................73
      3.3.12.2 AGENTSK23 (New CM6.0)...................................................................74
      3.3.12.3 AGENTSK24 (New CM7.0)...................................................................76
   3.3.13 SKILLADD8, SKILLADD23 and SKILLADD24...........................................78
      3.3.13.1 SKILLADD8 (New MV2)........................................................................78
      3.3.13.2 SKILLADD23 (New CM6.0)..................................................................79
      3.3.13.3 SKILLADD24 (New CM7.0)..................................................................80
   3.3.14 TGMOVE20 and TGMOVE23.....................................................................82
      3.3.14.1 TGMOVE20 (New CM3.1)....................................................................82
      3.3.14.2 TGMOVE23 (New CM6.0)....................................................................82
   3.3.15 VTGMOVE20 (New CM3.1)........................................................................83
   3.3.16 VDNMOVE20, VDNMOVE23 and VDNMOVE24.......................................84
      3.3.16.1 VDNMOVE20 (New CM3.1)..................................................................84
      3.3.16.2 VDNMOVE23 (New CM6.0)..................................................................85
      3.3.16.3 VDNMOVE24 (New CM7.0)..................................................................85
   3.3.17  MVVDN9 and MVVDN23...........................................................................86
      3.3.17.1 MVVDN9 (New CM3)............................................................................86
      3.3.17.2 MVVDN23 (New CM6.0).......................................................................86
   3.3.18 CHGVDNSK8 and CHGVDNSK23.............................................................87
      3.3.18.1 CHGVDNSK8 (New MV2).....................................................................87
      3.3.18.2 CHGVDNSK23 (New CM6.0)...............................................................87
   3.3.19 VPARMS.....................................................................................................88
   3.3.20 VECTOR20 and VECTOR24..........................................................................89
      3.3.20.1 VECTOR20 (New CM3.1).....................................................................90
      3.3.20.2 VECTOR24 (New CM7.0).....................................................................91
   3.3.21 Vector Steps...................................................................................................92
      3.3.21.1 Queue to...................................................................................................92
      3.3.21.2 Check........................................................................................................93
      3.3.21.3 Route To Number.....................................................................................95
      3.3.21.4 Announcement..........................................................................................97
      3.3.21.5 Wait...........................................................................................................97
      3.3.21.6 Goto Step and Goto Vector......................................................................98
      3.3.21.7 Disconnect..............................................................................................109
      3.3.21.8 Busy........................................................................................................109
      3.3.21.9 Stop.........................................................................................................109

Issue 1.0                                             Avaya, Inc. – Proprietary                                         Page 11 of
                                                                253
                                            Use pursuant to Company Instructions
```

<a id="pdf-page-012"></a>

## PDF page 12

Source: SPI-SYN24; PDF page 12; extracted characters: 5049.

```text
      3.3.21.10 Collect Digits.........................................................................................110
      3.3.21.11 Route To Digits.....................................................................................110
      3.3.21.12 Messaging Split....................................................................................111
      3.3.21.13 Adjunct Routing....................................................................................111
      3.3.21.14 Converse..............................................................................................112
      3.3.21.15 Consider...............................................................................................112
      3.3.21.16 Reply.....................................................................................................113
      3.3.21.17 Return...................................................................................................113
      3.3.21.18 Set.........................................................................................................114
   3.3.22  CHGVEC20 AND CHGVEC24.................................................................115
      3.3.22.1 CHGVEC20 (New CM3.1)..................................................................115
      3.3.22.2 CHGVEC24 (New CM7.0)..................................................................116
   3.3.23 REQLIST5 (New G3V6)............................................................................117
   3.3.24 ADMLIST20 (New CM3.1)........................................................................118
   3.3.25 REQNAM20 (New CM3.1)........................................................................119
   3.3.26 ADMNAM20 and ADMNAM24..................................................................120
      3.3.26.1 ADMNAM20 (New CM3.1)..................................................................120
      3.3.26.2 ADMNAM24 (New CM7.0)..................................................................123
   3.3.27 RCODENAM20 (New CM3.1)...................................................................125
   3.3.28  CHGNAM20 and CHGNAM24.................................................................126
      3.3.28.1 CHGNAM20 (New CM3.1)..................................................................126
      3.3.28.2  CHGNAM24 (New CM7.0).................................................................128
   3.3.29 MVRCODE20 (New CM3.1).....................................................................130
   3.3.30 RCODE20 (New CM3.1)...........................................................................131
   3.3.31 CRCODE20 (New CM3.1)........................................................................134
   3.3.32 USERID21 (New CM4).............................................................................136
3.4 Call Processing.....................................................................................................137
   3.4.1 TIME20 (New CM3.1).................................................................................137
   3.4.2 ALOGON20, ALOGON23 and ALOGON24................................................138
      3.4.2.1 ALOGON20 (New CM3.1)....................................................................139
      3.4.2.2 ALOGON23 (New CM6.0)....................................................................141
      3.4.2.3 ALOGON24 (New CM7.0)....................................................................144
   3.4.3  ALOGOFF20 and ALOGOFF24.................................................................147
      3.4.3.1 ALOGOFF20 (New CM3.1)...................................................................147
      3.4.3.2 ALOGOFF24 (New CM7.0)...................................................................147
   3.4.4  AVAIL22, AVAIL23 and AVAIL24..............................................................148
      3.4.4.1 AVAIL22 (New CM5.2)..........................................................................148
      3.4.4.2 AVAIL23 (New CM6.0)..........................................................................149
      3.4.4.3 AVAIL24 (New CM7.0)..........................................................................150
   3.4.5  ACD20 and ACD24....................................................................................151
      3.4.5.1 ACD20 (New CM3.1)............................................................................151
      3.4.5.2 ACD24 (New CM7.0)............................................................................152
   3.4.6  ACW22 and ACW24..................................................................................153

Issue 1.0                                             Avaya, Inc. – Proprietary                                           Page 12 of
                                                                 253
                                            Use pursuant to Company Instructions
```

<a id="pdf-page-013"></a>

## PDF page 13

Source: SPI-SYN24; PDF page 13; extracted characters: 4769.

```text
      3.4.6.1 ACW22 (New CM5.2)...........................................................................153
      3.4.6.2  ACW24 (New CM7.0)..........................................................................154
   3.4.7  AUX22, AUX23 and AUX24.......................................................................155
      3.4.7.1 AUX22 (New CM5.2)............................................................................155
      3.4.7.2 AUX23 (New CM6.0)............................................................................156
      3.4.7.3 AUX24 (New CM7.0)............................................................................157
   3.4.8 OTHER22 and OTHER24...........................................................................158
      3.4.8.1 OTHER22 (New CM5.2).......................................................................158
      3.4.8.2 OTHER24 (New CM7.0).......................................................................159
   3.4.9  DIGITS20 and DIGITS24...........................................................................160
      3.4.9.1 DIGITS20 (New CM3.1)........................................................................160
      3.4.9.2 DIGITS24 (New CM7.0)........................................................................162
   3.4.10 AEVENT20 and AEVENT24.....................................................................164
      3.4.10.1 AEVENT20 (New CM3.1)...................................................................165
      3.4.10.2 AEVENT24 (New CM7.0)...................................................................166
   3.4.11 IDLE20, IDLE23 and IDLE24....................................................................167
      3.4.11.1 IDLE20 (New CM3.1)..........................................................................167
      3.4.11.2 IDLE23 (New CM6.0)..........................................................................168
      3.4.11.3 IDLE24 (New CM7.0)..........................................................................169
   3.4.12  SETUP22 and SETUP24.........................................................................170
      3.4.12.1 SETUP22 (New CM5.2)......................................................................170
      3.4.12.2 SETUP24 (New CM7.0)......................................................................171
   3.4.13 QUEUED20, QUEUED23 and QUEUED24..............................................172
      3.4.13.1 QUEUED20 (New CM3.1)..................................................................172
      3.4.13.2 QUEUED23 (New CM6.0)..................................................................173
      3.4.13.3 QUEUED24 (New CM7.0)..................................................................174
   3.4.14 DAQUEUED20, DAQUEUED23 and DAQUEUED24..............................175
      3.4.14.1 DAQUEUED20 (New CM3.1).............................................................175
      3.4.14.2 DAQUEUED23 (New CM6.0).............................................................176
      3.4.14.3 DAQUEUED24 (New CM7.0).............................................................177
   3.4.15  DCON22, DCON23 and DCON24...........................................................178
      3.4.15.1 DCON22 (New CM5.2).......................................................................178
      3.4.15.2 DCON23 (New CM6.0).......................................................................179
      3.4.15.3 DCON24 (New CM7.0).......................................................................180
   3.4.16 DABN22 and DABN24..............................................................................181
      3.4.16.1 DABN22 (New CM5.2)........................................................................181
      3.4.16.2 DABN24 (New CM7.0)........................................................................182
   3.4.17 DADFWD20 and DADFWD24..................................................................183
      3.4.17.1 DADFWD20 (New CM3.1)..................................................................183
      3.4.17.2 DADFWD24 (New CM7.0)..................................................................184
   3.4.18 DFWD20, DFWD23 and DFWD24...........................................................185
      3.4.18.1 DFWD20 (New CM3.1).......................................................................185

Issue 1.0                                           Avaya, Inc. – Proprietary                                        Page 13 of
                                                               253
                                           Use pursuant to Company Instructions
```

<a id="pdf-page-014"></a>

## PDF page 14

Source: SPI-SYN24; PDF page 14; extracted characters: 4799.

```text
      3.4.18.2 DFWD23 (New CM6.0).......................................................................187
      3.4.18.3 DFWD24 (New CM7.0).......................................................................189
   3.4.19 MBUSY20 and MBUSY24........................................................................191
      3.4.19.1 MBUSY20 (New CM3.1).....................................................................191
      3.4.19.2 MBUSY24 (New CM7.0).....................................................................191
   3.4.20 FBUSY20 and FBUSY24..........................................................................192
      3.4.20.1 FBUSY20 (New CM3.1)......................................................................192
      3.4.20.2 FBUSY24 (New CM7.0)......................................................................192
   3.4.21 VSTART20 and VSTART24......................................................................193
      3.4.21.1 VSTART20 (New CM3.1)....................................................................193
      3.4.21.2 VSTART24 (New CM7.0)....................................................................193
   3.4.22 VSTOP20 and VSTOP24..........................................................................194
      3.4.22.1 VSTOP20 (New CM3.1)......................................................................194
      3.4.22.2 VSTOP24 (New CM7.0)......................................................................194
   3.4.23 FDISC20 and FDISC24............................................................................195
      3.4.23.1 FDISC20 (New CM3.1).......................................................................195
      3.4.23.2 FDISC24 (New CM7.0).......................................................................196
   3.4.24 HOLD20 and HOLD24..............................................................................197
      3.4.24.1 HOLD20 (New CM3.1)........................................................................197
      3.4.24.2 HOLD24 (New CM7.0)........................................................................198
   3.4.25 RECON20, RECON23 and RECON24.....................................................199
      3.4.25.1 RECON20 (New CM3.1).....................................................................199
      3.4.25.2 RECON23 (New CM6.0).....................................................................200
      3.4.25.3 RECON24 (New CM7.0).....................................................................201
   3.4.26 COMP20 and COMP24............................................................................202
      3.4.26.1 COMP20 (New CM3.1).......................................................................202
      3.4.26.2 COMP24 (New CM7.0).......................................................................202
   3.4.27 LOOKAH20 and LOOKAH24....................................................................203
      3.4.27.1 LOOKAH20 (New CM3.1)...................................................................203
      3.4.27.2 LOOKAH24 (New CM7.0)...................................................................203
   3.4.28 AROUTE20 and AROUTE24....................................................................204
      3.4.28.1 AROUTE20 (New CM3.1)...................................................................204
      3.4.28.2 AROUTE24 (New CM7.0)...................................................................204
   3.4.29 SKSTATE20 and SKSTATE23.................................................................205
      3.4.29.1 SKSTATE20 (New CM3.1).................................................................205
      3.4.29.2 SKSTATE23 (New CM6.0).................................................................206
   3.4.30 ASA20 and ASA23....................................................................................207
      3.4.30.1 ASA20 (New CM3.1)...........................................................................207
      3.4.30.2 ASA23 (New CM6.0)...........................................................................207
   3.4.31 DNEVENT20 and DNEVENT24................................................................208
      3.4.31.1 DNEVENT20 (New CM3.1).................................................................208
      3.4.31.2 DNEVENT24 (New CM7.0).................................................................209

Issue 1.0                                            Avaya, Inc. – Proprietary                                        Page 14 of
                                                               253
                                           Use pursuant to Company Instructions
```

<a id="pdf-page-015"></a>

## PDF page 15

Source: SPI-SYN24; PDF page 15; extracted characters: 4833.

```text
     3.4.32 MODEVENT20 (New CM3.1)...................................................................210
     3.4.33 RAUDIT and RAUDIT24...........................................................................211
        3.4.33.1 RAUDIT...............................................................................................211
        3.4.33.2 RAUDIT24 (New CM7.0)....................................................................212
     3.4.34 TAUDIT20 and TAUDIT24........................................................................213
        3.4.34.1 TAUDIT20 (New CM3.1).....................................................................214
        3.4.34.2 TAUDIT24 (New CM7.0).....................................................................215
     3.4.35  AUDAVAIL22, AUDAVAIL23 and AUDAVAIL24.....................................216
        3.4.35.1 AUDAVAIL22 (New CM5.2)................................................................216
        3.4.35.2 AUDAVAIL23 (New CM6.0)................................................................217
        3.4.35.3 AUDAVAIL24 (New CM7.0)................................................................218
     3.4.36 AUDACD20, AUDACD23 and AUDACD24..............................................219
        3.4.36.1 AUDACD20 (New CM3.1)...................................................................219
        3.4.36.2 AUDACD23 (New CM6.0)...................................................................220
        3.4.36.3 AUDACD24 (New CM7.0)...................................................................221
     3.4.37 AUDACW20, AUDACW23 and AUDACW24............................................222
        3.4.37.1 AUDACW20 (New CM3.1)..................................................................222
        3.4.37.2 AUDACW23 (New CM6.0)..................................................................223
        3.4.37.3 AUDACW24 (New CM7.0)..................................................................224
     3.4.38 AUDAUX20, AUDAUX23 and AUDAUX24...............................................225
        3.4.38.1 AUDAUX20 (New CM3.1)...................................................................225
        3.4.38.2 AUDAUX23 (New CM6.0)...................................................................226
        3.4.38.3 AUDAUX24 (New CM7.0)...................................................................227
     3.4.39  AUDOTHER22 and AUDOTHER24........................................................228
        3.4.39.1 AUDOTHER22 (New CM5.2).............................................................228
        3.4.39.2 AUDOTHER24 (New CM7.0).............................................................229
     3.4.40 AUDUNSTF20 and AUDUNSTF24...........................................................230
        3.4.40.1 AUDUNSTF20 (New CM3.1)..............................................................230
        3.4.40.2 AUDUNSTF24 (New CM7.0)..............................................................230
     3.4.41 EWTAUDIT20 and EWTAUDIT23............................................................231
        3.4.41.1 EWTAUDIT20 (New CM3.1)...............................................................231
        3.4.41.2 EWTAUDIT23 (New CM6.0)...............................................................232
     3.4.42 VAUDIT20 (New CM3.1)...........................................................................233
     3.4.43 XFER20 and XFER24...............................................................................234
        3.4.43.1 XFER20 (New CM3.1)........................................................................234
        3.4.43.2 XFER24 (New CM7.0)........................................................................236
     3.4.44  CPERROR7 and CPERROR24...............................................................238
        3.4.44.1 CPERROR7........................................................................................238
        3.4.44.2 CPERROR24 (New CM7.0)................................................................238
  3.5 Miscellaneous.......................................................................................................239
     3.5.1 NOP.............................................................................................................239
4. Message Index...........................................................................................................240


 Issue 1.0                                            Avaya, Inc. – Proprietary                                        Page 15 of
                                                                253
                                            Use pursuant to Company Instructions
```

<a id="pdf-page-016"></a>

## PDF page 16

Source: SPI-SYN24; PDF page 16; extracted characters: 754.

```text
   4.1 Alphabetical List....................................................................................................240
5. Virtual trunk mapping.................................................................................................250
 REFERENCES.............................................................................................................252


































































  Issue 1.0                                                   Avaya, Inc. – Proprietary                                                 Page 16 of
                                                                         253
                                                   Use pursuant to Company Instructions
```

<a id="pdf-page-017"></a>

## PDF page 17

Source: SPI-SYN24; PDF page 17; extracted characters: 937.

```text
                                             LIST OF FIGURES

Figure 1 Data Communication Protocol Layers...............................................................19


                                              LIST OF TABLES

Table 1 Reporting Adjunct to Switch Messages – Alphabetical List.............................240
Table 2 Switch to Reporting Adjunct Messages – Alphabetical List.............................241
Table 3 Reporting Adjunct to Switch Messages – Opcode List....................................245
Table 4 Switch to Reporting Adjunct Messages – Opcode List....................................246






















































 Issue 1.0                                       Avaya, Inc. – Proprietary                                  Page 17 of
                                                          253
                                         Use pursuant to Company Instructions
```

<a id="pdf-page-018"></a>

## PDF page 18

Source: SPI-SYN24; PDF page 18; extracted characters: 3396.

```text
Subject:Call Center Protocol Specification                                          Date:   May 19, 2015
        for Switch / Reporting Adjunct Interface -
        Overview and Syntax of SPI Messages                                         From:   Raechel Greschler
        Issue: 0.7                                                                          DR 2Y229
        COMPAS ID: 160965                                                                   +1.303.538.5607
                                                                                            greschler@avaya.com
                                                                                            Issue 1.0

                                                     REQUIREMENTS


1.        Introduction
This document contains the protocol specification for the switch interface to Call Center reporting
adjuncts. Reporting adjuncts are management information systems that reside on an adjunct processor.
They track ACD activity and collect data provided by the switch, and use this data to generate various
real-time and historical reports that allow the customer to monitor and manage their call centers. The data
collected includes information about agents, splits, trunks, trunk groups, VDNs, and vectors. Reporting
adjuncts also have some limited switch administration capabilities.

First an overview of communication protocols is presented. This is followed by the message syntax; these
define the Application protocol that is used in the switch communications with reporting adjuncts. The
syntax defines the message layouts used in the protocol. The semantics document1 (call trees) provides
protocol rules and example call trees, the message sequences for the call trees, and how the reporting
adjuncts interpret each message sequence including what data items get updated. The syntax section
and semantics document are separated into subsections on Translations Pumpup, Switch Administration,
and Call Processing. The database tables document2 lists all of the database tables and defines each of
the items in the tables.

1.1       Purpose
This paper was written to document and baseline the switch/reporting adjunct interface protocol. It will be
used as the requirements and design specification for the Switch Protocol Interpreter (SPI). It is also
intended to serve as an interface specification and reference for switch development.

It is hoped that this will also prove useful as a reference for System Test in verifying the switch-reporting
adjunct protocol, Field Support and Services in isolating link and data collection problems, Technical
Writers in providing training and customer documentation, and Product Management and Product
Marketing in answering questions about the how reporting adjuncts interpret call data and what
information gets recorded.

1.2       Overview
This section provides an overview of the functions of a data communications protocol. Included is some
background and definitions that will be helpful in understanding the protocol specified in this document.
       1.2.1        OSI Reference Model
The Open Systems Interconnection (OSI) Reference Model separates the data communication functions
into seven layers (or levels) as shown in Figure 1. The OSI Model is included to compare what is provided
by the TCP/IP protocol to what is needed for process communications.
```

<a id="pdf-page-019"></a>

## PDF page 19

Source: SPI-SYN24; PDF page 19; extracted characters: 3335.

```text
Each layer of the OSI Reference Model defines both the services that that layer provides to the upper
layers and the functions it must perform to provide these services. Each layer needs the services of the
layers beneath it to accomplish its task. The text, taken from 3 only provides an introductory description to
each layer.

     APPLICATION                                                             USER                             USER
    PRESENTATION                                                          DEFINED                          DEFINED
        SESSION                                                           SESSION                          SESSION
      TRANSPORT
       NETWORK                            PACKET                           PACKET                              TCP
       DATA LINK                                                                                                IP
        PHYSICAL                            LINK                             LINK                             LINK
       OSI MODEL                             X.25                            BX.25                           TCP/IP
                                    Figure 1 Data Communication Protocol Layers

1.2.1.1                    Physical Layer
The Physical Layer provides for the transmission of data bits between two data link entities. To do this it
must provide the mechanical, electrical, functional, and procedural mechanisms needed to activate,
maintain, and deactivate physical connections between Data Link entities.

1.2.1.2                    Data Link Layer
The Data Link Layer is responsible for providing error-free delivery of Network Layer data over the data
circuit provided by the Physical Layer. It can also provide sequential delivery of data and flow control to
prevent a fast transmitter from drowning a slow receiver.

1.2.1.3                    Network Layer
The Network Layer establishes, maintains, and terminates connections between communicating end
systems. It is responsible for providing a path between the end systems specified by the Transport Layer.

1.2.1.4                    Transport Layer
The Transport Layer provides all transport services to the Session Layer, either directly or through the
lower layers. The Transport Layer also provides end-to-end error detection and recovery, and flow control
on each transport connection so that users receiving data can temporarily stop the flow of data if they
cannot process it as fast as it is arriving.

1.2.1.5                    Session Layer
The Session Layer provides the means for cooperating Presentation entities to organize and synchronize
their dialogues and manage their data exchanges.

1.2.1.6                    Presentation Layer
It is the responsibility of the Presentation Layer to request that the Session Layer establish and later
terminate a session. The Presentation Layer deals with the internal attributes of the communicating
resources. It can on request modify the syntax of data without changing its meaning (e.g., change data
characters from ASCII to EBCDIC). The Presentation Layer can also provide other data transformation
services such as data compression.

1.2.1.7                    Application Layer
The Application Layer dictates how communicating users will manage their conversations.
```

<a id="pdf-page-020"></a>

## PDF page 20

Source: SPI-SYN24; PDF page 20; extracted characters: 3315.

```text
       1.2.2        X.25 Protocol
X.254 is a layered data communications protocol patterned after the OSI Reference Model but it only
covers the first three layers. If services at other layers are required, other protocols must be used in
addition to X.25 (e.g., BX.25).

The X.25 Physical Layer and Link Layer closely resemble their OSI peers with only a few exceptions, the
most notable being that X.25 only deals with single, full-duplex, point-to-point links.

The X.25 Packet Layer provides most of the services of the OSI Network Layer and a portion of the
Transport Layer services. The main OSI Network Layer functions not included in the X.25 Packet Layer
are routing and switching, since X.25 is a network interface specification and not an internal network
specification. The main OSI Transport Layer feature provided in the X.25 Packet Layer is the end-to-end
data acknowledgement.
       1.2.3        BX.25 Protocol
BX.255 goes beyond X.25 and defines five levels of protocol. The first three correspond to the Physical,
Link, and Packet Layers of X.25. Since only a few of the features from the OSI Presentation Layer are
incorporated in BX.25, they are included in the definition of the Session Layer rather than in a separate
layer.

At the highest level is the application, which must be defined by the user. The Application Protocol must
specify the syntax and semantics of the information that will flow across the connection.
       1.2.4        TCP/IP Protocol
The TCP/IP connection requires DEFINITY ECS 7.1 or later software and hardware including the C-LAN
card.  This connection is only available on the Sun SPARCservers and requires CentreVu CMS R3V6 or
later.  TCP/IP will be provided over both an Ethernet (for a LAN/WAN) and a PPP (for a modem)
connection.

The TCP/IP connection will be transparent to the R3V6 or later CMS application except for link
administration.  The differences between the TCP/IP connection and the X.25 connection will be at the
session layer and below.

One 10BaseT Ethernet connection will support the message traffic equivalent to a fully loaded 19.2 Kbps
X.25 connection.  The TCP/IP over Ethernet connection and the TCP/IP over PPP connection will
continue to support the advertised 40,000 Call Center busy hour calls per CMS.
       1.2.5        Reporting Adjunct Protocol
The reporting adjunct will use the AT&T X.25 Network Interface [Error: Reference source not found]
software to provide the services of the Physical, Link, and Packet levels of the BX.25 protocol. The
reporting adjunct will package the X.25 p-command interface library supplied with this software into a
Transport Connection library which will provide for the transparent transfer of data between the
communicating Session Layers. It relieves the Session Layer of any concern about the way in which the
data transfer is achieved, including the case where the reporting adjunct is communicating with a switch
simulator that may reside on the same or a different computer as the reporting adjunct.
CMS also supports a TCP/IP connection to the switch.

The CMS Session Layer will comply with the standard BX.25 Session Layer protocol [Error: Reference
source not found].

This document specifies the syntax and semantics of the user-defined Application Protocol for the CMS
application.
```
