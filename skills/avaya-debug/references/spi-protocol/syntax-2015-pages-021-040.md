---
title: "SPI-SYN24 - complete source pages 21-40"
layer: L4
scope: "Verbatim page-text transcription of supplied source; original PDF preserves all graphical content."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# SPI-SYN24: PDF pages 21-40

[Library index](index.md) | [Coverage and source anomalies](coverage.md)

Original PDF: [complete source](../../assets/spi-protocol/spi-syntax-2015.pdf). These are documentary source excerpts; test and administration instructions are not authorization to execute them. Text is searchable but does not reproduce all bit-grid geometry, figures or fonts. Consult the original PDF for those details.

<a id="pdf-page-021"></a>

## PDF page 21

Source: SPI-SYN24; PDF page 21; extracted characters: 3863.

```text
Switches will send buffers of data according to the following table.

                                        Switch         CMS Buffer Size            Interval
                                      S75 R1V3                 n/a                   n/a
                                         G1.1                  200               1 second
                                          G3i                  244               1 second
                                          G3r              252 bytes             1 second
                                     CM6.2 SP4             252 bytes            0.1 seconds
                                        CM6.3

The switch also sends the packet if the buffer is full (which is the case with CHGVEC and VECTOR
messages).

The overhead on the link is 4 bytes for the session layer for each buffer, 3 bytes for the packet layer for
each 128 byte packet, and 5 bytes for the link layer for each 128 byte packet.

1.3       Terminology
This section provides definitions for some commonly used but often misunderstood terms.

ATM                Asynchronous Transfer Mode - Definity support of ATM falls into two areas.  The first is
                   Port Network Connectivity (PNC), primarily remote PNC over an ATM Wide Area Network
                   (WAN).  The second is a set of new ATM trunk circuit packs which can support 256
                   circuits each.
BSR                Best service routing.  Provides call vectoring functionality which builds upon Lookahead
                   Interflow to route a call to the "best" split or skill on a single switch or to the "best" split/skill
                   in a network of Definity switches.
CentreVu           The external product name for a set of features which were originally called Agent
Advocate           Allocation.
CentreVu           The external product name for a set of features which were originally called Best Service
Virtual            Routing (BSR).
Routing
iln                The switch assigns an internal line number to all extensions. The iln-VDN extension
                   association is reported to reporting adjuncts during the translation pumpup and then the
                   iln is used to identify VDN extensions in all subsequent transactions between CMS and
                   the switch. The iln is only used by reporting adjuncts to track VDNs (see itn for an
                   explanation of extension call tracking).
itn                The switch assigns an internal trunk number to all trunks (including software facilities used
                   to place station-to-station calls or used to transfer a call to another destination). The itn-
                   trunk association is reported to reporting adjuncts during the translation pumpup and then
                   the itn is used to identify trunks in all subsequent transactions between the reporting
                   adjuncts and the switch. When software facilities are used to process a call, the switch will
                   "create" an itn value and use it for notifying the reporting adjuncts of the events associated
                   with a call.
location-id        A number, 1-44 (G3V8-G3V11), 1-250 (MV2-CM6.2) and 1-2000 (CM6.3-, but not
                   supported until SPI language 24), that is assigned to one or more port networks on
                   Communication Manager. All hardware residing on a port network will be associated with
                   that port network's location-id (via the "change cabinet X" form).  Location-id is supported
                   by the optional 'Multiple Locations' feature.
loginID            Each EAS agent is given a login number called a loginID. This means that when the agent
                   logs into a physical extension, the properties such as assigned skills, class of restriction,
```

<a id="pdf-page-022"></a>

## PDF page 22

Source: SPI-SYN24; PDF page 22; extracted characters: 4602.

```text
                   coverage path, etc., are associated with the agent's loginID rather than with the physical
                   extension.
measured           See measured extension.
agent
measured           See measured extension.
agent
position
measured           The measured domain of a reporting adjunct is the collection of all measured splits,
domain             measured extensions, measured trunk groups, measured trunks, measured VDNs, and
                   measured vectors on the switch.
measured           A measured extension is one that is administered as measured on the switch. All
extension          extensions that are members of a measured split are automatically measured extensions.
                   The switch will give the reporting adjunct information about measured extensions during
                   the translation pumpup, and will then notify the reporting adjunct of any events and
                   translation changes associated with the measured extensions, and the reporting adjunct
                   will collect agent data for the agent that has staffed that extension.
measured           A measured split is one that is administered as measured on the switch. The switch tells
split              the reporting adjunct which splits are measured. The switch will give the reporting adjunct
                   information about measured splits during the translation pumpup, and will then notify the
                   reporting adjunct of any events and translation changes associated with the measured
                   splits, and the reporting adjunct will collect split data.
measured           A measured trunk is a trunk that is a member of a measured trunk group. The switch will
trunk              give the reporting adjunct information about measured trunks during the translation
                   pumpup, and will then notify the reporting adjunct of any events associated with measured
                   trunks, and the reporting adjunct will collect trunk and trunk group data.
measured           A measured trunk group is one that is administered as measured on the switch. The
trunk group        switch will give the reporting adjunct information about measured trunk groups during the
                   translation pumpup, and will then notify the reporting adjunct of any events and translation
                   changes associated with the measured trunk groups, and the reporting adjunct will collect
                   trunk group data.
measured           A measured VDN is one that is administered as measured on the switch. VDNs must be
VDN                administered as measured. The switch also sends messages for unmeasured VDNs. In
                   CM6, the SPI messages for unmeasured VDNs can be stopped by setting “Used for BSR
                   Polling?”. The switch will give the reporting adjunct information about measured VDNs
                   during the translation pumpup, and will then notify the reporting adjunct of any events and
                   translation changes associated with the measured VDNs, and the reporting adjunct will
                   collect VDN data.
measured           All vectors are automatically measured by the reporting adjunct. The switch will notify the
vector             reporting adjunct of all events associated with vectors.
modification       A modification number associated with a particular entity on the switch is used by the
number             reporting adjunct and its clients to identify whether cached data for the entity is valid.
                   Entities to which modification numbers apply include VDNs and vectors.  The modification
                   number for an entity is incremented when the administration for the entity is changed.
reason code        The code agents enter when changing to the AUX work state or logging out.  This code
                   indicates the reason for the state change.
skill              In an EAS environment, a skill can be defined as a specific customer need/requirement
                   that can be assigned to an agent.
terminal           The switch assigns a terminal number (also referred to as an agent position number) to
number             each measured extension in a non-EAS environment. The terminal number-extension
                   association is reported to the reporting adjunct during the translation pumpup, and then
                   the terminal number is used to identify extensions (agent positions) in all subsequent
                   transactions between the reporting adjunct and the switch.
```

