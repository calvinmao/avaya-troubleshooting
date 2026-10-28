---
title: "SPI-DTP6 - complete source pages 15-28"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-DTP6: PDF pages 15-28

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-enhancements-cm6-2010.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-015"></a>

## PDF page 15

Source: SPI-DTP6; PDF page 15; extracted characters: 3224.

```text
 -15-


                     Verify:  A DCON23 message is sent with the agent surplus flag set to 0.
                             Abstract Test 56:  ACD: Agent surplus flag “call surplus” in DCON23
                     Action:  Have a call route to an agent after queuing. The agent answers the call.
                     Verify:  A DCON23 message is sent with the agent surplus flag set to 1.
                             Abstract Test 57:  ACD: Agent surplus flag “agent surplus” in DCON23
                     Action:  Have a call route to an agent without queuing. The agent answers the call.
                     Verify:  A DCON23 message is sent with the agent surplus flag set to 2.


9.3.2                                                     VECTOR
NOTE: This message is sent by the switch when the CMS/IQ requests it with a VPARMS to the switch. (Vector
administration, find one)
Requirement Numbers:   138486-110
                             Abstract Test 58:  VECTOR23 check step: all levels
                     Action: On the switch, administer a vector with “check…all-levels”. On R16.1 CMS, retrieve that
                     vector from the switch.
                     Verify:  The vector is successfully retrieved with the correct data.
                     Verify:  Using SPI logs, the new message has the correct structure.
                             Abstract Test 59:  VECTOR23 check step: single level
                     Action:  On the switch, administer a vector with “check…pref-level #”. On R16.1  CMS, retrieve
                     that vector from the switch.
                     Verify:  The vector is successfully retrieved with the correct data.
                     Verify:  Using SPI logs, the new message has the correct structure.
Test Case Type:  Priority
                             Abstract Test 60:  VECTOR23 check step:  range
                     Action:  On the switch, administer a vector with “check…pref-range # to #”. On R16.1  CMS,
                     retrieve that vector from the switch.
                     Verify:  The vector is successfully retrieved with the correct data.
                     Verify:  Using SPI logs, the new message has the correct structure.


9.3.3                                                     CHGVEC
NOTE: This message is sent by the CMS/IQ to change the vector administration. (Vector administration, modify)
Test Case Type:  Functional
Requirement Numbers:   138486-110
                             Abstract Test 61:  CHGVEC23 check step: all-levels w/ < Call Center Release 5.0
                     Action: On R16.1 CMS, add a vector step of “check…all-levels”. Send that change to the switch.
                     Verify:  The vector is successfully changed on the switch with the correct data.
                     Verify:  The switch reports to CMS that the changes were successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                             Abstract Test 62:  CHGVEC23 check step: pref-level w/ < Call Center Release 5.0

                                                 Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-016"></a>

## PDF page 16

Source: SPI-DTP6; PDF page 16; extracted characters: 3197.

```text
 -16-


                    Action: On R16.1 CMS, add a vector step of “check…pref-level #”. Send that change to the
                    switch.
                    Verify:  The vector is not changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the operation failed at the switch.
                            Abstract Test 63:  CHGVEC23 check step: pref-range w/ < Call Center Release 5.0
                    Action: On R16.1 CMS, add a vector step of “check…pref-range # to #”. Send that change to the
                    switch.
                    Verify:  The vector is not changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the operation failed at the switch.
                            Abstract Test 64:  CHGVEC23 check step: all levels
                    Action: On R16.1 CMS, add a vector step of “check…all-levels”. Send that change to the switch.
                    Verify:  The vector is successfully changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the changes were successful.
                    Verify:  Using SPI logs, the new message has the correct structure.
                            Abstract Test 65:  CHGVEC23 check step: single level
                    Action: On R16.1 CMS, add a vector step of “check…pref-level #”. Send that change to the
                    switch.
                    Verify:  The vector is successfully changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the changes were successful.
                    Verify:  Using SPI logs, the new message has the correct structure.
