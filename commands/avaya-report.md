---
description: Generate a formal Avaya SR troubleshooting report from the current session analysis. Outputs a structured markdown report ready for Avaya support case submission.
---

Generate a formal troubleshooting report from the analysis performed in this session. Use the following structure exactly:

```markdown
# SR <number> — Troubleshooting Report

## <Problem Title>

**Date**: <today's date>
**Products**: <comma-separated product list>
**Environment**: <versions if known>

---

### 1. Problem Statement

**Symptom**: <what the customer observes>
**Impact**: <scope — how many users/calls/agents affected>
**Reproduction**: <steps or conditions to trigger>
**First occurrence**: <date/time if known>

---

### 2. Evidence Collected

| Source | Date | Key Content |
|--------|------|-------------|
| <log file / trace> | <date> | <what was found> |

---

### 3. Analysis

#### Layer-by-Layer Findings

| Layer | Finding | Evidence |
|-------|---------|----------|
| CM | <finding> | <log ref> |
| AES | <finding> | <log ref> |
| Application | <finding> | <log ref> |

#### Cross-Layer Correlation

<Describe how findings across layers combine to explain the symptom.>

---

### 4. Root Cause

<Specific, evidence-supported root cause statement. Cite the exact config, code path, or bug.>

---

### 5. Recommended Resolution

**Short-term (workaround)**:
- <action>

**Long-term (permanent fix)**:
- <action>
- PEA/patch request if applicable

---

### 6. Open Items

| Status | Item | Owner |
|--------|------|-------|
| ⏳ Pending | <item> | <owner> |

---

### 7. Vendor Escalation (if applicable)

| Component | Owner | Evidence to Provide |
|-----------|-------|---------------------|
| <component> | <BBE/Verint/Nuance/Customer> | <log/trace> |
```

Fill in all sections from the analysis in this session. If a section has no data yet, mark it `— Not yet determined —` and add it to Open Items. For security assessments, also include the security assessment table from the security-vulnerability reference.

---

### 8. Capture Lessons (post-report nudge)

After the report is rendered, ask the user **exactly once**:

> 💡 Any findings from this case worth saving to the knowledge base?
> (`yes` → run `/avaya-learn`  |  `no` → skip  |  `list` → show candidates first)

- `yes` → invoke the full `/avaya-learn` flow.
- `list` → run steps 1–3 of `/avaya-learn` (scan + classify + draft) without saving, then ask again.
- `no` or no answer → stop silently. Do not re-prompt later in the session.