<a id="pdf-page-023"></a>

## PDF page 23

Source: SPI-SYN24; PDF page 23; extracted characters: 3293.

```text
                   In an EAS environment the terminal number is the agent's login ID in packed decimal
                   format.
unmeasured         An unmeasured extension is one that is not administered as measured on the switch. The
extension          switch will notify the reporting adjunct of certain events associated with unmeasured
                   extensions, for example, if a measured trunk is forwarded to an unmeasured extension. In
                   this case, the trunk is in the measured domain so event notification is required, and the
                   reporting adjunct will collect trunk (and VDN/vector and split) data, but does not collect
                   agent data. The agent position number is reported to the reporting adjunct as terminal "0",
                   which the reporting adjunct interprets as an unmeasured extension.
unmeasured         An unmeasured split is one that is not administered as measured on the switch. The
split              switch will notify the reporting adjunct of certain events associated with unmeasured splits,
                   for example, if a measured trunk is queued to an unmeasured split. In this case, the trunk
                   is in the measured domain so event notification is required, and the reporting adjunct will
                   collect trunk (and VDN/vector) data but does not collect split data. The split number is
                   reported to the reporting adjunct as split "0", which the reporting adjunct interprets as an
                   unmeasured split.
unmeasured         An unmeasured trunk is one that is not a member of a measured trunk group. This
trunk              includes, for example, software facilities used to place station-to-station calls (see itn for
                   further details). The switch will notify the reporting adjunct of certain events associated
                   with unmeasured trunks, for example, if an unmeasured trunk is used to carry a measured
                   VDN call. In this case, the VDN (and vector) is in the measured domain so event
                   notification is required, and the reporting adjunct will collect VDN/vector (and split/agent)
                   data but does not collect trunk or trunk group data. The trunk number is reported to the
                   reporting adjunct as an itn, but the reporting adjunct will not recognize it as a measured
                   trunk from the translation pumpup so it interprets it as an unmeasured trunk, and tracks
                   the events on this trunk for the duration of the call so that is can collect the call data.
unmeasured         An unmeasured trunk group is one that is not administered as measured on the switch.
trunk group        The switch does not tell the reporting adjunct about these trunk groups (but may tell the
                   reporting adjunct about its members - see unmeasured trunk).
unmeasured         An unmeasured VDN is one that is not administered as measured on the switch. The
VDN                switch will notify the reporting adjunct of all events associated with unmeasured VDNs.
                   The VDN is reported to the reporting adjunct as iln "0", which the reporting adjunct
                   interprets as an unmeasured VDN.
```

<a id="pdf-page-024"></a>

## PDF page 24

Source: SPI-SYN24; PDF page 24; extracted characters: 4787.