Test Case Type:  Priority
                            Abstract Test 66:  CHGVEC23 check step:  range
                    Action: On R16.1 CMS, add a vector step of “check…pref-range # to #”. Send that change to the
                    switch.
                    Verify:  The vector is successfully changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the changes were successful.
                    Verify:  Using SPI logs, the new message has the correct structure.
9.3.4                                                     VPARMS
NOTE: This message is sent by the CMS/IQ to request a vector. (Vector administration, find one)
Test Case Type:  Functional
Requirement Numbers:   138486-120
                            Abstract Test 67:  VECTOR20 check step: all levels
                    Action: On the switch, administer a vector with “check…all-levels”. On R15 CMS, retrieve that
                    vector from the switch.
                    Verify:  The vector is successfully retrieved with the correct data.
                            Abstract Test 68:  VECTOR20 check step: single level
                    Action:  On the switch, administer a vector with “check…pref-level #”. On R15 CMS, retrieve that
                    vector from the switch.


                                                Avaya – PROPRIETARY
                                         Use pursuant to Company Instruction
```

<a id="pdf-page-017"></a>

## PDF page 17

Source: SPI-DTP6; PDF page 17; extracted characters: 2028.

```text
 -17-


                    Verify:  The request is denied with rcode 43 (unsupported step type for this CMS release).
                           Abstract Test 69:  VECTOR20 check step:  range
                    Action:  On the switch, administer a vector with “check…pref-range # to #”. On R15 CMS,
                    retrieve that vector from the switch.
                    Verify:  The request is denied with rcode 43 (unsupported step type for this CMS release).
9.3.5                                                     CHVEC20
NOTE: This message is sent by the CMS/IQ to change the vector administration. (Vector administration, modify)
Requirement Numbers:   138486-130
                           Abstract Test 70:  CHGVEC20 check step: all levels
                    Action: On the switch, administer a vector with “check…all-levels”. On R15 CMS, change the
                    check step. Send that change to the switch.
                    Verify:  The vector is successfully changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the changes were successful.
                           Abstract Test 71:  CHGVEC20 check step: single level
                    Action:  On the switch, administer a vector with “check…pref-level #”. On R15 CMS, change the
                    check step. Send that change to the switch.
                    Verify:  The request is denied with rcode 43 (unsupported step type for this CMS release).
                           Abstract Test 72:  CHGVEC20 check step:  range
                    Action:  On the switch, administer a vector with “check…pref-range # to #”. On R15 CMS,
                    change the check step. Send that change to the switch.
                    Verify:  The request is denied with rcode 43 (unsupported step type for this CMS release).


























                                               Avaya – PROPRIETARY
                                        Use pursuant to Company Instruction
```

<a id="pdf-page-018"></a>

## PDF page 18

Source: SPI-DTP6; PDF page 18; extracted characters: 2635.

```text
 -18-



9.4                                          SPI Protocol changes for increased # of skills per agent [GMU]

When testing for messages, make sure as many odd combinations of skills are administered for the agent.
Refer to MR defsw091448.

REF: [j.wallerius] I assume this version of CMS does not support CM6.0, specifically increase of agent skills from
60 to 120. If it does then it might be nice to sp    read the agent's skill across the skill position range.


9.4.1                                                     AGENTSK
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-140
                            Abstract Test 73:  Expand the AGENTSK message into a series message format with up to
                                      two messages in the series
                    Action: CMS generates an APARMS7 via a “find one” command for agent skills to CM so the
                    PBX can respond with a AGENTSK23
                    Verify:  AGENTSK23 message has correct format for various agent skills
                    Action: execute test for various combinations of Call Center Releases and CMS settings.
                    Verify: only R16.1 CMS settings will provide AGENTSK23, all other AGENTSKxx will continue
                    to have the correct format and be processed correctly by CMS
Test Case Type: Functional
                            Abstract Test 74: CCREL 6.0, R15CMS, 120 skills adm on agent
                    Verify: that only the first 60 skills show up in the AGENTSKxx message
                            Abstract Test 75: CCREL 6.0, R15 CMS, 60 skills adm on 2nd page of agent form
                    Verify: that the 60 skills from the second page of agent form show up in the AGENTSKxx
                    message
