#!/usr/bin/env python3
"""
build-mobile.py — Hebraico Trainer build script

Dois objetivos:
1. Atualiza licoes/manifest.js a partir de todos os licao-*.json
2. Gera hebraico-trainer-mobile.html (arquivo único para uso offline via file://)

Uso:
    python build-mobile.py          # atualiza manifest.js + gera mobile HTML
    python build-mobile.py --only-manifest  # só atualiza manifest.js
"""

import json
import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
LICOES_DIR = SCRIPT_DIR / "licoes"
INDEX_HTML  = SCRIPT_DIR / "index.html"
MOBILE_OUT  = SCRIPT_DIR / "hebraico-trainer-mobile.html"
MANIFEST_JS = LICOES_DIR / "manifest.js"

MANIFEST_HEADER = """\
/* AUTO-GERADO por build-mobile.py — não edite diretamente.
   Para adicionar lições: crie licao-XX.json e rode: python build-mobile.py */
"""


def load_lessons():
    files = sorted(LICOES_DIR.glob("licao-*.json"))
    if not files:
        print("⚠  Nenhum arquivo licao-*.json encontrado em licoes/")
        return []
    lessons = []
    for f in files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
        lessons.append(data)
        print(f"   ✓ {f.name}  ({len(data.get('vocab', []))} vocab, {len(data.get('exercicios', []))} exercícios)")
    return lessons


def write_manifest(lessons):
    payload = json.dumps(lessons, ensure_ascii=False, indent=2)
    content = MANIFEST_HEADER + f"window.LICOES_MANIFEST = {payload};\n"
    with open(MANIFEST_JS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ manifest.js atualizado ({len(lessons)} lição/lições)")


def build_mobile(lessons):
    if not INDEX_HTML.exists():
        print("⚠  index.html não encontrado — mobile build ignorado")
        return
    html = INDEX_HTML.read_text(encoding="utf-8")
    payload = json.dumps(lessons, ensure_ascii=False)
    inline = f'<script>window.LICOES_MANIFEST = {payload};</script>'
    mobile_html = html.replace('<script src="licoes/manifest.js"></script>', inline)
    with open(MOBILE_OUT, "w", encoding="utf-8") as f:
        f.write(mobile_html)
    size_kb = MOBILE_OUT.stat().st_size // 1024
    print(f"✓ {MOBILE_OUT.name} gerado ({size_kb} KB)")


def main():
    only_manifest = "--only-manifest" in sys.argv
    print("\n-- Hebraico Trainer build -----------------------")
    lessons = load_lessons()
    if not lessons:
        sys.exit(1)
    write_manifest(lessons)
    if not only_manifest:
        build_mobile(lessons)
    print("-------------------------------------------------\n")


if __name__ == "__main__":
    main()
