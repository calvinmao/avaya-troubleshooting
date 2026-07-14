#!/usr/bin/env python3
"""
lint_metadata.py — Structural lint for the avaya-debug knowledge base.

Validates that every lessons/*.md and references/*.md file conforms to the
YAML frontmatter schema documented in docs/reform/schema.md.

Exit code:
    0 if all files pass
    1 if any files fail (details printed to stderr)

Usage:
    python3 scripts/lint_metadata.py                # lint entire KB
    python3 scripts/lint_metadata.py --verbose      # show OK lines too
    python3 scripts/lint_metadata.py --domain=aes-cti-jtapi  # single domain

Zero external dependencies beyond PyYAML.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "skills" / "avaya-debug" / "lessons"
REFERENCES_DIR = REPO_ROOT / "skills" / "avaya-debug" / "references"

VALID_LAYERS = {"L1", "L2", "L3", "L4", "L5"}
VALID_TYPES = {"fact", "process", "decision", "experience", "pattern"}
VALID_MATURITY = {"draft", "verified", "canonical"}
VALID_PROMO_STATUS = {"pending", "promoted", "rejected"}


class LintError(Exception):
    def __init__(self, file: Path, msg: str, line: int | None = None):
        self.file = file
        self.msg = msg
        self.line = line

    def __str__(self):
        loc = f"{self.file.relative_to(REPO_ROOT)}"
        if self.line is not None:
            loc += f":{self.line}"
        return f"{loc}: {self.msg}"


# ---------------------------------------------------------------------------
# YAML block extraction
# ---------------------------------------------------------------------------

# Top-of-file frontmatter (file-level block)
TOP_FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# Per-entry frontmatter for L-NNN entries: opens with `^---\n`, closes with
# `\n---\n\s*## L-\d{3}`. To avoid matching markdown horizontal rules or
# table separators, we require the closing fence to be immediately followed
# by a `## L-NNN` heading. We search only text AFTER the file-level FM,
# and the caller advances the cursor past each match to prevent overlap.
ENTRY_FM_RE = re.compile(
    r"^---\n(.*?)\n---\n\s*(?=## L-\d{3})",
    re.MULTILINE | re.DOTALL,
)


def _parse_block(raw: str, line: int, path: Path) -> dict:
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise LintError(path, f"YAML parse error: {e}", line=line)
    if not isinstance(parsed, dict):
        raise LintError(path, f"frontmatter must be a mapping, got {type(parsed).__name__}", line=line)
    return parsed


def extract_top_frontmatter(text: str, path: Path) -> tuple[int, str, dict] | None:
    """Extract the single YAML block at the top of the file, if present."""
    m = TOP_FM_RE.match(text)
    if not m:
        return None
    raw = m.group(1)
    parsed = _parse_block(raw, 1, path)
    return (1, raw, parsed, m.end())


def extract_entry_frontmatters(text: str, path: Path, start: int = 0) -> list[tuple[int, str, dict]]:
    """
    Extract per-entry YAML blocks that are immediately followed by `## L-NNN`.

    Uses a cursor-advancing loop (not finditer) so that each match starts
    strictly after the previous one ended — this prevents a single body
    region from being reinterpreted as YAML.
    """
    out = []
    cursor = start
    while True:
        m = ENTRY_FM_RE.search(text, cursor)
        if not m:
            break
        raw = m.group(1)
        line = text[: m.start()].count("\n") + 1
        parsed = _parse_block(raw, line, path)
        out.append((line, raw, parsed))
        cursor = m.end()
    return out


# ---------------------------------------------------------------------------
# Lessons file validation
# ---------------------------------------------------------------------------

L_HEADING_RE = re.compile(r"^## (L-\d{3}) — ", re.MULTILINE)


def lint_lesson_file(path: Path) -> list[LintError]:
    errors: list[LintError] = []
    text = path.read_text(encoding="utf-8")

    if path.name == "README.md":
        return errors  # README is documentation, not a lesson data file

    try:
        top = extract_top_frontmatter(text, path)
    except LintError as e:
        errors.append(e)
        return errors

    if top is None:
        errors.append(LintError(path, "no file-level YAML frontmatter block found"))
        return errors

    file_line, _, file_fm, top_end = top
    for required in ("domain", "default_layer", "default_type"):
        if required not in file_fm:
            errors.append(LintError(path, f"file-level frontmatter missing required field: {required}", line=file_line))

    dl = file_fm.get("default_layer")
    if dl is not None and dl not in VALID_LAYERS:
        errors.append(LintError(path, f"default_layer '{dl}' not in {sorted(VALID_LAYERS)}", line=file_line))
    dt = file_fm.get("default_type")
    if dt is not None and dt not in VALID_TYPES:
        errors.append(LintError(path, f"default_type '{dt}' not in {sorted(VALID_TYPES)}", line=file_line))

    # Per-entry frontmatter blocks (each followed by ## L-NNN heading)
    try:
        entry_blocks = extract_entry_frontmatters(text, path, start=top_end)
    except LintError as e:
        errors.append(e)
        return errors

    # Cross-check with ## L-NNN headings
    headings = L_HEADING_RE.findall(text)

    if len(entry_blocks) != len(headings):
        errors.append(LintError(
            path,
            f"count mismatch: {len(entry_blocks)} L-NNN frontmatter blocks vs {len(headings)} ## L-NNN headings"
        ))

    # Validate each entry block
    seen_ids: list[str] = []
    for i, (line, _, fm) in enumerate(entry_blocks):
        # Required fields
        for required in ("id", "layer", "type", "maturity", "versions", "provenance", "promotion", "owner"):
            if required not in fm:
                errors.append(LintError(path, f"L-NNN entry missing required field: {required}", line=line))

        # Enum validation
        if fm.get("layer") and fm["layer"] not in VALID_LAYERS:
            errors.append(LintError(path, f"layer '{fm['layer']}' not in {sorted(VALID_LAYERS)}", line=line))
        if fm.get("type") and fm["type"] not in VALID_TYPES:
            errors.append(LintError(path, f"type '{fm['type']}' not in {sorted(VALID_TYPES)}", line=line))
        if fm.get("maturity") and fm["maturity"] not in VALID_MATURITY:
            errors.append(LintError(path, f"maturity '{fm['maturity']}' not in {sorted(VALID_MATURITY)}", line=line))

        # ID format
        entry_id = fm.get("id", "")
        if entry_id and not re.fullmatch(r"L-\d{3}", entry_id):
            errors.append(LintError(path, f"id '{entry_id}' must match pattern L-NNN (zero-padded 3 digits)", line=line))

        # ID matches corresponding heading
        if i < len(headings):
            if entry_id != headings[i]:
                errors.append(LintError(
                    path,
                    f"id '{entry_id}' in frontmatter does not match heading '{headings[i]}' (block {i+1})",
                    line=line,
                ))

        # Monotonicity
        if entry_id in seen_ids:
            errors.append(LintError(path, f"duplicate id '{entry_id}'", line=line))
        elif seen_ids and entry_id.startswith("L-"):
            prev_num = int(seen_ids[-1].split("-")[1])
            curr_num = int(entry_id.split("-")[1])
            if curr_num <= prev_num:
                errors.append(LintError(path, f"id '{entry_id}' not monotonically increasing (prev={seen_ids[-1]})", line=line))
        seen_ids.append(entry_id)

        # Promotion consistency
        promo = fm.get("promotion") or {}
        if isinstance(promo, dict):
            ps = promo.get("status")
            if ps and ps not in VALID_PROMO_STATUS:
                errors.append(LintError(path, f"promotion.status '{ps}' not in {sorted(VALID_PROMO_STATUS)}", line=line))
            if ps == "promoted":
                if not promo.get("target"):
                    errors.append(LintError(path, "promotion.status=promoted requires non-null promotion.target", line=line))
                if not promo.get("date"):
                    errors.append(LintError(path, "promotion.status=promoted requires non-null promotion.date", line=line))
            elif ps == "rejected":
                if not promo.get("date"):
                    errors.append(LintError(path, "promotion.status=rejected requires non-null promotion.date", line=line))

        # Provenance shape
        prov = fm.get("provenance") or {}
        if isinstance(prov, dict):
            if not prov.get("sr"):
                errors.append(LintError(path, "provenance.sr is required", line=line))
            if not prov.get("date"):
                errors.append(LintError(path, "provenance.date is required", line=line))

    return errors


# ---------------------------------------------------------------------------
# References file validation
# ---------------------------------------------------------------------------

def lint_reference_file(path: Path) -> list[LintError]:
    errors: list[LintError] = []
    text = path.read_text(encoding="utf-8")

    try:
        top = extract_top_frontmatter(text, path)
    except LintError as e:
        errors.append(e)
        return errors

    if top is None:
        errors.append(LintError(path, "no file-level YAML frontmatter block found"))
        return errors

    line, _, fm, _ = top

    required = ("title", "layer", "scope", "maturity", "applicable_versions",
                "last_reviewed", "owner", "staleness_risks", "related_docs")
    for req in required:
        if req not in fm:
            errors.append(LintError(path, f"reference missing required field: {req}", line=line))

    if fm.get("layer") and fm["layer"] not in VALID_LAYERS:
        errors.append(LintError(path, f"layer '{fm['layer']}' not in {sorted(VALID_LAYERS)}", line=line))
    if fm.get("maturity") and fm["maturity"] not in VALID_MATURITY:
        errors.append(LintError(path, f"maturity '{fm['maturity']}' not in {sorted(VALID_MATURITY)}", line=line))

    # staleness_risks and related_docs must be lists
    for list_field in ("staleness_risks", "related_docs", "applicable_versions"):
        val = fm.get(list_field)
        if val is not None and not isinstance(val, list):
            errors.append(LintError(path, f"{list_field} must be a list, got {type(val).__name__}", line=line))

    return errors


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def collect_files(domain: str | None) -> Iterable[tuple[str, Path]]:
    if domain:
        for kind, dirp in (("lesson", LESSONS_DIR), ("reference", REFERENCES_DIR)):
            fp = dirp / f"{domain}.md"
            if fp.exists():
                yield kind, fp
        return

    for fp in sorted(LESSONS_DIR.glob("*.md")):
        yield "lesson", fp
    for fp in sorted(REFERENCES_DIR.glob("*.md")):
        yield "reference", fp


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--verbose", action="store_true", help="print OK lines for passing files")
    p.add_argument("--domain", type=str, default=None, help="restrict lint to one domain name")
    args = p.parse_args()

    all_errors: list[LintError] = []
    total_files = 0

    for kind, fp in collect_files(args.domain):
        total_files += 1
        errs = lint_lesson_file(fp) if kind == "lesson" else lint_reference_file(fp)
        if errs:
            all_errors.extend(errs)
            print(f"FAIL {fp.relative_to(REPO_ROOT)} ({len(errs)} error{'s' if len(errs) != 1 else ''})")
            for e in errs:
                print(f"  {e}", file=sys.stderr)
        elif args.verbose:
            print(f"OK   {fp.relative_to(REPO_ROOT)}")

    print(f"\n{total_files} file(s) checked; {len(all_errors)} error(s)")
    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main())