9.4.2                                                     SKILLADD
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-150
                            Abstract Test 76:  Expand the SKILLADD message  into a series message format with up
                                      to two messages in the series
                    Action: Use a CMS to change skills for an agent (“modify”)
                    Verify:  verify skills change correctly for various settings and values.
Test Case Type:Functional
                            Abstract Test 77: CCREL 6.0, R15 CMS, 120 skills adm on agent form
                    Verify: skills change as expected, document the behavior



                                                Avaya – PROPRIETARY
                                         Use pursuant to Company Instruction
```

<a id="pdf-page-019"></a>

## PDF page 19

Source: SPI-DTP6; PDF page 19; extracted characters: 2334.

```text
 -19-


9.4.3                                                    ALOGON
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-160
                           Abstract Test 78:  Expand the ALOGON message into  a series message format with up to
                                     two messages in the series
                    Action:  login an agent with various skill settings
                    Verify:  verify skill messages in ALOGON is correct
Test Case Type:Functional
                           Abstract Test 79: CCREL 6.0, R15 CMS, 120 skills adm on agent form
                    Verify: ALOGON message shows only the first 60 of the 120 skills.
                    Action: log in an agent with 60 skills on page 2 of the agent form
                    Verify ALOGON message
                    Action: log in an agent with 30 skills on page 1 and 30 skills on page 2
                    Verify ALOGON message
9.4.4                                                    AVAIL, AUDAVAIL, AUDACW, AUDAUX
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-170
                           Abstract Test 80:  Double the skill bit maps in the  AVAIL, AUDAVAIL, AUDACD and
                                     AUDACW messages
                    Action:  Change agent state to AUTO-IN or MANUAL-IN
                    Verify:  verify AVAIL message has correct skill bit mapping
                    Action: wait for an audit
                    Verify: the AUDAVAIL message for the correct skill bit mapping
                    Action: change agent to ACW, wait for audit
                    Verify: the AUDACW message for the correct skill bit mapping
                    Action: change agent to AUX, wait for audit
                    Verify: the AUDAUX message for the correct skill bit mapping
                    Action: repeat for various settings of skills, CMS Releases and Call Center Releases.
                    Verify: correct skill bit mappings
Test Case Type: Functional
                           Abstract Test 81:Try various skill settings measured and unmeasured and repeat the above
                                     test case.





                                              Avaya – PROPRIETARY
                                        Use pursuant to Company Instruction
```

<a id="pdf-page-020"></a>

## PDF page 20

Source: SPI-DTP6; PDF page 20; extracted characters: 2669.

```text
 -20-



9.5                                          SPI Protocol changes for Percent Allocation Routing [GMU]
Refer to MR defsw090160

9.5.1                                                     DFWD
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-180
                                   Abstract Test 82:  Add information about a call being  redirected by a VDN with a PRT
                                                table to the DFWD SPI message
                          Action:  Make a call to a measured VDN with PRT
                          Verify:  DFWD SPI message matches requirements
Test Case Type: Functional
                                   Abstract Test 83:Try other call type scenarios with different aspects of the call measured
                                                or not.
                          •                                           Originate on
                                                                           measured/unmeasured Trunk
                                                                           measured agent, unmeasured station
                          •                                           Call a VDN with PRT that is measured/unmeasured
                                                                           Consider enabling/disabling VDN Override
                                                                           Note the DFWD to the VDN with PRT will have vec_num=0
                          •                                           Routing point has a
                                                                           measured/unmeasured VDN/vector
                                             •                                           again consider VDN Override settings
                                                                           measured/unmeasured VDN/PRT
                                             •                                           again consider VDN Override settings
                                                           Verify the DFWD at this point will have PRT number, and VDN routing internal line
                                       number, and the Routing point Target Percentage set.
                                   Abstract Test 84: Consider testing with covering to a VDN with PRT
                                   Abstract Test 85: Test toggling all fields in the DFWD message [e.smelko]












                                                            Avaya – PROPRIETARY
                                                    Use pursuant to Company Instruction
```

<a id="pdf-page-021"></a>

## PDF page 21

Source: SPI-DTP6; PDF page 21; extracted characters: 171.

```text
 -21-



