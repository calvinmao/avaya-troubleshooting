---
title: "SPI-DTP6 - complete source pages 1-14"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-DTP6: PDF pages 1-14

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-enhancements-cm6-2010.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-001"></a>

## PDF page 1

Source: SPI-DTP6; PDF page 1; extracted characters: 5427.

```text
           subject: Avaya Communication Manager 6.0                                                                                    date:                                  April 10, 2010
           Call Center DTP
           SPI Protocol Enhancements                                                                                                   from:                     Raechel Greschler
           Element IDs: 10577 10578 10579 10582                                                                                                     D2-H26
           Issue: 1.1                                                                                                                               303-538-5607
           COMPAS ID: 139877                                                                                                                        greschler@avaya.com

                                                                                                                                                    Gene Uba
                                                                                                                                                    D2-H43
                                                                                                                                                    303-538-2694
                                                                                                                                                    gmuba@avaya.com


                                                                                   DEVELOPMENT TEST PLAN


  1.                                      Introduction
  This Development Test Plan describes the procedures for    testing SPI Protocol Enhancements provided in the Avaya
  Communication Manager (CM) 6.0 Call Center release.

  The following guidelines were used in formulating test cases included in this plan:
                    Admin.  DEFINITY® Administration Feature DTP Test Case Guidelines, COMPAS ID: 12926    [2].
                    Call Proc.  DEFINITY® Call Processing Feature DTP Test Case Guidelines, COMPAS ID: 12929     [3].
  Unit test cases have not been included in section 9 of this test plan.  The following checklist was used in determining
  the need for and formulating unit test cases included in this plan.
                    DEFINITY Unit Test Case Checklist, COMPAS ID: 30472   [4].

  This test plan has been written in accordance with the DTP process defined in:
                    DTP Process Work Instruction, COMPAS ID: 12925     [1].

  The DTP process consists of writing and executing the test cases.  The execution of the test cases will be recorded
  using the DEET tool which can be accessed at http://info.dr.avaya.com/defty/deet
  1.1                                          Document Updates.
                                      Version Date                   Description
                                      0.1 2/10/2009 Initial Draft
                                      0.2                                                                                                                              4/9/2009                                                                                Draft of sections 9.1, 9.2 & 9.3
                                      0.3                                                                                                                              4/23/2009                                                                Review copy for sections 9.1, 9.2 & 9.3
                                      0.4                                                                                                                              5/11/2009                                                                Incorporate comments from review of sections 9.1, 9.2 & 9.3
                                      0.5                                                                                                                              5/15/2009                                                                Section 9.4 and 9.5 added
                                      0.6                                                                                                                              5/28/2009                                                                Updated after review
                                      1.0                                                                                                                              5/29/2009                                                                Final version for DEET
                                      1.1                                                                                                                              4/22/2010                                                                Update for MR 74500 (NOTE: MR 73525 is still open)
  2.                                      Document References
  2.1                                          Source Documents
The following documents are those that provide specific in  put to this document. Each source document has been
reviewed.

                                                                                       Avaya – PROPRIETARY
                                                                           Use pursuant to Company Instruction
```

<a id="pdf-page-002"></a>

## PDF page 2

Source: SPI-DTP6; PDF page 2; extracted characters: 9074.

