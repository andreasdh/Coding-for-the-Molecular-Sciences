from __future__ import annotations

import json
import re
from pathlib import Path

NOTEBOOKS = sorted(Path("docs/data_handling").glob("*.ipynb"))

# LaTeX commands that can accidentally be interpreted as JSON escapes when a
# notebook is assembled as raw JSON text. Only single (not already escaped)
# backslashes are changed.
LATEX_COMMANDS = [
    "alpha", "bar", "beta", "cdot", "Delta", "varepsilon", "frac",
    "ge", "in", "le", "left", "mathrm", "mu", "operatorname", "pm",
    "quad", "rightarrow", "right", "sqrt", "sum", "text", "times",
]
COMMAND_PATTERN = re.compile(
    r"(?<!\\)\\(" + "|".join(re.escape(command) for command in LATEX_COMMANDS) + r")"
)
SPACING_PATTERN = re.compile(r"(?<!\\)\\([;,%])")


def double_single_latex_backslashes(text: str) -> str:
    text = COMMAND_PATTERN.sub(lambda match: r"\\" + match.group(1), text)
    text = SPACING_PATTERN.sub(lambda match: r"\\" + match.group(1), text)
    return text


def repair_remaining_invalid_escapes(text: str, path: Path) -> str:
    # If an invalid escape remains, JSON tells us its exact position. Double
    # that single backslash and retry until the file parses, while leaving
    # valid JSON escapes such as \n untouched.
    for _ in range(100):
        try:
            json.loads(text)
            return text
        except json.JSONDecodeError as exc:
            if "Invalid \\escape" not in exc.msg:
                raise
            pos = exc.pos
            if pos >= len(text) or text[pos] != "\\":
                pos = text.rfind("\\", max(0, exc.pos - 2), exc.pos + 1)
            if pos < 0:
                raise
            print(f"Repairing invalid escape in {path} at character {pos}")
            text = text[:pos] + "\\\\" + text[pos + 1 :]
    raise RuntimeError(f"Too many invalid escapes while repairing {path}")


def validate_semantic_controls(data: dict, path: Path) -> None:
    # Tabs/carriage returns/backspace/form-feed in markdown are almost always a
    # sign that an unescaped LaTeX command such as \text or \rightarrow was
    # interpreted as a JSON control escape.
    bad = []
    for index, cell in enumerate(data.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        controls = [char for char in ("\t", "\r", "\b", "\f") if char in source]
        if controls:
            bad.append((index, controls))
    if bad:
        raise RuntimeError(f"Unexpected control characters remain in {path}: {bad}")


changed = []
for path in NOTEBOOKS:
    original = path.read_text(encoding="utf-8")
    repaired = double_single_latex_backslashes(original)
    repaired = repair_remaining_invalid_escapes(repaired, path)
    data = json.loads(repaired)
    validate_semantic_controls(data, path)

    if repaired != original:
        path.write_text(repaired, encoding="utf-8")
        changed.append(path)
        print(f"Repaired: {path}")
    else:
        print(f"Already valid: {path}")

print(f"Repaired {len(changed)} notebook(s).")