10.              Notes




















































                 Avaya – PROPRIETARY
               Use pursuant to Company Instruction
```

<a id="pdf-page-022"></a>

## PDF page 22

Source: SPI-DTP6; PDF page 22; extracted characters: 651.

```text
 -22-

                                                References
1.                               MultiVantage™ DTP Process Work Instruction , COMPAS ID:  12925

2.                               DEFINITY® Administration Feature DTP Test Case Guidelines, COMPAS ID: 12926.

3.                               DEFINITY® Call Processing Feature DTP Test Case Guidelines, COMPAS ID: 12929.

4.                               DEFINITY® Unit Test Case Checklist, COMPAS ID: 30472.













































                                          Avaya – PROPRIETARY
                                    Use pursuant to Company Instruction
```

<a id="pdf-page-023"></a>

## PDF page 23

Source: SPI-DTP6; PDF page 23; extracted characters: 6431.

```text
 -23-

                                                TABLE OF CONTENTS


DEVELOPMENT TEST PLAN ....................................................................................................... 1
1. Introduction ............................................................................................................................. 1
Admin.  DEFINITY® Administration Feature DTP Test Case Guidelines, COMPAS ID:
12926[2]. .......................................................................................................................................... 1
Call Proc.  DEFINITY® Call Processing Feature DTP Test Case Guidelines, COMPAS ID:
12929[3]. .......................................................................................................................................... 1
    1.1 Document Updates. ......................................................................................................... 1
2. Document References ............................................................................................................. 1
    2.1 Source Documents .......................................................................................................... 1
    2.2 Related Documents ......................................................................................................... 2
3. Scope ....................................................................................................................................... 2
4. Terminology ............................................................................................................................ 2
5.                                                 Lab System Configuration ...................................................................................................... 2
6. Special Software/Firmware Needed ........................................................................................                                                                                                                  2
7. Administration Required ......................................................................................................... 2
8.                                                 Test Case Format .................................................................................................................... 2
9. Test Cases ............................................................................................................................... 3
    9.1                                                                         SPI Protocol changes for language 23 [RG] ................................................................... 4
    9.2                                                                         SPI Protocol changes for Interruptible Aux [RG] ........................................................... 6
        9.2.1                                                                                     AVAIL & AUDAVAIL .......................................................................................... 6
        9.2.2                                                                                     AUX & AUDAUX.................................................................................................. 7
        9.2.3 AEVENT ................................................................................................................. 7
        9.2.4 AGENTSK ............................................................................................................ 10
        9.2.5 ALOGON .............................................................................................................. 10
        9.2.6 SKILLADD ........................................................................................................... 10
        9.2.7 MVAGSTFD ......................................................................................................... 12
    9.3                                                                         SPI Protocol changes for Route Calls by Skill Level [RG] .......................................... 14
        9.3.1 DCON ................................................................................................................... 14
        9.3.2 VECTOR............................................................................................................... 15
        9.3.3 CHGVEC .............................................................................................................. 15
        9.3.4 VPARMS .............................................................................................................. 16
        9.3.5 CHVEC20 ............................................................................................................. 17
    9.4                                                                         SPI Protocol changes for increased # of skills per agent [GMU] ................................. 18
        9.4.1 AGENTSK ............................................................................................................ 18
        9.4.2 SKILLADD ........................................................................................................... 18
        9.4.3 ALOGON .............................................................................................................. 19
        9.4.4 AVAIL, AUDAVAIL, AUDACW, AUDAUX .................................................... 19
    9.5                                                                         SPI Protocol changes for Percent Allocation Routing [GMU] ..................................... 20
        9.5.1 DFWD ................................................................................................................... 20
10. Notes ................................................................................................................................. 21
TABLE OF CONTENTS  ........................................................................................................... 23
TABLE OF TEST CASES   .........................................................................................................   25

                                                           Avaya – PROPRIETARY
                                                   Use pursuant to Company Instruction
```

<a id="pdf-page-024"></a>

## PDF page 24

Source: SPI-DTP6; PDF page 24; extracted characters: 143.

```text
 -24-
























































              Avaya – PROPRIETARY
            Use pursuant to Company Instruction