```text
 -2-


           •                                           Call Center 6.x Product Requirements Document (PRD), CID: 134439 (Section 2.7.5).
           •                                           Avaya Communication Manager Call Center 6.0 SRAD/RFS: MIS Link and SPI Protocol Enhancements,
                       Element IDs 10577, 10578, 10579, 10582, CID: 138486.
           •                                           Avaya Communication Manager 6.0 Call Center ISD: SPI Protocol Enhancements, Element IDs 10577,
                       10578, 10579, 10582, CID: 139876.
This set of features is defined by the following element IDs:
                       10577                                 Enhance SPI link messages in La  nguage 23 to support Interruptible Aux feature
                       10578                                 Enhance SPI link messages in La  nguage 23 to support Route Calls by Skill Level feature
                       10579                                 Enhanced reporting support for the Percent Allocation Routing feature
                       10582                                 Enhance SPI messages to support increased # of skills per agent

2.2                                          Related Documents
None.

3.                                     Scope
This test plan covers the CM requirements (10-180) from CID: 138486. The CMS/IQ requirements (CMS10-
CMS40) are not covered in this test plan.

4.                                      Terminology
                                                                  TERM DEFINITION
                                    Abstract Test #                                                                                                                                                                                                                                                                                                                                  This is the test case description that is recorded in the DEET tracking tool.  This
                                                                                                                           will typically be a unique and concise description of the test.  Only text, no
                                                                                                                           graphics or tables.
                                    DEET                                                                                                                                                                                                                                                                                                                                                                                                                                                   DTP Execution Entry Tool.  A website application that reads in a DTP or
                                                                                                                           MR_ASSESS, and tracks the state of each Test Case.  The website location is
                                                                                                                           http://info.dr.avaya.com/defty/deet   .  Submit the completed DTP to this on-line
                                                                                                                           tool to track test results/status
                                    Requirement Numbers                                                                                                                                                                                                                                    This can be numbers associated with the Requirement Feature Specifications
                                                                                                                           (RFS), or with the Modification Request (MR).
                                    S8100.                                                                                                                                                                                                                                                                                                                                                                                                                                          Previously known as Definity One or IP600.
                                    S8300                                                                                                                                                                                                                                                                                                                                                                                                                                                  Previously known as C-hawk
                                    S8700                                                                                                                                                                                                                                                                                                                                                                                                                                                  Previously known as Stingray or Seagull server
                                    Server                                                                                                                                                                                                                                                                                                                                                                                                                                                  Controller or Server of the switch or gateway.  For example, G3R, G3SI, G3CSI,
                                                                                                                           S8700,S8300, S8100, ANY or OTHER
                                    Test Case Type BIT                                                                                                                                                                                                                                                                       BIT stands for Base Integrity Test.  This test type is associated with software base
                                                                                                                           breakage avoidance.  These tests are not required under a DTP, but are required in
                                                                                                                           the MR_ASSESS when code is submitted to the base.
                                    Test Case Type Functional                                                                                                                                                                                 “Idiot” proofing test cases of the new feature ("What if..").
                                    Test Case Type Priority                                                                                                                                                                                                                 Basic functionality of the new feature.
                                    Test Case Type Unit                                                                                                                                                                                                                                                                Test cases whose results require special tools
5.                                      Lab System Configuration
Testing will require a CM 6.0 switch connected to either a CMS R16.1 or an IQ 5.1.
6.                                      Special Software/Firmware Needed
No special software or firmware is necessary.
7.                                      Administration Required
No special administration or  license files are required.
8.                                      Test Case Format
A test case is the instructions that will be executed to verify one or more requirements. Each test case must contain
enough information so the individuals reviewing and executing the plan can determine how to execute the test case
and verify the results. For more information on the DTP document, see the DTP process work instructions,
COMPAS ID 12925  [1].

                                                                                                              Avaya – PROPRIETARY
                                                                                              Use pursuant to Company Instruction
```

<a id="pdf-page-003"></a>

## PDF page 3

Source: SPI-DTP6; PDF page 3; extracted characters: 1308.

```text
 -3-


9.                                      Test Cases
All test cases involving SPI messages can be checked in multiple ways.
−                                       If CMS is getting administration from the switch, the information displayed by CMS can be checked.
−                                       If CMS is changing information on the switch, the new information on the switch can be checked.
−                                       The switch side of the link can be watched using the wlog after executing “test mo l 5126 p 0 t 226” on the SAT.
−                                       The CMS side of the link can be watched using spi.log.


If the tests are run prior to a CMS R16.1 or IQ 5.1 being available, execute the following commands from the SAT:
           go tcm
           rdd :mis_ap
           wr Cms_type 19
           quit
This will force the switch to use language 23. The messages sent from the switch to the CMS can be watched using
wlog. The CMS spi.log will not be accurate since it won’t be using language 23. The messages sent from the CMS to
the switch cannot be tested with this method.


































                                                   Avaya – PROPRIETARY
                                            Use pursuant to Company Instruction
```

