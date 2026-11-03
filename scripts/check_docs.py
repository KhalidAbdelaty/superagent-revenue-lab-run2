"""Fail if README.md links to a repository file that does not exist."""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
readme = (root / "README.md").read_text()
missing = [p for p in re.findall(r"\]\(([^)#:]+)\)", readme) if not (root / p).exists()]
for path in missing:
    print(f"README.md links to a missing file: {path}")
sys.exit(1 if missing else 0)
