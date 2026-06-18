"""Fix notebook markdown LaTeX for KaTeX rendering.

KaTeX (Cursor/Jupyter) reliably uses $...$ inline and $$...$$ display math.
Converts \\(...\\) and \\[...\\] and escapes currency $ outside math.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "notebooks"


def convert_delimiters(text: str) -> str:
    text = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: f"\n\n$${m.group(1).strip()}$$\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: f"${m.group(1)}$",
        text,
        flags=re.DOTALL,
    )
    return text


def is_currency_dollar(text: str, i: int) -> bool:
    """True if $ at i is currency ($1 move), not math ($2E, $95\\%)."""
    if i + 1 >= len(text) or not text[i + 1].isdigit():
        return False
    k = i + 1
    while k < len(text) and (text[k].isdigit() or text[k] == "."):
        k += 1
    if k < len(text):
        ch = text[k]
        if ch in "/\\_<>=$" or ch.isalpha():
            return False
        if ch == " " and k + 1 < len(text):
            rest = text[k + 1:]
            for word in ("move", "stock", "or ", "and ", "stop", "when", "gains"):
                if rest.startswith(word):
                    return True
    return True


def repair_bad_currency_escapes(text: str) -> str:
    """Undo currency escapes that broke math ($2\\%, $1_{...}, $6/36, etc.)."""
    rules = [
        (r"\\\$(\d+)/", r"$\1/"),
        (r"\\\$(\d+)\\%", r"$\1\\%"),
        (r"\\\$(\d+)_", r"$\1_"),
        (r"\\\$(\d+)([A-Za-z])", r"$\1\2"),
        (r"\\\$(\d+)\s*([<>=])", r"$\1 \2"),
        (r"\\\$(\d+)\$", r"$\1$"),
    ]
    for pat, repl in rules:
        text = re.sub(pat, repl, text)
    return text


def escape_currency(text: str) -> str:
    """Escape $ before digits when used as currency."""
    parts: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j == -1:
                parts.append(text[i:])
                break
            parts.append(text[i:j + 2])
            i = j + 2
            continue
        if text[i] == "$" and (i == 0 or text[i - 1] != "\\"):
            if is_currency_dollar(text, i):
                parts.append("\\$")
                i += 1
                continue
            j = i + 1
            while j < n:
                if text[j] == "$" and text[j - 1] != "\\":
                    if j + 1 < n and text[j + 1] == "$":
                        j += 1
                        continue
                    break
                j += 1
            if j < n and text[j] == "$":
                parts.append(text[i:j + 1])
                i = j + 1
            else:
                parts.append(text[i])
                i += 1
        else:
            parts.append(text[i])
            i += 1
    return "".join(parts)


def normalize_display_math(text: str) -> str:
    def clean_block(m: re.Match) -> str:
        inner = m.group(1).strip()
        return f"\n\n$${inner}$$\n"

    text = re.sub(r"\$\$(.*?)\$\$", clean_block, text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def fix_markdown(text: str) -> str:
    if not text:
        return text
    text = convert_delimiters(text)
    text = repair_bad_currency_escapes(text)
    text = escape_currency(text)
    text = repair_bad_currency_escapes(text)
    text = normalize_display_math(text)
    return text


def process_notebook(path: Path) -> int:
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    changes = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", "")
        old = "".join(src) if isinstance(src, list) else src
        new = fix_markdown(old)
        if new != old:
            changes += 1
            lines = new.split("\n")
            cell["source"] = [line + "\n" for line in lines[:-1]] + (
                [lines[-1] + "\n"] if lines[-1] else []
            )
    if changes:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=2, ensure_ascii=False)
    return changes


def main():
    total_cells = 0
    total_files = 0
    for nb_path in sorted(ROOT.rglob("*.ipynb")):
        n = process_notebook(nb_path)
        if n:
            total_files += 1
            total_cells += n
            print(f"  {nb_path.relative_to(ROOT.parent)}: {n} cells")
    print(f"Updated {total_cells} cells in {total_files} notebooks")


if __name__ == "__main__":
    main()
