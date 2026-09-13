#!/usr/bin/env python3
"""
Compare Human.json (human-corrected) vs LLM.json (raw model output) files.

Counts how many fields the human changed relative to the LLM output, and
reports where. Works on a single file pair or scans Results/ for every
*_Human.json / *_LLM.json pair it can find.

Usage:
  python compare_human_llm.py                       # scan Results/ for all pairs
  python compare_human_llm.py <human.json> <llm.json>  # compare one pair
  python compare_human_llm.py --verbose              # also list every changed field
"""

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = REPO_ROOT / "Results"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def diff(human, llm, path=""):
    """
    Recursively compare two JSON-like structures.
    Returns a list of (path, llm_value, human_value) for every leaf that changed,
    plus entries for added/removed keys or list items.
    """
    changes = []

    if isinstance(human, dict) and isinstance(llm, dict):
        keys = set(human.keys()) | set(llm.keys())
        for key in sorted(keys):
            sub_path = f"{path}.{key}" if path else key
            if key not in llm:
                changes.append((sub_path, "<missing>", human[key]))
            elif key not in human:
                changes.append((sub_path, llm[key], "<removed>"))
            else:
                changes.extend(diff(human[key], llm[key], sub_path))

    elif isinstance(human, list) and isinstance(llm, list):
        max_len = max(len(human), len(llm))
        for i in range(max_len):
            sub_path = f"{path}[{i}]"
            if i >= len(llm):
                changes.append((sub_path, "<missing>", human[i]))
            elif i >= len(human):
                changes.append((sub_path, llm[i], "<removed>"))
            else:
                changes.extend(diff(human[i], llm[i], sub_path))

    else:
        if human != llm:
            changes.append((path, llm, human))

    return changes


def count_leaves(value):
    """Count total number of leaf fields in a JSON structure (for a % changed)."""
    if isinstance(value, dict):
        return sum(count_leaves(v) for v in value.values()) or 1
    if isinstance(value, list):
        return sum(count_leaves(v) for v in value) or 1
    return 1


def compare_pair(human_path: Path, llm_path: Path, verbose: bool = False):
    human = load_json(human_path)
    llm = load_json(llm_path)

    changes = diff(human, llm)
    total_fields = count_leaves(human)

    print(f"\n=== {human_path.relative_to(REPO_ROOT)}  vs  {llm_path.relative_to(REPO_ROOT)} ===")
    print(f"Fields changed: {len(changes)} / {total_fields} "
          f"({(len(changes) / total_fields * 100):.1f}%)")

    if verbose:
        for sub_path, old_val, new_val in changes:
            print(f"  - {sub_path}")
            print(f"      LLM:   {old_val!r}")
            print(f"      Human: {new_val!r}")

    return len(changes), total_fields


def find_pairs():
    """Find every *_Human.json / *_LLM.json (or Human.json/LLM.json) pair under Results/."""
    pairs = []
    seen = set()

    for human_file in RESULTS_DIR.rglob("*Human.json"):
        stem = human_file.name[: -len("Human.json")]  # e.g. "Kullig_" or ""
        candidates = [
            human_file.parent / f"{stem}LLM.json",
            human_file.parent / f"{stem}LLm.json",
        ]
        for llm_file in candidates:
            if llm_file.exists() and human_file not in seen:
                pairs.append((human_file, llm_file))
                seen.add(human_file)
                break

    return sorted(pairs)


def main():
    args = sys.argv[1:]
    verbose = "--verbose" in args
    args = [a for a in args if a != "--verbose"]

    if len(args) == 2:
        pairs = [(Path(args[0]).resolve(), Path(args[1]).resolve())]
    elif len(args) == 0:
        pairs = find_pairs()
        if not pairs:
            print("No Human.json/LLM.json pairs found under Results/.")
            return
    else:
        print(__doc__)
        sys.exit(1)

    grand_changes = 0
    grand_total = 0
    for human_path, llm_path in pairs:
        try:
            changed, total = compare_pair(human_path, llm_path, verbose=verbose)
            grand_changes += changed
            grand_total += total
        except Exception as e:
            print(f"\n=== {human_path} vs {llm_path} ===")
            print(f"  ERROR: {e}")

    if len(pairs) > 1:
        print(f"\n=== TOTAL across {len(pairs)} pairs ===")
        print(f"Fields changed: {grand_changes} / {grand_total} "
              f"({(grand_changes / grand_total * 100):.1f}%)")


if __name__ == "__main__":
    main()