```

<a id="pdf-page-025"></a>

## PDF page 25

Source: SPI-DTP6; PDF page 25; extracted characters: 5274.

```text
 -25-

                                         TABLE OF TEST CASES

Test Case Type: Priority ................................................................................................................ 4
   Requirement Numbers: 138486-10 .......................................................................................... 4
       Abstract Test 1: System-parameters Feature-related Form, CMS ........................................ 4
       Abstract Test 2: System-parameters Feature-related Form, IQ ............................................. 4
Test Case Type: Functional ........................................................................................................... 4
       Abstract Test 3: System-parameters Feature-related Form, CMS & IQ ............................... 4
Test Case Type: Priority ................................................................................................................ 5
   Requirement Numbers: 138486-20 .......................................................................................... 5
       Abstract Test 4: Release and Language in XSTAT20 (CMS) .............................................. 5
       Abstract Test 5: Release and Language in XSTAT20 (IQ) ................................................... 5
Test Case Type: Functional ........................................................................................................... 6
   Requirement Numbers: 138486-30 .......................................................................................... 6
       Abstract Test 6: Agent goes available without notification, AVAIL23 ................................ 6
       Abstract Test 7: AUDAVAIL23 ........................................................................................... 6
Test Case Type: Priority ................................................................................................................ 6
       Abstract Test 8: Agent forced auto-in, AVAIL23 ................................................................. 6
       Abstract Test 9: AUDAVAIL23 ........................................................................................... 6
Test Case Type: Functional ........................................................................................................... 6
       Abstract Test 10: Agent forced manual-in, AVAIL23 .......................................................... 6
       Abstract Test 11: AUDAVAIL23 ......................................................................................... 6
       Abstract Test 12: Agent goes available during notification, AVAIL23 ................................ 6
       Abstract Test 13: AUDAVAIL23 ......................................................................................... 6
       Abstract Test 14: Agent goes available after notify/clear, AVAIL23 ................................... 7
       Abstract Test 15: AUDAVAIL23 ......................................................................................... 7
   Requirement Numbers: 138486-71 .......................................................................................... 7
       Abstract Test 16: Agent goes into AUX, AUX23................................................................. 7
       Abstract Test 17: AUDAUX23 ............................................................................................. 7
Test Case Type: Priority ................................................................................................................ 7
       Abstract Test 18: Agent goes into AUX, AUX23................................................................. 7
       Abstract Test 19: AUDAUX23 ............................................................................................. 7
   Requirement Numbers: 138486-72 138486-73 ....................................................................... 7
       Abstract Test 20: (R16.1) skill enters interrupt, AEVENT ................................................... 7
Test Case Type: Functional ........................................................................................................... 8
       Abstract Test 21: (R16.1) agent goes into AUX, skill in interrupt, AEVENT ..................... 8
       Abstract Test 22: (R16.1) agent goes from pending AUX, skill in interrupt, AEVENT ...... 8
Test Case Type: Priority ................................................................................................................ 8
       Abstract Test 23: (R16.1) skill leaves interrupt, AEVENT .................................................. 8
Test Case Type: Functional ........................................................................................................... 8
       Abstract Test 24: (R16.1) agent changes to AVAIL, AEVENT ........................................... 8
       Abstract Test 25: (R16.1) agent changes to ACW, AEVENT .............................................. 8
       Abstract Test 26: (R16.1) agent changes to AUX, AEVENT ............................................... 8

                                                    Avaya – PROPRIETARY
                                            Use pursuant to Company Instruction
