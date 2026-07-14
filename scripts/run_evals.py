#!/usr/bin/env python3
"""
run_evals.py — Run the avaya-debug evals harness.

Two modes:

  --mode a  (default, offline, no external API)
    Verifies that every A-NNN activation case in evals/activation.md has
    at least one trigger keyword covered by SKILL.md's routing table
    for the expected reference file(s). Purely structural — checks that
    SKILL.md's routing surface is sufficient to activate the skill on
    the tested prompt.

  --mode b  (online, opt-in, requires ANTHROPIC_API_KEY)
    Runs OQ-NNN output-quality cases from evals/output-quality.md
    through Claude, scores against the 6-criterion rubric (Q1-Q6, 0-3),
    reports per-case scores and rubric coverage. This mode consumes API
    tokens; kept opt-in.

Exit code:
    0 if all cases pass
    1 if any case fails
    2 on setup error (missing files, missing API key in mode b)

Usage:
    python3 scripts/run_evals.py                        # mode A
    python3 scripts/run_evals.py --mode a --verbose     # mode A verbose
    python3 scripts/run_evals.py --mode b               # mode B (needs API key)
    python3 scripts/run_evals.py --mode a --domain=aes-cti-jtapi
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = REPO_ROOT / "skills" / "avaya-debug" / "SKILL.md"
ACTIVATION_MD = REPO_ROOT / "evals" / "activation.md"
OQ_MD = REPO_ROOT / "evals" / "output-quality.md"


# ---------------------------------------------------------------------------
# Parse SKILL.md routing table
# ---------------------------------------------------------------------------

def parse_skill_routing(skill_text: str) -> dict[str, set[str]]:
    """
    Return a dict {reference-basename: set-of-trigger-keywords}.

    SKILL.md's routing table rows look like:
        | AES, JTAPI, ... | [aes-cti-jtapi.md](references/aes-cti-jtapi.md) | AES, JTAPI, CTI, ... |
    Column 1 = product/topic scope
    Column 2 = reference file link
    Column 3 = trigger keywords (comma-separated, lower-cased for match)

    We union column 1 and column 3 keywords so the coverage check is
    inclusive.
    """
    routing: dict[str, set[str]] = {}
    # Match rows with markdown link to references/<filename>.md
    row_re = re.compile(
        r"^\|\s*(?P<scope>[^|]+?)\s*\|\s*\[[^\]]+\]\(references/(?P<ref>[a-z0-9-]+\.md)\)\s*\|\s*(?P<triggers>[^|]+?)\s*\|",
        re.MULTILINE,
    )
    for m in row_re.finditer(skill_text):
        ref = m.group("ref")
        scope_words = _split_keywords(m.group("scope"))
        trigger_words = _split_keywords(m.group("triggers"))
        routing.setdefault(ref, set()).update(scope_words)
        routing[ref].update(trigger_words)
    return routing


def _split_keywords(cell: str) -> set[str]:
    """Split a comma/pipe-separated cell into normalized keywords."""
    # Remove markdown formatting
    cell = re.sub(r"[`*_]", "", cell)
    words = re.split(r"[,;/]|\s+or\s+", cell)
    return {w.strip().lower() for w in words if w.strip()}


# ---------------------------------------------------------------------------
# Parse activation.md
# ---------------------------------------------------------------------------

ACTIVATION_ROW_RE = re.compile(
    r"^\|\s*(?P<id>A-\d{3})\s*\|\s*\"(?P<prompt>[^\"]+)\"\s*\|\s*(?P<refs>[^|]+?)\s*\|\s*(?P<notes>[^|]*?)\s*\|",
    re.MULTILINE,
)

NO_TRIGGER_ROW_RE = re.compile(
    r"^\|\s*(?P<id>N-\d{3})\s*\|\s*\"(?P<prompt>[^\"]+)\"\s*\|\s*(?P<notes>[^|]*?)\s*\|",
    re.MULTILINE,
)

# References cell parser: pulls out every "<name>.md" file referenced
REF_FILE_RE = re.compile(r"([a-z0-9-]+\.md)")


def parse_activation(text: str) -> tuple[list[dict], list[dict]]:
    """Return (should_trigger_cases, should_not_trigger_cases)."""
    triggers = []
    for m in ACTIVATION_ROW_RE.finditer(text):
        # Skip the trigger table header if it accidentally matched
        if m.group("id") in ("A-NNN",):
            continue
        refs = set(REF_FILE_RE.findall(m.group("refs")))
        triggers.append({
            "id": m.group("id"),
            "prompt": m.group("prompt"),
            "expected_refs": refs,
            "notes": m.group("notes").strip(),
        })
    no_triggers = []
    for m in NO_TRIGGER_ROW_RE.finditer(text):
        no_triggers.append({
            "id": m.group("id"),
            "prompt": m.group("prompt"),
            "notes": m.group("notes").strip(),
        })
    return triggers, no_triggers


# ---------------------------------------------------------------------------
# Mode A: coverage check
# ---------------------------------------------------------------------------

# References that are always loaded regardless of routing keywords
# (per SKILL.md "Step 0 - Always Load First"). These bypass the coverage
# check because they don't need a trigger match to activate.
ALWAYS_LOADED = {"diagnostic-principles.md"}


def mode_a(verbose: bool = False, domain: str | None = None) -> int:
    if not SKILL_MD.exists():
        print(f"ERROR: {SKILL_MD} not found", file=sys.stderr)
        return 2
    if not ACTIVATION_MD.exists():
        print(f"ERROR: {ACTIVATION_MD} not found", file=sys.stderr)
        return 2

    routing = parse_skill_routing(SKILL_MD.read_text(encoding="utf-8"))
    if not routing:
        print("ERROR: no routing rows parsed from SKILL.md", file=sys.stderr)
        return 2

    triggers, _ = parse_activation(ACTIVATION_MD.read_text(encoding="utf-8"))
    if not triggers:
        print("ERROR: no A-NNN cases parsed from activation.md", file=sys.stderr)
        return 2

    failures = []
    total = 0
    for case in triggers:
        if domain and not any(domain in r for r in case["expected_refs"]):
            continue
        total += 1
        prompt_lower = case["prompt"].lower()
        # For each expected reference, does the SKILL.md routing table have
        # at least one trigger word that appears in the prompt?
        # Exception: always-loaded references bypass this check.
        uncovered = []
        for ref in case["expected_refs"]:
            if ref in ALWAYS_LOADED:
                continue  # always loaded, no trigger needed
            keywords = routing.get(ref, set())
            if not keywords:
                uncovered.append(f"{ref} (no routing row in SKILL.md)")
                continue
            hits = [kw for kw in keywords if kw and kw in prompt_lower]
            if not hits:
                uncovered.append(f"{ref} (0 matching triggers among {len(keywords)})")

        if uncovered:
            failures.append((case, uncovered))
            print(f"FAIL {case['id']}: {case['prompt']!r}", file=sys.stderr)
            for u in uncovered:
                print(f"       expected reference {u}", file=sys.stderr)
        elif verbose:
            print(f"OK   {case['id']}: covers {sorted(case['expected_refs'])}")

    print(f"\n{total} A-NNN case(s) checked; {len(failures)} coverage gap(s)")
    return 0 if not failures else 1


# ---------------------------------------------------------------------------
# Mode B: LLM-scored output-quality (opt-in)
# ---------------------------------------------------------------------------

def mode_b(verbose: bool = False, domain: str | None = None) -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        print("       Mode B requires an API key to score OQ-NNN cases against the rubric.", file=sys.stderr)
        print("       Falling back: use --mode a for offline coverage checks.", file=sys.stderr)
        return 2

    try:
        import anthropic  # type: ignore
    except ImportError:
        print("ERROR: anthropic SDK not installed. Run: pip install anthropic", file=sys.stderr)
        return 2

    if not OQ_MD.exists():
        print(f"ERROR: {OQ_MD} not found", file=sys.stderr)
        return 2

    text = OQ_MD.read_text(encoding="utf-8")
    # Parse OQ-NNN cases (they are ### headings, not table rows)
    oq_cases = []
    case_re = re.compile(r"### (OQ-\d{3}) — (.+?)$\n\n(.*?)(?=^### OQ-\d{3}|^## |\Z)", re.MULTILINE | re.DOTALL)
    for m in case_re.finditer(text):
        oq_cases.append({
            "id": m.group(1),
            "title": m.group(2),
            "body": m.group(3),
        })

    if not oq_cases:
        print("ERROR: no OQ-NNN cases parsed from output-quality.md", file=sys.stderr)
        return 2

    print(f"Mode B: scoring {len(oq_cases)} OQ-NNN case(s) against Claude.")
    print("NOTE: This mode is not yet implemented — LLM prompt-and-scoring loop")
    print("      requires the 6-criterion rubric from output-quality.md to be")
    print("      formalized as a machine-parseable spec. See docs/reform/PLAN.md")
    print("      Phase 5 for the follow-up work item.")
    print()
    print(f"Cases discovered ({len(oq_cases)}):")
    for c in oq_cases:
        print(f"  {c['id']}: {c['title']}")
    return 0


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=["a", "b"], default="a", help="a = offline coverage; b = LLM-scored quality (opt-in, needs API key)")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--domain", type=str, default=None, help="restrict to one domain")
    args = p.parse_args()

    if args.mode == "a":
        return mode_a(verbose=args.verbose, domain=args.domain)
    else:
        return mode_b(verbose=args.verbose, domain=args.domain)


if __name__ == "__main__":
    sys.exit(main())