```text
2.        PROTOCOL SPECIFICATION
This section defines the reporting adjunct Application Protocol. The reporting adjunct Application (a.k.a.
the reporting adjunct Session) is responsible for establishing communications between the reporting
adjunct and switch applications. The reporting adjunct Application can be in any of the following states (on
the reporting adjunct side of the communications path).

QUIESCENT               The reporting adjunct Application is idle.  Data Collection is turned off. The reporting
                        adjunct is waiting for the user to request that a reporting adjunct Application be
                        initiated.
WAITING                 The reporting adjunct Application is waiting for notification from the session layer that
SESSION                 the session has been established.  The reporting adjunct Application will be in this
ACCEPT (WSA)            state whenever the session layer does not have a session currently established.
REQUEST                 When the session layer has notified the reporting adjunct Application that the session
TRANSLATION             has been established, the reporting adjunct Application begins its connection by
CHANGE                  requesting translation change status.  The reporting adjunct Application enters this
STATUS                  state and remains here until a valid answer (XSTAT) has been received. The status of
(RTCS)                  translations and the state of the reporting adjunct  database determine the form of
                        pumpup used.  This state may also be entered when the user requests new
                        translations or when the Application timer AT3 expires.

                        When the RTCS state is entered, the Application timer AT1 is started (2 minutes).  If
                        the timer expires before the switch response is received, a new RTCS message is
                        sent and the timer is set again.
PUMPUP                  Once the answer to the request for translation change status has been received, the
                        application enters the pumpup state.  During this state the switch sends the requested
                        translations, depending on whether the request was for full translations (RFTB) or
                        logons (RLTB).  When the final message of the pumpup is received and processed
                        successfully, the reporting adjunct Application enters the DATA TRANSFER state. If
                        for some reason the pumpup fails (e.g., the reporting adjunct gets more data
                        than it expects), the reporting adjunct Application will return to the RTCS state. During
                        pumpup, the Application timer AT3 is set (2 minutes) and is reset (2 minutes) each
                        time a TIME message is received.  If the timer ever is allowed to expire, the pumpup is
                        aborted, the Application returns to the RTCS state, and a new reporting adjunct
                        Application connection will be established.
DATA                    The reporting adjunct Application is in data transfer state. The reporting adjunct
TRANSFER                database is up-to-date with the switch database and the reporting adjunct is actively
                        tracking the status of the ACD facilities and collecting real-time data. Switch
                        administration commands can now communicate with the switch application.

                        While the reporting adjunct Application is in DATA TRANSFER state, the reporting
                        adjunct will set the AT3 timer (2 minutes). The reporting adjunct will reset the AT3
                        timer whenever a TIME message is received (the switch will send a TIME message
                        every minute). If the timer expires (i.e., data transfer timed-out) the reporting adjunct
                        will initiate another reporting adjunct Application connection.
BUSIED-OUT              The reporting adjunct Application has been busied-out for administration purposes at
                        the switch. This is usually done by the switch administrator when making changes that
                        will affect the reporting adjunct database configuration. These changes typically result
                        in the "translation-change" flag being set at the switch so that when the reporting
                        adjunct initiates another reporting adjunct Application connection, full translations will
                        be requested and the reporting adjunct real-time database will be updated to reflect
                        the changes that were made at the switch.
```

<a id="pdf-page-025"></a>

## PDF page 25

Source: SPI-SYN24; PDF page 25; extracted characters: 461.

```text
While the reporting adjunct Application is BUSIED-OUT, the reporting adjunct will set
the AT2 timer (2 minutes).  When the timer expires, the reporting adjunct will initiate
another reporting adjunct Application connection to see if the session has been
released from busy-out at the switch. If the reporting adjunct Application is still busied-
out the timer will be reset.

The switch will busy-out the link if the Session layer queue in the switch overflows.
```

<a id="pdf-page-026"></a>

## PDF page 26

Source: SPI-SYN24; PDF page 26; extracted characters: 3726.

```text
3.      PROTOCOL SYNTAX

3.1     Compatibility
This section indicates the switch releases that support each of the messages. Each message layout is
also preceded with a compatibility table. Most message types (functions) have more than one version of
the message used for different switch releases.  Only one version is used in each release. Typically a
new version was created to accommodate larger capacities. The message layouts for a single message
type are grouped under a single third-level heading.

The table indicates which releases of the switch use each of the messages. In the syntax section that
follows the table, a left arrow "" indicates messages from the reporting adjunct and a right arrow ""
indicates messages from the switch.

Cross-reference tables in the appendix list the messages alphabetically and by opcode.

                Message             Op Code      Language 22      Language 23       Language 24
                                                     Pumpup
                RTCS21              x34          y                n                 n
                RTCS23              x37          n                y                 n
                RTCS24              x3D          n                n                 y
                XFAIL21             xf9          y                n                 n
                XFAIL23             x0d          n                y                 n
                XFAIL24             x29          n                n                 y
                XSTAT20             xb1          y                y                 n
                XSTAT24             x2c          n                n                 y
                RFTB                x06          y                y                 y
                RLTB                x0c          y                y                 y
                XOPEN20             xb2          y                y                 y
                XCLOSE20            xb3          y                y                 y
                XVDN20              xb4          y                n                 n
                XVDN23              x11          n                y                 n
                XVDN24              x2d          n                n                 y
                XSPLIT20            xb5          y                y                 n
                XSPLIT24            x2e          n                n                 y
                XAGENT20            xb6          y                y                 n
                XAGENT24            x2f          n                n                 y
                XTKGRP20            xb7          y                y                 n
                XTKGRP24            x30          n                n                 y
                XTGVDN20            xb8          y                y                 n
                XTGVDN24            x31          n                n                 y
                XTRUNK20            xb9          y                y                 n
                XTRUNK24            x25          n                n                 y
                                             Switch Administration
                BUSYOUT20           xba          y                y                 y
                RELBUSY20           xbb          y                y                 y
                ARVDN20             xbc          y                n                 n
                ARVDN23             x12          n                y                 n
                ARVDN24             x32          n                n                 y
                ARAGENT20           xbd          y                y                 n
```

<a id="pdf-page-027"></a>

## PDF page 27

Source: SPI-SYN24; PDF page 27; extracted characters: 2909.

