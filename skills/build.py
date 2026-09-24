#!/usr/bin/env python3
"""Assemble les skills Eagr : insère _socle.md dans chaque SKILL.src.md, vérifie, et produit dist/<nom>.skill."""
import re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOCLE = (ROOT / "_socle.md").read_text(encoding="utf-8").strip()
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
errors = []

for src in sorted(ROOT.glob("*/SKILL.src.md")):
    skill = src.parent.name
    text = src.read_text(encoding="utf-8")
    if text.count("<!-- SOCLE -->") != 1:
        errors.append(f"{skill}: marqueur <!-- SOCLE --> absent ou multiple")
        continue
    out = text.replace("<!-- SOCLE -->", SOCLE)
    fm = re.match(r"^---\n(.*?)\n---\n", out, re.S)
    name = re.search(r"^name:\s*(.+)$", fm.group(1), re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", fm.group(1), re.M).group(1).strip()
    if name != skill:
        errors.append(f"{skill}: name '{name}' différent du dossier")
    if len(desc) > 1024:
        errors.append(f"{skill}: description trop longue ({len(desc)} > 1024)")
    (src.parent / "SKILL.md").write_text(out, encoding="utf-8")
    with zipfile.ZipFile(DIST / f"{skill}.skill", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{skill}/SKILL.md", out)
    print(f"{skill:18} desc={len(desc):4} lignes={out.count(chr(10))}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