<a id="pdf-page-004"></a>

## PDF page 4

Source: SPI-DTP6; PDF page 4; extracted characters: 2671.

```text
 -4-



9.1                                          SPI Protocol changes for language 23 [RG]
Server:   (any)
Test Case Type:  Priority
Requirement Numbers:   138486-10
                           Abstract Test 1:  System-parameters Feature-related Form, CMS
                    Action:  On the SAT, go to page 12 of “change system-parameters feature-related”. Go to the
                    “CMS (appl mis):” field. Press help.
                    Verify:  The help message includes R16.1.
                    Action:  Enter R16.1. Tab out of the field.
                    Verify:  The value is accepted.
                    Action:  Submit the form.
                    Verify:  The form submits successfully.
                    Action:  Bring the form back up. Go to page 12.
                    Verify:  The CMS field contains R16.1.
                           Abstract Test 2:  System-parameters Feature-related Form, IQ
                    Action:  On the SAT, go to page 12 of “change system-parameters feature-related”. Go to the “IQ
                    (appl ccr):” field. Press help.
                    Verify:  The help message includes 5.1.
                    Action:  Enter 5.1. Tab out of the field.
                    Verify:  The value is accepted.
                    Action:  Submit the form.
                    Verify:  The form submits successfully.
                    Action:  Bring the form back up. Go to page 12.
                    Verify:  The IQ field contains 5.1.
Test Case Type:  Functional
                           Abstract Test 3:  System-parameters Feature-related Form, CMS & IQ
                    Action:  On the SAT, go to page 12 of “change system-parameters feature-related”. Enter R16.1 in
                    CMS and 5.0 in IQ. Submit the form.
                    Verify:  The error message “Allowed CMS/IQ combinations: R16.1/5.1, R15/5.0, R14.1/4.0,
                    R14/4.0 & R13.1/4.0” is displayed.
                    Action:  On the SAT, go to page 12 of “change system-parameters feature-related”. Enter
                    R15/R16 in CMS and 5.1 in IQ. Submit the form.
                    Verify:  The error message “Allowed CMS/IQ combinations: R16.1/5.1, R15/5.0, R14.1/4.0,
                    R14/4.0 & R13.1/4.0” is displayed.
                    Action:  On the SAT, go to page 12 of “change system-parameters feature-related”. Enter R16.1 in
                    CMS and 5.1 in IQ. Submit the form.
                    Verify:  The form submits successfully.

                                               Avaya – PROPRIETARY
                                        Use pursuant to Company Instruction
```

<a id="pdf-page-005"></a>

## PDF page 5

Source: SPI-DTP6; PDF page 5; extracted characters: 1124.

```text
 -5-


Test Case Type:  Priority
Requirement Numbers:   138486-20
                        Abstract Test 4:  Release and Language in XSTAT20 (CMS)
                 Action:  On the SAT, set CMS release to R16.1 and IQ to blank. During pumpup, check the
                 XSTAT20 message.
                 Verify:  The release specified in the message is 2 (CM6.0).
                 Verify:  The language specified in the message is 0x17 (language 23).
                 Verify:  The dot specified in the message is 0.
                        Abstract Test 5:  Release and Language in XSTAT20 (IQ)
                 Action:  On the SAT, set CMS release to blank and IQ to 5.1. During pumpup, check the
                 XSTAT20 message.
                 Verify:  The release specified in the message is 2 (CM6.0).
                 Verify:  The language specified in the message is 0x17 (language 23).
                 Verify:  The dot specified in the message is 0.


































                                         Avaya – PROPRIETARY
                                   Use pursuant to Company Instruction
```

<a id="pdf-page-006"></a>

## PDF page 6

Source: SPI-DTP6; PDF page 6; extracted characters: 3513.

