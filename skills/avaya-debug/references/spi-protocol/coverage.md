---
title: "SPI full-document coverage and source anomalies"
layer: L4
scope: "Whole supplied-document preservation and structural coverage; separate source errors and missing external references."
maturity: canonical
applicable_versions: ["Dated supplied SPI documents; verify current product applicability"]
last_reviewed: "2026-10-28"
owner: "Avaya domain reference maintainers"
staleness_risks: ["Source transcription is not graphical layout", "Historical product and protocol applicability"]
related_docs: []
---

# Coverage and source boundaries

[Library index](index.md) | [Message index](messages.md) | [Test index](cm6-tests.md)

| Check | Verified coverage |
|---|---|
| Original source PDFs | Both retained byte-for-byte, with SHA-256 checks |
| Physical pages | SPI-SYN24 253/253; SPI-DTP6 28/28; total 281/281 |
| Main printed TOC | 299/299 entries mapped, including REFERENCES |
| Main bookmark/body sections | 305/305, including six ALOGON EAS/non-EAS sections omitted from printed TOC |
| Main leaf sections | 224/224 |
| Main messages | 180 alphabetic entries and 180 opcode entries, cross-checked |
| CM6 section ranges | 39/39 |
| CM6 Abstract Tests | 85/85 body and printed-index entries |
| Text spans | Every source page has an exact retained extracted span and hash; text-empty pages remain mapped |
| Diagrams/bit layouts/fonts | Preserved in original PDFs; no claim that text transcription is graphically lossless |

Complete file/page and source inventories: [coverage.json](../../assets/spi-protocol/coverage.json), [syntax inventory](../../assets/spi-protocol/syntax-inventory.json), [CM6 inventory](../../assets/spi-protocol/cm6-inventory.json). Structural coverage preserves all supplied content; it is not independent validation of every historical command or applicability to current builds.

## Source inconsistencies retained

| Source | Pages | Issue |
|---|---|---|
| SPI-SYN24 | [1] | Header Issue0.7 and footer Issue1.0 coexist; preserve both. |
| SPI-SYN24 | [139, 140, 141, 142, 144, 145] | Six numbered ALOGON EAS/non-EAS subheads are absent from printed TOC but present in body/bookmarks; all included. |
| SPI-SYN24 | [17, 250, 251] | Table5 is absent from the front list; supplemental inventory includes it. |
| SPI-SYN24 | [16, 245, 246, 247, 248, 249] | Opcode tables lack a separate numbered TOC entry; both directions included. |
| SPI-SYN24 | [250] | Table5 prints T35000 at cabinet0/carrier0/slot7/circuit0; formula yields cabinet2/slot22/circuit0. Neighbor pattern suggests T03500, but source is preserved uncorrected. |
| SPI-SYN24 | [252, 253] | Page252 is REFERENCES heading; untitled page253 holds the five bibliography entries, not blank. |
| SPI-SYN24 | [244] | Extracted text is empty; retain original page for visual fidelity without inferring semantic absence. |
| SPI-SYN24 | [24, 137] | Session text says AT3; call-processing TIME says AT2 for two-minute liveness timeout. Preserve discrepancy. |
| SPI-DTP6 | [1] | Cover date2010-04-10 versus version 1.1 update2010-04-22; PDFCreationDate also2010-04-22. |
| SPI-DTP6 | [1, 2, 4, 20] | Introduction says unit tests not included insection 9, then refers to unit tests included inplan; section 9 showsPriority/Functional groups only. |
| SPI-DTP6 | [9, 10] | AT35 says noAEVENT forR15/R16, but its continuation asks forAVAIL aftertheAEVENT message. |
| SPI-DTP6 | [17, 23, 27] | Section/TOC spellingCHVEC20 versus test titlesCHGVEC20. |
| SPI-DTP6 | [19, 23, 28] | Section9.4.4 namesAVAIL/AUDAVAIL/AUDACW/AUDAUX; AT80 title namesAVAIL/AUDAVAIL/AUDACD/AUDACW, while action sequence auditsAUX. |
| SPI-DTP6 | [10, 18] | Section9.2.4 note says AGENTSK is sent byCMS/IQ, but9.4.1 saysCMS sendsAPARMS7 andPBX respondsAGENTSK23. |
| SPI-DTP6 | [18] | Embedded j.wallerius review comment expresses an assumption about CMS not supportingCM6/120skills. |
| SPI-DTP6 | [14, 15] | DCON note says sent when call rings atagent; later surplus tests include agent answer before verification. |
| SPI-DTP6 | [26] | AT28 index lacks the dotted leader used by most other entries. |

Source-title note: SPI-SYN24 section 3.3.5.3 ARSPLIT24 has an unclosed parenthesis in the printed TOC (p.10), bookmark and body heading (p.61). The section index retains the source title; this is a source punctuation defect, not omitted content.

## External references not supplied

The originals cite additional COMPAS process, SRAD, detailed call-tree semantics and database-definition documents. Their references are retained; their external contents are not included or claimed covered. SPI-SYN24 points to COMPAS 21003 for detailed call trees and 19974 for database definitions. Consult the inventories and final original pages for the complete bibliography. No source inconsistency is silently corrected in the archived text/PDFs.
