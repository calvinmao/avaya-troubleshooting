---
description: Provide Avaya log collection guidance for a specific product. Usage: /avaya-logs [product]. Returns exact commands, file paths, and log levels needed to capture evidence for the named product.
argument-hint: "[product: AES | AACC | POM | Recording | CM | SIP | Analytics | IPO]"
---

Load the `log-collection.md` reference from `${CLAUDE_PLUGIN_ROOT}/skills/avaya-debug/references/log-collection.md` and, if the product is also mentioned in another reference (e.g., AES → `aes-cti-jtapi.md`), load that too.

Then provide a targeted log collection guide for the requested product:

1. **What to collect**: specific log files, trace exports, and diagnostic outputs
2. **How to collect**: exact CLI commands or UI steps with copy-pasteable syntax
3. **Log level settings**: how to temporarily raise log verbosity (and how to restore it)
4. **Trace enables**: any DMCC, TSAPI, CSTA, g3trace, csta_trace, or tcpdump captures needed
5. **Time window**: recommended capture duration and how to align timestamps
6. **What to look for**: key patterns, error strings, or event sequences that confirm the issue

Format the output as a numbered checklist the customer can follow without Avaya expertise.

If no product argument is provided, ask: "Which product do you need log collection guidance for? (e.g., AES, AACC, POM, Recording, CM, SIP/SM, Analytics, IP Office)"