```text
 -6-



9.2                                          SPI Protocol changes for Interruptible Aux [RG]
9.2.1                                                    AVAIL & AUDAVAIL
Test Case Type:  Functional
Requirement Numbers:   138486-30
                             Abstract Test 6:  Agent goes available without notification, AVAIL23
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. With that agent logged in but not being notified, have the agent go available (either auto-in or
                     manual-in).
                     Verify:  An AVAIL23 message is sent with the Interruptible Aux field set to 0.
                             Abstract Test 7:  AUDAVAIL23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAVAIL23 message is sent with the Interruptible Aux field set to 0.
Test Case Type:  Priority
                             Abstract Test 8:  Agent forced auto-in, AVAIL23
                     Action:  On the switch, administer an agent with a skill that has interruptible aux, forced auto-in.
                     With that agent logged in and in AUX, have that skill go into an interrupt state. After the timer
                     expires, the agent is forced to auto-in.
                     Verify:  An AVAIL23 message is sent with the Interruptible Aux field set to 1.
                             Abstract Test 9:  AUDAVAIL23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAVAIL23 message is sent with the Interruptible Aux field set to 1.
Test Case Type:  Functional
                             Abstract Test 10:  Agent forced manual-in, AVAIL23
                     Action:  On the switch, administer an agent with a skill that has interruptible aux, forced manual-
                     in. With that agent logged in and in AUX, have that skill go into an interrupt state. After the timer
                     expires, the agent is forced to manual-in.
                     Verify:  An AVAIL23 message is sent with the Interruptible Aux field set to 2.
                             Abstract Test 11:  AUDAVAIL23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAVAIL23 message is sent with the Interruptible Aux field set to 2.
                             Abstract Test 12:  Agent goes available during notification, AVAIL23
                     Action:  On the switch, administer an agent with a skill that has interruptible aux with notification
                     (not forced to available). With that agent logged in and in AUX, have that skill go into an interrupt
                     state. While the agent is being notified, have the agent go available (either auto-in or manual-in).
                     Verify:  An AVAIL23 message is sent with the Interruptible Aux field set to 3.
                             Abstract Test 13:  AUDAVAIL23

                                                 Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-007"></a>

## PDF page 7

Source: SPI-DTP6; PDF page 7; extracted characters: 3533.

```text
 -7-


                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAVAIL23 message is sent with the Interruptible Aux field set to 3.
                             Abstract Test 14:  Agent goes available after notify/clear, AVAIL23
                     Action:  On the switch, administer an agent with a skill that has interruptible aux with notification
                     (not forced to available). With that agent logged in and in AUX, have that skill go into an interrupt
                     state. Then have the skill meet the service level target so the notification clears. Then have the
                     agent go available (either auto-in or manual-in).
                     Verify:  An AVAIL23 message is sent with the Interruptible Aux field set to 0.
                             Abstract Test 15:  AUDAVAIL23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAVAIL23 message is sent with the Interruptible Aux field set to 0.
9.2.2                                                    AUX & AUDAUX
Requirement Numbers:   138486-71
                             Abstract Test 16:  Agent goes into AUX, AUX23
                     Action:  On the switch, login an agent. Have the agent go into AUX with a non-interruptible
                     reason code.
                     Verify:  An AUX23 message is sent with the Interruptible Aux field set to 0.
                             Abstract Test 17:  AUDAUX23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAUX23message is sent with the Interruptible Aux field set to 0.
Test Case Type:  Priority
                             Abstract Test 18:  Agent goes into AUX, AUX23
                     Action:  On the switch, login an agent. Have the agent go into AUX with an interruptible reason
                     code.
                     Verify:  An AUX23 message is sent with the Interruptible Aux field set to 1.
                             Abstract Test 19:  AUDAUX23
                     Action:  After the previous test case, on the SAT, run “test MO logical 8192 physical 587 test-
                     number 0”. This will force an audit.
                     Verify:  An AUDAUX23message is sent with the Interruptible Aux field set to 1.