```

<a id="pdf-page-026"></a>

## PDF page 26

Source: SPI-DTP6; PDF page 26; extracted characters: 5492.

```text
 -26-


       Abstract Test 27: (R16.1) agent forced to available, AEVENT ........................................... 8
       Abstract Test 28: (R16.1) agent goes into AUX, forced avail, skill in interrupt, AEVENT        9
       Abstract Test 29: (R15/R16) skill enters interrupt, no AEVENT ......................................... 9
       Abstract Test 30: (R15/R16) agent goes into AUX, skill in interrupt, no AEVENT ........... 9
       Abstract Test 31: (R15/R16) agent goes from pending AUX, skill in interrupt, no
       AEVENT ................................................................................................................................. 9
       Abstract Test 32: (R15/R16) skill leaves interrupt, no AEVENT ........................................ 9
       Abstract Test 33: (R15/R16) agent changes work mode, no AEVENT ............................... 9
       Abstract Test 34: (R15/R16) agent forced to available, no AEVENT .................................. 9
       Abstract Test 35: (R15/R16) agent goes into AUX, forced avail, skill in interrupt, no
       AEVENT ................................................................................................................................. 9
   Requirement Numbers: 138486-40 ........................................................................................ 10
       Abstract Test 36: (R15/R16) AGENTSK20 ....................................................................... 10
Test Case Type: Priority .............................................................................................................. 10
       Abstract Test 37: (R16.1) AGENTSK23 ............................................................................ 10
   Requirement Numbers: 138486-50 ........................................................................................ 10
       Abstract Test 38: ALOGON23 ........................................................................................... 10
   Requirement Numbers: 138486-60 ........................................................................................ 10
       Abstract Test 39: (R15/R16) SKILLADD8 – add skill....................................................... 10
       Abstract Test 40: (R15/R16) SKILLADD8 – remove skill ................................................ 11
Test Case Type: Functional ......................................................................................................... 11
       Abstract Test 41: (R15/R16) SKILLADD8 – change level ................................................ 11
       Abstract Test 42: (R15/R16) SKILLADD8 – to/from reserve ............................................ 11
       Abstract Test 43: (R15/R16) SKILLADD8 – change skill number .................................... 12
       Abstract Test 44: (R16.1) SKILLADD23 ........................................................................... 12
   Requirement Numbers: 138486-70 ........................................................................................ 12
       Abstract Test 45: MVAGSTFD21 – change skill number .................................................. 12
       Abstract Test 46: MVAGSTFD21 – change skill level ...................................................... 12
Test Case Type: Priority .............................................................................................................. 13
       Abstract Test 47: MVAGSTFD23 ...................................................................................... 13
   Requirement Numbers: 138486-80 ........................................................................................ 14
       Abstract Test 48: Skill level in DCON23 ........................................................................... 14
Test Case Type: Functional ......................................................................................................... 14
   Requirement Numbers: 138486-90 ........................................................................................ 14
       Abstract Test 49: Preference match in DCON23, “all-levels” ............................................ 14
       Abstract Test 50: Preference match in DCON23, “pref-level”, match ............................... 14
       Abstract Test 51: Preference match in DCON23, “pref-level”, no match .......................... 14
Test Case Type: Priority .............................................................................................................. 14
       Abstract Test 52: Preference match in DCON23, “pref-range”, match .............................. 14
Test Case Type: Functional ......................................................................................................... 14
       Abstract Test 53: Preference match in DCON23, “pref-range”, no match ......................... 14
       Abstract Test 54: Preference match in DCON23, queue-to ................................................ 14
   Requirement Numbers: 138486-100 ...................................................................................... 14
       Abstract Test 55: non-ACD: Agent surplus flag in DCON23 ............................................ 14
       Abstract Test 56: ACD: Agent surplus flag “call surplus” in DCON23 ............................. 15
                                                  Avaya – PROPRIETARY
                                           Use pursuant to Company Instruction
```

<a id="pdf-page-027"></a>

## PDF page 27

Source: SPI-DTP6; PDF page 27; extracted characters: 5594.

```text
 -27-


       Abstract Test 57: ACD: Agent surplus flag “agent surplus” in DCON23 .......................... 15
   Requirement Numbers: 138486-110 ...................................................................................... 15
       Abstract Test 58: VECTOR23 check step: all levels .......................................................... 15
       Abstract Test 59: VECTOR23 check step: single level ...................................................... 15
Test Case Type: Priority .............................................................................................................. 15
       Abstract Test 60: VECTOR23 check step:  range .............................................................. 15