```text
Message         Op Code    Language 22    Language 23   Language 24
ARAGENT24       x33        n              n             y
ARSPLIT20       xbe        y              n             n
ARSPLIT23       x13        n              y             n
ARSPLIT24       x34        n              n             y
ARTKGRP20       xbf        y              n             n
ARTKGRP23       x14        n              y             n
ARTKGRP24       x35        n              n             y
ARTGVDN20       xc0        y              y             n
ARTGVDN24       x36        n              n             y
ARTRUNK20       xc1        y              y             n
ARTRUNK24       x26        n              n             y
AGMOVE20        xf8        y              y             y
MVAGSTFD21      x35        y              n             n
MVAGSTFD23      x38        n              y             n
MVAGSTFD24      x3e        n              n             y
APARMS7         x28        y              y             n
APARMS24        x3f        n              n             y
AGENTSK20       xc2        y              n             n
AGENTSK23       x04        n              y             n
AGENTSK24       x37        n              n             y
SKILLADD8       x2d        y              n             n
SKILLADD23      x39        n              y             n
SKILLADD24      x40        n              n             y
TGMOVE20        xc3        y              n             n
TGMOVE23        x16        n              y             y
VTGMOVE20       xc4        y              y             y
VDNMOVE20       xc5        y              n             n
VDNMOVE23       x18        n              y             n
VDNMOVE24       x38        n              n             y
MVVDN9          x2f        y              n             n
MVVDN23         x3c        n              y             y
CHGVDNSK8       x2e        y              n             n
CHGVDNSK23      x3a        n              y             y
VPARMS          x15        y              y             y
VECTOR20        xc6        y              y             n
VECTOR24        x52        n              n             y
CHGVEC20        x33        y              y             n
CHGVEC24        x44        n              n             y
REQLIST5        x23        y              y             y
ADMLIST20       xc8        y              y             y
REQNAM20        x30        y              y             y
ADMNAM20        xc9        y              y             n
ADMNAM24        X2b        n              n             y
RCODENAM20      0x31       y              y             y
CHGNAM20        0x32       y              y             n
CHGNAM24        x41        n              n             y
MVRCODE20       xca        y              y             y
RCODE20         xcb        y              y             y
CRCODE20        xcc        y              y             y
```

<a id="pdf-page-028"></a>

## PDF page 28

Source: SPI-SYN24; PDF page 28; extracted characters: 2992.

```text
Message         Op Code     Language 22    Language 23    Language 24
USERID21        x36         y              y              y
                           Call Processing
TIME20          xcd         y              y              y
ALOGON20        xce         y              n              n
ALOGON23        x05         n              y              n
ALOGON24        x28         n              n              y
ALOGOFF20       xcf         y              y              n
ALOGOFF24       x39         n              n              y
AVAIL22         x01         y              n              n
AVAIL23         x0e         n              y              n
AVAIL24         x3a         n              n              y
ACD20           xd1         y              y              n
ACD24           x3b         n              n              y
ACW22           xff         y              y              n
ACW24           x3c         n              n              y
AUX22           x03         y              n              n
AUX23           x0f         n              y              n
AUX24           x3d         n              n              y
OTHER22         xfa         y              y              y
OTHER24         x3e         n              n              y
DIGITS20        xd5         y              y              n
DIGITS24        x3f         n              n              y
AEVENT20        xd6         y              y              n
AEVENT24        x40         n              n              y
IDLE20          xd7         y              n              n
IDLE23          x1b         n              y              n
IDLE24          x41         n              n              y
SETUP22         xfe         y              y              n
SETUP24         x42         n              n              y
QUEUED20        xd9         y              n              n
QUEUED23        x1c         n              y              n
QUEUED24        x43         n              n              y
DAQUEUED20      xda         y              n              n
DAQUEUED23      x1d         n              y              n
DAQUEUED24      x44         n              n              y
DCON22          xfd         y              n              n
DCON23          x0b         n              y              y
DCON24          x45         n              n              y
DABN22          xfc         y              y              n
DABN24          x46         n              n              y
DADFWD20        xdd         y              y              n
DADFWD24        x2a         n              n              y
DFWD20          xde         y              n              n
DFWD23          x0c         n              y              n
DFWD24          x47         n              n              y
MBUSY20         xdf         y              y              n
MBUSY24         x48         n              n              y
FBUSY20         xe0         y              y              n
FBUSY24         x49         n              n              y
```

<a id="pdf-page-029"></a>

## PDF page 29

Source: SPI-SYN24; PDF page 29; extracted characters: 2959.

```text
Message         Op Code    Language 22    Language 23    Language 24
VSTART20        xe1        y              y              n
VSTART24        x4a        n              n              y
VSTOP20         xe2        y              y              n
VSTOP24         x4b        n              n              y
FDISC20         xe3        y              y              n
FDISC24         x4c        n              n              y
HOLD20          xe4        y              y              n
HOLD24          x4d        n              n              y
RECON20         xe5        y              n              n
RECON23         x1e        n              y              n
RECON24         x4e        n              n              y
COMP20          xe6        y              y              n
COMP24          x4f        n              n              y
LOOKAH20        xe7        y              y              n
LOOKAH24        x50        n              n              y
AROUTE20        xe8        y              y              n
AROUTE24        x51        n              n              y
SKSTATE20       xe9        y              n              n
SKSTATE23       x1f        n              y              y
ASA20           xea        y              n              n
ASA23           x20        n              y              y
DNEVENT20       xeb        y              y              n
DNEVENT24       x53        n              n              y
MODEVENT20      xec        y              y              y
RAUDIT          x08        y              y              n
RAUDIT24        x42        n              n              y
TAUDIT20        xee        y              y              n
TAUDIT24        x54        n              n              y
AUDAVAIL22      x02        y              n              n
AUDAVAIL23      x08        n              y              n
AUDAVAIL24      x55        n              n              y
AUDACD20        xf0        y              n              n
AUDACD23        x06        n              y              n
AUDACD24        x56        n              n              y
AUDACW20        xf1        y              n              n
AUDACW23        x07        n              y              n
AUDACW24        x57        n              n              y
AUDAUX20        xf2        y              n              n
AUDAUX23        x10        n              y              n
AUDAUX24        x58        n              n              y
AUDOTHER22      xfb        y              y              n
AUDOTHER24      x59        n              n              y
AUDUNSTF20      xf4        y              y              n
AUDUNSTF24      x5a        n              n              y
EWTAUDIT20      xf5        y              n              n
EWTAUDIT23      x22        n              y              y
VAUDIT20        xf6        y              y              y
XFER20          xf7        y              y              n
XFER24          x5b        n              n              y
```