9.2.3                                                     AEVENT
NOTE: This message is sent by the switch when an agent begins (type=0, button=6) or ends (type=0, button=7)
Interruptible Aux notification.
Requirement Numbers:   138486-72 138486-73
                             Abstract Test 20:  (R16.1) skill enters interrupt, AEVENT
                     Action:  (R16.1) Have a skill with more than one agent administered for Interruptible Aux. With
                     the agents in Aux, have the skill go into an interrupt state. Each agent is notified.
                     Verify:  An AEVENT message is sent with type=0, button=6 is sent for each agent that was
                     notified.

                                                 Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-008"></a>

## PDF page 8

Source: SPI-DTP6; PDF page 8; extracted characters: 3943.

```text
 -8-


Test Case Type:  Functional
                            Abstract Test 21:  (R16.1) agent goes into AUX, skill in interrupt, AEVENT
                    Action:  (R16.1) Have a skill in an interrupt state. Have an agent with that skill as interruptible go
                    into AUX. The agent is notified.
                    Verify:  An AEVENT message is sent with type=0, button=6 is sent for the agent that was notified.
                            Abstract Test 22:  (R16.1) agent goes from pending AUX, skill in interrupt, AEVENT
                    Action:  (R16.1) Have a skill in an interrupt state. Have an agent with that skill as interruptible on
                    a call. The agent pushes AUX and goes into a pending AUX state. The agent ends the call and
                    immediately goes into AUX. The agent is notified.
                    Verify:  An AEVENT message is sent with type=0, button=6 is sent for the agent that was notified.
Test Case Type:  Priority
                            Abstract Test 23:  (R16.1) skill leaves interrupt, AEVENT
                    Action:  (R16.1) Have a skill with more than one agent administered for Interruptible Aux. With
                    the agents in Aux, have the skill go into an interrupt state. Each agent is notified. Have the skill
                    leave the interrupt state. Each agent stops being notified.
                    Verify:  An AEVENT message is sent with type=0, button=7 is sent for each agent that was
                    cleared.
Test Case Type:  Functional
                            Abstract Test 24:  (R16.1) agent changes to AVAIL, AEVENT
                    Action:  (R16.1) Have a skill with an agent administered for Interruptible Aux. With the agent in
                    Aux, have the skill go into an interrupt state. The agent is notified. Have the agent go into AVAIL
                    (either auto-in or manual-in). The agent stops being notified.
                    Verify:  No AEVENT message is sent with type=0, button=7 is sent for the agent.
                            Abstract Test 25:  (R16.1) agent changes to ACW, AEVENT
                    Action:  (R16.1) Have a skill with an agent administered for Interruptible Aux. With the agent in
                    Aux, have the skill go into an interrupt state. The agent is notified. Have the agent go into ACW.
                    The agent stops being notified.
                    Verify:  An AEVENT message is sent with type=0, button=7 is sent for the agent.
                    Verify:  The AEVENT message is sent before the ACW message.
                            Abstract Test 26:  (R16.1) agent changes to AUX, AEVENT
                    Action:  (R16.1) Have a skill with an agent administered for Interruptible Aux. With the agent in
                    Aux, have the skill go into an interrupt state. The agent is notified. Have the agent go into AUX
                    with a non-interruptible reason code. The agent stops being notified.
                    Verify:  An AEVENT message is sent with type=0, button=7 is sent for the agent.
                    Verify:  The AEVENT message is sent before the AUX message.
                            Abstract Test 27:  (R16.1) agent forced to available, AEVENT
                    Action:  (R16.1) Have a skill with more than one agent administered for Interruptible Aux (forced
                    to either auto-in or manual-in). With the agents in Aux, have the skill go into an interrupt state.
                    Each agent is notified. After the timer, each agent stops being notified and is forced to available.
                    Verify:  No AEVENT message is sent with type=0, button=7 is sent for each agent that was
                    cleared.

                                                Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-009"></a>

## PDF page 9

Source: SPI-DTP6; PDF page 9; extracted characters: 3949.

```text
 -9-


                            Abstract Test 28:  (R16.1) agent goes into AUX, forced avail, skill in interrupt, AEVENT
                     Action:  (R16.1) Have a skill in an interrupt state. Have an agent with that skill as interruptible
                     (auto-in or manual-in) go into AUX. The agent is notified. After the timer, the agent stops being
                     notified and is forced to available.
                     Verify:  No AEVENT message is sent with type=0, button=7 is sent for the agent.
                            Abstract Test 29:  (R15/R16) skill enters interrupt, no AEVENT
                     Action:  (R15/R16) Have a skill with more than one agent administered for Interruptible Aux.
                     With the agents in Aux, have the skill go into an interrupt state.
                     Verify:  No AEVENT message is sent.
                            Abstract Test 30:  (R15/R16) agent goes into AUX, skill in interrupt, no AEVENT
                     Action:  (R15/R16) Have a skill in an interrupt state. Have an agent with that skill as interruptible
                     go into AUX. The agent is notified.
                     Verify:  No AEVENT message is sent.
                            Abstract Test 31:  (R15/R16) agent goes from pending AUX, skill in interrupt, no
                                       AEVENT
                     Action:  (R15/R16) Have a skill in an interrupt state. Have an agent with that skill as interruptible
                     on a call. The agent pushes AUX and goes into a pending AUX state. The agent ends the call and
                     immediately goes into AUX. The agent is notified.
                     Verify:  No AEVENT message is sent.
                            Abstract Test 32:  (R15/R16) skill leaves interrupt, no AEVENT
                     Action:  (R15/R16) Have a skill with more than one agent administered for Interruptible Aux.
                     With the agents in Aux, have the skill go into an interrupt state. Each agent is notified. Have the
                     skill leave the interrupt state. Each agent stops being notified.
                     Verify:  No AEVENT message is sent.
                            Abstract Test 33:  (R15/R16) agent changes work mode, no AEVENT
                     Action:  (R15/R16) Have a skill with an agent administered for Interruptible Aux. With the agent
                     in Aux, have the skill go into an interrupt state. The agent is notified. Have the agent go into a
                     different work mode (AVAIL or ACW). The agent stops being notified.
                     Verify:  No AEVENT message is sent.
                            Abstract Test 34:  (R15/R16) agent forced to available, no AEVENT
                     Action:  (R15/R16) Have a skill with more than one agent administered for Interruptible Aux
                     (forced to either auto-in or manual-in). With the agents in Aux, have the skill go into an interrupt
                     state. Each agent is notified. After the timer, each agent stops being notified and is forced to
                     available.
                     Verify:  No AEVENT message is sent.
                     Verify:  An AVAIL message for each agent.
                            Abstract Test 35:  (R15/R16) agent goes into AUX, forced avail, skill in interrupt, no
                                       AEVENT
                     Action:  (R15/R16) Have a skill in an interrupt state. Have an agent with that skill as interruptible
                     (auto-in or manual-in) go into AUX. The agent is notified. After the timer, the agent stops being
                     notified and is forced to available.
                     Verify:  No AEVENT message is sent.

                                                Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-010"></a>

