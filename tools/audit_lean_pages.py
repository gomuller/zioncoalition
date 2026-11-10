#!/usr/bin/env python3
"""READ-ONLY dependency and size audit for a future lean GitHub Pages deployment.
Run from repository root: python3 tools/audit_lean_pages.py
Does not modify, remove, rename, or compress any file.
"""
from pathlib import Path
from collections import Counter
import json
import re
from urllib.parse import unquote

root = Path.cwd()
skip = {".git", "node_modules", ".venv"}
files = [p for p in root.rglob("*") if p.is_file() and not any(part in skip for part in p.relative_to(root).parts)]
media_ext = {".png", ".gif", ".jpg", ".jpeg", ".webp", ".mp4", ".svg"}
text_ext = {".html", ".css", ".js", ".json", ".md", ".xml", ".txt"}
media = [p for p in files if p.suffix.lower() in media_ext]
texts = [p for p in files if p.suffix.lower() in text_ext]
refs = Counter()
# Conservative string-level scan, including URL-encoded spaces; count exact path and basename mentions.
text = []
for p in texts:
    try:
        text.append((p.relative_to(root).as_posix(), unquote(p.read_text(encoding="utf-8"))))
    except (UnicodeError, OSError):
        pass
for p in media:
    path = p.relative_to(root).as_posix()
    basename = p.name
    refs[path] = sum(body.count(path) for _, body in text)
    if refs[path] == 0:
        refs[path] = sum(body.count(basename) for _, body in text)
by_ext = Counter()
for p in files:
    by_ext[p.suffix.lower()] += p.stat().st_size
all_bytes = sum(p.stat().st_size for p in files)
png = [p for p in media if p.suffix.lower() == ".png"]
report = {
    "notice": "Conservative static audit, NOT a safe-to-delete list. JS-computed, CSS-generated, GitHub-linked, and external references may be missed.",
    "file_count": len(files),
    "total_bytes": all_bytes,
    "bytes_by_extension": dict(by_ext.most_common()),
    "png_count": len(png),
    "png_bytes": sum(p.stat().st_size for p in png),
    "media_with_no_literal_reference_count": sum(refs[p.relative_to(root).as_posix()] == 0 for p in media),
    "largest_media": [
        {"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "literal_mentions": refs[p.relative_to(root).as_posix()]}
        for p in sorted(media, key=lambda x: x.stat().st_size, reverse=True)[:25]
    ],
}
print(json.dumps(report, indent=2))