<a id="pdf-page-030"></a>

## PDF page 30

Source: SPI-SYN24; PDF page 30; extracted characters: 296.

```text
Message          Op Code    Language 22    Language 23     Language 24
CPERROR7         x2a        y              y               n
CPERROR24        x43        n              n               y
                             Miscellaneous
NOP              x0b        y              y               y
```

<a id="pdf-page-031"></a>

## PDF page 31

Source: SPI-SYN24; PDF page 31; extracted characters: 1023.

```text
3.2      Translation Pumpup


       3.2.1       RTCS21, RTCS23 and RTCS24
The Request Translation Change Status message is sent by the reporting adjunct as part of the
translation pumpup for Communication Manager servers. It is the initial message used to request a
session and tells the switch the maximum number of measured entities configured on the reporting
adjunct. If the switch's current measured capacities are within the reporting adjuncts maximum capacities,
the expected response is an XSTAT message and a TIME message. If the switch has more capacity then
the reporting adjunct can measure, the switch will reject the session with a XFAIL message. The switch
may also reject the session with a BUSYOUT or an RCODE (reason code = 1) message.

After a successful pumpup the switch will not allow more than the maximum number to be later
administered as measured for each entity. With EAS, the switch will restrict an agent from logging on if
the maximum number of measured agents/skills are already logged on.
```

<a id="pdf-page-032"></a>

## PDF page 32

Source: SPI-SYN24; PDF page 32; extracted characters: 2565.

```text
      3.2.1.1              RTCS21 (New CM4)


                                                               Switch    Vect   Skill
                                               First Release   CM4       y/n    y/n
                                               Last Release    CM5.2

     7  6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1  0
              RTCS21                s   e     / / /                      splits                           / / / / / / /      a
                            agpos (cont)                                / / / / /                   trunk groups
      / /                          trunks                          /                            vdns

opcode             RTCS21 = 52 (0x34)
s                  system flag;0 = CMS, 1 = IQ
e                  enhanced dial-plan (EDP) support flag; 0 = no longer used, 1 = always
splits             number of splits that can be measured, 1-2000
agpos              number of agent/skill pairs that can be measured, 1-60000
trunk groups       number of trunk groups that can be measured, 1-2000
trunks             number of trunks that can be measured, 1-12000
vdns               number of VDNs that can be measured, 1-20000

      3.2.1.2              RTCS23 (New CM6.0)


                                                               Switch    Vect   Skill
                                               First Release   CM6.0     y/n    y/n
                                               Last Release    CM6.3



     7  6   5   4   3   2   1   0   7   6  5   4   3   2   1   0   7   6   5   4   3  2   1   0   7   6   5   4   3   2   1  0
              RTCS23                s   e   /                        splits                               / / / / / / /      a
                            agpos (cont)                                / / / / /                   trunk groups
      / /                          trunks                          /                            vdns

opcode             RTCS23 = 55 (0x37)
s                  system flag;0 = CMS, 1 = IQ or WAE
e                  enhanced dial-plan (EDP) support flag; 0 = no longer used, 1 = always
splits             number of splits/skills that can be measured, 1-8000
agpos              number of agent/skill pairs that can be measured, 1-100000
trunk groups       number of trunk groups that can be measured, 1-2000
trunks             number of trunks that can be measured, 1-12000
vdns               number of VDNs that can be measured, 1-30000
```

<a id="pdf-page-033"></a>

## PDF page 33

Source: SPI-SYN24; PDF page 33; extracted characters: 1278.

```text
3.2.1.3                    RTCS24 (New CM7.0)


                                                              Switch   Vect    Skill
                                              First Release   CM7.0    y/n     y/n
                                              Last Release



    7   6   5   4   3   2  1   0   7   6   5  4   3   2   1   0   7  6   5   4   3   2   1  0   7   6   5   4   3  2   1   0
              RTCS24               s   e   /                       splits                             / / / / /      agpos
                           agpos (cont)                                / / / / /                  trunk groups
                               trunks                             /                           vdns

opcode            RTCS24 = 61 (0x3D)
s                 system flag;0 = CMS, 1 = IQ or WAE
e                 enhanced dial-plan (EDP) support flag; 0 = no longer used, 1 = always
splits            number of splits/skills that can be measured, 1-8000
agpos             number of agent/skill pairs that can be measured, 1-360000
trunk groups      number of trunk groups that can be measured, 1-2000
trunks            number of trunks that can be measured, 1-24,000 (64,000 future)
vdns              number of VDNs that can be measured, 1-30000
```