## PDF page 10

Source: SPI-DTP6; PDF page 10; extracted characters: 3107.

```text
 -10-


                     Verify:  An AVAIL message for the agent after the AEVENT message.


9.2.4                                                     AGENTSK
NOTE: This message is sent by the CMS/IQ when they want to see an agent’s skills (change agent skills, find one).
Requirement Numbers:   138486-40
                             Abstract Test 36:  (R15/R16) AGENTSK20
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, retrieve that agent from the switch.
                     Verify:  The agent is successfully retrieved using AGENTSK20 with the correct data.
                     Verify:  Using SPI logs, the message has the correct structure.
Test Case Type:  Priority
                             Abstract Test 37:  (R16.1) AGENTSK23
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R16.1 CMS, retrieve that agent from the switch.
                     Verify:  The agent is successfully retrieved with the correct data.
                     Verify:  Using SPI logs, the new message has the correct structure.

9.2.5                                                    ALOGON
NOTE: This message is sent by the switch when an agent logs in.
Requirement Numbers:   138486-50
                             Abstract Test 38:  ALOGON23
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. Log in the agent.
                     Verify:  A LOGON23 message is sent.
                     Verify:  Using SPI logs, the new message has the correct structure.


9.2.6                                                     SKILLADD
NOTE: This message is sent by the CMS/IQ when they want to change an agent’s skills (change agent skills,
modify).
Requirement Numbers:   138486-60
                             Abstract Test 39:  (R15/R16) SKILLADD8 – add skill
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, add a skill.
                     Verify:  The skill is successfully added with the correct data on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, add a reserve skill.
                     Verify:  The skill is successfully added with the correct data on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.

                                                  Avaya – PROPRIETARY
                                           Use pursuant to Company Instruction
```

