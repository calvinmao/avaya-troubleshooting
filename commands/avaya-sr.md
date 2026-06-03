---
description: Start a structured Avaya SR troubleshooting session. Usage: /avaya-sr [SR-number] [product] [symptom]. Activates the avaya-debug skill, loads the correct product reference files, and begins layer-by-layer diagnosis.
argument-hint: "[SR-number] [product] [brief symptom]"
---

Activate the `avaya-debug` skill and begin a structured troubleshooting session.

Parse the arguments:
- **SR number**: e.g. `SR-12345678` or `00123456`
- **Product**: e.g. `AES`, `AACC`, `Oceana`, `POM`, `Recording`, `SIP`, `Certificate`
- **Symptom**: brief description of the fault

Then:

1. Print a session header:
   ```
   # SR <number> — Troubleshooting Session
   **Product**: <product> | **Date**: <today> | **Symptom**: <symptom>
   ```

2. Based on the product, announce which reference file(s) you will load (from the progressive loading table in the avaya-debug skill), then load them via the Read tool using the path `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/references/<file>.md`.

3. Ask the user for evidence if not yet provided:
   - Log files, trace exports, or paste excerpts
   - Environment versions (CM, AES, AACC, etc.)
   - Reproduction steps and affected scope

4. Begin layer-by-layer analysis as soon as evidence arrives. Always cite specific log lines or trace timestamps in your findings.

5. Maintain an open items table throughout the session:

   | Status | Item | Owner |
   |--------|------|-------|
   | 🔍 Investigating | [item] | Claude |
   | ⏳ Awaiting | [info needed] | Customer |
   | ✅ Resolved | [finding] | — |

If no arguments are provided, ask: "Please provide the SR number, product (e.g. AES, AACC, Recording), and a brief symptom description."
