---
title: "Complete SPI document library"
layer: L4
scope: "All supplied source pages and sections, versioned messages and test-plan coverage."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# Complete SPI document library

[Protocol interpretation and diagnostic guide](../spi-protocol.md) | [All versioned messages](messages.md) | [All CM6 Abstract Tests](cm6-tests.md) | [Coverage and anomalies](coverage.md)

This library preserves both supplied SPI documents in full: original PDF bytes plus every physical page in searchable companions. It covers historical versions, all fields and source tables, administration, vector steps, errors, indexes and back matter. Bit-layout diagrams, figures and visual relationships remain authoritative in the unchanged originals. Commands in the archived sources are reference data, not execution instructions or approval. Missing external documents are listed in the coverage report and are not silently claimed included.

| Source | Pages | Complete original | SHA-256 |
|---|---|---|---|
| SPI-SYN24 | 253 | [PDF](../../assets/spi-protocol/spi-syntax-2015.pdf) | `2b1116d4be9ac55d8d483f6c9aca6646afe379bb83117e4795373c68beda6115` |
| SPI-DTP6 | 28 | [PDF](../../assets/spi-protocol/spi-enhancements-cm6-2010.pdf) | `25cccc7b5cffeb74b9f09e7a4e06827c44deacc5844dbeaa404537c0f7a5ff70` |

## How to read

Search the message index for an exact versioned name and direction; open its section/page range. Read all continuation pages and parent/shared field rules. Page markers and the machine coverage map provide bounded source spans; do not load the whole library into context merely to answer a focused question. Use the PDF whenever transcription cannot establish bit position, layout or graphical meaning. Match the actual negotiated language and product applicability.

## SPI syntax: complete section map

