import json
from pathlib import Path

paths = [
    Path("docs/numerical_methods/equations.ipynb"),
    Path("docs/numerical_methods/numerical_differentiation.ipynb"),
    Path("docs/numerical_methods/numerical_integration.ipynb"),
    Path("docs/numerical_methods/differential_equations.ipynb"),
]

lines = []
for path in paths:
    nb = json.loads(path.read_text(encoding="utf-8"))
    lines.append(f"===== {path} | {len(nb.get('cells', []))} cells =====")
    for i, cell in enumerate(nb.get("cells", [])):
        source = "".join(cell.get("source", []))
        lines.append(f"--- CELL {i:02d} [{cell.get('cell_type')}] ---")
        lines.extend(source.splitlines())
        lines.append("")
    lines.append("")

Path("numerical_inspection.txt").write_text("\n".join(lines), encoding="utf-8")