<a id="pdf-page-011"></a>

## PDF page 11

Source: SPI-DTP6; PDF page 11; extracted characters: 3622.

```text
 -11-


                             Abstract Test 40:  (R15/R16) SKILLADD8 – remove skill
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, remove a non-reserve skill without interruptible aux.
                     Verify:  The skill is successfully removed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, remove a reserve skill.
                     Verify:  The skill is successfully removed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
Test Case Type:  Functional
                             Abstract Test 41:  (R15/R16) SKILLADD8 – change level
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, Change a skill level a non-reserve skill without interruptible aux.
                     Verify:  The skill level is successfully changed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change a reserve level on a reserve skill.
                     Verify:  The skill level is successfully changed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change a skill with a non-reserve level that uses interruptible aux to a reserve
                     skill.
                     Verify:  The skill level is not changed on the switch.
                     Verify:  The switch reports to CMS that the operation failed at the switch.
                             Abstract Test 42:  (R15/R16) SKILLADD8 – to/from reserve
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change a skill without interruptible aux from a non-reserve skill level to a
                     reserve level.
                     Verify:  The skill level is successfully changed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change a skill without interruptible aux from a reserve level on a non-reserve
                     skill level.
                     Verify:  The skill level is successfully changed on the switch.


                                                 Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-012"></a>

## PDF page 12

Source: SPI-DTP6; PDF page 12; extracted characters: 3645.

```text
 -12-


                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                             Abstract Test 43:  (R15/R16) SKILLADD8 – change skill number
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change the skill number of a non-reserve skill without interruptible aux.
                     Verify:  The skill number is successfully changed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change the skill number of a non-reserve skill with interruptible aux.
                     Verify:  The skill number is successfully changed on the switch. The interruptible aux value is
                     cleared out.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R15 CMS, change the skill number of a reserve skill.
                     Verify:  The skill number is successfully changed on the switch.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.
                             Abstract Test 44:  (R16.1) SKILLADD23
                     Action:  On the switch, administer an agent with multiple skills, some of which have interruptible
                     aux. On R16.1 CMS, change the interruptible aux value for a skill with interruptible aux.
                     Verify:  The agent is successfully changed on the switch with the correct data.
                     Verify:  The switch reports to CMS that the change was successful.
                     Verify:  Using SPI logs, the new message has the correct structure.

9.2.7                                                     MVAGSTFD
NOTE: This message is sent by the CMS/IQ when they want to change several agent’s skills (multi-agent skill
change, modify).
Requirement Numbers:   138486-70
                             Abstract Test 45:  MVAGSTFD21 – change skill number
                     Action:  On the switch, administer several agents with multiple skills and skill levels, some of
                     which have interruptible aux. On R15 CMS, change a skill they have in common to a different skill
                     number.
                     Verify:  The agents are successfully changed on the switch with the correct data. If there was an
                     interruptible aux value, it is cleared out.
                     Verify:  The switch reports to CMS that the changes were successful.
                     Verify:  Using SPI logs, the message has the correct structure.
                             Abstract Test 46:  MVAGSTFD21 – change skill level
                     Action:  On the switch, administer several agents with multiple skills and skill levels, some of

                                                 Avaya – PROPRIETARY
                                          Use pursuant to Company Instruction