| Section | Title | Source pages | First page text |
|---|---|---|---|
| FRONT-ABSTRACT | Cover/abstract, ancestors, application exceptions and external-document pointers | 1-1 | [p.1](syntax-2015-pages-001-020.md#pdf-page-001) |
| FRONT-CHANGES | Change history; requirements-oriented and message-oriented language24 changes | 2-6 | [p.2](syntax-2015-pages-001-020.md#pdf-page-002) |
| FRONT-QUICKLINKS | Links to SPI message designs | 7-8 | [p.7](syntax-2015-pages-001-020.md#pdf-page-007) |
| FRONT-TOC | Printed table of contents including REFERENCES | 9-16 | [p.9](syntax-2015-pages-001-020.md#pdf-page-009) |
| FRONT-LISTS | List of figures/tables | 17-17 | [p.17](syntax-2015-pages-001-020.md#pdf-page-017) |
| UNTITLED-253 | Untitled final page: five REFERENCES bibliography entries | 253-253 | [p.253](syntax-2015-pages-241-253.md#pdf-page-253) |
| TEXT-EMPTY-244 | Text-empty index page; original visual page still required | 244-244 | [p.244](syntax-2015-pages-241-253.md#pdf-page-244) |
| 1 | Introduction | 18-23 | [p.18](syntax-2015-pages-001-020.md#pdf-page-018) |
| 1.1 | Purpose | 18-18 | [p.18](syntax-2015-pages-001-020.md#pdf-page-018) |
| 1.2 | Overview | 18-21 | [p.18](syntax-2015-pages-001-020.md#pdf-page-018) |
| 1.2.1 | OSI Reference Model | 18-19 | [p.18](syntax-2015-pages-001-020.md#pdf-page-018) |
| 1.2.1.1 | Physical Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.2 | Data Link Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.3 | Network Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.4 | Transport Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.5 | Session Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.6 | Presentation Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.1.7 | Application Layer | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| 1.2.2 | X.25 Protocol | 20-20 | [p.20](syntax-2015-pages-001-020.md#pdf-page-020) |
| 1.2.3 | BX.25 Protocol | 20-20 | [p.20](syntax-2015-pages-001-020.md#pdf-page-020) |
| 1.2.4 | TCP/IP Protocol | 20-20 | [p.20](syntax-2015-pages-001-020.md#pdf-page-020) |
| 1.2.5 | Reporting Adjunct Protocol | 20-21 | [p.20](syntax-2015-pages-001-020.md#pdf-page-020) |
| 1.3 | Terminology | 21-23 | [p.21](syntax-2015-pages-021-040.md#pdf-page-021) |
| 2 | PROTOCOL SPECIFICATION | 24-25 | [p.24](syntax-2015-pages-021-040.md#pdf-page-024) |
| 3 | PROTOCOL SYNTAX | 26-239 | [p.26](syntax-2015-pages-021-040.md#pdf-page-026) |
| 3.1 | Compatibility | 26-30 | [p.26](syntax-2015-pages-021-040.md#pdf-page-026) |
| 3.2 | Translation Pumpup | 31-52 | [p.31](syntax-2015-pages-021-040.md#pdf-page-031) |
| 3.2.1 | ←RTCS21, RTCS23 and RTCS24 | 31-33 | [p.31](syntax-2015-pages-021-040.md#pdf-page-031) |
| 3.2.1.1 | ←RTCS21 (New CM4) | 32-32 | [p.32](syntax-2015-pages-021-040.md#pdf-page-032) |
| 3.2.1.2 | ←RTCS23 (New CM6.0) | 32-32 | [p.32](syntax-2015-pages-021-040.md#pdf-page-032) |
| 3.2.1.3 | ←RTCS24 (New CM7.0) | 33-33 | [p.33](syntax-2015-pages-021-040.md#pdf-page-033) |
| 3.2.2 | →RCODE20 | 34-34 | [p.34](syntax-2015-pages-021-040.md#pdf-page-034) |
| 3.2.3 | →XFAIL21, XFAIL23 and XFAIL24 | 34-35 | [p.34](syntax-2015-pages-021-040.md#pdf-page-034) |
| 3.2.3.1 | →XFAIL21 (New CM4) | 34-34 | [p.34](syntax-2015-pages-021-040.md#pdf-page-034) |
| 3.2.3.2 | →XFAIL23 (New CM6.0) | 35-35 | [p.35](syntax-2015-pages-021-040.md#pdf-page-035) |
| 3.2.3.3 | →XFAIL24 (New CM7.0) | 35-35 | [p.35](syntax-2015-pages-021-040.md#pdf-page-035) |
| 3.2.4 | →BUSYOUT20 (New CM3.1) | 35-35 | [p.35](syntax-2015-pages-021-040.md#pdf-page-035) |
| 3.2.5 | →XSTAT20 and XSTAT24 | 36-38 | [p.36](syntax-2015-pages-021-040.md#pdf-page-036) |
| 3.2.5.1 | →XSTAT20 (New CM3.1) | 36-37 | [p.36](syntax-2015-pages-021-040.md#pdf-page-036) |
| 3.2.5.2 | →XSTAT24 (New CM7.0) | 38-38 | [p.38](syntax-2015-pages-021-040.md#pdf-page-038) |
| 3.2.6 | →TIME20 (New CM3.1) | 39-39 | [p.39](syntax-2015-pages-021-040.md#pdf-page-039) |
| 3.2.7 | ←RFTB | 40-40 | [p.40](syntax-2015-pages-021-040.md#pdf-page-040) |
| 3.2.8 | ←RLTB | 40-40 | [p.40](syntax-2015-pages-021-040.md#pdf-page-040) |
| 3.2.9 | →XOPEN20 (New CM3.1) | 41-41 | [p.41](syntax-2015-pages-041-060.md#pdf-page-041) |
| 3.2.10 | →XCLOSE20 (New CM3.1) | 42-42 | [p.42](syntax-2015-pages-041-060.md#pdf-page-042) |
| 3.2.11 | →XVDN20, XVDN23 and XVDN24 | 43-45 | [p.43](syntax-2015-pages-041-060.md#pdf-page-043) |
| 3.2.11.1 | →XVDN20 (New CM3.1) | 43-43 | [p.43](syntax-2015-pages-041-060.md#pdf-page-043) |
| 3.2.11.2 | →XVDN23 (New CM6.0) | 44-44 | [p.44](syntax-2015-pages-041-060.md#pdf-page-044) |
| 3.2.11.3 | →XVDN24 (New CM7.0) | 45-45 | [p.45](syntax-2015-pages-041-060.md#pdf-page-045) |
| 3.2.12 | →XSPLIT20 and XSPLIT24 | 46-46 | [p.46](syntax-2015-pages-041-060.md#pdf-page-046) |
| 3.2.12.1 | →XSPLIT20 (New CM3.1) | 46-46 | [p.46](syntax-2015-pages-041-060.md#pdf-page-046) |
| 3.2.12.2 | →XSPLIT24 (New CM7.0) | 46-46 | [p.46](syntax-2015-pages-041-060.md#pdf-page-046) |
| 3.2.13 | →XAGENT20 and XAGENT24 | 47-48 | [p.47](syntax-2015-pages-041-060.md#pdf-page-047) |
| 3.2.13.1 | →XAGENT20 (New CM3.1) | 47-47 | [p.47](syntax-2015-pages-041-060.md#pdf-page-047) |
| 3.2.13.2 | →XAGENT24 (New CM7.0) | 48-48 | [p.48](syntax-2015-pages-041-060.md#pdf-page-048) |
| 3.2.14 | →XTKGRP20 and XTKGRP24 | 49-49 | [p.49](syntax-2015-pages-041-060.md#pdf-page-049) |
| 3.2.14.1 | →XTKGRP20 (New CM3.1) | 49-49 | [p.49](syntax-2015-pages-041-060.md#pdf-page-049) |
| 3.2.14.2 | →XTKGRP24 (New CM7.0) | 49-49 | [p.49](syntax-2015-pages-041-060.md#pdf-page-049) |
| 3.2.15 | →XTGVDN20 and XTGVDN24 | 50-50 | [p.50](syntax-2015-pages-041-060.md#pdf-page-050) |
| 3.2.15.1 | →XTGVDN20 (New CM3.1) | 50-50 | [p.50](syntax-2015-pages-041-060.md#pdf-page-050) |
| 3.2.15.2 | →XTGVDN24 (New CM7.0) | 50-50 | [p.50](syntax-2015-pages-041-060.md#pdf-page-050) |
| 3.2.16 | →XTRUNK20 and XTRUNK24 | 51-52 | [p.51](syntax-2015-pages-041-060.md#pdf-page-051) |
| 3.2.16.1 | →XTRUNK20 (New CM3.1) | 51-51 | [p.51](syntax-2015-pages-041-060.md#pdf-page-051) |
| 3.2.16.2 | →XTRUNK24 (New CM7.0) | 52-52 | [p.52](syntax-2015-pages-041-060.md#pdf-page-052) |
| 3.2.17 | →SKSTATE20 and SKSTATE23 | 52-52 | [p.52](syntax-2015-pages-041-060.md#pdf-page-052) |
| 3.2.18 | →ALOGON20, ALOGON23 and ALOGON24 | 52-52 | [p.52](syntax-2015-pages-041-060.md#pdf-page-052) |
| 3.3 | Switch Administration | 53-136 | [p.53](syntax-2015-pages-041-060.md#pdf-page-053) |
| 3.3.1 | →BUSYOUT20 (New CM3.1) | 54-54 | [p.54](syntax-2015-pages-041-060.md#pdf-page-054) |
| 3.3.2 | →RELBUSY20 (New CM3.1) | 54-54 | [p.54](syntax-2015-pages-041-060.md#pdf-page-054) |
| 3.3.3 | →ARVDN20, ARVDN23 and ARVDN24 | 55-57 | [p.55](syntax-2015-pages-041-060.md#pdf-page-055) |
| 3.3.3.1 | →ARVDN20 (New CM3.1) | 55-55 | [p.55](syntax-2015-pages-041-060.md#pdf-page-055) |
| 3.3.3.2 | →ARVDN23 (New CM6.0) | 56-56 | [p.56](syntax-2015-pages-041-060.md#pdf-page-056) |
| 3.3.3.3 | →ARVDN24 (New CM7.0) | 57-57 | [p.57](syntax-2015-pages-041-060.md#pdf-page-057) |
| 3.3.4 | →ARAGENT20 and ARAGENT24 | 58-59 | [p.58](syntax-2015-pages-041-060.md#pdf-page-058) |
| 3.3.4.1 | →ARAGENT20 (New CM3.1) | 58-58 | [p.58](syntax-2015-pages-041-060.md#pdf-page-058) |
| 3.3.4.2 | →ARAGENT24 (New CM7.0) | 59-59 | [p.59](syntax-2015-pages-041-060.md#pdf-page-059) |
| 3.3.5 | →ARSPLIT20, ARSPLIT23 and ARSPLIT24 | 60-61 | [p.60](syntax-2015-pages-041-060.md#pdf-page-060) |
| 3.3.5.1 | →ARSPLIT20 (New CM3.1) | 60-60 | [p.60](syntax-2015-pages-041-060.md#pdf-page-060) |
| 3.3.5.2 | →ARSPLIT23 (New CM6.0) | 60-60 | [p.60](syntax-2015-pages-041-060.md#pdf-page-060) |
| 3.3.5.3 | →ARSPLIT24 (New CM7.0 | 61-61 | [p.61](syntax-2015-pages-061-080.md#pdf-page-061) |
| 3.3.6 | →ARTKGRP20, ARTKGRP23 and ARTKGRP24 | 62-63 | [p.62](syntax-2015-pages-061-080.md#pdf-page-062) |
| 3.3.6.1 | →ARTKGRP20 (New CM3.1) | 62-62 | [p.62](syntax-2015-pages-061-080.md#pdf-page-062) |
| 3.3.6.2 | →ARTKGRP23 (New CM6.0) | 62-62 | [p.62](syntax-2015-pages-061-080.md#pdf-page-062) |
| 3.3.6.3 | →ARTKGRP24 (New CM7.0) | 63-63 | [p.63](syntax-2015-pages-061-080.md#pdf-page-063) |
| 3.3.7 | →ARTGVDN20 and ARTGVDN24 | 64-64 | [p.64](syntax-2015-pages-061-080.md#pdf-page-064) |
| 3.3.7.1 | →ARTGVDN20 (New CM3.1) | 64-64 | [p.64](syntax-2015-pages-061-080.md#pdf-page-064) |
| 3.3.7.2 | →ARTGVDN24 (New CM7.0) | 64-64 | [p.64](syntax-2015-pages-061-080.md#pdf-page-064) |
| 3.3.8 | →ARTRUNK20 and ARTRUNK24 | 65-66 | [p.65](syntax-2015-pages-061-080.md#pdf-page-065) |
| 3.3.8.1 | →ARTRUNK20 (New CM3.1) | 65-65 | [p.65](syntax-2015-pages-061-080.md#pdf-page-065) |
| 3.3.8.2 | →ARTRUNK24 (New CM7.0) | 66-66 | [p.66](syntax-2015-pages-061-080.md#pdf-page-066) |
| 3.3.9 | →AGMOVE20 (New CM3.1) | 67-67 | [p.67](syntax-2015-pages-061-080.md#pdf-page-067) |
| 3.3.10 | ← MVAGSTFD21, MVAGSTFD23 and MVAGSTFD24 | 68-71 | [p.68](syntax-2015-pages-061-080.md#pdf-page-068) |
| 3.3.10.1 | ←MVAGSTFD21 (New CM4) | 69-69 | [p.69](syntax-2015-pages-061-080.md#pdf-page-069) |
| 3.3.10.2 | ←MVAGSTFD23 (New CM6.0) | 70-70 | [p.70](syntax-2015-pages-061-080.md#pdf-page-070) |
| 3.3.10.3 | ←MVAGSTFD24 (New CM7.0) | 71-71 | [p.71](syntax-2015-pages-061-080.md#pdf-page-071) |
| 3.3.11 | ←APARMS7 and APARMS24 | 72-72 | [p.72](syntax-2015-pages-061-080.md#pdf-page-072) |
| 3.3.11.1 | ←APARMS7 (New G3V11) | 72-72 | [p.72](syntax-2015-pages-061-080.md#pdf-page-072) |
| 3.3.11.2 | ←APARMS24 (New CM7.0) | 72-72 | [p.72](syntax-2015-pages-061-080.md#pdf-page-072) |
| 3.3.12 | →AGENTSK20, AGENTSK23, AGENTSK24 | 73-77 | [p.73](syntax-2015-pages-061-080.md#pdf-page-073) |
| 3.3.12.1 | →AGENTSK20 (New CM3.1) | 73-73 | [p.73](syntax-2015-pages-061-080.md#pdf-page-073) |
| 3.3.12.2 | →AGENTSK23 (New CM6.0) | 74-75 | [p.74](syntax-2015-pages-061-080.md#pdf-page-074) |
| 3.3.12.3 | →AGENTSK24 (New CM7.0) | 76-77 | [p.76](syntax-2015-pages-061-080.md#pdf-page-076) |
| 3.3.13 | ←SKILLADD8, SKILLADD23 and SKILLADD24 | 78-81 | [p.78](syntax-2015-pages-061-080.md#pdf-page-078) |
| 3.3.13.1 | ←SKILLADD8 (New MV2) | 78-78 | [p.78](syntax-2015-pages-061-080.md#pdf-page-078) |
| 3.3.13.2 | ←SKILLADD23 (New CM6.0) | 79-79 | [p.79](syntax-2015-pages-061-080.md#pdf-page-079) |
| 3.3.13.3 | ←SKILLADD24 (New CM7.0) | 80-81 | [p.80](syntax-2015-pages-061-080.md#pdf-page-080) |
| 3.3.14 | →TGMOVE20 and TGMOVE23 | 82-82 | [p.82](syntax-2015-pages-081-100.md#pdf-page-082) |
| 3.3.14.1 | →TGMOVE20 (New CM3.1) | 82-82 | [p.82](syntax-2015-pages-081-100.md#pdf-page-082) |
| 3.3.14.2 | →TGMOVE23 (New CM6.0) | 82-82 | [p.82](syntax-2015-pages-081-100.md#pdf-page-082) |
| 3.3.15 | →VTGMOVE20 (New CM3.1) | 83-83 | [p.83](syntax-2015-pages-081-100.md#pdf-page-083) |
| 3.3.16 | →VDNMOVE20, VDNMOVE23 and VDNMOVE24 | 84-85 | [p.84](syntax-2015-pages-081-100.md#pdf-page-084) |
| 3.3.16.1 | →VDNMOVE20 (New CM3.1) | 84-84 | [p.84](syntax-2015-pages-081-100.md#pdf-page-084) |
| 3.3.16.2 | →VDNMOVE23 (New CM6.0) | 85-85 | [p.85](syntax-2015-pages-081-100.md#pdf-page-085) |
| 3.3.16.3 | →VDNMOVE24 (New CM7.0) | 85-85 | [p.85](syntax-2015-pages-081-100.md#pdf-page-085) |
| 3.3.17 | ← MVVDN9 and MVVDN23 | 86-86 | [p.86](syntax-2015-pages-081-100.md#pdf-page-086) |
| 3.3.17.1 | ←MVVDN9 (New CM3) | 86-86 | [p.86](syntax-2015-pages-081-100.md#pdf-page-086) |
| 3.3.17.2 | ←MVVDN23 (New CM6.0) | 86-86 | [p.86](syntax-2015-pages-081-100.md#pdf-page-086) |
| 3.3.18 | ←CHGVDNSK8 and CHGVDNSK23 | 87-87 | [p.87](syntax-2015-pages-081-100.md#pdf-page-087) |
| 3.3.18.1 | ←CHGVDNSK8 (New MV2) | 87-87 | [p.87](syntax-2015-pages-081-100.md#pdf-page-087) |
| 3.3.18.2 | ←CHGVDNSK23 (New CM6.0) | 87-87 | [p.87](syntax-2015-pages-081-100.md#pdf-page-087) |
| 3.3.19 | ←VPARMS | 88-88 | [p.88](syntax-2015-pages-081-100.md#pdf-page-088) |
| 3.3.20 | VECTOR20 and VECTOR24 | 89-91 | [p.89](syntax-2015-pages-081-100.md#pdf-page-089) |
| 3.3.20.1 | →VECTOR20 (New CM3.1) | 90-90 | [p.90](syntax-2015-pages-081-100.md#pdf-page-090) |
| 3.3.20.2 | →VECTOR24 (New CM7.0) | 91-91 | [p.91](syntax-2015-pages-081-100.md#pdf-page-091) |
| 3.3.21 | Vector Steps | 92-114 | [p.92](syntax-2015-pages-081-100.md#pdf-page-092) |
| 3.3.21.1 | Queue to | 92-92 | [p.92](syntax-2015-pages-081-100.md#pdf-page-092) |
| 3.3.21.2 | Check | 93-94 | [p.93](syntax-2015-pages-081-100.md#pdf-page-093) |
| 3.3.21.3 | Route To Number | 95-96 | [p.95](syntax-2015-pages-081-100.md#pdf-page-095) |
| 3.3.21.4 | Announcement | 97-97 | [p.97](syntax-2015-pages-081-100.md#pdf-page-097) |
| 3.3.21.5 | Wait | 97-97 | [p.97](syntax-2015-pages-081-100.md#pdf-page-097) |
| 3.3.21.6 | Goto Step and Goto Vector | 98-108 | [p.98](syntax-2015-pages-081-100.md#pdf-page-098) |
| 3.3.21.7 | Disconnect | 109-109 | [p.109](syntax-2015-pages-101-120.md#pdf-page-109) |
| 3.3.21.8 | Busy | 109-109 | [p.109](syntax-2015-pages-101-120.md#pdf-page-109) |
| 3.3.21.9 | Stop | 109-109 | [p.109](syntax-2015-pages-101-120.md#pdf-page-109) |
| 3.3.21.10 | Collect Digits | 110-110 | [p.110](syntax-2015-pages-101-120.md#pdf-page-110) |
| 3.3.21.11 | Route To Digits | 110-110 | [p.110](syntax-2015-pages-101-120.md#pdf-page-110) |
| 3.3.21.12 | Messaging Split | 111-111 | [p.111](syntax-2015-pages-101-120.md#pdf-page-111) |
| 3.3.21.13 | Adjunct Routing | 111-111 | [p.111](syntax-2015-pages-101-120.md#pdf-page-111) |
| 3.3.21.14 | Converse | 112-112 | [p.112](syntax-2015-pages-101-120.md#pdf-page-112) |
| 3.3.21.15 | Consider | 112-112 | [p.112](syntax-2015-pages-101-120.md#pdf-page-112) |
| 3.3.21.16 | Reply | 113-113 | [p.113](syntax-2015-pages-101-120.md#pdf-page-113) |
| 3.3.21.17 | Return | 113-113 | [p.113](syntax-2015-pages-101-120.md#pdf-page-113) |
| 3.3.21.18 | Set | 114-114 | [p.114](syntax-2015-pages-101-120.md#pdf-page-114) |
| 3.3.22 | ← CHGVEC20 AND CHGVEC24 | 115-116 | [p.115](syntax-2015-pages-101-120.md#pdf-page-115) |
| 3.3.22.1 | ←CHGVEC20 (New CM3.1) | 115-115 | [p.115](syntax-2015-pages-101-120.md#pdf-page-115) |
| 3.3.22.2 | ←CHGVEC24 (New CM7.0) | 116-116 | [p.116](syntax-2015-pages-101-120.md#pdf-page-116) |
| 3.3.23 | ←REQLIST5 (New G3V6) | 117-117 | [p.117](syntax-2015-pages-101-120.md#pdf-page-117) |
| 3.3.24 | →ADMLIST20 (New CM3.1) | 118-118 | [p.118](syntax-2015-pages-101-120.md#pdf-page-118) |
| 3.3.25 | ←REQNAM20 (New CM3.1) | 119-119 | [p.119](syntax-2015-pages-101-120.md#pdf-page-119) |
| 3.3.26 | →ADMNAM20 and ADMNAM24 | 120-124 | [p.120](syntax-2015-pages-101-120.md#pdf-page-120) |
| 3.3.26.1 | →ADMNAM20 (New CM3.1) | 120-122 | [p.120](syntax-2015-pages-101-120.md#pdf-page-120) |
| 3.3.26.2 | →ADMNAM24 (New CM7.0) | 123-124 | [p.123](syntax-2015-pages-121-140.md#pdf-page-123) |
| 3.3.27 | ←RCODENAM20 (New CM3.1) | 125-125 | [p.125](syntax-2015-pages-121-140.md#pdf-page-125) |
| 3.3.28 | ← CHGNAM20 and CHGNAM24 | 126-129 | [p.126](syntax-2015-pages-121-140.md#pdf-page-126) |
| 3.3.28.1 | ←CHGNAM20 (New CM3.1) | 126-127 | [p.126](syntax-2015-pages-121-140.md#pdf-page-126) |
| 3.3.28.2 | ← CHGNAM24 (New CM7.0) | 128-129 | [p.128](syntax-2015-pages-121-140.md#pdf-page-128) |
| 3.3.29 | →MVRCODE20 (New CM3.1) | 130-130 | [p.130](syntax-2015-pages-121-140.md#pdf-page-130) |
| 3.3.30 | →RCODE20 (New CM3.1) | 131-133 | [p.131](syntax-2015-pages-121-140.md#pdf-page-131) |
| 3.3.31 | →CRCODE20 (New CM3.1) | 134-135 | [p.134](syntax-2015-pages-121-140.md#pdf-page-134) |
| 3.3.32 | ←USERID21 (New CM4) | 136-136 | [p.136](syntax-2015-pages-121-140.md#pdf-page-136) |
| 3.4 | Call Processing | 137-238 | [p.137](syntax-2015-pages-121-140.md#pdf-page-137) |
| 3.4.1 | →TIME20 (New CM3.1) | 137-137 | [p.137](syntax-2015-pages-121-140.md#pdf-page-137) |
| 3.4.2 | →ALOGON20, ALOGON23 and ALOGON24 | 138-146 | [p.138](syntax-2015-pages-121-140.md#pdf-page-138) |
| 3.4.2.1 | →ALOGON20 (New CM3.1) | 139-140 | [p.139](syntax-2015-pages-121-140.md#pdf-page-139) |
| 3.4.2.1.1 | →ALOGON20, without EAS (New CM3.1) | 139-139 | [p.139](syntax-2015-pages-121-140.md#pdf-page-139) |
| 3.4.2.1.2 | →ALOGON20, with EAS (New CM3.1) | 140-140 | [p.140](syntax-2015-pages-121-140.md#pdf-page-140) |
| 3.4.2.2 | →ALOGON23 (New CM6.0) | 141-143 | [p.141](syntax-2015-pages-141-160.md#pdf-page-141) |
| 3.4.2.2.1 | →ALOGON23, without EAS (New CM6.0) | 141-141 | [p.141](syntax-2015-pages-141-160.md#pdf-page-141) |
| 3.4.2.2.2 | →ALOGON23, with EAS (New CM6.0) | 142-143 | [p.142](syntax-2015-pages-141-160.md#pdf-page-142) |
| 3.4.2.3 | →ALOGON24 (New CM7.0) | 144-146 | [p.144](syntax-2015-pages-141-160.md#pdf-page-144) |
| 3.4.2.3.1 | →ALOGON24, without EAS (New CM7.0) | 144-144 | [p.144](syntax-2015-pages-141-160.md#pdf-page-144) |
| 3.4.2.3.2 | →ALOGON24, with EAS (New CM7.0) | 145-146 | [p.145](syntax-2015-pages-141-160.md#pdf-page-145) |
| 3.4.3 | → ALOGOFF20 and ALOGOFF24 | 147-147 | [p.147](syntax-2015-pages-141-160.md#pdf-page-147) |
| 3.4.3.1 | →ALOGOFF20 (New CM3.1) | 147-147 | [p.147](syntax-2015-pages-141-160.md#pdf-page-147) |
| 3.4.3.2 | →ALOGOFF24 (New CM7.0) | 147-147 | [p.147](syntax-2015-pages-141-160.md#pdf-page-147) |
| 3.4.4 | → AVAIL22, AVAIL23 and AVAIL24 | 148-150 | [p.148](syntax-2015-pages-141-160.md#pdf-page-148) |
| 3.4.4.1 | →AVAIL22 (New CM5.2) | 148-148 | [p.148](syntax-2015-pages-141-160.md#pdf-page-148) |
| 3.4.4.2 | →AVAIL23 (New CM6.0) | 149-149 | [p.149](syntax-2015-pages-141-160.md#pdf-page-149) |
| 3.4.4.3 | →AVAIL24 (New CM7.0) | 150-150 | [p.150](syntax-2015-pages-141-160.md#pdf-page-150) |
| 3.4.5 | → ACD20 and ACD24 | 151-152 | [p.151](syntax-2015-pages-141-160.md#pdf-page-151) |
| 3.4.5.1 | →ACD20 (New CM3.1) | 151-151 | [p.151](syntax-2015-pages-141-160.md#pdf-page-151) |
| 3.4.5.2 | →ACD24 (New CM7.0) | 152-152 | [p.152](syntax-2015-pages-141-160.md#pdf-page-152) |
| 3.4.6 | → ACW22 and ACW24 | 153-154 | [p.153](syntax-2015-pages-141-160.md#pdf-page-153) |
| 3.4.6.1 | →ACW22 (New CM5.2) | 153-153 | [p.153](syntax-2015-pages-141-160.md#pdf-page-153) |
| 3.4.6.2 | → ACW24 (New CM7.0) | 154-154 | [p.154](syntax-2015-pages-141-160.md#pdf-page-154) |
| 3.4.7 | → AUX22, AUX23 and AUX24 | 155-157 | [p.155](syntax-2015-pages-141-160.md#pdf-page-155) |
| 3.4.7.1 | →AUX22 (New CM5.2) | 155-155 | [p.155](syntax-2015-pages-141-160.md#pdf-page-155) |
| 3.4.7.2 | →AUX23 (New CM6.0) | 156-156 | [p.156](syntax-2015-pages-141-160.md#pdf-page-156) |
| 3.4.7.3 | →AUX24 (New CM7.0) | 157-157 | [p.157](syntax-2015-pages-141-160.md#pdf-page-157) |
| 3.4.8 | →OTHER22 and OTHER24 | 158-159 | [p.158](syntax-2015-pages-141-160.md#pdf-page-158) |
| 3.4.8.1 | →OTHER22 (New CM5.2) | 158-158 | [p.158](syntax-2015-pages-141-160.md#pdf-page-158) |
| 3.4.8.2 | →OTHER24 (New CM7.0) | 159-159 | [p.159](syntax-2015-pages-141-160.md#pdf-page-159) |
| 3.4.9 | → DIGITS20 and DIGITS24 | 160-163 | [p.160](syntax-2015-pages-141-160.md#pdf-page-160) |
| 3.4.9.1 | →DIGITS20 (New CM3.1) | 160-161 | [p.160](syntax-2015-pages-141-160.md#pdf-page-160) |
| 3.4.9.2 | →DIGITS24 (New CM7.0) | 162-163 | [p.162](syntax-2015-pages-161-180.md#pdf-page-162) |
| 3.4.10 | →AEVENT20 and AEVENT24 | 164-166 | [p.164](syntax-2015-pages-161-180.md#pdf-page-164) |
| 3.4.10.1 | →AEVENT20 (New CM3.1) | 165-165 | [p.165](syntax-2015-pages-161-180.md#pdf-page-165) |
| 3.4.10.2 | →AEVENT24 (New CM7.0) | 166-166 | [p.166](syntax-2015-pages-161-180.md#pdf-page-166) |
| 3.4.11 | →IDLE20, IDLE23 and IDLE24 | 167-169 | [p.167](syntax-2015-pages-161-180.md#pdf-page-167) |
| 3.4.11.1 | →IDLE20 (New CM3.1) | 167-167 | [p.167](syntax-2015-pages-161-180.md#pdf-page-167) |
| 3.4.11.2 | →IDLE23 (New CM6.0) | 168-168 | [p.168](syntax-2015-pages-161-180.md#pdf-page-168) |
| 3.4.11.3 | →IDLE24 (New CM7.0) | 169-169 | [p.169](syntax-2015-pages-161-180.md#pdf-page-169) |
| 3.4.12 | → SETUP22 and SETUP24 | 170-171 | [p.170](syntax-2015-pages-161-180.md#pdf-page-170) |
| 3.4.12.1 | →SETUP22 (New CM5.2) | 170-170 | [p.170](syntax-2015-pages-161-180.md#pdf-page-170) |
| 3.4.12.2 | →SETUP24 (New CM7.0) | 171-171 | [p.171](syntax-2015-pages-161-180.md#pdf-page-171) |
| 3.4.13 | →QUEUED20, QUEUED23 and QUEUED24 | 172-174 | [p.172](syntax-2015-pages-161-180.md#pdf-page-172) |
| 3.4.13.1 | →QUEUED20 (New CM3.1) | 172-172 | [p.172](syntax-2015-pages-161-180.md#pdf-page-172) |
| 3.4.13.2 | →QUEUED23 (New CM6.0) | 173-173 | [p.173](syntax-2015-pages-161-180.md#pdf-page-173) |
| 3.4.13.3 | →QUEUED24 (New CM7.0) | 174-174 | [p.174](syntax-2015-pages-161-180.md#pdf-page-174) |
| 3.4.14 | →DAQUEUED20, DAQUEUED23 and DAQUEUED24 | 175-177 | [p.175](syntax-2015-pages-161-180.md#pdf-page-175) |
| 3.4.14.1 | →DAQUEUED20 (New CM3.1) | 175-175 | [p.175](syntax-2015-pages-161-180.md#pdf-page-175) |
| 3.4.14.2 | →DAQUEUED23 (New CM6.0) | 176-176 | [p.176](syntax-2015-pages-161-180.md#pdf-page-176) |
| 3.4.14.3 | →DAQUEUED24 (New CM7.0) | 177-177 | [p.177](syntax-2015-pages-161-180.md#pdf-page-177) |
| 3.4.15 | → DCON22, DCON23 and DCON24 | 178-180 | [p.178](syntax-2015-pages-161-180.md#pdf-page-178) |
| 3.4.15.1 | →DCON22 (New CM5.2) | 178-178 | [p.178](syntax-2015-pages-161-180.md#pdf-page-178) |
| 3.4.15.2 | →DCON23 (New CM6.0) | 179-179 | [p.179](syntax-2015-pages-161-180.md#pdf-page-179) |
| 3.4.15.3 | →DCON24 (New CM7.0) | 180-180 | [p.180](syntax-2015-pages-161-180.md#pdf-page-180) |
| 3.4.16 | →DABN22 and DABN24 | 181-182 | [p.181](syntax-2015-pages-181-200.md#pdf-page-181) |
| 3.4.16.1 | →DABN22 (New CM5.2) | 181-181 | [p.181](syntax-2015-pages-181-200.md#pdf-page-181) |
| 3.4.16.2 | →DABN24 (New CM7.0) | 182-182 | [p.182](syntax-2015-pages-181-200.md#pdf-page-182) |
| 3.4.17 | →DADFWD20 and DADFWD24 | 183-184 | [p.183](syntax-2015-pages-181-200.md#pdf-page-183) |
| 3.4.17.1 | →DADFWD20 (New CM3.1) | 183-183 | [p.183](syntax-2015-pages-181-200.md#pdf-page-183) |
| 3.4.17.2 | →DADFWD24 (New CM7.0) | 184-184 | [p.184](syntax-2015-pages-181-200.md#pdf-page-184) |
| 3.4.18 | →DFWD20, DFWD23 and DFWD24 | 185-190 | [p.185](syntax-2015-pages-181-200.md#pdf-page-185) |
| 3.4.18.1 | →DFWD20 (New CM3.1) | 185-186 | [p.185](syntax-2015-pages-181-200.md#pdf-page-185) |
| 3.4.18.2 | →DFWD23 (New CM6.0) | 187-188 | [p.187](syntax-2015-pages-181-200.md#pdf-page-187) |
| 3.4.18.3 | →DFWD24 (New CM7.0) | 189-190 | [p.189](syntax-2015-pages-181-200.md#pdf-page-189) |
| 3.4.19 | →MBUSY20 and MBUSY24 | 191-191 | [p.191](syntax-2015-pages-181-200.md#pdf-page-191) |
| 3.4.19.1 | →MBUSY20 (New CM3.1) | 191-191 | [p.191](syntax-2015-pages-181-200.md#pdf-page-191) |
| 3.4.19.2 | →MBUSY24 (New CM7.0) | 191-191 | [p.191](syntax-2015-pages-181-200.md#pdf-page-191) |
| 3.4.20 | →FBUSY20 and FBUSY24 | 192-192 | [p.192](syntax-2015-pages-181-200.md#pdf-page-192) |
| 3.4.20.1 | →FBUSY20 (New CM3.1) | 192-192 | [p.192](syntax-2015-pages-181-200.md#pdf-page-192) |
| 3.4.20.2 | →FBUSY24 (New CM7.0) | 192-192 | [p.192](syntax-2015-pages-181-200.md#pdf-page-192) |
| 3.4.21 | →VSTART20 and VSTART24 | 193-193 | [p.193](syntax-2015-pages-181-200.md#pdf-page-193) |
| 3.4.21.1 | →VSTART20 (New CM3.1) | 193-193 | [p.193](syntax-2015-pages-181-200.md#pdf-page-193) |
| 3.4.21.2 | →VSTART24 (New CM7.0) | 193-193 | [p.193](syntax-2015-pages-181-200.md#pdf-page-193) |
| 3.4.22 | →VSTOP20 and VSTOP24 | 194-194 | [p.194](syntax-2015-pages-181-200.md#pdf-page-194) |
| 3.4.22.1 | →VSTOP20 (New CM3.1) | 194-194 | [p.194](syntax-2015-pages-181-200.md#pdf-page-194) |
| 3.4.22.2 | →VSTOP24 (New CM7.0) | 194-194 | [p.194](syntax-2015-pages-181-200.md#pdf-page-194) |
| 3.4.23 | →FDISC20 and FDISC24 | 195-196 | [p.195](syntax-2015-pages-181-200.md#pdf-page-195) |
| 3.4.23.1 | →FDISC20 (New CM3.1) | 195-195 | [p.195](syntax-2015-pages-181-200.md#pdf-page-195) |
| 3.4.23.2 | →FDISC24 (New CM7.0) | 196-196 | [p.196](syntax-2015-pages-181-200.md#pdf-page-196) |
| 3.4.24 | →HOLD20 and HOLD24 | 197-198 | [p.197](syntax-2015-pages-181-200.md#pdf-page-197) |
| 3.4.24.1 | →HOLD20 (New CM3.1) | 197-197 | [p.197](syntax-2015-pages-181-200.md#pdf-page-197) |
| 3.4.24.2 | →HOLD24 (New CM7.0) | 198-198 | [p.198](syntax-2015-pages-181-200.md#pdf-page-198) |
| 3.4.25 | →RECON20, RECON23 and RECON24 | 199-201 | [p.199](syntax-2015-pages-181-200.md#pdf-page-199) |
| 3.4.25.1 | →RECON20 (New CM3.1) | 199-199 | [p.199](syntax-2015-pages-181-200.md#pdf-page-199) |
| 3.4.25.2 | →RECON23 (New CM6.0) | 200-200 | [p.200](syntax-2015-pages-181-200.md#pdf-page-200) |
| 3.4.25.3 | →RECON24 (New CM7.0) | 201-201 | [p.201](syntax-2015-pages-201-220.md#pdf-page-201) |
| 3.4.26 | →COMP20 and COMP24 | 202-202 | [p.202](syntax-2015-pages-201-220.md#pdf-page-202) |
| 3.4.26.1 | →COMP20 (New CM3.1) | 202-202 | [p.202](syntax-2015-pages-201-220.md#pdf-page-202) |
| 3.4.26.2 | →COMP24 (New CM7.0) | 202-202 | [p.202](syntax-2015-pages-201-220.md#pdf-page-202) |
| 3.4.27 | →LOOKAH20 and LOOKAH24 | 203-203 | [p.203](syntax-2015-pages-201-220.md#pdf-page-203) |
| 3.4.27.1 | →LOOKAH20 (New CM3.1) | 203-203 | [p.203](syntax-2015-pages-201-220.md#pdf-page-203) |
| 3.4.27.2 | →LOOKAH24 (New CM7.0) | 203-203 | [p.203](syntax-2015-pages-201-220.md#pdf-page-203) |
| 3.4.28 | →AROUTE20 and AROUTE24 | 204-204 | [p.204](syntax-2015-pages-201-220.md#pdf-page-204) |
| 3.4.28.1 | →AROUTE20 (New CM3.1) | 204-204 | [p.204](syntax-2015-pages-201-220.md#pdf-page-204) |
| 3.4.28.2 | →AROUTE24 (New CM7.0) | 204-204 | [p.204](syntax-2015-pages-201-220.md#pdf-page-204) |
| 3.4.29 | →SKSTATE20 and SKSTATE23 | 205-206 | [p.205](syntax-2015-pages-201-220.md#pdf-page-205) |
| 3.4.29.1 | →SKSTATE20 (New CM3.1) | 205-205 | [p.205](syntax-2015-pages-201-220.md#pdf-page-205) |
| 3.4.29.2 | →SKSTATE23 (New CM6.0) | 206-206 | [p.206](syntax-2015-pages-201-220.md#pdf-page-206) |
| 3.4.30 | →ASA20 and ASA23 | 207-207 | [p.207](syntax-2015-pages-201-220.md#pdf-page-207) |
| 3.4.30.1 | →ASA20 (New CM3.1) | 207-207 | [p.207](syntax-2015-pages-201-220.md#pdf-page-207) |
| 3.4.30.2 | →ASA23 (New CM6.0) | 207-207 | [p.207](syntax-2015-pages-201-220.md#pdf-page-207) |
| 3.4.31 | →DNEVENT20 and DNEVENT24 | 208-209 | [p.208](syntax-2015-pages-201-220.md#pdf-page-208) |
| 3.4.31.1 | →DNEVENT20 (New CM3.1) | 208-208 | [p.208](syntax-2015-pages-201-220.md#pdf-page-208) |
| 3.4.31.2 | →DNEVENT24 (New CM7.0) | 209-209 | [p.209](syntax-2015-pages-201-220.md#pdf-page-209) |
| 3.4.32 | →MODEVENT20 (New CM3.1) | 210-210 | [p.210](syntax-2015-pages-201-220.md#pdf-page-210) |
| 3.4.33 | ←RAUDIT and RAUDIT24 | 211-212 | [p.211](syntax-2015-pages-201-220.md#pdf-page-211) |
| 3.4.33.1 | ←RAUDIT | 211-211 | [p.211](syntax-2015-pages-201-220.md#pdf-page-211) |
| 3.4.33.2 | ←RAUDIT24 (New CM7.0) | 212-212 | [p.212](syntax-2015-pages-201-220.md#pdf-page-212) |
| 3.4.34 | →TAUDIT20 and TAUDIT24 | 213-215 | [p.213](syntax-2015-pages-201-220.md#pdf-page-213) |
| 3.4.34.1 | →TAUDIT20 (New CM3.1) | 214-214 | [p.214](syntax-2015-pages-201-220.md#pdf-page-214) |
| 3.4.34.2 | →TAUDIT24 (New CM7.0) | 215-215 | [p.215](syntax-2015-pages-201-220.md#pdf-page-215) |
| 3.4.35 | → AUDAVAIL22, AUDAVAIL23 and AUDAVAIL24 | 216-218 | [p.216](syntax-2015-pages-201-220.md#pdf-page-216) |
| 3.4.35.1 | →AUDAVAIL22 (New CM5.2) | 216-216 | [p.216](syntax-2015-pages-201-220.md#pdf-page-216) |
| 3.4.35.2 | →AUDAVAIL23 (New CM6.0) | 217-217 | [p.217](syntax-2015-pages-201-220.md#pdf-page-217) |
| 3.4.35.3 | →AUDAVAIL24 (New CM7.0) | 218-218 | [p.218](syntax-2015-pages-201-220.md#pdf-page-218) |
| 3.4.36 | →AUDACD20, AUDACD23 and AUDACD24 | 219-221 | [p.219](syntax-2015-pages-201-220.md#pdf-page-219) |
| 3.4.36.1 | →AUDACD20 (New CM3.1) | 219-219 | [p.219](syntax-2015-pages-201-220.md#pdf-page-219) |
| 3.4.36.2 | →AUDACD23 (New CM6.0) | 220-220 | [p.220](syntax-2015-pages-201-220.md#pdf-page-220) |
| 3.4.36.3 | →AUDACD24 (New CM7.0) | 221-221 | [p.221](syntax-2015-pages-221-240.md#pdf-page-221) |
| 3.4.37 | →AUDACW20, AUDACW23 and AUDACW24 | 222-224 | [p.222](syntax-2015-pages-221-240.md#pdf-page-222) |
| 3.4.37.1 | →AUDACW20 (New CM3.1) | 222-222 | [p.222](syntax-2015-pages-221-240.md#pdf-page-222) |
| 3.4.37.2 | →AUDACW23 (New CM6.0) | 223-223 | [p.223](syntax-2015-pages-221-240.md#pdf-page-223) |
| 3.4.37.3 | →AUDACW24 (New CM7.0) | 224-224 | [p.224](syntax-2015-pages-221-240.md#pdf-page-224) |
| 3.4.38 | →AUDAUX20, AUDAUX23 and AUDAUX24 | 225-227 | [p.225](syntax-2015-pages-221-240.md#pdf-page-225) |
| 3.4.38.1 | →AUDAUX20 (New CM3.1) | 225-225 | [p.225](syntax-2015-pages-221-240.md#pdf-page-225) |
| 3.4.38.2 | →AUDAUX23 (New CM6.0) | 226-226 | [p.226](syntax-2015-pages-221-240.md#pdf-page-226) |
| 3.4.38.3 | →AUDAUX24 (New CM7.0) | 227-227 | [p.227](syntax-2015-pages-221-240.md#pdf-page-227) |
| 3.4.39 | → AUDOTHER22 and AUDOTHER24 | 228-229 | [p.228](syntax-2015-pages-221-240.md#pdf-page-228) |
| 3.4.39.1 | →AUDOTHER22 (New CM5.2) | 228-228 | [p.228](syntax-2015-pages-221-240.md#pdf-page-228) |
| 3.4.39.2 | →AUDOTHER24 (New CM7.0) | 229-229 | [p.229](syntax-2015-pages-221-240.md#pdf-page-229) |
| 3.4.40 | →AUDUNSTF20 and AUDUNSTF24 | 230-230 | [p.230](syntax-2015-pages-221-240.md#pdf-page-230) |
| 3.4.40.1 | →AUDUNSTF20 (New CM3.1) | 230-230 | [p.230](syntax-2015-pages-221-240.md#pdf-page-230) |
| 3.4.40.2 | →AUDUNSTF24 (New CM7.0) | 230-230 | [p.230](syntax-2015-pages-221-240.md#pdf-page-230) |
| 3.4.41 | →EWTAUDIT20 and EWTAUDIT23 | 231-232 | [p.231](syntax-2015-pages-221-240.md#pdf-page-231) |
| 3.4.41.1 | →EWTAUDIT20 (New CM3.1) | 231-231 | [p.231](syntax-2015-pages-221-240.md#pdf-page-231) |
| 3.4.41.2 | →EWTAUDIT23 (New CM6.0) | 232-232 | [p.232](syntax-2015-pages-221-240.md#pdf-page-232) |
| 3.4.42 | →VAUDIT20 (New CM3.1) | 233-233 | [p.233](syntax-2015-pages-221-240.md#pdf-page-233) |
| 3.4.43 | →XFER20 and XFER24 | 234-237 | [p.234](syntax-2015-pages-221-240.md#pdf-page-234) |
| 3.4.43.1 | →XFER20 (New CM3.1) | 234-235 | [p.234](syntax-2015-pages-221-240.md#pdf-page-234) |
| 3.4.43.2 | →XFER24 (New CM7.0) | 236-237 | [p.236](syntax-2015-pages-221-240.md#pdf-page-236) |
| 3.4.44 | ← CPERROR7 and CPERROR24 | 238-238 | [p.238](syntax-2015-pages-221-240.md#pdf-page-238) |
| 3.4.44.1 | ←CPERROR7 | 238-238 | [p.238](syntax-2015-pages-221-240.md#pdf-page-238) |
| 3.4.44.2 | ←CPERROR24 (New CM7.0) | 238-238 | [p.238](syntax-2015-pages-221-240.md#pdf-page-238) |
| 3.5 | Miscellaneous | 239-239 | [p.239](syntax-2015-pages-221-240.md#pdf-page-239) |
| 3.5.1 | ←NOP | 239-239 | [p.239](syntax-2015-pages-221-240.md#pdf-page-239) |
| 4 | Message Index | 240-249 | [p.240](syntax-2015-pages-221-240.md#pdf-page-240) |
| 4.1 | Alphabetical List | 240-249 | [p.240](syntax-2015-pages-221-240.md#pdf-page-240) |
| 5 | Virtual trunk mapping | 250-251 | [p.250](syntax-2015-pages-241-253.md#pdf-page-250) |
| REFERENCES | REFERENCES | 252-253 | [p.252](syntax-2015-pages-241-253.md#pdf-page-252) |
| FIGURE-1 | Data Communication Protocol Layers | 19-19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) |
| VECTOR-GOTO-CONDITIONS | Goto Step/Goto Vector conditions, thresholds, formats, comparators and variable/digit layouts | 98-108 | [p.98](syntax-2015-pages-081-100.md#pdf-page-098) |
| TABLE-1 | Reporting Adjunct to Switch Messages - Alphabetical List | 240-240 | [p.240](syntax-2015-pages-221-240.md#pdf-page-240) |
| TABLE-2 | Switch to Reporting Adjunct Messages - Alphabetical List | 241-243 | [p.241](syntax-2015-pages-241-253.md#pdf-page-241) |
| TABLE-3 | Reporting Adjunct to Switch Messages - Opcode List | 245-245 | [p.245](syntax-2015-pages-241-253.md#pdf-page-245) |
| TABLE-4 | Switch to Reporting Adjunct Messages - Opcode List | 246-249 | [p.246](syntax-2015-pages-241-253.md#pdf-page-246) |
| TABLE-5 | Virtual Trunk Mapping formulas/examples/continuation | 250-251 | [p.250](syntax-2015-pages-241-253.md#pdf-page-250) |
| ERROR-CODE-TABLES | RCODE/CRCODE administration return-code and count tables | 131-135 | [p.131](syntax-2015-pages-121-140.md#pdf-page-131) |

## CM6 plan: complete section map

| Section | Title | Source pages | First page text |
|---|---|---|---|
| 1 | Introduction | 1-1 | [p.1](cm6-enhancements-pages-001-014.md#pdf-page-001) |
| 1.1 | Document Updates | 1-1 | [p.1](cm6-enhancements-pages-001-014.md#pdf-page-001) |
| 2 | Document References | 1-2 | [p.1](cm6-enhancements-pages-001-014.md#pdf-page-001) |
| 2.1 | Source Documents | 1-2 | [p.1](cm6-enhancements-pages-001-014.md#pdf-page-001) |
| 2.2 | Related Documents | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 3 | Scope | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 4 | Terminology | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 5 | Lab System Configuration | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 6 | Special Software/Firmware Needed | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 7 | Administration Required | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 8 | Test Case Format | 2-2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) |
| 9 | Test Cases | 3-20 | [p.3](cm6-enhancements-pages-001-014.md#pdf-page-003) |
| 9.1 | SPI Protocol changes for language 23 [RG] | 4-5 | [p.4](cm6-enhancements-pages-001-014.md#pdf-page-004) |
| 9.2 | SPI Protocol changes for Interruptible Aux [RG] | 6-13 | [p.6](cm6-enhancements-pages-001-014.md#pdf-page-006) |
| 9.2.1 | AVAIL & AUDAVAIL | 6-7 | [p.6](cm6-enhancements-pages-001-014.md#pdf-page-006) |
| 9.2.2 | AUX & AUDAUX | 7-7 | [p.7](cm6-enhancements-pages-001-014.md#pdf-page-007) |
| 9.2.3 | AEVENT | 7-10 | [p.7](cm6-enhancements-pages-001-014.md#pdf-page-007) |
| 9.2.4 | AGENTSK | 10-10 | [p.10](cm6-enhancements-pages-001-014.md#pdf-page-010) |
| 9.2.5 | ALOGON | 10-10 | [p.10](cm6-enhancements-pages-001-014.md#pdf-page-010) |
| 9.2.6 | SKILLADD | 10-12 | [p.10](cm6-enhancements-pages-001-014.md#pdf-page-010) |
| 9.2.7 | MVAGSTFD | 12-13 | [p.12](cm6-enhancements-pages-001-014.md#pdf-page-012) |
| 9.3 | SPI Protocol changes for Route Calls by Skill Level [RG] | 14-17 | [p.14](cm6-enhancements-pages-001-014.md#pdf-page-014) |
| 9.3.1 | DCON | 14-15 | [p.14](cm6-enhancements-pages-001-014.md#pdf-page-014) |
| 9.3.2 | VECTOR | 15-15 | [p.15](cm6-enhancements-pages-015-028.md#pdf-page-015) |
| 9.3.3 | CHGVEC | 15-16 | [p.15](cm6-enhancements-pages-015-028.md#pdf-page-015) |
| 9.3.4 | VPARMS | 16-17 | [p.16](cm6-enhancements-pages-015-028.md#pdf-page-016) |
| 9.3.5 | CHVEC20 (source heading spelling) | 17-17 | [p.17](cm6-enhancements-pages-015-028.md#pdf-page-017) |
| 9.4 | SPI Protocol changes for increased # of skills per agent [GMU] | 18-19 | [p.18](cm6-enhancements-pages-015-028.md#pdf-page-018) |
| 9.4.1 | AGENTSK | 18-18 | [p.18](cm6-enhancements-pages-015-028.md#pdf-page-018) |
| 9.4.2 | SKILLADD | 18-18 | [p.18](cm6-enhancements-pages-015-028.md#pdf-page-018) |
| 9.4.3 | ALOGON | 19-19 | [p.19](cm6-enhancements-pages-015-028.md#pdf-page-019) |
| 9.4.4 | AVAIL, AUDAVAIL, AUDACW, AUDAUX | 19-19 | [p.19](cm6-enhancements-pages-015-028.md#pdf-page-019) |
| 9.5 | SPI Protocol changes for Percent Allocation Routing [GMU] | 20-20 | [p.20](cm6-enhancements-pages-015-028.md#pdf-page-020) |
| 9.5.1 | DFWD | 20-20 | [p.20](cm6-enhancements-pages-015-028.md#pdf-page-020) |
| 10 | Notes | 21-21 | [p.21](cm6-enhancements-pages-015-028.md#pdf-page-021) |
| references | References (unnumbered heading) | 22-22 | [p.22](cm6-enhancements-pages-015-028.md#pdf-page-022) |
| toc | Table of Contents | 23-23 | [p.23](cm6-enhancements-pages-015-028.md#pdf-page-023) |
| blank | Intervening blank page | 24-24 | [p.24](cm6-enhancements-pages-015-028.md#pdf-page-024) |
| test-index | Table of Test Cases | 25-28 | [p.25](cm6-enhancements-pages-015-028.md#pdf-page-025) |

## Every physical page

| Source | Page | Text companion | Text status |
|---|---|---|---|
| SPI-SYN24 | 1 | [p.1](syntax-2015-pages-001-020.md#pdf-page-001) | Full extracted source span retained |
| SPI-SYN24 | 2 | [p.2](syntax-2015-pages-001-020.md#pdf-page-002) | Full extracted source span retained |
| SPI-SYN24 | 3 | [p.3](syntax-2015-pages-001-020.md#pdf-page-003) | Full extracted source span retained |
| SPI-SYN24 | 4 | [p.4](syntax-2015-pages-001-020.md#pdf-page-004) | Full extracted source span retained |
| SPI-SYN24 | 5 | [p.5](syntax-2015-pages-001-020.md#pdf-page-005) | Full extracted source span retained |
| SPI-SYN24 | 6 | [p.6](syntax-2015-pages-001-020.md#pdf-page-006) | Full extracted source span retained |
| SPI-SYN24 | 7 | [p.7](syntax-2015-pages-001-020.md#pdf-page-007) | Full extracted source span retained |
| SPI-SYN24 | 8 | [p.8](syntax-2015-pages-001-020.md#pdf-page-008) | Full extracted source span retained |
| SPI-SYN24 | 9 | [p.9](syntax-2015-pages-001-020.md#pdf-page-009) | Full extracted source span retained |
| SPI-SYN24 | 10 | [p.10](syntax-2015-pages-001-020.md#pdf-page-010) | Full extracted source span retained |
| SPI-SYN24 | 11 | [p.11](syntax-2015-pages-001-020.md#pdf-page-011) | Full extracted source span retained |
| SPI-SYN24 | 12 | [p.12](syntax-2015-pages-001-020.md#pdf-page-012) | Full extracted source span retained |
| SPI-SYN24 | 13 | [p.13](syntax-2015-pages-001-020.md#pdf-page-013) | Full extracted source span retained |
| SPI-SYN24 | 14 | [p.14](syntax-2015-pages-001-020.md#pdf-page-014) | Full extracted source span retained |
| SPI-SYN24 | 15 | [p.15](syntax-2015-pages-001-020.md#pdf-page-015) | Full extracted source span retained |
| SPI-SYN24 | 16 | [p.16](syntax-2015-pages-001-020.md#pdf-page-016) | Full extracted source span retained |
| SPI-SYN24 | 17 | [p.17](syntax-2015-pages-001-020.md#pdf-page-017) | Full extracted source span retained |
| SPI-SYN24 | 18 | [p.18](syntax-2015-pages-001-020.md#pdf-page-018) | Full extracted source span retained |
| SPI-SYN24 | 19 | [p.19](syntax-2015-pages-001-020.md#pdf-page-019) | Full extracted source span retained |
| SPI-SYN24 | 20 | [p.20](syntax-2015-pages-001-020.md#pdf-page-020) | Full extracted source span retained |
| SPI-SYN24 | 21 | [p.21](syntax-2015-pages-021-040.md#pdf-page-021) | Full extracted source span retained |
| SPI-SYN24 | 22 | [p.22](syntax-2015-pages-021-040.md#pdf-page-022) | Full extracted source span retained |
| SPI-SYN24 | 23 | [p.23](syntax-2015-pages-021-040.md#pdf-page-023) | Full extracted source span retained |
| SPI-SYN24 | 24 | [p.24](syntax-2015-pages-021-040.md#pdf-page-024) | Full extracted source span retained |
| SPI-SYN24 | 25 | [p.25](syntax-2015-pages-021-040.md#pdf-page-025) | Full extracted source span retained |
| SPI-SYN24 | 26 | [p.26](syntax-2015-pages-021-040.md#pdf-page-026) | Full extracted source span retained |
| SPI-SYN24 | 27 | [p.27](syntax-2015-pages-021-040.md#pdf-page-027) | Full extracted source span retained |
| SPI-SYN24 | 28 | [p.28](syntax-2015-pages-021-040.md#pdf-page-028) | Full extracted source span retained |
| SPI-SYN24 | 29 | [p.29](syntax-2015-pages-021-040.md#pdf-page-029) | Full extracted source span retained |
| SPI-SYN24 | 30 | [p.30](syntax-2015-pages-021-040.md#pdf-page-030) | Full extracted source span retained |
| SPI-SYN24 | 31 | [p.31](syntax-2015-pages-021-040.md#pdf-page-031) | Full extracted source span retained |
| SPI-SYN24 | 32 | [p.32](syntax-2015-pages-021-040.md#pdf-page-032) | Full extracted source span retained |
| SPI-SYN24 | 33 | [p.33](syntax-2015-pages-021-040.md#pdf-page-033) | Full extracted source span retained |
| SPI-SYN24 | 34 | [p.34](syntax-2015-pages-021-040.md#pdf-page-034) | Full extracted source span retained |
| SPI-SYN24 | 35 | [p.35](syntax-2015-pages-021-040.md#pdf-page-035) | Full extracted source span retained |
| SPI-SYN24 | 36 | [p.36](syntax-2015-pages-021-040.md#pdf-page-036) | Full extracted source span retained |
| SPI-SYN24 | 37 | [p.37](syntax-2015-pages-021-040.md#pdf-page-037) | Full extracted source span retained |
| SPI-SYN24 | 38 | [p.38](syntax-2015-pages-021-040.md#pdf-page-038) | Full extracted source span retained |
| SPI-SYN24 | 39 | [p.39](syntax-2015-pages-021-040.md#pdf-page-039) | Full extracted source span retained |
| SPI-SYN24 | 40 | [p.40](syntax-2015-pages-021-040.md#pdf-page-040) | Full extracted source span retained |
| SPI-SYN24 | 41 | [p.41](syntax-2015-pages-041-060.md#pdf-page-041) | Full extracted source span retained |
| SPI-SYN24 | 42 | [p.42](syntax-2015-pages-041-060.md#pdf-page-042) | Full extracted source span retained |
| SPI-SYN24 | 43 | [p.43](syntax-2015-pages-041-060.md#pdf-page-043) | Full extracted source span retained |
| SPI-SYN24 | 44 | [p.44](syntax-2015-pages-041-060.md#pdf-page-044) | Full extracted source span retained |
| SPI-SYN24 | 45 | [p.45](syntax-2015-pages-041-060.md#pdf-page-045) | Full extracted source span retained |
| SPI-SYN24 | 46 | [p.46](syntax-2015-pages-041-060.md#pdf-page-046) | Full extracted source span retained |
| SPI-SYN24 | 47 | [p.47](syntax-2015-pages-041-060.md#pdf-page-047) | Full extracted source span retained |
| SPI-SYN24 | 48 | [p.48](syntax-2015-pages-041-060.md#pdf-page-048) | Full extracted source span retained |
| SPI-SYN24 | 49 | [p.49](syntax-2015-pages-041-060.md#pdf-page-049) | Full extracted source span retained |
| SPI-SYN24 | 50 | [p.50](syntax-2015-pages-041-060.md#pdf-page-050) | Full extracted source span retained |
| SPI-SYN24 | 51 | [p.51](syntax-2015-pages-041-060.md#pdf-page-051) | Full extracted source span retained |
| SPI-SYN24 | 52 | [p.52](syntax-2015-pages-041-060.md#pdf-page-052) | Full extracted source span retained |
| SPI-SYN24 | 53 | [p.53](syntax-2015-pages-041-060.md#pdf-page-053) | Full extracted source span retained |
| SPI-SYN24 | 54 | [p.54](syntax-2015-pages-041-060.md#pdf-page-054) | Full extracted source span retained |
| SPI-SYN24 | 55 | [p.55](syntax-2015-pages-041-060.md#pdf-page-055) | Full extracted source span retained |
| SPI-SYN24 | 56 | [p.56](syntax-2015-pages-041-060.md#pdf-page-056) | Full extracted source span retained |
| SPI-SYN24 | 57 | [p.57](syntax-2015-pages-041-060.md#pdf-page-057) | Full extracted source span retained |
| SPI-SYN24 | 58 | [p.58](syntax-2015-pages-041-060.md#pdf-page-058) | Full extracted source span retained |
| SPI-SYN24 | 59 | [p.59](syntax-2015-pages-041-060.md#pdf-page-059) | Full extracted source span retained |
| SPI-SYN24 | 60 | [p.60](syntax-2015-pages-041-060.md#pdf-page-060) | Full extracted source span retained |
| SPI-SYN24 | 61 | [p.61](syntax-2015-pages-061-080.md#pdf-page-061) | Full extracted source span retained |
| SPI-SYN24 | 62 | [p.62](syntax-2015-pages-061-080.md#pdf-page-062) | Full extracted source span retained |
| SPI-SYN24 | 63 | [p.63](syntax-2015-pages-061-080.md#pdf-page-063) | Full extracted source span retained |
| SPI-SYN24 | 64 | [p.64](syntax-2015-pages-061-080.md#pdf-page-064) | Full extracted source span retained |
| SPI-SYN24 | 65 | [p.65](syntax-2015-pages-061-080.md#pdf-page-065) | Full extracted source span retained |
| SPI-SYN24 | 66 | [p.66](syntax-2015-pages-061-080.md#pdf-page-066) | Full extracted source span retained |
| SPI-SYN24 | 67 | [p.67](syntax-2015-pages-061-080.md#pdf-page-067) | Full extracted source span retained |
| SPI-SYN24 | 68 | [p.68](syntax-2015-pages-061-080.md#pdf-page-068) | Full extracted source span retained |
| SPI-SYN24 | 69 | [p.69](syntax-2015-pages-061-080.md#pdf-page-069) | Full extracted source span retained |
| SPI-SYN24 | 70 | [p.70](syntax-2015-pages-061-080.md#pdf-page-070) | Full extracted source span retained |
| SPI-SYN24 | 71 | [p.71](syntax-2015-pages-061-080.md#pdf-page-071) | Full extracted source span retained |
| SPI-SYN24 | 72 | [p.72](syntax-2015-pages-061-080.md#pdf-page-072) | Full extracted source span retained |
| SPI-SYN24 | 73 | [p.73](syntax-2015-pages-061-080.md#pdf-page-073) | Full extracted source span retained |
| SPI-SYN24 | 74 | [p.74](syntax-2015-pages-061-080.md#pdf-page-074) | Full extracted source span retained |
| SPI-SYN24 | 75 | [p.75](syntax-2015-pages-061-080.md#pdf-page-075) | Full extracted source span retained |
| SPI-SYN24 | 76 | [p.76](syntax-2015-pages-061-080.md#pdf-page-076) | Full extracted source span retained |
| SPI-SYN24 | 77 | [p.77](syntax-2015-pages-061-080.md#pdf-page-077) | Full extracted source span retained |
| SPI-SYN24 | 78 | [p.78](syntax-2015-pages-061-080.md#pdf-page-078) | Full extracted source span retained |
| SPI-SYN24 | 79 | [p.79](syntax-2015-pages-061-080.md#pdf-page-079) | Full extracted source span retained |
| SPI-SYN24 | 80 | [p.80](syntax-2015-pages-061-080.md#pdf-page-080) | Full extracted source span retained |
| SPI-SYN24 | 81 | [p.81](syntax-2015-pages-081-100.md#pdf-page-081) | Full extracted source span retained |
| SPI-SYN24 | 82 | [p.82](syntax-2015-pages-081-100.md#pdf-page-082) | Full extracted source span retained |
| SPI-SYN24 | 83 | [p.83](syntax-2015-pages-081-100.md#pdf-page-083) | Full extracted source span retained |
| SPI-SYN24 | 84 | [p.84](syntax-2015-pages-081-100.md#pdf-page-084) | Full extracted source span retained |
| SPI-SYN24 | 85 | [p.85](syntax-2015-pages-081-100.md#pdf-page-085) | Full extracted source span retained |
| SPI-SYN24 | 86 | [p.86](syntax-2015-pages-081-100.md#pdf-page-086) | Full extracted source span retained |
| SPI-SYN24 | 87 | [p.87](syntax-2015-pages-081-100.md#pdf-page-087) | Full extracted source span retained |
| SPI-SYN24 | 88 | [p.88](syntax-2015-pages-081-100.md#pdf-page-088) | Full extracted source span retained |
| SPI-SYN24 | 89 | [p.89](syntax-2015-pages-081-100.md#pdf-page-089) | Full extracted source span retained |
| SPI-SYN24 | 90 | [p.90](syntax-2015-pages-081-100.md#pdf-page-090) | Full extracted source span retained |
| SPI-SYN24 | 91 | [p.91](syntax-2015-pages-081-100.md#pdf-page-091) | Full extracted source span retained |
| SPI-SYN24 | 92 | [p.92](syntax-2015-pages-081-100.md#pdf-page-092) | Full extracted source span retained |
| SPI-SYN24 | 93 | [p.93](syntax-2015-pages-081-100.md#pdf-page-093) | Full extracted source span retained |
| SPI-SYN24 | 94 | [p.94](syntax-2015-pages-081-100.md#pdf-page-094) | Full extracted source span retained |
| SPI-SYN24 | 95 | [p.95](syntax-2015-pages-081-100.md#pdf-page-095) | Full extracted source span retained |
| SPI-SYN24 | 96 | [p.96](syntax-2015-pages-081-100.md#pdf-page-096) | Full extracted source span retained |
| SPI-SYN24 | 97 | [p.97](syntax-2015-pages-081-100.md#pdf-page-097) | Full extracted source span retained |
| SPI-SYN24 | 98 | [p.98](syntax-2015-pages-081-100.md#pdf-page-098) | Full extracted source span retained |
| SPI-SYN24 | 99 | [p.99](syntax-2015-pages-081-100.md#pdf-page-099) | Full extracted source span retained |
| SPI-SYN24 | 100 | [p.100](syntax-2015-pages-081-100.md#pdf-page-100) | Full extracted source span retained |
| SPI-SYN24 | 101 | [p.101](syntax-2015-pages-101-120.md#pdf-page-101) | Full extracted source span retained |
| SPI-SYN24 | 102 | [p.102](syntax-2015-pages-101-120.md#pdf-page-102) | Full extracted source span retained |
| SPI-SYN24 | 103 | [p.103](syntax-2015-pages-101-120.md#pdf-page-103) | Full extracted source span retained |
| SPI-SYN24 | 104 | [p.104](syntax-2015-pages-101-120.md#pdf-page-104) | Full extracted source span retained |
| SPI-SYN24 | 105 | [p.105](syntax-2015-pages-101-120.md#pdf-page-105) | Full extracted source span retained |
| SPI-SYN24 | 106 | [p.106](syntax-2015-pages-101-120.md#pdf-page-106) | Full extracted source span retained |
| SPI-SYN24 | 107 | [p.107](syntax-2015-pages-101-120.md#pdf-page-107) | Full extracted source span retained |
| SPI-SYN24 | 108 | [p.108](syntax-2015-pages-101-120.md#pdf-page-108) | Full extracted source span retained |
| SPI-SYN24 | 109 | [p.109](syntax-2015-pages-101-120.md#pdf-page-109) | Full extracted source span retained |
| SPI-SYN24 | 110 | [p.110](syntax-2015-pages-101-120.md#pdf-page-110) | Full extracted source span retained |
| SPI-SYN24 | 111 | [p.111](syntax-2015-pages-101-120.md#pdf-page-111) | Full extracted source span retained |
| SPI-SYN24 | 112 | [p.112](syntax-2015-pages-101-120.md#pdf-page-112) | Full extracted source span retained |
| SPI-SYN24 | 113 | [p.113](syntax-2015-pages-101-120.md#pdf-page-113) | Full extracted source span retained |
| SPI-SYN24 | 114 | [p.114](syntax-2015-pages-101-120.md#pdf-page-114) | Full extracted source span retained |
| SPI-SYN24 | 115 | [p.115](syntax-2015-pages-101-120.md#pdf-page-115) | Full extracted source span retained |
| SPI-SYN24 | 116 | [p.116](syntax-2015-pages-101-120.md#pdf-page-116) | Full extracted source span retained |
| SPI-SYN24 | 117 | [p.117](syntax-2015-pages-101-120.md#pdf-page-117) | Full extracted source span retained |
| SPI-SYN24 | 118 | [p.118](syntax-2015-pages-101-120.md#pdf-page-118) | Full extracted source span retained |
| SPI-SYN24 | 119 | [p.119](syntax-2015-pages-101-120.md#pdf-page-119) | Full extracted source span retained |
| SPI-SYN24 | 120 | [p.120](syntax-2015-pages-101-120.md#pdf-page-120) | Full extracted source span retained |
| SPI-SYN24 | 121 | [p.121](syntax-2015-pages-121-140.md#pdf-page-121) | Full extracted source span retained |
| SPI-SYN24 | 122 | [p.122](syntax-2015-pages-121-140.md#pdf-page-122) | Full extracted source span retained |
| SPI-SYN24 | 123 | [p.123](syntax-2015-pages-121-140.md#pdf-page-123) | Full extracted source span retained |
| SPI-SYN24 | 124 | [p.124](syntax-2015-pages-121-140.md#pdf-page-124) | Full extracted source span retained |
| SPI-SYN24 | 125 | [p.125](syntax-2015-pages-121-140.md#pdf-page-125) | Full extracted source span retained |
| SPI-SYN24 | 126 | [p.126](syntax-2015-pages-121-140.md#pdf-page-126) | Full extracted source span retained |
| SPI-SYN24 | 127 | [p.127](syntax-2015-pages-121-140.md#pdf-page-127) | Full extracted source span retained |
| SPI-SYN24 | 128 | [p.128](syntax-2015-pages-121-140.md#pdf-page-128) | Full extracted source span retained |
| SPI-SYN24 | 129 | [p.129](syntax-2015-pages-121-140.md#pdf-page-129) | Full extracted source span retained |
| SPI-SYN24 | 130 | [p.130](syntax-2015-pages-121-140.md#pdf-page-130) | Full extracted source span retained |
| SPI-SYN24 | 131 | [p.131](syntax-2015-pages-121-140.md#pdf-page-131) | Full extracted source span retained |
| SPI-SYN24 | 132 | [p.132](syntax-2015-pages-121-140.md#pdf-page-132) | Full extracted source span retained |
| SPI-SYN24 | 133 | [p.133](syntax-2015-pages-121-140.md#pdf-page-133) | Full extracted source span retained |
| SPI-SYN24 | 134 | [p.134](syntax-2015-pages-121-140.md#pdf-page-134) | Full extracted source span retained |
| SPI-SYN24 | 135 | [p.135](syntax-2015-pages-121-140.md#pdf-page-135) | Full extracted source span retained |
| SPI-SYN24 | 136 | [p.136](syntax-2015-pages-121-140.md#pdf-page-136) | Full extracted source span retained |
| SPI-SYN24 | 137 | [p.137](syntax-2015-pages-121-140.md#pdf-page-137) | Full extracted source span retained |
| SPI-SYN24 | 138 | [p.138](syntax-2015-pages-121-140.md#pdf-page-138) | Full extracted source span retained |
| SPI-SYN24 | 139 | [p.139](syntax-2015-pages-121-140.md#pdf-page-139) | Full extracted source span retained |
| SPI-SYN24 | 140 | [p.140](syntax-2015-pages-121-140.md#pdf-page-140) | Full extracted source span retained |
| SPI-SYN24 | 141 | [p.141](syntax-2015-pages-141-160.md#pdf-page-141) | Full extracted source span retained |
| SPI-SYN24 | 142 | [p.142](syntax-2015-pages-141-160.md#pdf-page-142) | Full extracted source span retained |
| SPI-SYN24 | 143 | [p.143](syntax-2015-pages-141-160.md#pdf-page-143) | Full extracted source span retained |
| SPI-SYN24 | 144 | [p.144](syntax-2015-pages-141-160.md#pdf-page-144) | Full extracted source span retained |
| SPI-SYN24 | 145 | [p.145](syntax-2015-pages-141-160.md#pdf-page-145) | Full extracted source span retained |
| SPI-SYN24 | 146 | [p.146](syntax-2015-pages-141-160.md#pdf-page-146) | Full extracted source span retained |
| SPI-SYN24 | 147 | [p.147](syntax-2015-pages-141-160.md#pdf-page-147) | Full extracted source span retained |
| SPI-SYN24 | 148 | [p.148](syntax-2015-pages-141-160.md#pdf-page-148) | Full extracted source span retained |
| SPI-SYN24 | 149 | [p.149](syntax-2015-pages-141-160.md#pdf-page-149) | Full extracted source span retained |
| SPI-SYN24 | 150 | [p.150](syntax-2015-pages-141-160.md#pdf-page-150) | Full extracted source span retained |
| SPI-SYN24 | 151 | [p.151](syntax-2015-pages-141-160.md#pdf-page-151) | Full extracted source span retained |
| SPI-SYN24 | 152 | [p.152](syntax-2015-pages-141-160.md#pdf-page-152) | Full extracted source span retained |
| SPI-SYN24 | 153 | [p.153](syntax-2015-pages-141-160.md#pdf-page-153) | Full extracted source span retained |
| SPI-SYN24 | 154 | [p.154](syntax-2015-pages-141-160.md#pdf-page-154) | Full extracted source span retained |
| SPI-SYN24 | 155 | [p.155](syntax-2015-pages-141-160.md#pdf-page-155) | Full extracted source span retained |
| SPI-SYN24 | 156 | [p.156](syntax-2015-pages-141-160.md#pdf-page-156) | Full extracted source span retained |
| SPI-SYN24 | 157 | [p.157](syntax-2015-pages-141-160.md#pdf-page-157) | Full extracted source span retained |
| SPI-SYN24 | 158 | [p.158](syntax-2015-pages-141-160.md#pdf-page-158) | Full extracted source span retained |
| SPI-SYN24 | 159 | [p.159](syntax-2015-pages-141-160.md#pdf-page-159) | Full extracted source span retained |
| SPI-SYN24 | 160 | [p.160](syntax-2015-pages-141-160.md#pdf-page-160) | Full extracted source span retained |
| SPI-SYN24 | 161 | [p.161](syntax-2015-pages-161-180.md#pdf-page-161) | Full extracted source span retained |
| SPI-SYN24 | 162 | [p.162](syntax-2015-pages-161-180.md#pdf-page-162) | Full extracted source span retained |
| SPI-SYN24 | 163 | [p.163](syntax-2015-pages-161-180.md#pdf-page-163) | Full extracted source span retained |
| SPI-SYN24 | 164 | [p.164](syntax-2015-pages-161-180.md#pdf-page-164) | Full extracted source span retained |
| SPI-SYN24 | 165 | [p.165](syntax-2015-pages-161-180.md#pdf-page-165) | Full extracted source span retained |
| SPI-SYN24 | 166 | [p.166](syntax-2015-pages-161-180.md#pdf-page-166) | Full extracted source span retained |
| SPI-SYN24 | 167 | [p.167](syntax-2015-pages-161-180.md#pdf-page-167) | Full extracted source span retained |
| SPI-SYN24 | 168 | [p.168](syntax-2015-pages-161-180.md#pdf-page-168) | Full extracted source span retained |
| SPI-SYN24 | 169 | [p.169](syntax-2015-pages-161-180.md#pdf-page-169) | Full extracted source span retained |
| SPI-SYN24 | 170 | [p.170](syntax-2015-pages-161-180.md#pdf-page-170) | Full extracted source span retained |
| SPI-SYN24 | 171 | [p.171](syntax-2015-pages-161-180.md#pdf-page-171) | Full extracted source span retained |
| SPI-SYN24 | 172 | [p.172](syntax-2015-pages-161-180.md#pdf-page-172) | Full extracted source span retained |
| SPI-SYN24 | 173 | [p.173](syntax-2015-pages-161-180.md#pdf-page-173) | Full extracted source span retained |
| SPI-SYN24 | 174 | [p.174](syntax-2015-pages-161-180.md#pdf-page-174) | Full extracted source span retained |
| SPI-SYN24 | 175 | [p.175](syntax-2015-pages-161-180.md#pdf-page-175) | Full extracted source span retained |
| SPI-SYN24 | 176 | [p.176](syntax-2015-pages-161-180.md#pdf-page-176) | Full extracted source span retained |
| SPI-SYN24 | 177 | [p.177](syntax-2015-pages-161-180.md#pdf-page-177) | Full extracted source span retained |
| SPI-SYN24 | 178 | [p.178](syntax-2015-pages-161-180.md#pdf-page-178) | Full extracted source span retained |
| SPI-SYN24 | 179 | [p.179](syntax-2015-pages-161-180.md#pdf-page-179) | Full extracted source span retained |
| SPI-SYN24 | 180 | [p.180](syntax-2015-pages-161-180.md#pdf-page-180) | Full extracted source span retained |
| SPI-SYN24 | 181 | [p.181](syntax-2015-pages-181-200.md#pdf-page-181) | Full extracted source span retained |
| SPI-SYN24 | 182 | [p.182](syntax-2015-pages-181-200.md#pdf-page-182) | Full extracted source span retained |
| SPI-SYN24 | 183 | [p.183](syntax-2015-pages-181-200.md#pdf-page-183) | Full extracted source span retained |
| SPI-SYN24 | 184 | [p.184](syntax-2015-pages-181-200.md#pdf-page-184) | Full extracted source span retained |
| SPI-SYN24 | 185 | [p.185](syntax-2015-pages-181-200.md#pdf-page-185) | Full extracted source span retained |
| SPI-SYN24 | 186 | [p.186](syntax-2015-pages-181-200.md#pdf-page-186) | Full extracted source span retained |
| SPI-SYN24 | 187 | [p.187](syntax-2015-pages-181-200.md#pdf-page-187) | Full extracted source span retained |
| SPI-SYN24 | 188 | [p.188](syntax-2015-pages-181-200.md#pdf-page-188) | Full extracted source span retained |
| SPI-SYN24 | 189 | [p.189](syntax-2015-pages-181-200.md#pdf-page-189) | Full extracted source span retained |
| SPI-SYN24 | 190 | [p.190](syntax-2015-pages-181-200.md#pdf-page-190) | Full extracted source span retained |
| SPI-SYN24 | 191 | [p.191](syntax-2015-pages-181-200.md#pdf-page-191) | Full extracted source span retained |
| SPI-SYN24 | 192 | [p.192](syntax-2015-pages-181-200.md#pdf-page-192) | Full extracted source span retained |
| SPI-SYN24 | 193 | [p.193](syntax-2015-pages-181-200.md#pdf-page-193) | Full extracted source span retained |
| SPI-SYN24 | 194 | [p.194](syntax-2015-pages-181-200.md#pdf-page-194) | Full extracted source span retained |
| SPI-SYN24 | 195 | [p.195](syntax-2015-pages-181-200.md#pdf-page-195) | Full extracted source span retained |
| SPI-SYN24 | 196 | [p.196](syntax-2015-pages-181-200.md#pdf-page-196) | Full extracted source span retained |
| SPI-SYN24 | 197 | [p.197](syntax-2015-pages-181-200.md#pdf-page-197) | Full extracted source span retained |
| SPI-SYN24 | 198 | [p.198](syntax-2015-pages-181-200.md#pdf-page-198) | Full extracted source span retained |
| SPI-SYN24 | 199 | [p.199](syntax-2015-pages-181-200.md#pdf-page-199) | Full extracted source span retained |
| SPI-SYN24 | 200 | [p.200](syntax-2015-pages-181-200.md#pdf-page-200) | Full extracted source span retained |
| SPI-SYN24 | 201 | [p.201](syntax-2015-pages-201-220.md#pdf-page-201) | Full extracted source span retained |
| SPI-SYN24 | 202 | [p.202](syntax-2015-pages-201-220.md#pdf-page-202) | Full extracted source span retained |
| SPI-SYN24 | 203 | [p.203](syntax-2015-pages-201-220.md#pdf-page-203) | Full extracted source span retained |
| SPI-SYN24 | 204 | [p.204](syntax-2015-pages-201-220.md#pdf-page-204) | Full extracted source span retained |
| SPI-SYN24 | 205 | [p.205](syntax-2015-pages-201-220.md#pdf-page-205) | Full extracted source span retained |
| SPI-SYN24 | 206 | [p.206](syntax-2015-pages-201-220.md#pdf-page-206) | Full extracted source span retained |
| SPI-SYN24 | 207 | [p.207](syntax-2015-pages-201-220.md#pdf-page-207) | Full extracted source span retained |
| SPI-SYN24 | 208 | [p.208](syntax-2015-pages-201-220.md#pdf-page-208) | Full extracted source span retained |
| SPI-SYN24 | 209 | [p.209](syntax-2015-pages-201-220.md#pdf-page-209) | Full extracted source span retained |
| SPI-SYN24 | 210 | [p.210](syntax-2015-pages-201-220.md#pdf-page-210) | Full extracted source span retained |
| SPI-SYN24 | 211 | [p.211](syntax-2015-pages-201-220.md#pdf-page-211) | Full extracted source span retained |
| SPI-SYN24 | 212 | [p.212](syntax-2015-pages-201-220.md#pdf-page-212) | Full extracted source span retained |
| SPI-SYN24 | 213 | [p.213](syntax-2015-pages-201-220.md#pdf-page-213) | Full extracted source span retained |
| SPI-SYN24 | 214 | [p.214](syntax-2015-pages-201-220.md#pdf-page-214) | Full extracted source span retained |
| SPI-SYN24 | 215 | [p.215](syntax-2015-pages-201-220.md#pdf-page-215) | Full extracted source span retained |
| SPI-SYN24 | 216 | [p.216](syntax-2015-pages-201-220.md#pdf-page-216) | Full extracted source span retained |
| SPI-SYN24 | 217 | [p.217](syntax-2015-pages-201-220.md#pdf-page-217) | Full extracted source span retained |
| SPI-SYN24 | 218 | [p.218](syntax-2015-pages-201-220.md#pdf-page-218) | Full extracted source span retained |
| SPI-SYN24 | 219 | [p.219](syntax-2015-pages-201-220.md#pdf-page-219) | Full extracted source span retained |
| SPI-SYN24 | 220 | [p.220](syntax-2015-pages-201-220.md#pdf-page-220) | Full extracted source span retained |
| SPI-SYN24 | 221 | [p.221](syntax-2015-pages-221-240.md#pdf-page-221) | Full extracted source span retained |
| SPI-SYN24 | 222 | [p.222](syntax-2015-pages-221-240.md#pdf-page-222) | Full extracted source span retained |
| SPI-SYN24 | 223 | [p.223](syntax-2015-pages-221-240.md#pdf-page-223) | Full extracted source span retained |
| SPI-SYN24 | 224 | [p.224](syntax-2015-pages-221-240.md#pdf-page-224) | Full extracted source span retained |
| SPI-SYN24 | 225 | [p.225](syntax-2015-pages-221-240.md#pdf-page-225) | Full extracted source span retained |
| SPI-SYN24 | 226 | [p.226](syntax-2015-pages-221-240.md#pdf-page-226) | Full extracted source span retained |
| SPI-SYN24 | 227 | [p.227](syntax-2015-pages-221-240.md#pdf-page-227) | Full extracted source span retained |
| SPI-SYN24 | 228 | [p.228](syntax-2015-pages-221-240.md#pdf-page-228) | Full extracted source span retained |
| SPI-SYN24 | 229 | [p.229](syntax-2015-pages-221-240.md#pdf-page-229) | Full extracted source span retained |
| SPI-SYN24 | 230 | [p.230](syntax-2015-pages-221-240.md#pdf-page-230) | Full extracted source span retained |
| SPI-SYN24 | 231 | [p.231](syntax-2015-pages-221-240.md#pdf-page-231) | Full extracted source span retained |
| SPI-SYN24 | 232 | [p.232](syntax-2015-pages-221-240.md#pdf-page-232) | Full extracted source span retained |
| SPI-SYN24 | 233 | [p.233](syntax-2015-pages-221-240.md#pdf-page-233) | Full extracted source span retained |
| SPI-SYN24 | 234 | [p.234](syntax-2015-pages-221-240.md#pdf-page-234) | Full extracted source span retained |
| SPI-SYN24 | 235 | [p.235](syntax-2015-pages-221-240.md#pdf-page-235) | Full extracted source span retained |
| SPI-SYN24 | 236 | [p.236](syntax-2015-pages-221-240.md#pdf-page-236) | Full extracted source span retained |
| SPI-SYN24 | 237 | [p.237](syntax-2015-pages-221-240.md#pdf-page-237) | Full extracted source span retained |
| SPI-SYN24 | 238 | [p.238](syntax-2015-pages-221-240.md#pdf-page-238) | Full extracted source span retained |
| SPI-SYN24 | 239 | [p.239](syntax-2015-pages-221-240.md#pdf-page-239) | Full extracted source span retained |
| SPI-SYN24 | 240 | [p.240](syntax-2015-pages-221-240.md#pdf-page-240) | Full extracted source span retained |
| SPI-SYN24 | 241 | [p.241](syntax-2015-pages-241-253.md#pdf-page-241) | Full extracted source span retained |
| SPI-SYN24 | 242 | [p.242](syntax-2015-pages-241-253.md#pdf-page-242) | Full extracted source span retained |
| SPI-SYN24 | 243 | [p.243](syntax-2015-pages-241-253.md#pdf-page-243) | Full extracted source span retained |
| SPI-SYN24 | 244 | [p.244](syntax-2015-pages-241-253.md#pdf-page-244) | No extractable text; inspect original PDF |
| SPI-SYN24 | 245 | [p.245](syntax-2015-pages-241-253.md#pdf-page-245) | Full extracted source span retained |
| SPI-SYN24 | 246 | [p.246](syntax-2015-pages-241-253.md#pdf-page-246) | Full extracted source span retained |
| SPI-SYN24 | 247 | [p.247](syntax-2015-pages-241-253.md#pdf-page-247) | Full extracted source span retained |
| SPI-SYN24 | 248 | [p.248](syntax-2015-pages-241-253.md#pdf-page-248) | Full extracted source span retained |
| SPI-SYN24 | 249 | [p.249](syntax-2015-pages-241-253.md#pdf-page-249) | Full extracted source span retained |
| SPI-SYN24 | 250 | [p.250](syntax-2015-pages-241-253.md#pdf-page-250) | Full extracted source span retained |
| SPI-SYN24 | 251 | [p.251](syntax-2015-pages-241-253.md#pdf-page-251) | Full extracted source span retained |
| SPI-SYN24 | 252 | [p.252](syntax-2015-pages-241-253.md#pdf-page-252) | Full extracted source span retained |
| SPI-SYN24 | 253 | [p.253](syntax-2015-pages-241-253.md#pdf-page-253) | Full extracted source span retained |
| SPI-DTP6 | 1 | [p.1](cm6-enhancements-pages-001-014.md#pdf-page-001) | Full extracted source span retained |
| SPI-DTP6 | 2 | [p.2](cm6-enhancements-pages-001-014.md#pdf-page-002) | Full extracted source span retained |
| SPI-DTP6 | 3 | [p.3](cm6-enhancements-pages-001-014.md#pdf-page-003) | Full extracted source span retained |
| SPI-DTP6 | 4 | [p.4](cm6-enhancements-pages-001-014.md#pdf-page-004) | Full extracted source span retained |
| SPI-DTP6 | 5 | [p.5](cm6-enhancements-pages-001-014.md#pdf-page-005) | Full extracted source span retained |
| SPI-DTP6 | 6 | [p.6](cm6-enhancements-pages-001-014.md#pdf-page-006) | Full extracted source span retained |
| SPI-DTP6 | 7 | [p.7](cm6-enhancements-pages-001-014.md#pdf-page-007) | Full extracted source span retained |
| SPI-DTP6 | 8 | [p.8](cm6-enhancements-pages-001-014.md#pdf-page-008) | Full extracted source span retained |
| SPI-DTP6 | 9 | [p.9](cm6-enhancements-pages-001-014.md#pdf-page-009) | Full extracted source span retained |
| SPI-DTP6 | 10 | [p.10](cm6-enhancements-pages-001-014.md#pdf-page-010) | Full extracted source span retained |
| SPI-DTP6 | 11 | [p.11](cm6-enhancements-pages-001-014.md#pdf-page-011) | Full extracted source span retained |
| SPI-DTP6 | 12 | [p.12](cm6-enhancements-pages-001-014.md#pdf-page-012) | Full extracted source span retained |
| SPI-DTP6 | 13 | [p.13](cm6-enhancements-pages-001-014.md#pdf-page-013) | Full extracted source span retained |
| SPI-DTP6 | 14 | [p.14](cm6-enhancements-pages-001-014.md#pdf-page-014) | Full extracted source span retained |
| SPI-DTP6 | 15 | [p.15](cm6-enhancements-pages-015-028.md#pdf-page-015) | Full extracted source span retained |
| SPI-DTP6 | 16 | [p.16](cm6-enhancements-pages-015-028.md#pdf-page-016) | Full extracted source span retained |
| SPI-DTP6 | 17 | [p.17](cm6-enhancements-pages-015-028.md#pdf-page-017) | Full extracted source span retained |
| SPI-DTP6 | 18 | [p.18](cm6-enhancements-pages-015-028.md#pdf-page-018) | Full extracted source span retained |
| SPI-DTP6 | 19 | [p.19](cm6-enhancements-pages-015-028.md#pdf-page-019) | Full extracted source span retained |
| SPI-DTP6 | 20 | [p.20](cm6-enhancements-pages-015-028.md#pdf-page-020) | Full extracted source span retained |
| SPI-DTP6 | 21 | [p.21](cm6-enhancements-pages-015-028.md#pdf-page-021) | Full extracted source span retained |
| SPI-DTP6 | 22 | [p.22](cm6-enhancements-pages-015-028.md#pdf-page-022) | Full extracted source span retained |
| SPI-DTP6 | 23 | [p.23](cm6-enhancements-pages-015-028.md#pdf-page-023) | Full extracted source span retained |
| SPI-DTP6 | 24 | [p.24](cm6-enhancements-pages-015-028.md#pdf-page-024) | Full extracted source span retained |
| SPI-DTP6 | 25 | [p.25](cm6-enhancements-pages-015-028.md#pdf-page-025) | Full extracted source span retained |
| SPI-DTP6 | 26 | [p.26](cm6-enhancements-pages-015-028.md#pdf-page-026) | Full extracted source span retained |
| SPI-DTP6 | 27 | [p.27](cm6-enhancements-pages-015-028.md#pdf-page-027) | Full extracted source span retained |
| SPI-DTP6 | 28 | [p.28](cm6-enhancements-pages-015-028.md#pdf-page-028) | Full extracted source span retained |