<a id="pdf-page-034"></a>

## PDF page 34

Source: SPI-SYN24; PDF page 34; extracted characters: 2702.

```text
       3.2.2        RCODE20
The switch may reject the request to establish communications with the rcode 1 (illegal request).

Refer to RCODE20 in Switch Administration (section 3.3.30) for the layout.

       3.2.3        XFAIL21, XFAIL23 and XFAIL24
The Translations Fail message is sent by the switch in response to an RTCS that does not have large
enough capacities for the current switch configuration. The reporting adjunct will send the maximum
number of measured entities configured on the reporting adjunct in the RTCS. If the switch has more
measured entities than the reporting adjunct capacity, the switch will send back its current configuration
for each measured entity. With EAS the agpos field will contain the current number of agent/skill pairs
logged in.

When an XFAIL is received, the reporting adjunct will inform the user of the switch's capacities, giving the
user the choice of increasing the reporting adjunct capacities or working with the switch administrator to
reduce the switch capacities before the reporting adjunct Application connection can be established.

3.2.3.1                     XFAIL21 (New CM4)


                                                                Switch   Vect    Skill
                                               First Release    CM4      y/n     y/n
                                               Last Release     CM5.2



     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7  6   5   4   3   2   1   0   7   6   5   4   3   2   1   0
               time tag                       XFAIL21                                        seq num
                           seq num (cont)                                      tot siz                   / / / / /       skills
             skills (cont)                  / / / / / / /                                    agpos
          / / / / /                      tk grps                     / /                          trunks
     /                            vdns

                  time_tag      seconds past minute when message was formed, 0-59
                  opcode        XFAIL21 = 249 (0xf9)
                  seq num       sequence number, 0-0xffff ffff
                  tot siz       total size of message in bytes, 1-255
                  skills        number of splits that are currently measured, 1-2000
                  agpos         number of agent/skill pairs that are currently measured, 1-100000
                  tk grps       number of trunk groups that are currently measured, 1-2000
                  trunks        number of trunks that are currently measured, 1-12000
                  vdns          number of VDNs that are currently measured, 1-20000
```

<a id="pdf-page-035"></a>

## PDF page 35

Source: SPI-SYN24; PDF page 35; extracted characters: 3398.

```text
      3.2.3.2              XFAIL23 (New CM6.0)


                                                               Switch    Vect   Skill
                                               First Release   CM6.0     y/n    y/n
                                               Last Release    CM6.3



     7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
               time tag                      XFAIL23                                         seq num
                           seq num (cont)                                     tot siz                / / /          skills
             skills (cont)                  / / / / / / /                                   agpos
          / / / / /                      tk grps                     / /                          trunks
     /                            vdns

             time_tag      seconds past minute when message was formed, 0-59
             opcode        XFAIL23 = 13 (0x0d)
             seq num       sequence number, 0-0xffff ffff
             tot siz       total size of message in bytes, 1-255
             skills        number of splits that are currently measured, 1-8,000 (CM6.0 and later)
             agpos         number of agent/skill pairs that are currently measured, 1-100,000
             tk grps       number of trunk groups that are currently measured, 1-2,000
             trunks        number of trunks that are currently measured, 1-12,000
             vdns          number of VDNs that are currently measured, 1-30,000 (CM6.0 and later)

3.2.3.3                    XFAIL24 (New CM7.0)


                                                               Switch    Vect   Skill
                                               First Release   CM7.0     y/n    y/n
                                               Last Release



     7  6   5   4   3   2   1   0   7   6   5  4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0
               time tag                      XFAIL24                                         seq num
                           seq num (cont)                                     tot siz                / / /          skills
             skills (cont)               / / / / /                                      agpos
          / / / / /                      tk grps                                              trunks
     /                            vdns

            time_tag      seconds past minute when message was formed, 0-59
            opcode        XFAIL24 = 41 (0x29)
            seq num       sequence number, 0-0xffff ffff
            tot siz       total size of message in bytes, 1-255
            skills        number of splits that are currently measured, 1-8,000 (CM6.0 and later)
            agpos         number of agent/skill pairs that are currently measured, 1-360,000
            tk grps       number of trunk groups that are currently measured, 1-2,000
            trunks        number of trunks that are currently measured, 1-24,000 (64,000 future)
            vdns          number of VDNs that are currently measured, 1-30,000 (CM6.0 and later)


       3.2.4        BUSYOUT20 (New CM3.1)
The switch may reject the request to establish communications RTCS by sending a BUSYOUT20
message. Refer to BUSYOUT20 in Switch Administration (section 3.3.1) for the layout.
```

<a id="pdf-page-036"></a>

## PDF page 36

Source: SPI-SYN24; PDF page 36; extracted characters: 3141.

