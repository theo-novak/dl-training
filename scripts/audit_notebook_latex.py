"""Audit notebook markdown for KaTeX LaTeX issues."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "notebooks"

ISSUES = []


def cell_text(source):
    if isinstance(source, list):
        return "".join(source)
    return source


def audit_latex(text: str, path: str, cell_idx: int):
    # Unsupported KaTeX environments
    for m in re.finditer(r"\\begin\{(equation|eqnarray|align\*?)\}", text):
        ISSUES.append((path, cell_idx, f"env {m.group(1)}", m.group(0)))

    # \[ \] display (may not render in some KaTeX configs)
    if re.search(r"\\\[", text):
        ISSUES.append((path, cell_idx, "display \\[", "has \\["))

    # \( \) inline - note for conversion
    if re.search(r"\\\(", text):
        ISSUES.append((path, cell_idx, "inline \\(", "has \\("))

    # Broken: single backslash before common commands outside proper escaping
    # Unmatched math delimiters
    dollars = [i for i, c in enumerate(text) if c == "$" and not text[max(0, i-1):i+2].startswith("\\$")]
    if len(dollars) % 2 != 0:
        ISSUES.append((path, cell_idx, "unmatched $", text[:80]))

    # Unicode math that should be in LaTeX for consistency (optional)
    for ch in ["μ", "σ", "ρ", "θ", "τ", "λ", "∫", "≈", "≤", "≥"]:
        if ch in text and "$" not in text[:50]:  # rough
            pass

    # \text with unescaped braces issues - rare

    # ampersand in align without env - in table cells ok

    # double backslash line breaks in math
    if re.search(r"\$\$.*\\\\.*\$\$", text, re.DOTALL):
        ISSUES.append((path, cell_idx, "\\\\ in $$", "check"))

    # \mid vs | 
    # \mathbf{1} - ok in KaTeX

    # stray backslash at end of line in math

    # \cdot vs *
    
    # Check for _ outside math (heuristic: underscore not preceded by \ or $)
    stripped = re.sub(r"\$[^$]+\$", "", text)
    stripped = re.sub(r"\\\([^)]*\\\)", "", stripped)
    if re.search(r"(?<!\\)\w_\w", stripped):
        ISSUES.append((path, cell_idx, "underscore outside math", re.search(r"(?<!\\)\w_\w", stripped).group(0)))


for nb_path in sorted(ROOT.rglob("*.ipynb")):
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue
        audit_latex(cell_text(cell.get("source", "")), str(nb_path.relative_to(ROOT.parent)), i)

print(f"Found {len(ISSUES)} potential issues")
for item in ISSUES[:80]:
    print(item)
if len(ISSUES) > 80:
    print(f"... and {len(ISSUES) - 80} more")
