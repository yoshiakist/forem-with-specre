#!/usr/bin/env python3
"""
coverage-uncovered.py — Filter specre coverage uncovered files by domain keyword.

Runs `specre coverage --json` and outputs coverage stats plus uncovered files,
optionally filtered by a case-insensitive substring match on file paths.

Usage:
    python3 .claude/commands/scripts/coverage-uncovered.py [keyword]

Examples:
    python3 .claude/commands/scripts/coverage-uncovered.py search
    python3 .claude/commands/scripts/coverage-uncovered.py auth
    python3 .claude/commands/scripts/coverage-uncovered.py          # all uncovered files

Output format:
    coverage=6.9
    tagged=284
    total=4106
    uncovered_count=74
    ---
    app/controllers/search_controller.rb
    app/services/search/article.rb
    ...
"""

import json
import subprocess
import sys


def main():
    keyword = sys.argv[1].lower() if len(sys.argv) > 1 else None

    result = subprocess.run(
        ["specre", "coverage", "--json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error: specre coverage failed (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    data = json.loads(result.stdout)

    uncovered = data.get("uncovered", [])
    if keyword:
        uncovered = [f for f in uncovered if keyword in f.lower()]

    print(f"coverage={data['coverage'] * 100:.1f}")
    print(f"tagged={data['tagged']}")
    print(f"total={data['total']}")
    print(f"uncovered_count={len(uncovered)}")
    print("---")
    for f in uncovered:
        print(f)


if __name__ == "__main__":
    main()