```text
       3.2.5         XSTAT20 and XSTAT24
The Translation Status message is sent by the switch when the request (RTCS) for a reporting adjunct
Application connection is accepted (the splits and agpos values are valid). If the "translations-changed"
flag in the XSTAT is set (c=1), the reporting adjunct will request full translations by sending the RFTB
message. If the "translations-changed" flag is not set (c=0), the reporting adjunct will request only logon
translations by sending the RLTB message. However, if the reporting adjunct must (re)configure the real-
time database because shared memory was cleared (e.g., initial session or adjunct rebooted), the
reporting adjunct will send the RFTB message regardless of the value of the "translations-changed" flag.

The XSTAT message also indicates that status (enabled/disabled) of the Call Vectoring, Call Prompting,
and EAS (skills) features on the switch.

The XSTAT message contains the reason for the XSTAT request in fault.

The XSTAT is sent by the switch, and is the last message sent in the buffer.  The message set SPI
language must change when capacities or supported features change.

3.2.5.1                     XSTAT20 (New CM3.1)


                                                                 Switch    Vect    Skill
                                                First Release    CM3.1     y/n     y/n
                                                Last Release     CM6.3



     7   6   5   4   3   2   1   0   7   6   5   4   3   2   1   0   7   6   5   4    3   2   1   0   7   6   5   4   3   2   1   0
               time_tag                        XSTAT20                                          seq num
                            seq num (cont)                                       tot siz              c   v   p   s       fault
        switch         release        / /          language           l       / / / /       dot               switch name
                                                          switch name (cont)
                                                          switch name (cont)
                                                          switch name (cont)
                                                          switch name (cont)
                                          switch name (cont)                                                    switch id
           switch id (cont)                                                    time zone
                                                            time zone (cont)
                                                            time zone (cont)
                                                            time zone (cont)
                                                            time zone (cont)
                                                            time zone (cont)
                                                            time zone (cont)
                                                            time zone (cont)
                                           time zone (cont)                                                      country
                display
```

<a id="pdf-page-037"></a>

## PDF page 37

Source: SPI-SYN24; PDF page 37; extracted characters: 3116.

```text
XSTAT20 (continued)

time_tag          seconds past minute when message was formed, 0-59
opcode            XSTAT20 = 177 (0xb1)
seq num           sequence number, 1-0xffff ffff
tot siz           total size of message in bytes; 1-255
c                 change status; 1 = translations changed
v                 vectoring; 1 = call vectoring is enabled
p                 prompting; 1 = call prompting is enabled
s                 EAS; 1 = EAS (skills) is enabled
fault             fault type; 0 = data link down, 1 = short power hit, 2 = buffer blocking, 3 = bad message, 4
                  = switch reload, 5 = modification
switch            switch identifier; 3 = G3
release           switch release; 1 = (not used), 2 = CM6.0, 3 = G3V3 (obsolete), 4 = G3V4 (obsolete), 5 =
                  G3V5 (obsolete), 6 = G3V6/G3V7 (obsolete), 8 = G3V8 (obsolete), 9 = G3V9/G3V10
                  (obsolete), 11 = G3V11 (obsolete), 12 = MV2, 13 = CM3, 14 = CM4/CM5.0, 15 = CM5.2
language          message set SPI language - must change when capacities or supported features change.
                           0 = not used (=> XSTAT)
                           1 =  R3.0 message set w/FSTATE (obsolete)
                           2 = G3V2/R3V2 message set w/multiple trunk state messages (obsolete)
                           3 = G3V4/R3V4 message set w/ vectoring enhancements (obsolete)
                           4 = G3V5/R3V5 message set w/ multiple agent states and audit messages
                           (obsolete)
                           5 = G3V6/R3V6 message set w/ BSR and Agent Allocation features (obsolete)
                           6 = G3V8/R3V8 message set w/ ATM enhancements and R8.3/G3V9/R3V9 w/
                           NCR and Holiday Vectoring (obsolete)
                           7 = G3V11/R3V11 message set w/ Enhanced Dialing Plan (6 and 7 digit
                           extensions) and Trunk Group Capacity Increases and BSR Application Plan
                           Capacity Increase (obsolete)
                           8 = MV2/R12 message set w/ Capacity Increases and Maximizer and Variables in
                           Vectors and Media Gateway and ASAI UU
                           9 = CM3/R13 message set w/ Variables in Vectors Enhancement
                           20 = CM3.1/R13.1 and IQ message set w/ IQ Names Admin, Sequence Numbers,
                           Message Sizes, and UCID in FSTATE/ASTATE message
                           21 = CM4.0/CM5.0/CM5.1/CMS R14/CMS R14.1/IQ 4.0 message set
                           22 = CM5.2/CMS R15/IQ 5.0 message set
                           23 = CM6.0/CMS R16/IQ 5.1
l                 LSP flag; 0 = Primary, 1 = LSP/ESS
dot               switch dot release number extracted from switch release string; 0-7
switch name       switch name (ASCII)
switch id         switch UCID node, 1-32767
time zone         time zone (ASCII)
country           country code; 1-25
display           display character set; 0 = roman (default), 1 = cyrillic, 2 = ukranian, 3 = katakana.
                  0, 1, 2 map to Euro font character set
```

<a id="pdf-page-038"></a>

## PDF page 38

Source: SPI-SYN24; PDF page 38; extracted characters: 3709.