```

<a id="pdf-page-013"></a>

## PDF page 13

Source: SPI-DTP6; PDF page 13; extracted characters: 1946.

```text
 -13-


                    which have interruptible aux. On R15 CMS, change a skill they have in common to a different skill
                    level.
                    Verify:  The agents are successfully changed on the switch with the correct data. If there was an
                    interruptible aux value, it is cleared out.
                    Verify:  The switch reports to CMS that the changes were successful.
                    Verify:  Using SPI logs, the message has the correct structure.
                    Action:  On the switch, administer several agents with multiple skills and skill levels, some of
                    which have interruptible aux. On R15 CMS, change a skill they have in common to a reserve skill
                    level.
                    Verify:  If there was not an interruptible aux value, the agents are successfully changed on the
                    switch with the correct data.
                    Verify:  If there was an interruptible aux value, the switch reports to CMS that the operation failed
                    at the switch for that agent.
                    Verify:  Using SPI logs, the message has the correct structure.
Test Case Type:  Priority
                           Abstract Test 47:  MVAGSTFD23
                    Action:  On the switch, administer several agents with multiple skills, some of which have
                    interruptible aux. On R16.1 CMS, change the interruptible aux value for a given skill number.
                    Verify:  The agents are successfully changed on the switch with the correct data.
                    Verify:  The switch reports to CMS that the changes were successful.
                    Verify:  Using SPI logs, the new message has the correct structure.



























                                              Avaya – PROPRIETARY
                                        Use pursuant to Company Instruction
```

<a id="pdf-page-014"></a>

## PDF page 14

Source: SPI-DTP6; PDF page 14; extracted characters: 3001.

```text
 -14-



9.3                                          SPI Protocol changes for Route Calls by Skill Level [RG]
9.3.1                                                    DCON
NOTE: This message is sent by the switch when the call is ringing at the agent.
Requirement Numbers:   138486-80
                            Abstract Test 48:  Skill level in DCON23
                    Action:  With EAS and a measured skill, have a call route to an agent via either a queue or check
                    vector step.
                    Verify:  A DCON23 message is sent with the skill level.
Test Case Type:  Functional
Requirement Numbers:   138486-90
                            Abstract Test 49:  Preference match in DCON23, “all-levels”
                    Action:  Have a call route to an agent via a “check…if available-agents…all-lvls” step.
                    Verify:  A DCON23 message is sent with the preference match set to 0.
                            Abstract Test 50:  Preference match in DCON23, “pref-level”, match
                    Action:  Have a call route to an agent via a “check…if available-agents… pref-level” step. The
                    agent matches the skill level.
                    Verify:  A DCON23 message is sent with the preference match set to 2.
                            Abstract Test 51:  Preference match in DCON23, “pref-level”, no match
                    Action:  Have a call route to an agent via a “check…if available-agents… pref-level” step. The
                    agent does not match the skill level
                    Verify:  A DCON23 message is sent with the preference match set to 1.
Test Case Type:  Priority
                            Abstract Test 52:  Preference match in DCON23, “pref-range”, match
                    Action:  Have a call route to an agent via a “check…if available-agents… pref-range” step. The
                    agent matches the skill range.
                    Verify:  A DCON23 message is sent with the preference match set to 2.
Test Case Type:  Functional
                            Abstract Test 53:  Preference match in DCON23, “pref-range”, no match
                    Action:  Have a call route to an agent via a “check…if available-agents… pref-range” step. The
                    agent does not match the skill range.
                    Verify:  A DCON23 message is sent with the preference match set to 1.
                            Abstract Test 54:  Preference match in DCON23, queue-to
                    Action:  Have a call route to an agent via a “queue-to” step.
                    Verify:  A DCON23 message is sent with the preference match set to 0.
Requirement Numbers:   138486-100
                            Abstract Test 55:  non-ACD: Agent surplus flag in DCON23
                    Action:  Have a non-ACD call go to a measured station.

                                                Avaya – PROPRIETARY
                                         Use pursuant to Company Instruction
```