Test Case Type: Functional ......................................................................................................... 15
   Requirement Numbers: 138486-110 ...................................................................................... 15
       Abstract Test 61: CHGVEC23 check step: all-levels w/ < Call Center Release 5.0 .......... 15
       Abstract Test 62: CHGVEC23 check step: pref-level w/ < Call Center Release 5.0 ......... 15
       Abstract Test 63: CHGVEC23 check step: pref-range w/ < Call Center Release 5.0 ........ 16
       Abstract Test 64: CHGVEC23 check step: all levels ......................................................... 16
       Abstract Test 65: CHGVEC23 check step: single level ..................................................... 16
Test Case Type: Priority .............................................................................................................. 16
       Abstract Test 66: CHGVEC23 check step:  range .............................................................. 16
Test Case Type: Functional ......................................................................................................... 16
   Requirement Numbers: 138486-120 ...................................................................................... 16
       Abstract Test 67: VECTOR20 check step: all levels .......................................................... 16
       Abstract Test 68: VECTOR20 check step: single level ...................................................... 16
       Abstract Test 69: VECTOR20 check step:  range .............................................................. 17
   Requirement Numbers: 138486-130 ...................................................................................... 17
       Abstract Test 70: CHGVEC20 check step: all levels ......................................................... 17
       Abstract Test 71: CHGVEC20 check step: single level ..................................................... 17
       Abstract Test 72: CHGVEC20 check step:  range .............................................................. 17
Test Case Type: Priority .............................................................................................................. 18
   Requirement Numbers: 138486-140 ...................................................................................... 18
       Abstract Test 73: Expand the AGENTSK message into a series message format with up to
       two messages in the series .................................................................................................... 18
Test Case Type: Functional ......................................................................................................... 18
       Abstract Test 74: CCREL 6.0, R15CMS, 120 skills adm on agent .................................... 18
       Abstract Test 75: CCREL 6.0, R15 CMS, 60 skills adm on 2 nd page of agent form .......... 18
Test Case Type: Priority .............................................................................................................. 18
   Requirement Numbers: 138486-150 ...................................................................................... 18
       Abstract Test 76: Expand the SKILLADD message  into a series message format with up
       to two messages in the series ................................................................................................ 18
Test Case Type: Functional ......................................................................................................... 18
       Abstract Test 77: CCREL 6.0, R15 CMS, 120 skills adm on agent form .......................... 18
Test Case Type: Priority .............................................................................................................. 19
   Requirement Numbers: 138486-160 ...................................................................................... 19
       Abstract Test 78: Expand the ALOGON message into  a series message format with up to
       two messages in the series .................................................................................................... 19
Test Case Type: Functional ......................................................................................................... 19
       Abstract Test 79: CCREL 6.0, R15 CMS, 120 skills adm on agent form .......................... 19
Test Case Type: Priority .............................................................................................................. 19
   Requirement Numbers: 138486-170 ...................................................................................... 19
                                                   Avaya – PROPRIETARY
                                            Use pursuant to Company Instruction
```

<a id="pdf-page-028"></a>

## PDF page 28

Source: SPI-DTP6; PDF page 28; extracted characters: 1873.

```text
 -28-


      Abstract Test 80: Double the skill bit maps in the  AVAIL, AUDAVAIL, AUDACD and
      AUDACW messages ............................................................................................................ 19
Test Case Type: Functional ......................................................................................................... 19
      Abstract Test 81: Try various skill settings measured and unmeasured and repeat the above
      test case. ................................................................................................................................ 19
Test Case Type: Priority .............................................................................................................. 20
   Requirement Numbers: 138486-180 ...................................................................................... 20
      Abstract Test 82: Add information about a call being  redirected by a VDN with a PRT
      table to the DFWD SPI message ........................................................................................... 20
Test Case Type: Functional ......................................................................................................... 20
      Abstract Test 83: Try other call type scenarios with different aspects of the call measured
      or not. .................................................................................................................................... 20
      Abstract Test 84: Consider testing with covering to a VDN with PRT .............................. 20
      Abstract Test 85: Test toggling all fields in the DFWD message [e.smelko] ..................... 20






































                                                Avaya – PROPRIETARY
                                         Use pursuant to Company Instruction
```