```text
3.2.5.2                     XSTAT24 (New CM7.0)


                                                               Switch    Vect    Skill
                                               First Release   CM7.0     y/n     y/n
                                               Last Release

     7  6   5   4   3   2   1   0   7   6   5   4   3   2   1  0   7   6   5   4   3   2   1   0   7   6   5   4   3   2   1  0
              time_tag                       XSTAT24                                         seq num
                           seq num (cont)                                      tot siz             c   v   p   s       fault
        switch         release       / /         language           l      / / / /        dot              switch name
                                                        switch name (cont)
                                                        switch name (cont)
                                                        switch name (cont)
                                                        switch name (cont)
                                         switch name (cont)                                                  switch id
           switch id (cont)                                                  time zone
                                                          time zone (cont)
                                                          time zone (cont)
                                                          time zone (cont)
                                                          time zone (cont)
                                                          time zone (cont)
                                                          time zone (cont)
                                                          time zone (cont)
                                          time zone (cont)                                                   country
               display               / /                         max_acd


time_tag           seconds past minute when message was formed, 0-59
opcode             XSTAT24 = 44 (0x2c)
seq num            sequence number, 1-0xffff ffff
tot siz            total size of message in bytes; 1-255
c                  change status; 1 = translations changed
v                  vectoring; 1 = call vectoring is enabled
p                  prompting; 1 = call prompting is enabled
s                  EAS; 1 = EAS (skills) is enabled
fault              fault type; 0 = data link down, 1 = short power hit, 2 = buffer blocking, 3 = bad message, 4
                   = switch reload, 5 = modification
switch             switch identifier; 3 = G3
release            switch release; 1 = (not used), 2 = CM6.0, 3 = CM7.0, 4-13 = (not used),
                   14 = CM4/CM5.0, 15 = CM5.2
language           message set SPI language - must change when capacities or supported features change.
                             0 = not used ( XSTAT)
                             21 = CM4.0/CM5.0/CM5.1/CMS R14/CMS R14.1/IQ 4.0 message set
                             22 = CM5.2/CMS R15/IQ 5.0 message set
                             23 = CM6.0/CMS R16/IQ 5.1
                             24 = CM7.0/CMS R18
l                  LSP flag; 0 = Primary, 1 = LSP/ESS
dot                switch dot release number extracted from switch release string; 0-7
switch name        switch name (ASCII)
switch id          switch UCID node, 1-32767
time zone          time zone (ASCII)
country            country code; 1-25
display            display character set; 0 = roman (default), 1 = cyrillic, 2 = ukranian, 3 = katakana.
                   0, 1, 2 map to Euro font character set
max_acd            maximum logged in ACD agents, 1-10,000
```

<a id="pdf-page-039"></a>

## PDF page 39

Source: SPI-SYN24; PDF page 39; extracted characters: 1206.

```text
       3.2.6        TIME20 (New CM3.1)
The TIME message is sent by the switch immediately after the XSTAT message in response to the RTCS
message.  The reporting adjunct first verifies that the switch clock is set (all parameters are valid) and if
so, the reporting adjunct clock is set.  If the switch clock is not set, the reporting adjunct will reinitiate the
reporting adjunct Application connection. The switch administrator must set the clock to enable the
connection to be established.

Once the reporting adjunct clock is set, the reporting adjunct sets an AT3 timer (2 minutes). If this timer
expires, the reporting adjunct will report that the translation pumpup timed-out and then initiate another
reporting adjunct session (i.e., the reporting adjunct sends another RTCS message). The reporting
adjunct will reset the AT3 timer each time a TIME message is received. If the switch expects the
translation pumpup to take longer than the time-out period, another TIME message will be sent.
Additionally, TIME messages can be inserted anywhere in the translation blocks - preferably every
minute, as is done during Call Processing.

Refer to TIME in Call Processing (section 3.4.1) for the layout.
```

<a id="pdf-page-040"></a>

## PDF page 40

Source: SPI-SYN24; PDF page 40; extracted characters: 2514.

```text
       3.2.7       RFTB


                                                              Switch   Vect    Skill
                                              First Release   G3V1     y/n     y/n
                                              Last Release

The Request Full Translation Block message is sent by the reporting adjunct to request a full
translation pumpup. This is required if the reporting adjunct user requests that additional or fewer splits be
measured, the switch indicates that translations have changed since the last session, or when the
reporting adjunct shared memory has been cleared (e.g., initial session or after an adjunct reboot). The
expected response is shown in the semantics document (depending on switch release and active
features) and includes all messages from the XOPEN block = 0 to the XCLOSE block = 0.

    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3   2  1   0
               RFTB                           NOP                            NOP                            NOP

                                                opcode      RFTB = 6 (0x06)


       3.2.8       RLTB


                                                              Switch   Vect    Skill
                                              First Release   G3V1     y/n     y/n
                                              Last Release

The Request Logon/Status Translations message is sent by the reporting adjunct as part of the
translation pumpup when the real-time database does not have to be reconfigured since the real-time
database is in synch with the switch translations. The reporting adjunct only needs an update of the
agents that are currently logged in, and the current state of each skill.

The expected response is a logon/status translation block.  XOPEN block = 5 surrounds the messages of
the logon/status pumpup.  An ALOGON message is sent for each staffed agent position.  If there are no
staffed agents, then an empty block (XOPEN to XCLOSE) is sent.  Within the XOPEN block = 5 and
XCLOSE block = 5 messages, the XOPEN block = 6 and XCLOSE block = 6 surrounds the SKSTATE for
all measured skills.



    7   6   5   4   3   2  1   0   7   6   5   4  3   2   1   0   7   6  5   4   3   2   1   0  7   6   5   4   3   2  1   0
               RLTB                           NOP                            NOP                            NOP

                                               opcode      RLTB = 12 (0x0c)
```
