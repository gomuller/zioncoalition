#!/usr/bin/env python3
"""Simulate a smaller Pages payload; DO NOT publish or delete anything.
Writes a manifest to runner temp only and compares actual ZIP sizes.
Exclusions are experimental and NOT proof files are unused.
"""
from pathlib import Path
from urllib.parse import unquote
import os,zipfile,json,collections
root=Path.cwd()
skip={".git","node_modules",".venv"}
files=[p for p in root.rglob("*") if p.is_file() and not any(q in skip for q in p.relative_to(root).parts)]
media_ext={".png",".gif",".jpg",".jpeg",".webp",".mp4",".svg"}
text_ext={".html",".css",".js",".json",".md",".xml",".txt"}
text=[]
for p in files:
    if p.suffix.lower() in text_ext:
        try: text.append(unquote(p.read_text(encoding="utf8")).lower())
        except (UnicodeError,OSError): pass
excluded=[]
for p in files:
    if p.suffix.lower() not in media_ext: continue
    rel=p.relative_to(root).as_posix().lower()
    name=p.name.lower()
    if not any(rel in body or name in body for body in text):
        excluded.append(p)
excluded_set=set(excluded)
print("SIMULATION ONLY: Excluded media may still be needed by external links, dynamic references, or users.")
print(json.dumps({"total_files":len(files),"excluded_files":len(excluded),"excluded_bytes":sum(p.stat().st_size for p in excluded),"included_bytes":sum(p.stat().st_size for p in files if p not in excluded)},indent=2))
for label,items in [("baseline",files),("candidate", [p for p in files if p not in excluded_set])]:
    target=Path(os.environ.get("RUNNER_TEMP","/tmp"))/f"lean-pages-{label}.zip"
    with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
        for p in items:
            z.write(p,p.relative_to(root).as_posix())
    print(f"{label} ZIP bytes: {target.stat().st_size:,}")
    target.unlink()
print("No production site files changed. Archives deleted after size measurement.")
